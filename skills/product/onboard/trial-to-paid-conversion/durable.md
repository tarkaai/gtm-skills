---
name: trial-to-paid-conversion-durable
description: >
  Trial-to-Paid Conversion — Durable Intelligence. Always-on AI agents monitor trial
  conversion metrics, detect anomalies, generate improvement hypotheses, run A/B experiments
  on interventions and onboarding flows, and auto-implement winners. Converges when successive
  experiments yield <2% lift.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Durable Intelligence"
time: "Ongoing — 12 hours setup, then 2-4 hours/week agent-managed"
outcome: "Trial-to-paid conversion sustained or improving >=50% over 6 months via autonomous optimization"
kpis: ["Trial-to-paid conversion rate (weekly trend)", "Experiment velocity (experiments/month)", "Cumulative AI lift (% improvement from auto-implemented changes)", "Time to convergence", "Anomaly detection latency"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add product/onboard/trial-to-paid-conversion"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Trial-to-Paid Conversion — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

An always-on AI agent continuously monitors trial conversion metrics, detects anomalies within hours, generates data-driven improvement hypotheses, runs controlled experiments on interventions and onboarding flows, and auto-implements winners. The trial-to-paid conversion rate sustains at >= 50% or improves over 6 months. The system converges when three successive experiments produce < 2% lift, indicating the local maximum has been found for the current product/market configuration.

## Leading Indicators

- Anomaly detection fires within 4 hours of a metric deviation exceeding 15%
- At least 2-3 experiments run per month (experiment velocity)
- Experiment win rate exceeds 30% (healthy hypothesis quality)
- Cumulative AI lift shows positive trend over a 3-month window
- Weekly optimization briefs generate on schedule with actionable recommendations
- No undetected metric drops lasting more than 48 hours

## Instructions

### 1. Build the trial conversion dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard that serves as the agent's primary data source for monitoring and diagnosis.

Required panels:

- **Trial-to-paid conversion rate (weekly, 12-week trend):** Line chart with threshold line at 50%. Break out by signup source (organic, paid, referral, direct).
- **72-hour activation rate (weekly trend):** Leading indicator. Drops here predict conversion drops 1-2 weeks later.
- **Funnel step conversion rates:** Bar chart showing conversion at each step: trial_started -> onboarding_tour_completed -> activation_reached -> feature_explored -> upgrade_prompt_shown -> upgrade_started -> payment_completed. Updated weekly.
- **Intervention effectiveness matrix:** Table showing each intervention type (milestone coaching, upgrade nudge, urgency prompt, rescue call, etc.) with: volume delivered, engagement rate, conversion lift vs. control.
- **Upgrade prompt performance by trigger type:** Table showing impressions, CTR, and conversion for each prompt trigger (limit proximity, feature gate, value milestone, expiry countdown).
- **Trial health score distribution:** Histogram showing the Hot/Warm/Cold distribution over time. A shift toward Cold indicates an onboarding or product issue.
- **Churn intervention save rate:** Percentage of at-risk trial users who re-engage after intervention, broken out by intervention type and risk tier.
- **Experiment tracker:** Active experiments, days running, preliminary results. This panel is informational — the autonomous-optimization drill handles evaluation decisions.
- **Cohort heatmap:** Weekly signup cohorts showing Day 1, 3, 7, 14 engagement. Visual early warning for engagement decay.

Set dashboard alerts for: conversion rate drops > 15% below 4-week average, activation rate drops > 20%, any upgrade prompt CTR drops > 40%, trial health score distribution shifts > 25% toward Cold.

### 2. Deploy continuous health monitoring

Run the `autonomous-optimization` drill to establish the daily and weekly monitoring cadence:

**Daily monitoring (n8n cron, 08:00 UTC):**
- Query PostHog for all trial conversion KPIs from the last 7 days
- Compare each metric against its 4-week rolling average using the `posthog-anomaly-detection` fundamental
- Classify: normal (within 10%), plateau (within 2% for 3+ weeks), warning (10-20% below), critical (> 20% below or below the 50% play threshold)
- Normal: log healthy status to Attio
- Warning: log observation to Attio with the specific metric and drift amount
- Critical: send immediate alert with metric, current value, expected value, and suggested investigation steps
- Plateau: trigger the autonomous-optimization diagnose phase (plateau = optimization opportunity)

**Weekly report (n8n cron, Monday 09:00 UTC):**
- Full trial funnel performance with week-over-week comparisons
- Intervention effectiveness by type and channel with lift calculations
- Upgrade prompt performance by trigger type
- Per-source-channel breakdown (are paid trial users converting differently than organic?)
- Active experiments and their status
- Trial health score distribution shift analysis
- Anomalies detected during the week and actions taken
- Recommended focus areas for the coming week

**Signup-source drift detection (weekly):**
- Compare this week's trial signup source distribution against 4-week average
- Flag if any source shifts by > 25% (e.g., paid traffic drops, organic surges)
- Drift changes the trial user profile, which may require onboarding path updates rather than tactical intervention fixes

### 3. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the trial-to-paid conversion play. This is the core loop that makes Durable fundamentally different from Scalable.

**Phase 1 — Monitor (daily):**
The trial-conversion-health-monitor feeds anomaly and plateau signals into this phase. When a metric deviates, the agent classifies the anomaly type:
- **Activation problem:** 72-hour activation rate dropped. Something is wrong with onboarding.
- **Engagement problem:** users activate but stop using the product before trial ends. Value delivery issue.
- **Intervention problem:** intervention effectiveness (CTR, save rate) dropped. Message fatigue or targeting drift.
- **Conversion problem:** activated users are not upgrading. Pricing, prompt timing, or urgency messaging issue.

**Phase 2 — Diagnose (triggered by anomaly or plateau):**
The agent gathers context:
- Pull the current intervention configuration from Attio (active interventions, trigger rules, email sequences, upgrade prompt copy, A/B test history)
- Pull 8-week metric history from the trial conversion dashboard
- Run `hypothesis-generation` with the anomaly type and context data
- Receive 3 ranked hypotheses. Example hypotheses for this play:
  - "Activation rate dropped because a product deploy changed the workflow that onboarding Step 3 references. Hypothesis: update the product tour to reference the new UI."
  - "Upgrade prompt CTR declined because the value-milestone prompt has shown the same copy to 4 consecutive cohorts. Hypothesis: refresh the copy with updated customer success data."
  - "Warm-segment conversion plateaued because the rescue email lands in promotions tab. Hypothesis: switch rescue email from Loops to a personal Gmail send via n8n."
  - "Trial expiry conversion dropped because competitors now offer 30-day trials. Hypothesis: test extending trial from 14 to 21 days for Warm-segment users."
- Store hypotheses in Attio as notes on the play record
- If risk = "high" (e.g., changes pricing, changes trial length for all users, modifies core onboarding flow): alert human for review, STOP
- If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use PostHog experiments to create a feature flag splitting traffic: control (current) vs. variant (hypothesis change)
- Implement the variant using the appropriate tool:
  - Onboarding flow changes: Intercom product tours
  - Email sequence changes: Loops
  - Upgrade prompt changes: Intercom in-app messages
  - Intervention routing changes: n8n workflow configuration
  - Trial length changes: PostHog feature flag controlling trial duration
- Set experiment duration: minimum 7 days or 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success metric, guardrail metrics

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog using `experiment-evaluation`
- Decision matrix:
  - **Significant winner (> 95% confidence, > 2% lift):** Adopt the variant. Update the live configuration. Log the change and lift in Attio.
  - **Significant loser:** Revert to control. Log the failure. Return to Phase 1. 7-day cooldown before testing the same variable.
  - **Inconclusive:** Extend for one more period if sample is close to significance. Otherwise, revert and move to the next hypothesis.
- Store the full evaluation in Attio: decision, confidence, effect size, reasoning

**Phase 5 — Report (weekly):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on trial-to-paid conversion
  - Current distance from estimated local maximum (based on diminishing experiment returns)
  - Intervention effectiveness trends (which interventions are improving, which are degrading)
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails (CRITICAL):**
- Maximum 1 active experiment on the trial funnel at a time. Never stack experiments.
- Auto-revert if primary conversion metric drops > 30% at any point during an experiment
- Human approval required for:
  - Changes to pricing or plan structure
  - Changes to trial length affecting > 50% of users
  - Any hypothesis the generator flags as "high risk"
  - Changes that reduce the intervention touchpoint count (e.g., removing a rescue campaign)
- Cooldown: 7 days after a failed experiment before testing the same variable
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- Never optimize what is not measured: if a KPI does not have PostHog tracking, fix tracking first using `posthog-gtm-events` before running experiments.

### 4. Detect convergence

The optimization loop tracks experiment yields over time. When three consecutive experiments produce < 2% improvement on the primary metric:

1. The play has reached its local maximum for the current product/market configuration
2. Reduce monitoring from daily to weekly
3. Generate a convergence report: "Trial-to-paid conversion optimized at [X%]. Current intervention matrix: [summary]. Further gains require strategic changes (new trial model, pricing restructure, product improvements, new signup channels) rather than tactical optimization of the current flow."
4. Continue weekly monitoring to detect regression from external changes (product updates, market shifts, seasonal patterns, competitor moves)

**Human action required:** When convergence is reached, review the report and decide whether to: accept the local maximum, invest in strategic changes to shift the ceiling (e.g., rebuild onboarding for a new ICP segment), or redirect optimization resources to another play.

## Time Estimate

- 4 hours: Dashboard build and alert configuration
- 4 hours: Health monitor deployment (daily + weekly n8n workflows)
- 4 hours: Autonomous optimization loop configuration and first hypothesis cycle
- Ongoing: 2-4 hours/week agent-managed (human reviews weekly briefs, approves high-risk experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, experiments, anomaly detection, feature flags, cohorts | Free tier or usage-based ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app message experiment variants, product tour variants | $29-85/seat/mo + Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email experiment variants, sequence updates | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop scheduling, alert routing, intervention routing, CRM sync | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief writing | Usage-based ~$15/MTok input, ~$75/MTok output ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Experiment logging, play record, intervention audit trail | Standard stack |

**Estimated play-specific cost:** ~$150-600/mo (shared stack costs + Anthropic API usage for hypothesis generation and evaluation)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners. Converges when successive experiments yield < 2% lift.
- `autonomous-optimization` — continuous daily/weekly monitoring of trial conversion funnel, intervention effectiveness, and trial health score distribution with anomaly alerts and cohort drift detection that feed into the optimization loop
- `dashboard-builder` — builds the PostHog dashboard that serves as the agent's primary data source for monitoring, diagnosis, and experiment tracking
