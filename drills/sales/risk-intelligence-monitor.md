---
name: risk-intelligence-monitor
description: Always-on monitoring of deal activity for emerging risks -- scan transcripts, emails, and deal data for risk signals and predict risk likelihood per deal
category: Sales
tools:
  - Attio
  - Fireflies
  - n8n
  - Anthropic
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - fireflies-transcription
  - call-transcript-risk-extraction
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - posthog-custom-events
  - posthog-anomaly-detection
  - anthropic-api-patterns
---

# Risk Intelligence Monitor

This drill creates an always-on system that continuously monitors all deal activity for emerging risk signals. It scans every new call transcript, email exchange, and CRM update for risk language, predicts risk likelihood for deals approaching proposal stage, and alerts the seller when new concerns emerge or existing risks escalate. It shifts risk management from periodic (after discovery calls) to continuous (across the entire deal lifecycle).

## Input

- Fireflies account processing all sales call recordings
- Attio CRM with deal pipeline configured and risk data fields populated
- n8n instance for workflow orchestration
- PostHog for event tracking and anomaly detection
- At least 4 weeks of risk discovery data (for prediction model baseline)

## Steps

### 1. Configure transcript monitoring webhook

Using `n8n-triggers`, create a webhook endpoint that Fireflies calls after processing each recording:

```json
{
  "trigger": "webhook",
  "url": "https://your-n8n.example.com/webhook/risk-monitor-transcript",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

This catches ALL calls -- not just dedicated risk discovery calls. A risk can surface on a demo, a technical deep-dive, or an executive briefing.

### 2. Build the continuous risk scanner in n8n

Using `n8n-workflow-basics`, create a workflow:

**Node 1: Webhook receiver** -- receives the Fireflies transcript notification.

**Node 2: Transcript fetch** -- retrieves the full transcript using the `call-transcript-risk-extraction` fundamental's GraphQL query.

**Node 3: Deal matcher** -- queries Attio for the deal record matching the call. Match by attendee email, meeting title, or calendar event ID. If no deal found, log and skip.

**Node 4: Risk extractor** -- sends transcript to Claude for risk extraction. Uses the same prompt as `call-transcript-risk-extraction` but adds existing risk data from the deal for comparison:
```
"Existing risks already identified for this deal: {existing_risk_data_json}
Identify NEW risks not already captured, and note if any existing risks have ESCALATED or been RESOLVED based on this conversation."
```

**Node 5: Delta calculator** -- compares new extraction against existing risk data:
- New risks: risks in this extraction not in existing data
- Escalated risks: existing risks whose severity or likelihood increased
- Resolved risks: existing risks that were addressed on this call
- Unchanged risks: no new information

**Node 6: Alert router** -- routes based on delta:
- New Critical risk (score >= 80): Immediate Slack alert to founder + sales lead
- Risk escalation (score increased by 20+): Slack alert + trigger `risk-mitigation-delivery`
- New Medium/High risk: Queue for next daily digest
- Risk resolved: Update CRM, fire success event
- No new risk signals: Log and exit

**Node 7: CRM updater** -- merges new risk data into the deal record. Appends new risks, updates scores on escalated risks, marks resolved risks.

**Node 8: Event logger** -- fires PostHog events for each risk change detected.

### 3. Add email risk detection

Using `n8n-triggers`, create a second workflow that monitors Attio for incoming emails:

Trigger: Attio webhook on new email activity logged to a deal.

Detection: Send the email body to Claude with a risk-focused prompt:

```
Analyze this email from a sales prospect. Does it contain any risk signals -- concerns, hesitation, references to internal blockers, mentions of competitors, requests for guarantees, or language suggesting cold feet?

Return JSON:
{
  "contains_risk_signals": true/false,
  "risks_detected": [
    {
      "category": "financial|technical|organizational|timeline|vendor",
      "summary": "...",
      "concern_quote": "...",
      "severity": 1-10,
      "likelihood": 1-10,
      "is_new": true/false
    }
  ],
  "sentiment_shift": "more_confident|neutral|more_concerned|disengaging"
}

Email: {email_body}
```

If `contains_risk_signals` is true, feed into the delta calculator (Node 5) from the transcript workflow.

If `sentiment_shift` is "disengaging," trigger an immediate alert regardless of specific risks -- the deal may be going dark.

### 4. Build predictive risk scoring

Using `n8n-scheduling`, create a daily cron workflow that scores every open deal's risk likelihood:

1. Query Attio for all deals in "Connected" or later stages
2. For each deal, compute a predictive risk score based on:
   - Historical risk patterns for this segment (from `risk-pattern-analysis`)
   - Deal age vs. average cycle time -> +20 if deal is aging
   - Number of stakeholders engaged -> +15 if only 1 contact (single-thread risk)
   - Days since last activity -> +25 if no activity in 7+ days (going dark)
   - Pain-to-price ratio -> +20 if below 5x (weak value foundation)
   - Champion identified? -> +15 if no champion
   - Existing unaddressed risks -> their risk_score contributes directly
3. Classify deals: Green (0-30), Yellow (31-60), Red (61+)
4. For Red deals: send Slack alert with the specific risk factors and suggested actions
5. Fire PostHog event: `deal_risk_prediction` with the score and contributing factors

### 5. Generate daily risk digest

Using `n8n-scheduling`, create a daily digest workflow:

1. Aggregate all risk events from the last 24 hours
2. Group by deal
3. Generate a brief:

```markdown
## Daily Risk Digest -- {date}

### New Risks Detected (3)
- **{company}**: {risk_summary} (Score: {score}, Category: {category})
  Action: {recommended action}
- ...

### Risk Escalations (1)
- **{company}**: {risk_summary} escalated from {old_score} to {new_score}
  Reason: {what changed}

### Risks Resolved (2)
- **{company}**: {risk_summary} resolved via {mitigation_type}

### Deals at Risk (Red)
- **{company}**: Predictive score {score}/100 -- {top risk factor}
- ...

### Overall Pipeline Risk
- Total deals with unaddressed Critical risks: {n}
- Avg mitigation coverage across pipeline: {n}%
- Risk trend (7-day): {improving/stable/worsening}
```

4. Post to Slack and store in Attio

### 6. Track monitoring performance

Log metrics for system health:
- Detection latency: time from call end to risk alert
- False positive rate: alerts where no real risk existed
- Coverage: % of deals with risk data vs. total pipeline
- Resolution rate: % of detected risks that get mitigated

## Output

- Continuous scanning of all call transcripts and emails for risk signals
- Real-time alerts when new Critical risks emerge or existing risks escalate
- Daily predictive risk scoring for every open deal
- Daily risk digest summarizing pipeline risk posture
- Detection performance metrics

## Triggers

Runs continuously via n8n webhooks (transcripts, emails) and daily cron (predictive scoring, digest). No manual trigger needed once configured.
