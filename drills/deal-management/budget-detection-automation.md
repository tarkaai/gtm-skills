---
name: budget-detection-automation
description: Auto-detect budget objections in sales call transcripts and CRM activity, classify root cause, and trigger budget navigation workflows
category: Deal Management
tools:
  - Fireflies
  - Attio
  - n8n
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - budget-objection-classification
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - posthog-custom-events
---

# Budget Detection Automation

This drill creates an always-on system that monitors every sales call transcript and CRM email activity for budget objections, classifies them automatically, and triggers the `budget-objection-response` drill without manual intervention. It differentiates budget objections from price objections — a prospect saying "this is too expensive" is NOT the same as "we don't have budget for this."

## Input

- Fireflies account processing all sales call recordings
- Attio CRM with deal pipeline configured
- n8n instance for workflow orchestration
- PostHog for event tracking

## Steps

### 1. Configure Fireflies transcript webhook

Using `n8n-triggers`, create a webhook endpoint that Fireflies calls after processing each recording:

```json
{
  "trigger": "webhook",
  "url": "https://your-n8n.example.com/webhook/fireflies-budget-detection",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

Configure Fireflies to send webhooks on "Transcript Ready" events.

### 2. Build the budget detection workflow in n8n

Using `n8n-workflow-basics`, create a workflow:

**Node 1: Webhook receiver** — receives the Fireflies transcript notification.

**Node 2: Transcript fetch** — retrieves the full transcript from Fireflies.

**Node 3: Deal matcher** — queries Attio for the deal matching the call attendees, meeting title, or calendar event ID. If no deal found, log and skip.

**Node 4: Budget objection detector** — sends the transcript to Claude with a detection-specific prompt:

```
Analyze this sales call transcript. Identify any BUDGET objections (NOT price objections).

Budget objections are about the AVAILABILITY of funds:
- "We don't have budget for this"
- "That's not in our plan this year"
- "We'd need to get that approved by finance"
- "Our budget is committed to other projects"
- "We'd need to wait for next fiscal year"
- "I don't control that budget"
- "Procurement would need to approve that"

These are NOT budget objections (they are price objections):
- "That's too expensive"
- "Your competitor is cheaper"
- "We can't justify that cost"
- "The ROI doesn't make sense"

For each budget objection found, return:
{
  "objections": [
    {
      "quote": "exact transcript quote",
      "speaker": "prospect name",
      "timestamp_approx": "MM:SS if available",
      "budget_objection_type": "no_allocated_budget|budget_exhausted|wrong_budget_owner|competing_priorities|procurement_friction|budget_smokescreen",
      "severity": 1-10,
      "context": "What was being discussed when this came up"
    }
  ],
  "objection_count": 0,
  "overall_budget_risk": "none|low|medium|high|critical"
}

If no budget objections are detected, return objection_count: 0.

Transcript:
{transcript_text}
```

**Node 5: Severity router** — routes based on detection results:
- `objection_count == 0`: No budget objection. Log as clean call. Exit.
- `objection_count >= 1` and `overall_budget_risk` is "low" or "medium": Trigger `budget-objection-response` drill silently.
- `objection_count >= 1` and `overall_budget_risk` is "high" or "critical": Send Slack alert AND trigger `budget-objection-response` drill.

**Node 6: CRM update** — writes budget objection data to the deal record in Attio using `attio-deals` and creates a note using `attio-notes`:
```json
{
  "budget_objection_detected": true,
  "budget_objection_source": "call_transcript",
  "budget_objection_root_cause": "competing_priorities",
  "budget_objection_severity": 7,
  "budget_objection_quote": "We'd love to do this but our entire Q2 budget is going toward the Salesforce migration",
  "detection_timestamp": "2026-03-30T14:22:00Z"
}
```

**Node 7: Event logging** — fires PostHog events:
```json
{
  "event": "budget_objection_detected",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript",
    "root_cause": "competing_priorities",
    "severity": 7,
    "overall_budget_risk": "high",
    "time_to_detection_minutes": 45,
    "auto_response_triggered": true
  }
}
```

### 3. Add email budget detection

Create a second n8n workflow monitoring Attio for incoming emails with budget signals:

Trigger: Attio webhook on new email activity logged to a deal in Proposed or Negotiation stage.

Detection prompt:
```
Analyze this email from a sales prospect. Does it contain a BUDGET objection?
Budget objections are about fund availability, not price perception.
Return JSON: {"contains_budget_objection": true/false, "objection_quote": "...", "root_cause": "...", "severity": 1-10}
Email: {email_body}
```

If budget objection detected, feed into the same severity router and CRM update flow.

### 4. Build predictive budget risk scoring

Using `n8n-scheduling`, create a daily cron workflow that predicts which deals are likely to face budget objections:

1. Query Attio for deals in the "Proposed" or "Negotiation" stage
2. Score each deal for budget objection likelihood:
   - No economic buyer identified -> +25 points
   - Prospect fiscal year ends within 60 days -> +20 points (budget may be exhausted)
   - Deal value > $50K and no procurement discussion yet -> +15 points
   - No budget timeline discussed in discovery -> +20 points
   - Champion title is not VP+ (may not control budget) -> +10 points
   - Multiple stakeholders mentioned but only 1 engaged -> +10 points
3. Deals scoring >= 50 points: flag as "budget risk" in Attio
4. Fire PostHog event: `budget_objection_predicted` with risk score
5. Send Slack alert: "Deal {name} has a {score}% budget risk. Discuss budget early in the next conversation to get ahead of it."

### 5. Track detection performance

Using `posthog-custom-events`, track detection accuracy:
```json
{
  "event": "budget_detection_result",
  "properties": {
    "deal_id": "...",
    "detection_source": "call_transcript|email|predictive",
    "detected": true,
    "correctly_classified_as_budget": true,
    "time_to_detection_minutes": 45,
    "auto_response_triggered": true
  }
}
```

After 4+ weeks, measure:
- Detection rate: what % of budget objections were auto-detected?
- False positive rate: how often did it misclassify a price objection as budget?
- Price/budget confusion rate: how often were the two types conflated?
- Prediction accuracy: for predicted budget risks, how many materialized?

## Output

- Always-on monitoring of all sales calls and emails for budget objections
- Distinction between budget objections and price objections (separate handling pipelines)
- Automatic classification and response workflow triggering within 2 hours of call end
- Predictive scoring flagging at-risk deals before the budget conversation
- Detection performance metrics in PostHog

## Triggers

Runs continuously via n8n webhooks (call transcripts, email activity) and daily cron (predictive scoring).
