---
name: usage-monitoring-alerts-durable
description: >
  Usage Drop Alerting — Durable Intelligence. Autonomous optimization agent continuously
  tunes detection thresholds, intervention content, and routing rules. Detects metric
  anomalies, generates improvement hypotheses, runs experiments, and auto-implements winners.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "Ongoing — 8 hours setup, then 2 hours/week monitoring"
outcome: "Re-engagement rate sustained or improving over 6 months with <2% variation between optimization cycles"
kpis: ["Re-engagement rate trend (6-month)", "Experiment velocity (experiments/month)", "AI lift (% improvement from autonomous changes)", "False positive trend", "Net churn reduction trend", "Time to convergence"]
slug: "usage-monitoring-alerts"
install: "npx gtm-skills add product/retain/usage-monitoring-alerts"
drills:
  - autonomous-optimization
  - usage-drop-detection
  - dashboard-builder
---

# Usage Drop Alerting — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The system finds and maintains its local maximum. An autonomous agent monitors the full detection-and-intervention pipeline, detects when any component underperforms, generates hypotheses for improvement, runs A/B experiments, and auto-implements winners. Weekly optimization briefs report what changed and why. The play converges when successive experiments produce <2% improvement — meaning the system has found the best achievable performance given current product, audience, and market conditions.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- At least 1 experiment per month produces a statistically significant improvement
- Weekly optimization briefs are generated and posted on schedule
- No metric degrades by more than 15% without the agent detecting and responding
- Human review only needed for high-risk hypotheses (budget changes, major targeting shifts)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play. The optimization target metrics are:

- **Primary:** Re-engagement rate (flagged accounts that return to 50%+ baseline within 14 days)
- **Secondary:** False positive rate, time-to-intervention, cost per save
- **Guardrails:** Email unsubscribe rate < 1%, Intercom message dismiss-without-engagement rate < 80%

Configure the n8n daily monitoring cron (Phase 1 of the `autonomous-optimization` drill) to check:

1. Re-engagement rate: compare last 2 weeks against 4-week rolling average
2. Detection volume: are we flagging more or fewer accounts than usual?
3. Intervention conversion by channel: is email, in-app, or human outperforming?
4. Segment-level performance: has any segment degraded?

Classification:
- **Normal** (within ±10%): Log, no action
- **Plateau** (±2% for 3+ weeks): Trigger hypothesis generation — the system has stalled
- **Drop** (>15% decline in re-engagement rate): Trigger urgent diagnosis
- **Spike** (>30% improvement): Investigate — could be a real win or a data anomaly

### 2. Configure the hypothesis generation targets

When the agent detects an anomaly, it generates hypotheses scoped to this play's specific optimization levers:

**Detection lever hypotheses:**
- "Tighten the power-user drop threshold from -25% to -20% because recent churns were caught too late"
- "Add a new detection signal: billing page visits combined with usage drops flag accounts 5 days earlier"
- "Exclude accounts with active support tickets from drop detection — they are engaged, just frustrated"

**Intervention lever hypotheses:**
- "Switch critical-tier first email from 'urgent' to 'personal check-in' tone because urgent emails have declining open rates"
- "Move in-app alert from dashboard banner to feature-specific tooltip because banner blindness is increasing"
- "Add a third step to the alert-tier sequence: a Loops email featuring a peer case study"

**Routing lever hypotheses:**
- "Route starter-plan alert-tier accounts to in-app only (no email) because email re-engagement rate for this segment is below 5%"
- "Lower the MRR threshold for human routing from $1000 to $500 because mid-tier accounts have higher save rates with human touch"

Each hypothesis must include: what to change, predicted impact on re-engagement rate, risk level (low/medium/high), and how to measure it.

### 3. Run the experiment cycle

For each accepted hypothesis (low and medium risk proceed automatically; high risk requires human approval):

1. Use PostHog feature flags to split traffic between control and variant
2. Minimum experiment duration: 14 days or 50+ flagged accounts per variant
3. Track: re-engagement rate, secondary metrics, and guardrail metrics for both variants
4. Auto-evaluate using the `experiment-evaluation` fundamental from the `autonomous-optimization` drill
5. If variant wins with 95% confidence: implement permanently, update the n8n workflow configuration
6. If variant loses: revert, log the learning, wait 7 days before testing the same lever

**Rate limit:** Maximum 1 active experiment at a time for this play. Never stack experiments — isolation is required for valid results.

### 4. Build the engagement health dashboard

Run the `dashboard-builder` drill to create a dedicated "Usage Drop Alerting — Health" dashboard in PostHog:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Re-engagement rate (12-week trend) | Line chart | Primary KPI trajectory |
| Detection volume by tier | Stacked bar (weekly) | Are we catching more or fewer drops? |
| Intervention conversion by channel | Grouped bar | Which channel works best right now? |
| Re-engagement rate by segment | Heatmap (plan x usage tier) | Which segments need attention? |
| Experiment log | Table | Active and completed experiments with outcomes |
| False positive rate trend | Line chart | Is detection accuracy improving? |
| Net churn impact | Line chart (churn rate overlay) | Business outcome |
| Optimization convergence | Line chart (experiment lift %) | Are we approaching local max? |

Configure alerts:
- Re-engagement rate drops below 30% for 2 consecutive weeks
- False positive rate exceeds 25%
- Guardrail breach: email unsubscribe rate exceeds 1%
- Convergence detected: 3 consecutive experiments produce <2% lift

### 5. Generate weekly optimization briefs

The agent generates a weekly brief every Monday at 09:00 UTC via the reporting phase of `autonomous-optimization`:

```
# Usage Drop Alerting — Optimization Brief (Week of {{date}})

## This Week
- Accounts flagged: {{count}} ({{trend}} vs last week)
- Re-engagement rate: {{rate}}% ({{trend}} vs 4-week avg)
- Active experiment: {{experiment_name}} — {{status}}
- Interventions sent: {{count}} (email: {{n}}, in-app: {{n}}, human: {{n}})

## Changes Made
- {{list of any auto-implemented changes this week}}

## Experiment Results
- {{completed experiment: hypothesis, result, decision, confidence}}

## Convergence Status
- Last 3 experiments produced: {{lift1}}%, {{lift2}}%, {{lift3}}% improvement
- Status: {{converging | optimizing | degrading}}

## Recommended Focus
- {{what the agent recommends investigating or testing next}}
```

Post to Slack and store in Attio as a note on the play's campaign record.

### 6. Handle convergence

When the system detects convergence (3 consecutive experiments produce <2% lift):

1. The play has reached its local maximum for current conditions
2. Reduce monitoring frequency from daily to every 3 days
3. Reduce experiment frequency from weekly to monthly maintenance checks
4. Generate a convergence report:
   - Final optimized configuration (thresholds, templates, routing rules)
   - Re-engagement rate at convergence
   - Total improvement from Baseline to convergence
   - Estimated churn prevented per month
5. Continue watching for degradation — if external conditions change (product update, seasonal shift, market change), re-engagement rate may drop and the agent should re-enter active optimization

If re-engagement rate drops >15% after convergence, the agent automatically reactivates daily monitoring and the full optimization loop.

## Time Estimate

- 4 hours: Configure autonomous optimization loop for this play's specific metrics
- 2 hours: Build the health dashboard
- 2 hours: Configure hypothesis generation targets and guardrails
- Ongoing: 2 hours/week reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, cohorts | Growth from $0.00045/event; https://posthog.com/pricing |
| n8n | Optimization loop cron, experiment implementation | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Anthropic Claude | Hypothesis generation, experiment evaluation, weekly briefs | API usage ~$10-50/mo; https://www.anthropic.com/pricing |
| Loops | Intervention email variants for experiments | Starter from $49/mo; https://loops.so/pricing |
| Intercom | In-app message variants for experiments | Starter from $39/mo; https://www.intercom.com/pricing |
| Attio | Optimization audit trail, convergence reporting | Pro from $34/seat/mo; https://attio.com/pricing |

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor, diagnose, experiment, evaluate, implement
- `usage-drop-detection` — The detection system being continuously optimized
- `dashboard-builder` — Build the engagement health dashboard for real-time visibility
