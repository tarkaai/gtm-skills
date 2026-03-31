---
name: winback-campaign-durable
description: >
  Churned User Win-back — Durable Intelligence. Autonomous AI agent continuously
  optimizes the winback system: tests new offers, adjusts timing, retires failing
  segments, recalibrates churn reason classification, and maintains reactivation
  rates at their local maximum without human input.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Durable Intelligence"
time: "40 hours setup + ongoing autonomous"
outcome: "Sustained ≥12% reactivation rate over 6 months via autonomous optimization"
kpis: ["Reactivation rate", "30-day retention of reactivated users", "Rechurn rate", "Cost per reactivation", "Experiment velocity", "Autonomous optimization lift"]
slug: "winback-campaign"
install: "npx gtm-skills add product/winback/winback-campaign"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Churned User Win-back — Durable Intelligence

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

The winback system runs autonomously. An AI agent monitors reactivation rates across all segments, detects when performance plateaus or drops, generates hypotheses for what to change (offer types, messaging copy, send timing, channel routing, segment definitions), runs A/B experiments, evaluates results, and auto-implements winners. The agent also recalibrates the churn reason classification model monthly as churn patterns shift.

The goal is to find and maintain the **local maximum** of the winback system — the best possible reactivation rate given the current product, user base, and competitive landscape.

Pass threshold: **Sustained ≥12% reactivation rate over 6 months** with the autonomous optimization loop running. Convergence: when 3 consecutive experiments produce <2% improvement, the system is at its local maximum.

## Leading Indicators

- The autonomous optimization loop runs weekly without human intervention
- Experiments are generated, executed, and evaluated automatically
- Reactivation rate does not degrade month-over-month (or recovers within 2 weeks when it dips)
- Weekly optimization briefs are generated and distributed
- 30-day retention of reactivated users remains above 55%
- Rechurn rate stays below 35%

## Instructions

### 1. Build the winback performance dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for the winback-campaign play. Include these panels:

- **Reactivation rate trend:** Weekly reactivation rate over the last 24 weeks. Add a horizontal threshold line at 12%.
- **Winback funnel:** `winback_email_sent` -> `winback_engaged` -> `winback_reactivated` -> `winback_retained_30d`. Shows the full email-to-retention pipeline.
- **Segment performance heatmap:** Reactivation rate by churn reason segment (rows) and recency sub-segment (columns). Color-coded: green >15%, yellow 8-15%, red <8%.
- **Offer effectiveness:** Reactivation rate and rechurn rate by offer type (discount, free trial, feature announcement, personal walkthrough). Shows which offers produce quality reactivations vs. deal-seekers.
- **Channel performance:** Side-by-side comparison of engagement rate and reactivation rate for email, in-app, and personal channels.
- **Reactivated user retention:** 30-day and 90-day retention curves for reactivated users vs. never-churned users.
- **Revenue recovered:** MRR from reactivated users this month, cumulative recovered MRR trend.
- **Experiment log:** Table showing all experiments run by the autonomous optimization loop: hypothesis, start date, result, metric impact.

### 2. Deploy the winback campaign health monitor

Run the `autonomous-optimization` drill to build the always-on monitoring layer:

- Daily anomaly checks on reactivation rate, email open rate, segment performance, rechurn rate, and reactivated user retention
- Weekly health briefs aggregating metrics, surfacing the biggest optimization opportunity, and listing active experiments
- Critical alerts when reactivation rate drops >30% below the 4-week average, email delivery fails, or rechurn rate exceeds 50%
- Segment retirement recommendations when a segment stays below 3% reactivation for 8+ weeks
- All signals stored in Attio for the optimization loop to query

This monitor is the eyes of the Durable system. Without it, the autonomous optimization loop has no signal to act on.

### 3. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill, configured for the winback-campaign play. The loop operates on a weekly cadence:

**Monitor (daily):** The `autonomous-optimization` checks all winback metrics against rolling averages. Anomalies trigger the Diagnose phase.

**Diagnose (triggered by anomaly):** The agent pulls 8 weeks of winback data from PostHog and the current system configuration from Attio (active segments, offer types, send timing, channel routing, sequence copy). It generates 3 ranked hypotheses. Examples of hypotheses the agent might generate:

- "Price churner reactivation dropped 18% — test a higher discount (25% vs. current 20%) for the fresh sub-segment to determine if the current offer is no longer competitive"
- "Inactive churner segment has been below 5% for 6 weeks — test replacing the re-education email with a 'new onboarding experience' invitation that puts them through the latest activation flow"
- "Email 1 open rate declined from 42% to 31% — test a new subject line format: question-based ('Still thinking about [product]?') vs. current announcement format"
- "Returning churned users who see the in-app welcome-back message reactivate at 3x the email-only rate — test adding a push notification (via Intercom) to drive more churned users back to the site"
- "30-day retention of discount-reactivated users is 45% vs. 72% for feature-announcement-reactivated users — reduce discount offers and increase feature-specific offers for all segments to improve reactivated user quality"
- "Stale churners (91-180 days) produce <4% reactivation — test retiring stale segment entirely and reallocating budget to fresh and mid segments"

**Experiment (triggered by hypothesis acceptance):** The agent implements the top hypothesis as a PostHog experiment. It creates a feature flag splitting the relevant population between control (current approach) and variant (hypothesis change). Maximum 1 active experiment at a time. Minimum 7 days or 100 users per variant.

**Evaluate (triggered by experiment completion):** The agent pulls results, calculates statistical significance, and decides:
- **Adopt:** Implement the winning variant. Update the Loops sequence, Intercom message, or n8n workflow accordingly. Log the change.
- **Iterate:** Generate a new hypothesis building on this result. Return to Diagnose.
- **Revert:** Restore the control. Log the failure. Return to Monitor.
- **Extend:** Keep the experiment running for another period if data is insufficient.

All decisions logged in Attio with: hypothesis, variants, sample size, result, confidence, and decision.

**Report (weekly):** The agent generates a weekly optimization brief:

```
# Winback Campaign Optimization Brief — Week of [date]

## Changes This Week
- [Experiment completed: adopted/reverted/extended — impact on reactivation rate]

## Current Performance
- Reactivation rate: [X%] (threshold: 12%, local max estimate: [Y%])
- Total reactivations this week: [N]
- 30-day retention of reactivated: [X%]
- Rechurn rate: [X%]
- Cost per reactivation: $[X]
- Revenue recovered this month: $[X] MRR

## Segment Health
| Segment | Reactivation | Trend | Volume | Status |
|---------|--------------|-------|--------|--------|
| Price (fresh) | [X%] | [trend] | [N] | [active/watch/retire] |
| Price (mid) | [X%] | ... | ... | ... |
| Feature (fresh) | [X%] | ... | ... | ... |
| Competitor (fresh) | [X%] | ... | ... | ... |
| Inactive (fresh) | [X%] | ... | ... | ... |
| Experience (mid) | [X%] | ... | ... | ... |

## Offer Quality
| Offer Type | Reactivation | 30-day Retention | Rechurn | Quality Score |
|------------|--------------|------------------|---------|---------------|
| Discount   | [X%]         | [X%]             | [X%]    | [high/med/low] |
| Free trial | [X%]         | [X%]             | [X%]    | ... |
| Feature announce | [X%]  | [X%]             | [X%]    | ... |

## Next Experiment
- Hypothesis: [description]
- Expected impact: [+/- X% on reactivation rate]
- Risk level: [low/medium]
- Start date: [date]

## Distance from Local Maximum
[Assessment: converging / still optimizing / degrading]
[If converging: N consecutive experiments with <2% improvement]
```

### 4. Set up monthly churn reason recalibration

Churn patterns shift as the product evolves and the market changes. Configure a monthly n8n workflow that:

1. Pulls all users who churned in the last 90 days
2. Re-analyzes the correlation between churn signals and stated churn reasons
3. Checks whether the segment assignments are still accurate (e.g., are users classified as "price churners" actually churning because of price, or has a product issue emerged?)
4. Adjusts segment assignment rules if classification accuracy drops below 70%
5. Identifies any new churn reason patterns that do not fit existing segments
6. Logs the recalibration results in PostHog (`winback_model_calibration` event) and Attio
7. If a new churn reason pattern affects >15% of recent churners, flag for human review — a new segment may be needed

### 5. Configure guardrails

The autonomous system must have hard limits:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If reactivation rate drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Discount offers exceeding 30% (margin protection)
  - Offer changes that affect >50% of the churned population
  - Any experiment the hypothesis generator flags as "high risk"
  - Retiring a segment that represents >20% of the churned population
- **Contact frequency cap:** No churned user receives more than 5 winback touches in a 90-day window, regardless of experiments.
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable again.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Quality floor:** If 30-day retention of reactivated users drops below 40%, pause all discount-based offers and investigate whether winback is producing low-quality reactivations.

### 6. Evaluate sustainability

This level runs continuously. Monthly check:
- Is reactivation rate above the 12% threshold?
- Has the optimization loop run experiments this month?
- Are weekly briefs being generated?
- Is reactivated user retention holding above 55%?
- Has the churn reason model been recalibrated?

If reactivation rate sustains or improves for 6 consecutive months, the play is durable. If the optimization loop detects convergence (<2% improvement for 3 consecutive experiments), report to the team: "Winback system is at local maximum. Reactivation rate of [X%] is the best achievable through tactical optimization. Further gains require strategic changes: product improvements that eliminate churn reasons, new winback channels, or addressing root causes in the retention plays upstream."

## Time Estimate

- 8 hours: Build winback performance dashboard
- 10 hours: Deploy health monitor (daily checks, weekly briefs, alerts)
- 12 hours: Configure autonomous optimization loop (monitor, diagnose, experiment, evaluate, report)
- 6 hours: Set up monthly churn reason recalibration
- 4 hours: Configure guardrails and test safety mechanisms
- Ongoing: Agent runs autonomously. Human reviews weekly briefs (~30 min/week).

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, dashboards, anomaly detection, retention analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated winback sequences at scale | $49/mo+ based on contacts — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app welcome-back messages, multi-channel messaging | $85/seat/mo Advanced; +$99/mo Proactive Support — [intercom.com/pricing](https://www.intercom.com/pricing) |
| n8n | Optimization loop, recalibration, monitoring workflows | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | ~$15-30/mo at weekly cadence — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost at Durable:** ~$175-400/mo (Intercom Advanced + Proactive + Loops + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor -> diagnose -> experiment -> evaluate -> implement. Runs weekly and finds the local maximum of the winback system.
- `autonomous-optimization` — play-specific monitoring that feeds signals to the optimization loop. Daily anomaly checks, weekly health briefs, critical alerts, segment retirement recommendations.
- `dashboard-builder` — PostHog dashboard with reactivation trends, segment heatmaps, offer quality analysis, retention curves, revenue recovery, and experiment log.
