---
name: health-score-dashboard-scalable
description: >
  Account Health Scoring — Scalable Automation. Connect health scores to automated interventions:
  in-app messages for declining accounts, triggered emails for at-risk, CRM tasks for critical.
  A/B test intervention strategies. Scale to 500+ accounts with >=75% prediction accuracy.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=75% prediction accuracy at 500+ accounts with automated interventions producing >=20% recovery rate"
kpis: ["Prediction accuracy at scale", "Intervention recovery rate", "Time from risk detection to intervention", "False positive rate", "Net retention impact"]
slug: "health-score-dashboard"
install: "npx gtm-skills add product/retain/health-score-dashboard"
drills:
  - health-score-alerting
  - churn-prevention
  - ab-test-orchestrator
  - threshold-engine
---
# Account Health Scoring — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Connect the validated health scoring system to automated intervention workflows. When an account's health drops, the right action fires automatically: in-app nudges, triggered emails, or CRM tasks for human outreach. A/B test intervention strategies to find what actually saves at-risk accounts. Scale from 20 manually scored accounts to 500+ with automated scoring and intervention.

**Pass threshold:** >=75% prediction accuracy at 500+ accounts AND automated interventions producing >=20% recovery rate (accounts that improve after intervention).

## Leading Indicators

- Interventions fire within 24 hours of a risk level change (no manual delay)
- In-app messages for declining accounts achieve >10% engagement rate
- At-risk outreach emails achieve >25% open rate and >5% reply rate
- At least 3 A/B tests completed on intervention strategies within 2 months
- False positive rate (accounts flagged At Risk that were actually fine) stays below 25%

## Instructions

### 1. Build automated intervention routing

Run the `health-score-alerting` drill to create the n8n workflow that connects score changes to actions:

**Tier 1 — In-app nudges (automated):**
When an account drops from Healthy to Monitor, or any dimension drops >15 points in a week, trigger an Intercom in-app message. The message content is dynamic based on which dimension declined:
- Usage dropped: "Your team hasn't been as active recently. Need help with anything?"
- Engagement dropped: "You haven't tried [underused feature] yet. Here's a quick guide."
- Support spiked: "We see you've had some issues. Here's a direct line to our team: [link]."
- Adoption stalled: "Complete your setup — connect [integration] to unlock [benefit]."

**Tier 2 — Outreach emails (automated):**
When an account enters At Risk tier, trigger a Loops email from the account owner. Personalize with the account's specific declining dimension and usage data. Include a calendar booking link for a check-in call.

**Tier 3 — Human intervention (CRM task):**
When an account enters Critical tier, create an Attio task for the account owner with full context: score history, dimension breakdown, specific signals that triggered the drop, and suggested talking points.

**Tier 4 — Expansion signals:**
When a Healthy account shows growth signals (usage in top 20th percentile, team penetration >80%), flag it in Attio as "Expansion Ready" and send an in-app message suggesting advanced features or plan upgrades.

### 2. Connect health scores to churn prevention

Run the `churn-prevention` drill, but replace its default churn detection with your health score system. Instead of building churn signals from scratch, use the health score's dimension scores as the signal layer:

- Health score < 40 = the `churn-prevention` drill's "high risk" tier
- Usage dimension declining for 3+ weeks = the drill's "usage decline" signal
- Support dimension < 30 = the drill's "support increase" signal

This avoids duplicate detection systems. The health score IS the churn detection layer.

### 3. A/B test intervention strategies

Run the `ab-test-orchestrator` drill to test which intervention approaches produce the highest recovery rate:

**Test 1: Message framing (Tier 1 nudges)**
- Control: Feature-focused message ("Try [feature] to save time")
- Variant: Outcome-focused message ("Teams like yours save 5 hours/week with [feature]")
- Metric: Engagement rate + 14-day health score recovery

**Test 2: Email sender (Tier 2 outreach)**
- Control: Email from "Customer Success Team"
- Variant: Email from the founder/CEO
- Metric: Open rate, reply rate, 14-day health score recovery

**Test 3: Intervention timing (Tier 2 outreach)**
- Control: Trigger email when score first enters At Risk
- Variant: Trigger email after 3 consecutive days in At Risk (more confident signal)
- Metric: Recovery rate, false positive rate

Use PostHog feature flags to split accounts into test groups. Run each test for 4+ weeks to accumulate enough data.

### 4. Scale to 500+ accounts

As your customer base grows, ensure the system handles scale:

- Verify the n8n scoring pipeline completes within 30 minutes for 500+ accounts (optimize PostHog queries if needed — batch by 50 accounts per query)
- Monitor PostHog event volume: 500 accounts x daily scoring = 500 events/day + dimension events
- Verify Attio API rate limits are not hit during bulk score writes (100 req/s limit)
- Add error handling: if the pipeline fails for a subset of accounts, log errors and continue scoring the rest
- Add a "stale score" alert: if any account was not scored in the last 48 hours, flag it for investigation

### 5. Measure net retention impact

Track the system's impact on business outcomes:

- Pull monthly churn rate from before health scoring was active (Baseline period)
- Compare to monthly churn rate after Scalable has been running for 1+ month
- Attribute: for each churned account, check whether the health score flagged it in advance and whether an intervention was attempted
- Calculate: "Accounts saved" = accounts that were At Risk, received intervention, and recovered to Monitor or Healthy
- Calculate dollar impact: sum of MRR for "accounts saved"

### 6. Evaluate against threshold

Run the `threshold-engine` drill:

- Prediction accuracy at 500+ accounts >=75%? (Of accounts that churned, were >=75% flagged in advance?)
- Intervention recovery rate >=20%? (Of accounts that received Tier 1-3 interventions, did >=20% improve their health score within 14 days?)

If PASS: Proceed to Durable. The system detects risk and automatically intervenes with measurable effect.

If FAIL: Diagnose — is the issue prediction accuracy (model needs recalibration at scale) or intervention effectiveness (messages not resonating)? Focus optimization effort on the weaker area.

## Time Estimate

- 12 hours: Build intervention routing workflow (alerting drill)
- 8 hours: Connect health scores to churn prevention system
- 16 hours: Design, launch, and monitor 3 A/B tests over 2 months
- 8 hours: Scale testing (pipeline performance, error handling)
- 8 hours: Measure retention impact and evaluate threshold
- 8 hours: Iterate on model weights and intervention copy based on results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data, dashboards, A/B testing | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Account records, score storage, tasks | Free tier or existing plan — [attio.com/pricing](https://attio.com/pricing) |
| n8n | Scoring pipeline + intervention routing | Self-hosted free or Cloud from EUR 20/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app messages for Tier 1 + Tier 4 | Starter $74/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered outreach emails for Tier 2 | Free tier (1K contacts) or Starter $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** ~$75-125/mo (Intercom + Loops)

## Drills Referenced

- `health-score-alerting` — Routes health score changes to tiered interventions
- `churn-prevention` — Provides the churn intervention framework, powered by health scores
- `ab-test-orchestrator` — Tests intervention strategies for statistical significance
- `threshold-engine` — Evaluates prediction accuracy and recovery rate against thresholds
