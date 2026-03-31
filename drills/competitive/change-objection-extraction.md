---
name: change-objection-extraction
description: Auto-extract change management objections from call transcripts, classify root causes, assess readiness, and update CRM with structured change resistance data
category: Competitive
tools:
  - Fireflies
  - Attio
  - Anthropic
  - n8n
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - change-resistance-diagnosis
  - status-quo-cost-analysis
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
---

# Change Objection Extraction

This drill creates an always-on pipeline that processes every sales call transcript to detect change management resistance, classify root causes, assess organizational change readiness, and update the CRM with structured data. It transforms vague "they don't want to switch" notes into actionable intelligence.

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
  "url": "https://your-n8n.example.com/webhook/fireflies-change-objection",
  "method": "POST",
  "expected_payload": {
    "transcript_id": "string",
    "meeting_title": "string",
    "attendees": ["email1", "email2"],
    "duration_minutes": 0
  }
}
```

### 2. Build the extraction workflow in n8n

Using `n8n-workflow-basics`, create a workflow with these nodes:

**Node 1: Webhook receiver** — receives the Fireflies transcript notification.

**Node 2: Transcript fetch** — retrieves the full transcript from Fireflies using the GraphQL API (see `fireflies-transcription`).

**Node 3: Deal matcher** — queries Attio for the deal record matching the call. Match by: attendee email address, meeting title containing company name, or calendar event ID. If no deal found, log a warning and skip.

**Node 4: Change resistance classifier** — sends the transcript to Claude using `change-resistance-diagnosis`. Returns:
- Resistance signals with root causes
- Change readiness score
- Recommended intervention sequence
- Deal risk level

**Node 5: Status quo cost update** — if the call surfaced new information about the current solution (spend, limitations, customizations), re-run `status-quo-cost-analysis` with updated inputs. Otherwise, skip.

**Node 6: Severity router** — routes based on the diagnosis:
- `resistance_signals` empty: No change resistance detected. Log as clean call. Exit.
- `change_readiness_score >= 50` and `deal_risk_level` is "low" or "medium": Standard handling. Queue the recommended interventions for delivery.
- `change_readiness_score < 50` or `deal_risk_level` is "high" or "critical": Urgent. Send Slack alert to the founder with the diagnosis summary and recommended sequence.

**Node 7: CRM update** — writes the structured change resistance data to the deal record in Attio using `attio-deals`:

```json
{
  "data": {
    "values": {
      "change_readiness_score": [{"value": 45}],
      "primary_resistance_cause": [{"value": "past_failure"}],
      "resistance_signal_count": [{"value": 3}],
      "recommended_rollout": [{"value": "pilot_first"}],
      "change_risk_level": [{"value": "high"}],
      "change_diagnosis_date": [{"value": "2026-03-30T00:00:00Z"}]
    }
  }
}
```

Create a structured note using `attio-notes` with the full diagnosis and recommended actions.

**Node 8: Event logging** — fires PostHog events:

```json
{
  "event": "change_resistance_extracted",
  "properties": {
    "deal_id": "...",
    "readiness_score": 45,
    "signal_count": 3,
    "primary_root_cause": "past_failure",
    "risk_level": "high",
    "recommended_rollout": "pilot_first",
    "call_id": "..."
  }
}
```

### 3. Track extraction accuracy

For the first 10 extractions, have the seller review the AI diagnosis:
- Did the AI correctly identify the root causes?
- Is the readiness score reasonable?
- Are the recommended interventions appropriate?

Log corrections in Attio. If AI accuracy < 80%, adjust the `change-resistance-diagnosis` prompt with examples of missed or misclassified resistance signals.

### 4. Build CRM views for change resistance management

Configure Attio views:
- **"Change Resistant — Needs Intervention"** list: filter deals where `change_readiness_score < 50`
- **"Change Ready — Proceed"** list: filter deals where `change_readiness_score >= 70`
- **"Awaiting Pilot Proposal"** list: filter deals where `recommended_rollout = "pilot_first"` and no pilot proposal sent
- Sort change-resistant deals by `change_readiness_score` ascending (lowest readiness = most attention needed)

## Output

- Always-on monitoring of all sales calls for change management resistance
- Automatic classification of root causes and readiness scoring
- Structured CRM data enabling pipeline segmentation by change readiness
- Severity-based alerting for high-risk deals
- PostHog events for pattern analysis

## Triggers

Runs continuously via n8n webhook triggered by Fireflies transcript completion. No manual trigger needed once configured.
