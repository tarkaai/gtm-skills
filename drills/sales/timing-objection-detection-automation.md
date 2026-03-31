---
name: timing-objection-detection-automation
description: Auto-detect timing objections in sales call transcripts and CRM activity, classify root cause, determine real vs smokescreen, and trigger response workflows
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
  - call-transcript-timing-extraction
  - call-transcript-timing-extraction
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - posthog-custom-events
---

# Timing Objection Detection Automation

This drill creates an always-on system that monitors every sales call transcript and CRM email activity for timing objections, classifies them by root cause, determines whether the objection is genuine or a smokescreen, and triggers the appropriate response workflow. It shifts timing objection handling from reactive to proactive.

## Input

- Fireflies account processing all sales call recordings
- Attio CRM with deal pipeline and timing scorecard fields configured (from `timing-scorecard-setup`)
- n8n instance for workflow orchestration
- PostHog for event tracking and pattern analysis

## Steps

### 1. Configure Fireflies transcript webhook

Set up Fireflies to notify n8n when a new transcript is ready:

Using `n8n-triggers`, create a webhook endpoint:

```json
{
  "trigger": "webhook",
  "url": "https://your-n8n.example.com/webhook/fireflies-timing-detection",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

Configure Fireflies to send a webhook to this URL after each transcript is processed. In Fireflies: Integrations > Webhooks > Add Webhook > set URL, select "Transcript Ready".

### 2. Build the timing objection detection workflow in n8n

Using `n8n-workflow-basics`, create a workflow with these nodes:

**Node 1: Webhook receiver** — receives the Fireflies transcript notification.

**Node 2: Transcript fetch** — retrieves the full transcript from Fireflies using the `call-transcript-timing-extraction` fundamental's GraphQL query.

**Node 3: Deal matcher** — queries Attio for the deal record matching the call. Match by: attendee email, meeting title containing company name, or calendar event ID. If no deal found, log a warning and skip.

**Node 4: Timing signal extractor** — runs `call-transcript-timing-extraction` on the full transcript. This extracts timeline category, urgency drivers, confidence, and slippage risk.

**Node 5: Timing objection detector** — sends the transcript to Claude with a focused prompt:

```
Analyze this sales call transcript for timing objections. A timing objection is any statement where the prospect delays, defers, or pushes back on timeline. Look for:
- "Not the right time"
- "Maybe next quarter/year"
- "We're focused on other things"
- "Need to wait for [event]"
- "Can we revisit this later?"
- "The timing doesn't work"
- Any deferral language that pushes decision to the future

Return JSON:
{
  "timing_objections_found": true/false,
  "objections": [
    {
      "objection_quote": "Exact words from the prospect",
      "context_quote": "What preceded the objection",
      "call_stage": "discovery|demo|proposal|negotiation|follow_up",
      "severity": 1-10,
      "prospect_language_signals": ["specific phrases indicating real vs smokescreen"]
    }
  ],
  "timeline_shift_detected": true/false,
  "previous_timeline_signals": "What the prospect previously indicated about timeline (if any)",
  "current_timeline_signals": "What they are now indicating"
}
```

If `timing_objections_found = false`: log as clean call, update Attio with timing extraction data, exit.

**Node 6: Severity router** — routes based on detection results:
- Timing objection found with `severity >= 7`: Urgent. Send Slack alert AND trigger `timing-objection-response` drill.
- Timing objection found with `severity < 7`: Standard. Trigger `timing-objection-response` drill silently.
- Timeline shift detected (without explicit objection): Warning. Update Attio timeline fields and alert seller.

**Node 7: CRM update** — writes timing objection data to the deal record in Attio using `attio-deals` and creates a structured note using `attio-notes`. Update timeline fields from timing extraction.

**Node 8: Event logging** — fires PostHog events for each detected timing objection:
```json
{
  "event": "timing_objection_detected",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript",
    "severity": 8,
    "call_stage": "proposal",
    "timeline_shift": true,
    "auto_response_triggered": true,
    "time_to_detection_minutes": 45
  }
}
```

### 3. Add email timing objection detection

Not all timing objections happen on calls. Using `n8n-triggers`, create a second workflow that monitors Attio for incoming emails containing timing objection signals:

Trigger: Attio webhook on new email activity logged to a deal in Connected or later stages.

Detection: Send the email body to Claude:
```
Analyze this email from a sales prospect. Does it contain a timing objection — any language deferring, delaying, or pushing the purchase timeline?

Return JSON:
{
  "contains_timing_objection": true/false,
  "objection_quote": "...",
  "root_cause_hint": "What the email suggests about the real reason",
  "severity": 1-10,
  "reengagement_signal": "Any indication of when they might be ready"
}
```

If `contains_timing_objection` is true, feed into the same severity router (Node 6).

### 4. Build proactive timeline risk detection

Beyond detecting objections that already happened, detect deals LIKELY to face timing objections:

Using `n8n-scheduling`, create a daily cron workflow:

1. Query Attio for deals in "Connected" or "Aligned" stages
2. For each deal, score timing objection likelihood:
   - `timeline_confidence <= 2` (vague or no timeline) -> +30 points
   - No urgency drivers identified -> +25 points
   - `slippage_risk = "High"` -> +20 points
   - Prospect canceled or rescheduled meetings 2+ times -> +15 points
   - No executive sponsor engaged -> +10 points
   - Deal age exceeds 2x average for this stage -> +10 points
3. Deals scoring >= 50 points flagged as "timing risk" in Attio
4. Fire PostHog event: `timing_objection_predicted` with risk score
5. Send Slack alert: "Deal {name} has a {score}% chance of timing objection. Strengthen urgency drivers before next call. Recommended: ask about {missing_urgency_driver}."

### 5. Track detection performance

Using `posthog-custom-events`, track detection accuracy:
```json
{
  "event": "timing_detection_result",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript|email|predictive",
    "detected": true,
    "time_to_detection_minutes": 30,
    "auto_response_triggered": true,
    "false_positive": false
  }
}
```

After 4+ weeks, measure:
- Detection rate: percentage of known timing objections auto-detected
- False positive rate: how often the system flags a non-objection
- Time to detection: latency from objection occurrence to workflow trigger
- Prediction accuracy: for predicted timing objections, how many materialized

## Output

- Always-on monitoring of all sales calls and emails for timing objections
- Automatic classification (real vs smokescreen) and response workflow triggering within 2 hours of call end
- Proactive scoring that flags deals at risk of timeline slippage
- Detection performance metrics in PostHog

## Triggers

Runs continuously via n8n webhooks (call transcripts, email activity) and daily cron (predictive scoring). No manual trigger needed once configured.
