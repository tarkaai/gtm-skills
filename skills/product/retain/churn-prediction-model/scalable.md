---
name: churn-prediction-model-scalable
description: >
  AI Churn Prediction — Scalable Automation. Segment the churn model by user persona, automate
  intervention A/B testing, and maintain 65%+ accuracy across 500+ users with no manual intervention.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=65% accuracy at 500+ users"
kpis: ["Prediction accuracy", "Churn rate", "Intervention success", "Segment metrics"]
slug: "churn-prediction-model"
install: "npx gtm-skills add product/retain/churn-prediction-model"
drills:
  - churn-signal-extraction
  - churn-intervention-routing
  - ab-test-orchestrator
  - dashboard-builder
---

# AI Churn Prediction — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Scale the churn prediction model from a validated Baseline to full production coverage. Segment scoring and interventions by user persona so the model handles different usage patterns. Run systematic A/B tests on intervention templates to find what saves the most users. Maintain 65%+ prediction accuracy across 500+ active users with zero manual scoring or routing.

## Leading Indicators

- Scoring pipeline handles 500+ users daily without errors or timeouts
- Per-segment accuracy stays within 10 percentage points of overall accuracy (no one segment dragging the average)
- At least 2 intervention A/B tests completed with statistically significant results
- Save rate (intervened users who re-engage) trends upward over the 2-month period

## Instructions

### 1. Segment the scoring model by persona

The Baseline model uses one set of "healthy usage" parameters for all users. At scale, different personas have different natural usage patterns. A power user going from 50 events/week to 25 is declining. A casual user at 5 events/week is normal.

Using the `churn-signal-extraction` drill, create persona-specific scoring contexts:

1. Query PostHog for user segments: segment by plan type, account age, team size, or usage tier
2. For each segment, calculate separate "healthy usage" baselines (average events/week, feature breadth, login frequency)
3. Pass persona-specific context to the `churn-score-computation` fundamental so the LLM scores relative to each user's expected behavior, not a global average

Store the persona assignment in Attio and PostHog as a user property (`churn_persona`).

### 2. Scale intervention routing

Using the `churn-intervention-routing` drill, expand the intervention templates for each persona:

- **Power users (high-volume, multi-feature):** Focus interventions on product roadmap visibility and executive engagement. These users churn for strategic reasons (competitor switch, budget cuts), not confusion.
- **Standard users (moderate, steady usage):** Focus interventions on feature discovery and value expansion. These users churn from stagnation.
- **Light users (low-volume, narrow feature use):** Focus interventions on activation and quick wins. These users churn because they never found enough value.

Create persona-specific email sequences in Loops and in-app messages in Intercom for each category.

### 3. A/B test interventions systematically

Run the `ab-test-orchestrator` drill to test intervention variations:

**Test 1 (weeks 1-3):** Email subject lines for high-risk re-engagement sequences. Hypothesis: personalized subject lines referencing the user's primary churn signal ("We noticed you stopped using [feature]") outperform generic re-engagement ("We miss you").

**Test 2 (weeks 3-5):** Intervention timing. Hypothesis: triggering intervention at medium-risk (score 26-50) catches users before they disengage fully, producing higher save rates than waiting until high-risk (score 51-75).

**Test 3 (weeks 5-7):** In-app vs. email for medium-risk users. Hypothesis: in-app messages produce faster re-engagement than email because the user is already in the product when they see the message.

For each test, use PostHog feature flags to split traffic and measure save rate (re-engagement within 14 days) as the primary metric.

### 4. Deploy the model health monitor

Run the `dashboard-builder` drill to set up ongoing monitoring:

- PostHog dashboard with prediction accuracy, intervention effectiveness, model calibration, and population distribution panels
- Weekly automated health check that alerts if false negative rate exceeds 15% or save rate drops below 10%
- Monthly calibration drift check comparing predicted risk distributions to actual churn outcomes

This monitoring catches model degradation before it impacts churn rates.

### 5. Calibrate monthly

At the end of each month, run a calibration pass:

1. Pull all `churn_risk_scored` events from 30 days ago
2. Compare predicted risk tiers to actual outcomes (retained vs. churned)
3. Identify systematic errors: are certain signals over-weighted or under-weighted?
4. Update the scoring prompt with calibration notes (e.g., "Weight feature_abandonment more heavily for power users; login_gap is less predictive for accounts with seasonal usage patterns")

The calibration notes accumulate in the system prompt, improving accuracy without retraining a traditional ML model.

### 6. Evaluate at scale

After 2 months, measure against the pass threshold:

- Prediction accuracy across 500+ users: must be >=65%
- Per-segment accuracy: no segment below 50%
- Overall churn rate reduction compared to pre-model baseline
- Save rate trend: improving or stable (not declining)

If PASS, proceed to Durable. If FAIL, identify the weakest segment, run targeted calibration on it, and extend the Scalable period by 2 weeks.

## Time Estimate

- 10 hours: segment the scoring model by persona, calculate per-segment baselines
- 12 hours: create persona-specific intervention templates (Loops sequences, Intercom messages)
- 15 hours: run 3 A/B tests on intervention variations (setup, monitoring, analysis)
- 8 hours: deploy and configure the model health monitor
- 10 hours: monthly calibration passes (2 passes over 2 months)
- 5 hours: final evaluation, documentation, Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohort segmentation, feature flags, A/B testing, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Daily scoring for 500+ users, calibration | ~$50-150/mo at scale — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Loops | Persona-specific re-engagement sequences | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages, product tours for at-risk users | Essential $29/seat/mo; Proactive Support $349/mo if using advanced targeting — [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $130-400/mo** (Anthropic API at scale + Loops + Intercom proactive messaging)

## Drills Referenced

- `churn-signal-extraction` — persona-segmented daily scoring with per-segment baselines
- `churn-intervention-routing` — persona-specific intervention templates and routing logic
- `ab-test-orchestrator` — systematic A/B testing of intervention variations
- `dashboard-builder` — ongoing monitoring of prediction accuracy, save rates, and calibration drift
