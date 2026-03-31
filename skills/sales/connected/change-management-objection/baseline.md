---
name: change-management-objection-baseline
description: >
  Change Management Objection Handling — Baseline Run. Automate change resistance extraction
  from every sales call transcript. Always-on pipeline: transcribe, diagnose root causes,
  score change readiness, log structured data to CRM, and queue targeted interventions.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Change resistance auto-diagnosed on >=80% of calls where it occurs, with >=65% resolution rate over 2 weeks"
kpis: ["Auto-diagnosis accuracy", "Change objection resolution rate", "Change support plan acceptance rate", "Deal progression rate"]
slug: "change-management-objection"
install: "npx gtm-skills add sales/connected/change-management-objection"
drills:
  - change-objection-extraction
  - posthog-gtm-events
---

# Change Management Objection Handling — Baseline Run

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Automate the post-call change resistance extraction pipeline so every sales call automatically produces structured resistance data in your CRM. Achieve auto-diagnosis on >= 80% of calls where change resistance occurs, with >= 65% resolution rate across all handled objections over 2 weeks. This proves the automation reliably detects and classifies change management concerns before scaling.

## Leading Indicators

- Fireflies transcripts processing within 15 minutes of call end
- Change resistance extraction completing automatically for >= 90% of calls
- Root cause classification accuracy >= 80% (validated by seller review)
- Change readiness scores appearing on deal records within 1 hour of call end
- Deals flagged as high change risk receiving Slack alerts same day
- CRM views populated: "Change Resistant" and "Change Ready" lists have accurate membership

## Instructions

### 1. Set up the automated change resistance extraction pipeline

Configure the always-on pipeline that fires after every sales call.

Run the `change-objection-extraction` drill to build the n8n workflow:
1. Fireflies transcript completion triggers the webhook
2. Transcript is matched to a deal in Attio by attendee email
3. Claude diagnoses change resistance: root causes, readiness score, recommended interventions
4. If new information about the current solution surfaces, status quo cost analysis is updated
5. Structured data is written to the Attio deal record
6. High-risk deals (readiness < 50 or risk = critical) trigger Slack alerts

**Human action required:** Test the webhook end-to-end with a real call before going live. Verify: Fireflies captures the transcript, the webhook fires, the extraction runs, and change resistance data appears in Attio. Check that the root cause classification makes sense.

### 2. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up the event taxonomy for change management. Configure these events:

- `change_resistance_extracted` — fires after extraction, includes: readiness_score, signal_count, primary_root_cause, risk_level, recommended_rollout
- `change_support_delivered` — fires when a change support asset is sent, includes: root_cause, asset_type, touch_number
- `change_support_engaged` — fires when prospect opens/clicks a change support asset
- `change_objection_resolved` — fires when a change objection leads to deal advancement, includes: root_cause, resolution_method, days_to_resolution
- `status_quo_cost_generated` — fires when a cost-of-staying analysis is produced

Set up a PostHog funnel: `change_resistance_extracted` -> `change_support_delivered` -> `change_support_engaged` -> `change_objection_resolved` -> `deal_advanced`

### 3. Validate extraction accuracy

For the first 10 calls where change resistance is detected, manually review the AI diagnosis:

For each call, evaluate:
- Did the AI correctly identify the root causes of resistance? (Precision)
- Did the AI miss any resistance signals that you noticed? (Recall)
- Is the change readiness score reasonable for this deal? (Calibration)
- Are the recommended interventions appropriate for this root cause? (Relevance)

Calculate:
- **Root cause precision:** AI root causes that are correct / total AI-identified root causes
- **Root cause recall:** Root causes you noted that the AI also found / total root causes you noted
- **Readiness calibration:** How many scores felt accurate within +/- 15 points

Target: Precision >= 0.85, Recall >= 0.80, Calibration >= 80%.

If below target, adjust the `change-resistance-diagnosis` prompt. Common fixes:
- Low precision: Add industry-specific resistance vocabulary to reduce false positives
- Low recall: Add more root cause examples to the prompt, especially for subtle political dynamics
- Poor calibration: Adjust the scoring weights based on what you observe

Log all corrections in Attio notes — these improve future extraction.

### 4. Deliver change support manually with structured data

At Baseline, you still deliver change support interventions manually, but now you have structured data guiding what to deliver:

For each deal where change resistance is diagnosed:
1. Review the automated diagnosis in Attio (root causes, readiness score, recommended sequence)
2. Prepare the intervention matched to the primary root cause (use the same approach validated in Smoke)
3. Deliver the intervention in your next conversation or via email
4. Log the outcome in Attio: what you delivered, prospect response, resolution status

**Human action required:** Deliver all change support interventions personally. The automation diagnoses; you act. This builds the training data needed for automated response delivery at Scalable.

### 5. Set up CRM views for change resistance management

Configure Attio views:
- **"Change Resistant — Needs Intervention"** list: filter deals where `change_readiness_score < 50`
- **"Change Ready — Proceed"** list: filter deals where `change_readiness_score >= 70`
- **"Awaiting Change Support"** list: filter deals where `change_risk_level` is set but no `change_objection_resolved` event
- Sort change-resistant deals by `change_readiness_score` ascending (lowest readiness = most urgent)

### 6. Evaluate against threshold

After 2 weeks, measure:
- What percentage of calls with change resistance were auto-diagnosed? (Target: >= 80%)
- What is the root cause classification accuracy? (Target: >= 80% precision)
- What is the change objection resolution rate? (Target: >= 65% of diagnosed objections resolved)
- What percentage of resolved deals advanced to the next stage?

If **PASS** (>= 80% auto-diagnosis and >= 65% resolution): The automated extraction pipeline is working reliably. Proceed to Scalable to add predictive readiness scoring and automated response delivery.

If **FAIL**: Diagnose:
- **Low auto-diagnosis rate:** Check Fireflies webhook reliability and transcript quality. Some calls may not be captured.
- **Low classification accuracy:** Review the extraction prompt. Add more examples of subtle resistance signals.
- **Low resolution rate:** The root cause matching may be wrong, or the interventions need refinement. Check whether you're delivering the right support for each root cause.

## Time Estimate

- Extraction pipeline setup and testing: 4 hours
- PostHog event configuration: 2 hours
- Validation of first 10 extractions (review + correction): 3 hours
- Manual change support delivery (10 interventions x 30 min): 5 hours
- CRM view configuration: 1.5 hours
- Threshold evaluation: 2.5 hours
- **Total: ~18 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, change resistance data, pipeline views | Plus $29/user/mo |
| Fireflies | Auto-transcribe calls for resistance extraction | Pro $10/user/mo (annual); Business $19/user/mo |
| Claude API (Anthropic) | Change resistance diagnosis + status quo cost analysis | Sonnet: $3/$15 per M tokens; ~$0.15-0.40 per call |
| PostHog | Event tracking, funnels, analytics | Free tier (1M events/mo) |
| n8n | Webhook automation (Fireflies -> extraction -> CRM) | Starter $24/mo; Pro $60/mo |
| Cal.com | Call scheduling | Free (1 user); Teams $15/user/mo |
| Clay | Incumbent solution research | Launch $185/mo |

**Estimated play-specific cost at Baseline:** ~$50-100/mo (Fireflies Pro + n8n Starter + Claude API usage). CRM, PostHog, Cal.com on free tiers.

## Drills Referenced

- `change-objection-extraction` — Always-on pipeline: transcribe calls, extract change resistance, classify root causes, score readiness, update CRM
- `posthog-gtm-events` — Define and implement the event taxonomy for change management tracking
