---
name: free-trial-optimization-durable
description: >
  Trial Conversion Optimization — Durable Intelligence. Always-on AI agents monitor trial
  conversion metrics, detect anomalies, generate improvement hypotheses, run A/B experiments,
  and auto-implement winners. Converges when successive experiments yield <2% lift.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "Ongoing — 10 hours setup, then 2-4 hours/week agent-managed"
outcome: "Trial-to-paid conversion sustained or improving >=30% over 6 months via autonomous optimization"
kpis: ["Trial-to-paid conversion rate (weekly trend)", "Experiment velocity (experiments/month)", "Cumulative AI lift (% improvement from auto-implemented changes)", "Time to convergence", "Anomaly detection latency"]
slug: "free-trial-optimization"
install: "npx gtm-skills add product/onboard/free-trial-optimization"
drills:
  - autonomous-optimization
  - trial-conversion-health-monitor
  - dashboard-builder
---

# Trial Conversion Optimization — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

An always-on AI agent continuously monitors trial conversion metrics, detects anomalies within hours, generates data-driven improvement hypotheses, runs controlled experiments, and auto-implements winners. The trial conversion rate sustains at >=30% or improves over 6 months. The system converges when three successive experiments produce <2% lift, indicating the local maximum has been found.

## Leading Indicators

- Anomaly detection fires within 4 hours of a metric deviation exceeding 15%
- At least 2-3 experiments run per month (experiment velocity)
- Experiment win rate exceeds 30% (healthy hypothesis quality)
- Cumulative AI lift shows positive trend over 3-month window
- Weekly optimization briefs generate on schedule with actionable recommendations
- No undetected metric drops lasting more than 48 hours

## Instructions

### 1. Build the trial conversion dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for the autonomous optimization loop. The dashboard serves as the agent's primary data source.

Required panels:
- **Trial-to-paid conversion rate (weekly, 12-week trend):** Line chart with threshold line at 30%. Break out by signup source.
- **72-hour activation rate (weekly trend):** Leading indicator. Drops here predict conversion drops 1-2 weeks later.
- **Funnel step conversion rates:** Bar chart showing conversion at each step: trial_started -> tour_completed -> activation_reached -> feature_explored -> upgrade_prompt_shown -> upgrade_started -> payment_completed. Updated weekly.
- **Upgrade prompt performance by trigger type:** Table showing impressions, CTR, and conversion for each prompt trigger (limit proximity, feature gate, value milestone, expiry countdown).
- **Churn intervention save rate:** Percentage of at-risk trial users who re-engage after intervention, broken out by intervention type.
- **Experiment tracker:** Active experiments, days running, preliminary results (do not use for decisions — the autonomous-optimization drill handles evaluation).
- **Cohort heatmap:** Weekly signup cohorts showing Day 1, 3, 7, 14 engagement. Visual early warning for engagement decay.

Set dashboard alerts for: conversion rate drops >15% below 4-week average, activation rate drops >20%, upgrade prompt CTR drops >40%.

### 2. Deploy continuous health monitoring

Run the `trial-conversion-health-monitor` drill to establish the daily and weekly monitoring cadence:

**Daily monitoring (n8n cron, 08:00 UTC):**
- Query PostHog for all trial conversion KPIs from the last 7 days
- Compare each metric against its 4-week rolling average using the `posthog-anomaly-detection` fundamental
- Classify: normal (within 10%), plateau (within 2% for 3+ weeks), warning (10-20% below), critical (>20% below or below play threshold)
- Normal: log healthy status to Attio
- Warning: log observation to Attio with the specific metric and drift amount
- Critical: send immediate alert with metric, current value, expected value, and suggested investigation steps
- Plateau: trigger the autonomous-optimization diagnose phase (plateau = optimization opportunity)

**Weekly report (n8n cron, Monday 09:00 UTC):**
- Full trial funnel performance with week-over-week comparisons
- Per-source-channel breakdown (are paid trial users converting differently than organic?)
- Upgrade prompt performance by trigger type
- Active experiments and their status
- Anomalies detected during the week and actions taken
- Recommended focus areas for the coming week

**Signup-source drift detection (weekly):**
- Compare this week's trial signup source distribution against 4-week average
- Flag if any source shifts by >25% (e.g., paid traffic drops, organic surges)
- Drift changes the trial user profile, which may require onboarding path updates rather than tactical fixes

### 3. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the trial conversion play. This is the core loop that makes Durable fundamentally different.

**Phase 1 — Monitor (daily):**
The trial-conversion-health-monitor feeds anomaly and plateau signals into this phase. When a metric deviates, the agent classifies the type: activation problem, engagement problem, prompt problem, or conversion problem.

**Phase 2 — Diagnose (triggered by anomaly or plateau):**
The agent gathers context:
- Pull the current onboarding configuration from Attio (tour version, email sequence, prompt triggers, A/B test history)
- Pull 8-week metric history from the trial conversion dashboard
- Run `hypothesis-generation` with the anomaly type and context data
- Receive 3 ranked hypotheses. Example hypotheses for trial conversion:
  - "Activation rate dropped because the product tour's Step 3 requires a feature that was changed in last week's deploy. Hypothesis: update the tour to reference the new UI."
  - "Upgrade prompt CTR declined because the Day -5 banner has been shown to the same cohort for 6 weeks. Hypothesis: refresh the copy and change the value proposition framing."
  - "Conversion rate plateaued because the email sequence has not been updated in 8 weeks. Hypothesis: test a new Day 3 email that addresses the most common objection from recent churned trial users."
- Store hypotheses in Attio as notes on the play record
- If risk = "high" (e.g., changes targeting, budget, or core flow): alert human for review, STOP
- If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use `posthog-experiments` to create a feature flag splitting traffic: control (current) vs. variant (hypothesis change)
- Implement the variant using the appropriate tool: Intercom for in-app changes, Loops for email changes, product code for flow changes
- Set experiment duration: minimum 7 days or 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success metric, guardrail metrics

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog using `experiment-evaluation`
- Decision matrix:
  - **Significant winner (>95% confidence, >2% lift):** Adopt the variant. Update the live configuration. Log the change and lift in Attio.
  - **Significant loser:** Revert to control. Log the failure. Return to Phase 1. 7-day cooldown before testing the same variable.
  - **Inconclusive:** Extend for one more period if sample is close. Otherwise, revert and move to the next hypothesis.
- Store the full evaluation in Attio: decision, confidence, effect size, reasoning

**Phase 5 — Report (weekly):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate: net metric change from all adopted changes
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on trial-to-paid conversion
  - Distance from estimated local maximum (based on diminishing experiment returns)
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails (CRITICAL):**
- Maximum 1 active experiment on the trial funnel at a time
- Auto-revert if primary conversion metric drops >30% during any experiment
- Human approval required for: changes to pricing/plan structure, changes affecting >50% of trial users, any "high risk" hypothesis
- Cooldown: 7 days after a failed experiment before testing the same variable
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.

### 4. Detect convergence

The optimization loop tracks experiment yields over time. When three consecutive experiments produce <2% improvement on the primary metric:
1. The play has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Generate a convergence report: "Trial conversion optimized at [X%]. Further gains require strategic changes (new trial model, pricing changes, product improvements) rather than tactical optimization of the current flow."
4. Continue weekly monitoring to detect regression from external changes (product updates, market shifts, seasonal patterns)

**Human action required:** When convergence is reached, review the report and decide whether to: accept the local maximum, invest in strategic changes to shift the ceiling, or redirect optimization resources to another play.

## Time Estimate

- 4 hours: Dashboard build and alert configuration
- 3 hours: Health monitor deployment (daily + weekly n8n workflows)
- 3 hours: Autonomous optimization loop configuration
- Ongoing: 2-4 hours/week agent-managed (human reviews weekly briefs, approves high-risk experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, experiments, anomaly detection, cohorts | Free tier or usage-based ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages for experiment variants | $29-85/seat/mo + Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email experiment variants | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop scheduling, alert routing, CRM sync | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Anthropic API | Hypothesis generation, experiment evaluation, report writing | Usage-based ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Experiment logging, play record, audit trail | Standard stack |

**Estimated play-specific cost:** ~$100-500/mo (shared stack costs + Anthropic API usage for hypothesis generation)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners. Converges when successive experiments yield <2% lift.
- `trial-conversion-health-monitor` — continuous daily/weekly monitoring of trial conversion funnel with anomaly alerts, cohort drift detection, and structured health reports that feed into the optimization loop
- `dashboard-builder` — builds the PostHog dashboard that serves as the agent's primary data source for monitoring and diagnosis
