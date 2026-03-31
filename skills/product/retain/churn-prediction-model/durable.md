---
name: churn-prediction-model-durable
description: >
  AI Churn Prediction — Durable Intelligence. Autonomous agent loop that monitors churn metrics,
  generates improvement hypotheses, runs experiments on scoring and interventions, and auto-implements
  winners. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving churn reduction over 6 months via AI"
kpis: ["Prediction accuracy", "Churn rate", "Intervention success", "Experiment velocity", "AI lift"]
slug: "churn-prediction-model"
install: "npx gtm-skills add product/retain/churn-prediction-model"
drills:
  - autonomous-optimization
  - churn-intervention-routing
---

# AI Churn Prediction — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The churn prediction model operates autonomously. An always-on agent loop monitors churn metrics, detects when accuracy or save rates plateau or decline, generates hypotheses for improvement, runs A/B experiments on scoring parameters and intervention templates, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% improvement -- the model has found its local maximum.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack
- No manual calibration needed -- the agent handles drift detection and self-correction
- Guardrail alerts fire correctly when thresholds are breached (tested by simulating a metric drop)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the churn prediction play. The optimization loop has 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent runs `posthog-anomaly-detection` on the play's core KPIs: prediction accuracy, save rate, churn rate, false negative rate. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current scoring parameters, intervention templates, recent calibration notes, 8-week metric history. It runs `hypothesis-generation` to produce 3 ranked hypotheses for what to change. Examples of hypotheses the agent might generate for this play:
- "Increase weight of feature_abandonment signal for power users — this segment's false negative rate spiked 12% after the latest product release changed feature usage patterns"
- "Switch high-risk intervention from email to in-app message — email open rates for high-risk users dropped 20% as users disengage from all channels"
- "Add a new signal: API call volume decline — 3 recent churners were API-heavy users whose frontend usage was low but API usage collapsed"

If the top hypothesis is high-risk, the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits traffic between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 7 days or 100 samples per variant, whichever is longer.

For scoring parameter experiments: the agent creates a variant scoring prompt with adjusted weights or new signals and runs both prompts in parallel, comparing accuracy.

For intervention experiments: the agent creates a variant intervention template and routes a random subset of at-risk users to it, measuring save rate.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide: adopt (implement the winner permanently), iterate (build on the result with a new experiment), revert (the variant hurt performance), or extend (insufficient data, keep running).

Adopted changes are logged in Attio with full context: what changed, why, the experiment results, and the confidence level. This creates an audit trail of every model evolution.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net metric change from all adopted changes
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure churn-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add churn-specific safeguards:

- **False negative spike:** If false negative rate (missed churners) exceeds 20% for 2 consecutive weeks, pause all experiments and revert to the last known good scoring configuration
- **Intervention fatigue:** If save rate drops below 5% for 3 consecutive weeks, pause interventions and flag for strategic review (the interventions may be annoying users rather than saving them)
- **Population drift:** If the percentage of users in critical+high risk tiers exceeds 35% of active users, the issue is likely systemic (product problem, pricing change, competitor) rather than individual churn — alert the team for strategic response
- **Budget cap:** Anthropic API spend for scoring must not exceed $200/mo without human approval

### 3. Deploy the model health monitor at Durable cadence

Run the `autonomous-optimization` drill with enhanced frequency:
- Health check: runs weekly (same as Scalable)
- Calibration drift detection: runs weekly instead of monthly (Durable needs faster feedback)
- Intelligence brief: integrates with the `autonomous-optimization` weekly report

The model health monitor feeds data to the autonomous optimization loop. When it detects calibration drift, that becomes an anomaly that triggers the optimization cycle.

### 4. Maintain intervention routing

The `churn-intervention-routing` drill continues to run daily at Durable level. The autonomous optimization loop may modify intervention templates, timing, or routing thresholds as experiment outcomes dictate. The routing drill executes whatever the current best configuration is.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments produce <2% improvement on any KPI:

1. The play has reached its local maximum for that KPI
2. Reduce experiment frequency from continuous to monthly maintenance checks
3. Generate a convergence report: current performance levels, total improvement since Durable started, recommended strategic changes for further gains (new data sources, product changes, new channels)

Full convergence (all KPIs converged) triggers a shift to maintenance mode: daily scoring and intervention continue, but the optimization loop slows to monthly checks. The agent still monitors for anomalies — external changes (competitor launch, pricing change, product update) can break convergence and re-activate the optimization loop.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Churn rate: sustained at or below the level achieved at Scalable, or improving
- Prediction accuracy: maintained at 65%+ with no sustained drops
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static model

This level runs continuously. Review monthly: what improved, what converged, what external factors changed.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations)
- 10 hours: configure churn-specific guardrails and test them
- 10 hours: enhance model health monitor for Durable cadence
- 80 hours: ongoing monitoring, hypothesis review, guardrail management over 6 months (~3 hours/week)
- 20 hours: monthly strategic reviews and convergence analysis
- 10 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Daily scoring, hypothesis generation, experiment evaluation | ~$100-200/mo at Durable scale — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Loops | Intervention email sequences (modified by optimization loop) | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app interventions (modified by optimization loop) | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated play-specific cost: $180-450/mo** (Anthropic API for scoring + optimization + Loops + Intercom)

## Drills Referenced

- `autonomous-optimization` — the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum
- `autonomous-optimization` — monitors prediction accuracy, save rates, and calibration drift at Durable cadence
- `churn-intervention-routing` — executes the current best intervention configuration, updated by the optimization loop
