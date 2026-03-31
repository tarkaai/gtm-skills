---
name: at-risk-intervention-durable
description: >
  At-Risk User Intervention — Durable Intelligence. Autonomous AI agent continuously
  optimizes the intervention system: recalibrates the scoring model, experiments with
  messaging and timing, adapts channel strategy, and maintains save rates at their
  local maximum without human input.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Durable Intelligence"
time: "40 hours setup + ongoing autonomous"
outcome: "Sustained ≥25% save rate over 6 months via autonomous optimization"
kpis: ["Save rate", "Response rate", "30-day retention of saved users", "Experiment velocity", "Scoring model precision", "Autonomous optimization lift"]
slug: "at-risk-intervention"
install: "npx gtm-skills add product/winback/at-risk-intervention"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# At-Risk User Intervention — Durable Intelligence

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

The intervention system runs autonomously. An AI agent monitors intervention effectiveness, detects when save rates plateau or drop, generates hypotheses for what to change (scoring thresholds, message copy, channel routing, intervention timing), runs A/B experiments, evaluates results, and auto-implements winners. The agent also recalibrates the churn risk scoring model monthly as user behavior patterns shift.

The goal is to find and maintain the **local maximum** of the intervention system — the best possible save rate given the current product, user base, and competitive landscape.

Pass threshold: **Sustained ≥25% save rate over 6 months** with the autonomous optimization loop running. Convergence: when 3 consecutive experiments produce <2% improvement, the system is at its local maximum.

## Leading Indicators

- The autonomous optimization loop runs weekly without human intervention
- Experiments are generated, executed, and evaluated automatically
- Save rate does not degrade month-over-month (or recovers within 2 weeks when it dips)
- Weekly optimization briefs are generated and distributed
- Scoring model precision and recall remain above 60% and 70% respectively

## Instructions

### 1. Build the intervention health dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for the at-risk-intervention play. Include these panels:

- **Save rate trend:** Weekly save rate over the last 24 weeks. Add a horizontal threshold line at 25%.
- **Save funnel:** `intervention_sent` -> `intervention_engaged` -> `intervention_saved` -> `retained_30d`. Shows the full intervention-to-retention pipeline.
- **Channel performance:** Side-by-side comparison of response rate, save rate, and cost per save for in-app, email, and personal channels. Updated weekly.
- **Segment heatmap:** Save rate by user segment (rows) and channel (columns). Color-coded: green >30%, yellow 20-30%, red <20%.
- **Scoring model health:** Precision, recall, and false positive rate trend over the last 6 monthly calibrations.
- **Experiment log:** Table showing all experiments run by the autonomous optimization loop: hypothesis, start date, result, metric impact.

### 2. Deploy the intervention health monitor

Run the `autonomous-optimization` drill to build the always-on monitoring layer:

- Daily anomaly checks on save rate, response rate, intervention reach, and channel performance
- Weekly health briefs aggregating metrics, surfacing the biggest optimization opportunity, and listing active experiments
- Critical alerts when save rate drops >20% below the 4-week average or intervention delivery fails
- All signals stored in Attio for the optimization loop to query

This monitor is the eyes of the Durable system. Without it, the autonomous optimization loop has no signal to act on.

### 3. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill, configured for the at-risk-intervention play. The loop operates on a weekly cadence:

**Monitor (daily):** The `autonomous-optimization` checks all intervention metrics against rolling averages. Anomalies trigger the Diagnose phase.

**Diagnose (triggered by anomaly):** The agent pulls 8 weeks of intervention data from PostHog and the current system configuration from Attio (scoring thresholds, message variants, channel routing rules, timing windows). It generates 3 ranked hypotheses. Examples of hypotheses the agent might generate:

- "Save rate for light users dropped 15% — test a more educational message variant that leads with a quick-start guide instead of a case study"
- "Email channel response time increased from 6h to 18h — test sending interventions at 10am user-local-time instead of the current 09:00 UTC"
- "False positive rate climbed to 35% — raise the medium risk threshold from 46 to 55 to reduce intervention volume and improve relevance"
- "Personal outreach save rate exceeds email by 3x but only reaches 5% of high-risk users — test lowering the personal outreach threshold from critical-only to include high-risk accounts above $200 MRR"

**Experiment (triggered by hypothesis acceptance):** The agent implements the top hypothesis as a PostHog experiment. It creates a feature flag splitting the relevant population between control and variant. Maximum 1 active experiment at a time. Minimum 7 days or 100 users per variant.

**Evaluate (triggered by experiment completion):** The agent pulls results, calculates statistical significance, and decides: adopt (implement winner), iterate (new hypothesis building on result), revert (restore control), or extend (more data needed). All decisions logged in Attio.

**Report (weekly):** The agent generates a weekly optimization brief:

```
# At-Risk Intervention Optimization Brief — Week of [date]

## Changes This Week
- [Experiment completed: adopted/reverted/extended — impact on save rate]

## Current Performance
- Save rate: [X%] (threshold: 25%, local max estimate: [Y%])
- Response rate: [X%]
- 30-day retention of saved users: [X%]
- Active at-risk population: [N users]

## Scoring Model Health
- Precision: [X%] | Recall: [X%] | False positive rate: [X%]
- Last calibration: [date] | Next calibration: [date]

## Next Experiment
- Hypothesis: [description]
- Expected impact: [+/- X% on save rate]
- Risk level: [low/medium]
- Start date: [date]

## Distance from Local Maximum
[Assessment: converging / still optimizing / degrading]
[If converging: N consecutive experiments with <2% improvement]
```

### 4. Set up monthly scoring model recalibration

The churn risk scoring model drifts as user behavior evolves. Configure a monthly n8n workflow that:

1. Re-runs the `churn-risk-scoring` drill's step 1 (analyze churned vs. retained users) with the latest 90 days of data
2. Compares current signal weights against actual churn correlation
3. Adjusts point values for signals that have become more or less predictive
4. Recalculates precision, recall, and false positive rate
5. If precision drops below 50% or recall drops below 60%, flag for human review
6. Logs the recalibration results in PostHog (`churn_model_calibration` event) and Attio

### 5. Configure guardrails

The autonomous system must have hard limits:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If save rate drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Scoring model changes that affect >30% of the at-risk population size
  - Channel routing changes that redirect personal outreach volume by >50%
  - Any experiment the hypothesis generator flags as "high risk"
- **Intervention volume cap:** Never intervene with more than 20% of the active user base in a single week. If the scoring model suddenly flags a huge population, something is wrong — pause and investigate.
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing the same variable again.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.

### 6. Evaluate sustainability

This level runs continuously. Monthly check:
- Is save rate above the 25% threshold?
- Has the optimization loop run experiments this month?
- Are weekly briefs being generated?
- Has the scoring model been recalibrated?

If save rate sustains or improves for 6 consecutive months, the play is durable. If the optimization loop detects convergence (<2% improvement for 3 consecutive experiments), report to the team: "Intervention system is at local maximum. Save rate of [X%] is the best achievable through tactical optimization. Further gains require strategic changes: product improvements, new intervention channels, or addressing root causes of churn at the product level."

## Time Estimate

- 8 hours: Build intervention health dashboard
- 10 hours: Deploy health monitor (daily checks, weekly briefs, alerts)
- 12 hours: Configure autonomous optimization loop (monitor, diagnose, experiment, evaluate, report)
- 6 hours: Set up monthly scoring model recalibration
- 4 hours: Configure guardrails and test safety mechanisms
- Ongoing: Agent runs autonomously. Human reviews weekly briefs (~30 min/week).

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, dashboards, anomaly detection | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app interventions, multi-channel messaging | $85/seat/mo Advanced; +$99/mo Proactive Support — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered intervention emails | $49/mo+ based on contacts — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Optimization loop, scoring, monitoring workflows | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | ~$15-30/mo at weekly cadence — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost at Durable:** ~$175-350/mo (Intercom Advanced + Proactive + Loops + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor -> diagnose -> experiment -> evaluate -> implement. Runs weekly and finds the local maximum of the intervention system.
- `autonomous-optimization` — play-specific monitoring that feeds signals to the optimization loop. Daily anomaly checks, weekly health briefs, critical alerts.
- `dashboard-builder` — PostHog dashboard with save rate trends, channel performance, segment heatmaps, scoring model health, and experiment log.
