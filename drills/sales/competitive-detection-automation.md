---
name: competitive-detection-automation
description: Auto-detect competitor mentions in sales call transcripts and CRM activity, classify objection type and severity, and trigger competitive response workflows
category: Sales
tools:
  - Fireflies
  - Attio
  - n8n
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-objection-extraction
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - posthog-custom-events
---

# Competitive Detection Automation

This drill creates an always-on system that monitors every sales call transcript and CRM email for competitor mentions, classifies the competitive objection type and severity, and triggers the appropriate response workflow. It shifts competitive handling from reactive ("they mentioned a competitor on the call, now what?") to proactive ("competitor detected, battlecard pulled, response drafted within 2 hours of call end").

## Input

- Fireflies account processing all sales call recordings
- Attio CRM with deal pipeline configured
- n8n instance for workflow orchestration
- PostHog for event tracking
- List of known competitors to monitor (stored in Attio Competitors object)

## Steps

### 1. Configure Fireflies transcript webhook

Set up Fireflies to notify n8n when a new transcript is ready:

Using `n8n-triggers`, create a webhook endpoint:
```json
{
  "trigger": "webhook",
  "url": "https://your-n8n.example.com/webhook/fireflies-competitive-scan",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

### 2. Build the competitive detection workflow in n8n

Using `n8n-workflow-basics`, create a workflow:

**Node 1: Webhook receiver** — receives the Fireflies transcript notification.

**Node 2: Transcript fetch** — retrieves the full transcript from Fireflies using the GraphQL API.

**Node 3: Deal matcher** — queries Attio for the deal record matching the call. Match by attendee email, meeting title, or calendar event ID. If no deal found, log and skip.

**Node 4: Competitor scan** — two-phase detection:

*Phase A — Keyword scan:* Check the transcript for exact mentions of known competitor names (pulled from Attio Competitors object). This is fast and catches direct mentions.

*Phase B — Semantic scan:* Send the transcript to Claude for deeper competitive signal extraction:

```json
{
  "prompt": "Analyze this sales call transcript for competitive signals. Identify ANY mentions of competitors (by name or indirect reference like 'another vendor', 'the other solution', 'what we're using now'). For each competitor mention, extract:\n\nTranscript:\n{transcript_text}\n\nReturn JSON:\n{\n  \"competitor_mentions\": [\n    {\n      \"competitor_name\": \"Name or 'unnamed_competitor' if indirect reference\",\n      \"mention_quote\": \"Exact quote from transcript\",\n      \"context\": \"What was being discussed when the competitor was mentioned\",\n      \"competitive_objection_type\": \"active_evaluation|incumbent_loyalty|feature_comparison|price_comparison|social_proof|switching_cost|none\",\n      \"severity\": 1-10,\n      \"emotional_tone\": \"exploratory|committed|anxious|negotiating\",\n      \"response_quality\": \"strong|adequate|weak|no_response\",\n      \"follow_up_needed\": true/false\n    }\n  ],\n  \"competitive_deal\": true/false,\n  \"overall_competitive_risk\": \"low|medium|high|critical\"\n}"
}
```

**Node 5: Severity router** — routes based on detection results:
- `competitive_deal == false`: No competitor detected. Log as clean call. Exit.
- `competitive_deal == true` and `overall_competitive_risk` is "low" or "medium": Standard handling. Update deal record with competitor data. Queue `competitive-objection-response` drill for the seller's next prep session.
- `competitive_deal == true` and `overall_competitive_risk` is "high" or "critical": Urgent. Send Slack alert to seller immediately. Auto-pull battlecard from Attio and include in the alert. Trigger `competitive-objection-response` drill.

**Node 6: CRM update** — writes competitive data to the deal record in Attio:
- Set `competitor_mentioned` attribute with competitor name(s)
- Set `competitive_risk_level`
- Create a structured note with the full extraction results
- Link to the Competitor record in Attio

**Node 7: Event logging** — fires PostHog events:
```json
{
  "event": "competitor_detected",
  "properties": {
    "deal_id": "...",
    "competitor_name": "...",
    "competitive_objection_type": "active_evaluation",
    "severity": 7,
    "detection_source": "call_transcript",
    "overall_competitive_risk": "high",
    "auto_response_triggered": true,
    "time_to_detection_minutes": 30
  }
}
```

### 3. Add email competitor detection

Using `n8n-triggers`, create a second workflow monitoring Attio for incoming emails containing competitive signals:

Trigger: Attio webhook on new email activity logged to a deal.

Detection: Send the email body to Claude:
```
Analyze this email from a sales prospect. Does it mention any competitors (by name or indirect reference)?
Return JSON: {"mentions_competitor": true/false, "competitor_name": "...", "competitive_objection_type": "...", "severity": 1-10, "quote": "..."}
Email: {email_body}
```

If `mentions_competitor` is true, feed into the same severity router (Node 5).

### 4. Build predictive competitive risk scoring

Beyond detecting competitors already mentioned, score deals likely to face competitive objections:

Using `n8n-scheduling`, create a daily cron workflow:

1. Query Attio for deals in "Demo" or "Proposal" stage that have NOT yet had a competitor detected
2. For each deal, score competitive risk based on:
   - Industry has high competitive density -> +20 points
   - Prospect company size matches competitor's sweet spot -> +15 points
   - No champion identified yet -> +15 points
   - Multiple stakeholders involved (committee buy) -> +10 points
   - Prospect mentioned "evaluating options" in any communication -> +25 points
   - Prospect company is a known customer of a competitor (from enrichment) -> +30 points
3. Deals scoring >= 50 are flagged as "competitive risk likely"
4. Fire PostHog event: `competitive_risk_predicted` with the risk score
5. Update deal record in Attio with predictive risk score
6. For deals scoring >= 70, proactively pull the most likely competitor's battlecard and share with the seller before the next call

### 5. Track detection performance

Using `posthog-custom-events`, track detection accuracy:

```json
{
  "event": "competitive_detection_result",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript|email|predictive",
    "detected": true,
    "competitor_name": "...",
    "time_to_detection_minutes": 30,
    "auto_response_triggered": true,
    "false_positive": false
  }
}
```

After 4+ weeks, measure:
- Detection rate: what percentage of known competitive deals were auto-detected?
- False positive rate: how often did the system flag a non-competitive deal?
- Time to detection: how fast from competitor mention to workflow trigger?
- Prediction accuracy: for predicted competitive deals, how many actually involved competitors?

## Output

- Always-on monitoring of all sales calls and emails for competitor mentions
- Automatic classification and response workflow triggering within 2 hours of call end
- Predictive scoring that flags at-risk deals before the competitor is mentioned
- Detection performance metrics in PostHog

## Triggers

Runs continuously via n8n webhooks (call transcripts, email activity) and daily cron (predictive scoring). No manual trigger needed once configured.
