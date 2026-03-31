---
name: usage-based-upsell-durable
description: >
  Automatic Usage Upsell — Durable Intelligence. The autonomous optimization loop
  monitors all auto-upgrade metrics, generates hypotheses when performance plateaus
  or drops, runs experiments, and auto-implements winners. A play-specific health
  monitor feeds the loop. Converges when successive experiments produce <2% lift.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "40 hours setup + ongoing autonomous operation over 6 months"
outcome: "Sustained or improving acceptance ≥55% over 6 months via autonomous optimization"
kpis: ["Auto-upgrade acceptance rate (sustained)", "MRR from auto-upgrades (cumulative)", "Experiment velocity (experiments/month)", "AI lift (% improvement from agent-adopted changes)", "Convergence status"]
slug: "usage-based-upsell"
install: "npx gtm-skills add product/upsell/usage-based-upsell"
drills:
  - autonomous-optimization
  - usage-alert-health-monitor
  - dashboard-builder
---

# Automatic Usage Upsell — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The auto-upgrade system runs itself. The `autonomous-optimization` drill monitors all auto-upgrade metrics daily, detects anomalies (acceptance rate dropping, rollback rate spiking, a resource underperforming), generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. A weekly optimization brief reports what changed and why. Over 6 months, the system either sustains ≥55% acceptance rate or improves it — all without human intervention except for high-risk changes that trigger approval requests.

## Leading Indicators

- Autonomous monitoring detects and classifies its first anomaly within the first 2 weeks
- First agent-generated experiment launches within the first 3 weeks
- Weekly optimization briefs deliver on schedule every Monday for 4 consecutive weeks
- No metric degrades >20% for more than 7 days without the agent detecting and responding
- At least 2 experiments per month run and produce a clear adopt/revert/iterate decision

## Instructions

### 1. Build the auto-upgrade health dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard called "Auto-Upgrade System — Durable Health":

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Acceptance rate (weekly, 12-week trend) | Line chart | Core KPI — is acceptance sustaining or improving? |
| Acceptance by resource (weekly) | Stacked bar | Which resources are strongest and weakest |
| MRR from auto-upgrades (monthly, 6-month trend) | Line chart | Revenue impact trajectory |
| 30-day retention of upgraded accounts | Line chart | Are auto-upgrades creating sticky upgrades or pressure upgrades? |
| Opt-out rate by segment | Bar chart | Are certain segments rejecting auto-upgrades at higher rates? |
| Rollback rate trend | Line chart | Is buyer's remorse increasing? |
| Grace period timing histogram | Histogram | When in the grace period do users accept? (Immediate vs. last day) |
| Payment failure rate | Line chart | Billing health of the auto-upgrade pipeline |
| Detection accuracy (TP/FP/miss rates) | Multi-line | Is threshold detection staying calibrated? |
| Active experiments | Table | Currently running experiments with status and preliminary results |

Set PostHog alerts for the `autonomous-optimization` loop to consume:
- Acceptance rate drops >10% from 4-week rolling average
- Any resource acceptance rate falls below 40%
- Rollback rate exceeds 15% for 3 consecutive days
- Payment failure rate exceeds 8%
- MRR from auto-upgrades declines 20%+ month-over-month
- Zero auto-upgrades processed in 72 hours

### 2. Connect the usage-alert health monitor to the optimization loop

Run the `usage-alert-health-monitor` drill, Step 6. Build the webhook endpoint that the `autonomous-optimization` drill calls to retrieve current health metrics. Return a structured payload:

```json
{
  "play": "usage-based-upsell",
  "period": "last_7_days",
  "metrics": {
    "acceptance_rate": 0.58,
    "acceptance_rate_4wk_avg": 0.56,
    "mrr_from_auto_upgrades": 8500,
    "mrr_trend": "growing",
    "retention_30d": 0.82,
    "rollback_rate": 0.07,
    "payment_failure_rate": 0.03,
    "opt_out_rate": 0.35,
    "detection_true_positive_rate": 0.75,
    "detection_false_positive_rate": 0.18,
    "top_resource": "api_calls",
    "worst_resource": "storage",
    "worst_resource_acceptance": 0.41,
    "active_experiments": 1,
    "experiments_this_month": 2,
    "last_experiment_result": "adopted",
    "last_experiment_lift": 0.04
  }
}
```

This payload is the input the autonomous optimization agent uses to decide whether to investigate, hypothesize, or leave the system alone.

### 3. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play. The loop operates in 5 phases:

**Phase 1 — Monitor (daily, 06:00 UTC via n8n cron):**
The agent queries the health webhook (Step 2) and the PostHog dashboard alerts. It classifies the system state:
- **Healthy:** All metrics within ±10% of 4-week averages. Log and take no action.
- **Plateau:** Acceptance rate has been within ±2% for 3+ weeks. Trigger Phase 2 to find improvement.
- **Drop:** Any core metric declined >15% from its 4-week average. Trigger Phase 2 with urgency.
- **Spike:** Any metric improved >25% unexpectedly. Investigate whether it is real or a data anomaly.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current auto-upgrade configuration (grace period, messaging, segmentation rules, resource thresholds), 8-week metric history, recent experiment results. It generates 3 ranked hypotheses. Examples specific to this play:

- "Storage auto-upgrade acceptance is 20pp lower than API calls because users can reduce storage usage (delete files) but cannot reduce API call volume. Hypothesis: offer a 'clean up your storage' option alongside the upgrade prompt for storage-specific exceeded accounts."
- "Acceptance rate plateaued at 58% because the 72-hour grace period is too long — engaged users accept within 4 hours, and the remaining window gives ambivalent users time to opt out. Hypothesis: reduce grace period to 48 hours for accounts that have been on the plan >90 days."
- "Mid-market segment acceptance dropped because the extended 5-day grace period includes a weekend, and decision-makers are unavailable. Hypothesis: start mid-market grace periods on Monday/Tuesday only."

High-risk hypotheses (anything affecting >50% of auto-upgrades or changing pricing) require human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent uses PostHog feature flags to split traffic between control and variant. It implements the change using the appropriate tools:
- Grace period changes: update the n8n workflow configuration
- Messaging changes: create a new Intercom message variant
- Threshold changes: update the detection query parameters
- Routing changes: update the Attio deal creation rules

Minimum experiment duration: 14 days or 50 accounts per variant (whichever is longer). Maximum 1 active experiment at a time for this play.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls experiment results from PostHog. Decision:
- **Adopt:** The variant improved the target metric by ≥5% with statistical significance. Roll out to 100%. Update the live configuration. Log the change.
- **Iterate:** Directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** The variant performed worse or showed no difference. Restore control. Log the failure. Return to Phase 1.

**Phase 5 — Report (weekly, Monday 09:00 UTC):**
The agent generates a weekly optimization brief:

```
# Auto-Upgrade Optimization Brief — Week of [date]

## System Status: [Healthy / Plateau / Drop / Spike]

## Key Metrics (vs 4-week average)
- Acceptance rate: [X]% ([+/-Y]pp)
- MRR from auto-upgrades: $[N] ([+/-]%)
- 30-day retention: [X]% ([+/-Y]pp)
- Rollback rate: [X]% ([+/-Y]pp)

## This Week's Activity
- Anomalies detected: [N] ([list])
- Hypotheses generated: [N]
- Experiments running: [N] ([details])
- Experiments completed: [N] — [adopt/revert/iterate]

## Cumulative AI Lift
- Total experiments run: [N]
- Winners adopted: [N]
- Net acceptance rate change from AI: [+/-X]pp
- Net MRR change from AI: $[N]

## Convergence Status
- Consecutive experiments with <2% lift: [N]/3
- [Converged / Not converged]
- [If converged: "This play has reached its local maximum. Further gains require strategic changes (new resource types, pricing restructure, or product changes)."]

## Next Week
- [Planned action: monitor / investigate / launch experiment / evaluate experiment]
```

Post to Slack and store in Attio.

### 4. Define convergence criteria

The system has converged when 3 consecutive experiments produce less than 2% improvement in acceptance rate. At convergence:

1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from 2-4/month to 1/month (maintenance experiments)
3. Report to the team: "Auto-upgrade system optimized. Current acceptance: [X]%. MRR: $[N]/mo. Further gains require strategic changes."
4. Continue monitoring for external disruptions (product changes, pricing changes, market shifts) that could knock the system off its optimum

### 5. Evaluate sustainability

After 6 months, the play passes if:

- Acceptance rate has stayed ≥55% for all 6 months (no month-long dips below 50%)
- MRR from auto-upgrades has been stable or growing
- The autonomous loop has run at least 8 experiments total
- At least 3 experiments were adopted (the agent found real improvements)
- The system operated without human intervention for the majority of the period (human approval only for high-risk changes)

**Pass:** Sustained ≥55% acceptance over 6 months. The play is durable.
**Fail:** If acceptance degraded over time, check: Did the product change its pricing tiers without updating the auto-upgrade config? Did a competitor launch free alternatives that reduced users' willingness to pay more? Did detection accuracy drift? The autonomous loop should have caught these — if it did not, diagnose whether the monitoring thresholds were too loose.

## Time Estimate

- 8 hours: Build the comprehensive health dashboard with all 10 panels
- 4 hours: Configure the health webhook for the optimization loop
- 12 hours: Deploy and tune the autonomous optimization loop (n8n workflows, Claude prompts, PostHog experiment templates)
- 4 hours: Define convergence criteria and reporting templates
- 12 hours: Monitor and intervene for high-risk approvals over 6 months (2 hours/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, experiments, feature flags, anomaly detection | Free: 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Subscription management, billing data | 2.9% + $0.30/txn ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Optimization loop scheduling, experiment orchestration | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app message variants for experiments | Essential $29/seat/mo; Proactive Support add-on $349/mo for advanced targeting ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequence variants for experiments | Growth from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Experiment logging, optimization brief storage, deal tracking | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Claude Sonnet: $3/M input tokens, $15/M output tokens ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics daily, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `usage-alert-health-monitor` — provides the structured health payload the optimization loop consumes for anomaly detection
- `dashboard-builder` — creates the 10-panel PostHog dashboard that visualizes the complete auto-upgrade system health
