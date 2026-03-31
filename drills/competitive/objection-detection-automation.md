---
name: objection-detection-automation
description: Auto-detect price objections in sales call transcripts and CRM activity, classify severity, and trigger response workflows
category: Competitive
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

# Objection Detection Automation

This drill creates an always-on system that monitors every sales call transcript and CRM activity for price objections, classifies them automatically, and triggers the appropriate response workflow without manual intervention. It shifts objection handling from reactive ("prospect said it's too expensive, now what?") to proactive ("objection detected, response workflow initiated within 2 hours of call end").

## Input

- Fireflies account processing all sales call recordings
- Attio CRM with deal pipeline configured
- n8n instance for workflow orchestration
- PostHog for event tracking and pattern analysis

## Steps

### 1. Configure Fireflies transcript webhook

Set up Fireflies to notify n8n when a new transcript is ready:

Using `n8n-triggers`, create a webhook endpoint that Fireflies calls after processing each recording:

```json
{
  "trigger": "webhook",
  "url": "https://your-n8n.example.com/webhook/fireflies-transcript",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

Configure Fireflies to send a webhook to this URL after each transcript is processed. In Fireflies settings, go to Integrations > Webhooks > Add Webhook > set the URL and select "Transcript Ready" as the trigger event.

### 2. Build the detection workflow in n8n

Using `n8n-workflow-basics`, create a workflow with these nodes:

**Node 1: Webhook receiver** — receives the Fireflies transcript notification.

**Node 2: Transcript fetch** — retrieves the full transcript from Fireflies using the `call-transcript-objection-extraction` fundamental's GraphQL query.

**Node 3: Deal matcher** — queries Attio for the deal record matching the call. Match by: attendee email address, meeting title containing company name, or calendar event ID. If no deal found, log a warning and skip (the call may not be a sales call).

**Node 4: Objection classifier** — sends the transcript to Claude for objection extraction using the `call-transcript-objection-extraction` fundamental. Returns structured objection data.

**Node 5: Severity router** — routes based on the extraction results:
- `objection_count == 0`: No price objection detected. Log as clean call. Exit.
- `objection_count >= 1` and `deal_risk_level` is "low" or "medium": Standard handling. Trigger `price-objection-response` drill automatically.
- `objection_count >= 1` and `deal_risk_level` is "high" or "critical": Urgent. Send Slack alert to the founder/sales lead AND trigger `price-objection-response` drill.

**Node 6: CRM update** — writes the objection data to the deal record in Attio using `attio-deals` and creates a structured note using `attio-notes`.

**Node 7: Event logging** — fires PostHog events for each detected objection.

### 3. Add email objection detection

Not all price objections happen on calls. Using `n8n-triggers`, create a second workflow that monitors Attio for incoming emails containing price objection signals:

Trigger: Attio webhook on new email activity logged to a deal.

Detection: Send the email body to Claude with a simplified prompt:

```
Analyze this email from a sales prospect. Does it contain a price objection?
Return JSON: {"contains_price_objection": true/false, "objection_quote": "...", "root_cause": "...", "severity": 1-10}
Email: {email_body}
```

If `contains_price_objection` is true, feed into the same severity router (Node 5) as the call detection workflow.

### 4. Build the predictive detection layer

Beyond detecting objections that already happened, detect deals LIKELY to face price objections before the proposal call:

Using `n8n-scheduling`, create a daily cron workflow that:

1. Queries Attio for deals in the "Proposal" or "Negotiation" stage
2. For each deal, score objection likelihood based on:
   - `pain_to_price_ratio < 5` (weak value foundation) -> +30 points
   - No champion identified -> +20 points
   - Economic buyer not engaged -> +25 points
   - Competitor evaluation active -> +15 points
   - Deal value above prospect's typical spend (from enrichment) -> +10 points
3. Deals scoring >= 50 points are flagged as "objection likely" in Attio
4. Fire a PostHog event: `price_objection_predicted` with the risk score
5. Send a Slack alert to the seller: "Deal {name} has a {score}% chance of price objection. Strengthen the value story before the proposal call."

### 5. Track detection performance

Using `posthog-custom-events`, track detection system accuracy:

```json
{
  "event": "objection_detection_result",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript|email|predictive",
    "detected": true,
    "time_to_detection_minutes": 45,
    "auto_response_triggered": true
  }
}
```

After 4+ weeks, measure:
- Detection rate: what percentage of known objections were auto-detected?
- False positive rate: how often did the system flag a non-objection?
- Time to detection: how fast from objection occurrence to workflow trigger?
- Prediction accuracy: for predicted objections, how many actually materialized?

## Output

- Always-on monitoring of all sales calls and emails for price objections
- Automatic classification and response workflow triggering within 2 hours of call end
- Predictive scoring that flags at-risk deals before the objection occurs
- Detection performance metrics in PostHog

## Triggers

Runs continuously via n8n webhooks (call transcripts, email activity) and daily cron (predictive scoring). No manual trigger needed once configured.
