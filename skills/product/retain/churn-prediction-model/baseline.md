---
name: churn-prediction-model-baseline
description: >
  AI Churn Prediction — Baseline Run. Automate daily churn scoring and route at-risk users to
  tiered interventions. First always-on automation targeting 70%+ accuracy and 15%+ churn reduction.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=70% accuracy, >=15% churn reduction"
kpis: ["Prediction accuracy", "Churn rate", "Intervention success"]
slug: "churn-prediction-model"
install: "npx gtm-skills add product/retain/churn-prediction-model"
drills:
  - churn-signal-extraction
  - churn-intervention-routing
  - posthog-gtm-events
---

# AI Churn Prediction — Baseline Run

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Turn the Smoke Test's manual scoring run into an always-on daily pipeline. The agent scores every active user for churn risk each day and routes at-risk users to tiered interventions (in-app messages, email sequences, personal outreach). After 2 weeks, measure: does the model achieve 70%+ accuracy and do the interventions reduce churn by at least 15% compared to the pre-intervention baseline?

## Leading Indicators

- Daily scoring pipeline runs without errors for 7+ consecutive days
- At-risk users receive interventions within 24 hours of being flagged
- At least 10% of intervened users show re-engagement within 7 days (early signal that interventions work)
- False positive rate stays below 40% (model is not flagging too many healthy users)

## Instructions

### 1. Instrument churn prediction events

Run the `posthog-gtm-events` drill to add tracking events specific to the churn prediction pipeline:

- `churn_risk_scored` — fired daily for each user, properties: `risk_score`, `risk_tier`, `primary_signal`
- `churn_intervention_sent` — fired when an intervention is triggered, properties: `intervention_type`, `risk_tier`, `primary_signal`
- `churn_intervention_outcome` — fired 14 days after intervention, properties: `outcome` (saved/declined/churned), `original_risk_score`
- `churn_model_calibration` — fired weekly, properties: `true_positive_rate`, `false_positive_rate`, `save_rate`

These events enable PostHog funnel and cohort analysis of the entire prediction-to-intervention pipeline.

### 2. Automate daily churn scoring

Run the `churn-signal-extraction` drill in automated mode. Configure an n8n workflow that runs daily at a fixed time:

1. Query PostHog for all active users' behavioral signals (activity decay, feature abandonment, login gaps, etc.)
2. Batch-score users via the Anthropic API (20 users per request)
3. Write risk scores to Attio (`churn_risk_score` custom attribute) and PostHog (`churn_risk_scored` event)
4. Update PostHog cohorts: critical-risk, high-risk, medium-risk, low-risk

**Human action required:** After the first automated run, review 20 randomly sampled scores. Confirm the automated pipeline produces the same quality scores as the manual Smoke run. If accuracy degrades, check that the extraction queries are returning complete data.

### 3. Configure tiered interventions

Run the `churn-intervention-routing` drill to set up the intervention pipeline:

- **Critical risk (76-100):** Create Attio task for account owner with the user's churn signals. Intercom targeted message acknowledging the relationship.
- **High risk (51-75):** Enroll in a Loops re-engagement email sequence personalized to the user's primary churn signal (activity decay, feature abandonment, or support escalation).
- **Medium risk (26-50):** Intercom in-app message highlighting an unused feature relevant to the user's engagement pattern.

Configure the 14-day cooldown: no user receives more than one intervention per 14-day window.

### 4. Set up A/B measurement

Split your user base: 50% receive the churn prediction interventions (treatment), 50% receive no proactive outreach (control). Use PostHog feature flags to control the split. This is essential for measuring whether interventions actually reduce churn vs. natural retention patterns.

Track:
- Treatment group churn rate over 2 weeks
- Control group churn rate over 2 weeks
- Delta = treatment improvement over control

### 5. Run for 2 weeks and evaluate

After 14 days of the automated pipeline running:

1. Calculate prediction accuracy: what percentage of users flagged as high-risk/critical actually showed continued decline or churned?
2. Calculate intervention effectiveness: treatment group churn rate vs. control group churn rate
3. Check the pass threshold: >=70% prediction accuracy AND >=15% churn reduction (treatment vs. control)

If PASS, proceed to Scalable. If FAIL, diagnose:
- Low accuracy? Adjust signal weights or add new signals
- Low intervention effectiveness? Revise intervention templates and timing
- High false positive rate? Tighten the scoring thresholds

## Time Estimate

- 3 hours: instrument churn prediction events in PostHog
- 4 hours: automate daily scoring pipeline in n8n
- 4 hours: configure intervention routing (Intercom messages, Loops sequences, Attio tasks)
- 2 hours: set up A/B measurement with PostHog feature flags
- 3 hours: analyze 2-week results, calibrate, document

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, feature flags, A/B measurement | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Daily churn risk scoring | ~$0.01-0.03/user/day; ~$15-50/mo for 500 users — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Loops | Re-engagement email sequences | Free up to 1,000 contacts; $49/mo paid — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages for medium/critical risk users | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $50-100/mo** (Anthropic API + Loops if over free tier; Intercom if not already in stack)

## Drills Referenced

- `churn-signal-extraction` — automated daily scoring pipeline extracting signals and computing risk scores
- `churn-intervention-routing` — routes at-risk users to tiered interventions based on risk score and primary signal
- `posthog-gtm-events` — instruments the churn prediction events needed for pipeline monitoring
