---
name: product-qualified-lead-scoring-durable
description: >
  PQL Scoring System — Durable Intelligence. Autonomous optimization loop
  monitors scoring model health, detects accuracy drift, generates improvement
  hypotheses, runs experiments, and auto-implements winners. Weekly optimization
  briefs track convergence toward the local maximum.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation"
outcome: "Scoring accuracy sustained or improving ≥65% for 6+ months with <2 hours/month human oversight"
kpis: ["Scoring accuracy (sustained ≥65%)", "Model drift detection latency (days)", "Experiment velocity (tests/month)", "Autonomous optimization lift (%)", "Human intervention hours/month"]
slug: "product-qualified-lead-scoring"
install: "npx gtm-skills add product/onboard/product-qualified-lead-scoring"
drills:
  - autonomous-optimization
---

# PQL Scoring System — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The PQL scoring system runs autonomously with minimal human oversight. An always-on agent loop monitors scoring accuracy daily, detects when the model drifts (conversion correlation degrades, false positive/negative rates spike, score distribution skews), generates hypotheses for what to fix, runs A/B experiments on the top hypothesis, evaluates results, and auto-implements winners. Weekly optimization briefs report what changed, net impact on KPIs, and distance from the local maximum. The system converges when successive experiments produce <2% accuracy improvement. Human involvement drops to <2 hours/month (reviewing weekly briefs and approving high-risk changes).

## Leading Indicators

- Daily anomaly checks run without errors (visible as `pql_anomaly_check` events in PostHog)
- Model drift detected within 48 hours of accuracy degradation (amber alert fires when Hot-tier conversion drops below 3x Cold-tier)
- At least 1 experiment per month runs autonomously (hypothesis generated, feature flag set, results evaluated)
- Weekly optimization briefs posted to Slack with actionable metrics
- No human intervention required for low/medium-risk changes (auto-implemented)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for PQL scoring. This creates the five-phase always-on loop:

**Phase 1 — Monitor (daily via n8n cron):**

Configure the monitoring targets specific to PQL scoring:
- Primary KPI: Hot-tier PQL-to-conversion rate (target: >=4x Cold-tier rate)
- Secondary KPIs: false positive rate (<20%), false negative rate (<10%), scoring latency (<10 minutes)
- Use `posthog-anomaly-detection` to compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**

Gather PQL-specific context before generating hypotheses:
1. Pull current scoring model configuration from Attio (criteria, weights, thresholds)
2. Pull 8-week metric history from PostHog: conversion rates by tier, score distributions, weight calibration history
3. Check for external changes: new product features shipped (via release notes), significant traffic shifts (PostHog session counts), competitor launches (Clay news enrichment)
4. Run `hypothesis-generation` with the anomaly data + context
5. Receive 3 ranked hypotheses. Examples for PQL scoring:
   - "Pricing page visit signal lost predictive value because pricing changed 3 weeks ago — re-weight or replace"
   - "New onboarding flow increased activation but the model does not capture the new steps — add new intent signals"
   - "Enterprise user influx skewed fit scores — segment the model by company size"
6. If top hypothesis is high-risk (affects >50% of scoring population): send Slack alert for human review, STOP
7. If low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Design the experiment using `posthog-experiments`: create a feature flag that splits new users between control (current scoring) and variant (hypothesis change)
2. Implement the variant in the scoring n8n workflow. The n8n workflow reads the PostHog feature flag and applies the variant scoring logic for flagged users.
3. Set duration: minimum 7 days or 100+ users per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog: conversion rate by tier for control vs variant
2. Run `experiment-evaluation`:
   - **Adopt:** Variant improves primary KPI by >=5% with statistical significance. Update scoring workflow to use variant logic for all users. Log the change.
   - **Iterate:** Variant shows directional improvement but not significant. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant degrades performance. Disable variant, restore control. Log failure. Return to Phase 1.
   - **Extend:** Insufficient sample size. Keep running for another period.
3. Store full evaluation in Attio: decision, confidence interval, reasoning, net impact

**Phase 5 — Report (weekly via n8n cron):**

Generate a weekly PQL optimization brief:
- Anomalies detected this week (with classification)
- Hypotheses generated and their risk levels
- Experiments running, completed, or pending
- Net impact on scoring accuracy from all changes this week
- Current accuracy vs estimated local maximum
- Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy scoring model health monitoring

Run the `autonomous-optimization` drill to build the always-on dashboard and alerting layer:

**PostHog dashboard — "PQL Scoring Model Health":**
- Conversion rate by tier (Hot vs Warm vs Cold) — primary accuracy metric
- Score distribution histogram — detects clustering or skew
- False negative rate — converters missed by the model
- False positive rate — Hot-tier users who never engage
- Score-to-close correlation — higher scores should predict faster closes
- Model drift indicator — week-over-week Hot-tier conversion trend

**Weekly accuracy check (n8n cron, Monday 9 AM):**
- Compute conversion rate by tier for last 7 days
- Compare to 4-week rolling average
- Classify model health: Healthy (Hot >=4x Cold), Degrading (2-4x), Broken (<2x)
- Generate report with accuracy metrics, drift status, and criteria contribution analysis

**Drift alerts:**
- Amber: Hot conversion drops below 3x Cold for 1 week. Flag for review.
- Red: Hot conversion drops below 2x Cold for 2+ weeks OR false negative rate exceeds 15%. Auto-trigger the autonomous optimization loop (Phase 2).
- Distribution alert: If >40% of users score Hot or <10% score Hot. Threshold adjustment needed.

**Monthly criteria audit:**
- For each closed deal in the last 30 days, log which fit and intent criteria the user matched
- Rank criteria by correlation with closed deals
- Flag criteria that never appear in won deals (removal candidates)
- Flag patterns in won deals not captured by the model (addition candidates)
- Feed findings to the autonomous optimization loop as pre-generated hypotheses

### 3. Configure guardrails

Apply the `autonomous-optimization` guardrails specific to PQL scoring:

- **Rate limit:** Maximum 1 active experiment on the scoring model at a time
- **Revert threshold:** If Hot-tier conversion drops >30% during any experiment, auto-revert immediately
- **Human approval required for:**
  - Changes that affect scoring for >50% of the user base
  - Adding or removing a scoring dimension
  - Changes to fit scoring criteria (these require business judgment)
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for strategic review.
- **Never optimize without data:** If a KPI lacks PostHog tracking, fix tracking first (run `posthog-gtm-events`) before running experiments.

### 4. Evaluate durability

This level runs continuously. Monthly review criteria:

- Scoring accuracy sustained >=65% for each of the last 6 months
- Autonomous experiments maintain or improve accuracy without human intervention
- Human oversight time is <2 hours/month (reviewing briefs, approving high-risk changes)
- The model has adapted to at least 1 external change (product update, traffic shift, market change) without accuracy degradation

Convergence detection: when 3 consecutive experiments produce <2% accuracy improvement, the model has reached its local maximum. At convergence:
1. Reduce monitoring from daily to weekly
2. Report: "PQL scoring model is optimized. Current accuracy: [X]%. Further gains require strategic changes (new product signals, new market segments, product changes) rather than tactical optimization."

## Time Estimate

- 8 hours: Configure autonomous optimization loop (5 phases) with PQL-specific parameters
- 6 hours: Build scoring model health dashboard and drift alerts
- 4 hours: Set up guardrails and human approval workflows
- 2 hours: Validate end-to-end loop (trigger a test anomaly, verify hypothesis generation, confirm alerting)
- Ongoing: <2 hours/month reviewing weekly briefs and approving flagged changes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, event tracking | Free up to 1M events; paid ~$0.00005/event; Experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop scheduling (daily monitor, weekly report) | Self-hosted free; Cloud from EUR 24/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic | Hypothesis generation and experiment evaluation (Claude API) | Pay-per-use ~$0.01-0.03/call ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Score storage, experiment logging, audit trail | Pro $29/seat/month ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Ongoing firmographic enrichment | Pro $149/month ([clay.com/pricing](https://www.clay.com/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `autonomous-optimization` — builds the accuracy dashboard, weekly health reports, drift alerts, and criteria contribution analysis specific to lead scoring models
