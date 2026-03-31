---
name: usage-based-pricing-optimization-durable
description: >
  Pricing for Retention — Durable Intelligence. Autonomous agent monitors pricing health,
  detects metric anomalies, generates improvement hypotheses, runs experiments, and
  auto-implements winners. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving churn reduction over 6 months via AI"
kpis: ["Churn rate", "ARPU", "Net retention", "Experiment velocity", "AI lift"]
slug: "usage-based-pricing-optimization"
install: "npx gtm-skills add product/retain/usage-based-pricing-optimization"
drills:
  - autonomous-optimization
  - pricing-health-monitor
  - dashboard-builder
---

# Pricing for Retention — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An always-on AI agent continuously monitors pricing health metrics, detects when churn patterns shift or ARPU anomalies emerge, generates pricing improvement hypotheses, runs controlled experiments, evaluates results, and auto-implements winners. The system sustains or improves the churn reduction achieved at Scalable over 6+ months without manual intervention. Converges when 3 consecutive experiments produce <2% improvement, indicating the pricing has reached its local maximum.

## Leading Indicators

- Pricing health dashboard shows all metrics within normal bounds for 4+ consecutive weeks after Durable launch
- First autonomous experiment launched within 3 weeks of entering Durable
- Weekly optimization briefs delivered on schedule with actionable content
- No guardrail breaches in the first 30 days (the autonomous system is safe)
- At least 2 experiments completed in the first 60 days

## Instructions

### 1. Deploy the pricing health monitor

Run the `pricing-health-monitor` drill to build the observation layer:

a. Create the PostHog "Pricing Health" dashboard with these panel groups:

**Revenue panels:** ARPU trend (30-day rolling), ARPU by plan tier, Net Revenue Retention (NRR monthly and trailing 12-month), expansion revenue from usage growth, contraction revenue from downgrades.

**Churn panels:** Churn rate by plan, churn rate by usage band, churn rate by tenure, revenue churn vs. logo churn.

**Usage-to-revenue panels:** Usage per dollar spent (trend), percentage of customers at plan limits, overage revenue as percentage of total, usage growth rate vs. revenue growth rate.

b. Configure anomaly detection thresholds:
- ARPU drops >10% MoM -> High severity
- NRR below 100% for 2 consecutive months -> Critical
- Churn rate on any plan exceeds 2x the 90-day average -> High
- Customers at plan limit exceeds 40% -> Medium
- >5 support tickets mentioning billing in 7 days -> High

c. Build the daily monitoring n8n workflow (runs 07:00 UTC): query all pricing metrics, compare against thresholds, log anomalies as PostHog events, alert on Critical severity via Slack.

d. Build the weekly pricing digest n8n workflow (Monday 09:00 UTC): aggregate the week's data, compute WoW changes, identify top 3 trends, post to Slack and store in Attio.

e. Maintain dynamic PostHog cohorts for pricing stress signals: pricing-page-visitors (active customers visiting billing 2+ times/week), limit-approaching (80%+ of plan limit), overage-shock (last invoice 50%+ higher than previous), downgrade-candidates (usage below plan threshold for 2+ weeks).

### 2. Connect the autonomous optimization loop

Run the `autonomous-optimization` drill configured for pricing metrics:

a. **Monitor phase (daily):** The pricing health monitor from Step 1 feeds anomaly data into the optimization loop. When an anomaly is detected (ARPU drop, churn spike on a plan, usage-revenue divergence), it triggers the diagnosis phase.

b. **Diagnose phase:** When an anomaly fires, the agent gathers context:
- Pull the current pricing configuration from Stripe (plans, prices, tier boundaries)
- Pull 8-week metric history from PostHog (churn by plan, ARPU trend, usage distribution)
- Pull the cohort data for affected segments (which customers are in the anomalous group?)

Feed this context to Claude via the `hypothesis-generation` fundamental. Receive 3 ranked hypotheses. Examples of pricing-specific hypotheses the agent might generate:
- "Tier 2 boundary is too low — 35% of Pro customers are hitting the limit and churning. Raising the boundary from 10,000 to 15,000 included units would retain them at minimal revenue cost."
- "Overage rate is causing bill shock — customers whose invoice increased >40% MoM churn at 3x the base rate. Reducing the overage rate by 20% would smooth costs."
- "The Starter plan is underpriced — Starter users at P90 usage pay less per unit than Free users would under a per-unit model. A $5/mo base increase would align value and improve gross margin."

If risk = high, send to human for review and stop. If risk = low or medium, proceed.

c. **Experiment phase:** Take the top hypothesis and run it using the `pricing-experiment-runner` drill mechanics:
- Create variant prices in Stripe tagged with experiment metadata
- Set up a PostHog feature flag for 50/50 split on the affected segment
- Migrate treatment users to variant pricing at their next billing cycle
- Set experiment duration: minimum 2 billing cycles or until statistical significance
- Log the experiment in Attio with hypothesis, start date, success criteria

d. **Evaluate phase:** When the experiment completes:
- Pull results from PostHog (treatment vs. control on churn, ARPU, NRR)
- Run `experiment-evaluation` to decide: Adopt, Iterate, Revert, or Extend
- If Adopt: migrate all control users to the winning variant, archive old prices
- If Iterate: generate a new hypothesis building on this result, return to Diagnose
- If Revert: restore control pricing, log the failure, return to Monitor
- Store the full evaluation in Attio

e. **Report phase (weekly):** Generate a weekly optimization brief:
- Anomalies detected this week and their severity
- Active experiment status (enrollment, current metrics, estimated time to significance)
- Completed experiments (decisions made, impact realized)
- Net metric change from all adopted changes
- Current distance from estimated local maximum (based on diminishing returns curve)
- Recommended focus for next week

Post to Slack and store in Attio.

### 3. Build the executive pricing dashboard

Run the `dashboard-builder` drill to create an executive-level view:

a. Create a "Pricing Intelligence" dashboard in PostHog with:
- **Health score:** Composite metric combining NRR, churn trend, and ARPU stability (green/yellow/red)
- **Experiment tracker:** Active experiments, their hypotheses, and current results
- **Cumulative AI lift:** Total metric improvement from all adopted experiments since entering Durable
- **Convergence indicator:** Rolling window of last 3 experiments' improvement. If all <2%, display "Pricing Optimized."
- **Revenue impact:** MRR change attributable to pricing optimization (compare to pre-optimization baseline)

b. Set up monthly executive summaries via n8n: on the 1st of each month, generate a one-page report of pricing health, experiments run, decisions made, and net impact. Store in Attio and email to stakeholders via Loops.

### 4. Enforce guardrails

The autonomous system must operate within safety bounds:

- **Rate limit:** Maximum 1 active pricing experiment at a time. Queue additional hypotheses.
- **Revert threshold:** If treatment churn exceeds control by >50% at any weekly check, auto-revert.
- **Revenue floor:** If treatment ARPU drops >15% vs. control, auto-revert.
- **Human approval required for:** Any pricing change that affects >50% of customers, any change to the base price (vs. overage/tier boundaries), any change the hypothesis generator flags as high risk.
- **Cooldown:** After a reverted experiment, wait 30 days before testing a new hypothesis on the same pricing parameter.
- **Monthly experiment cap:** 2 pricing experiments per month maximum. If both fail, pause and flag for human strategic review.
- **Never test without sufficient data:** If the affected segment has <100 customers, flag for human decision instead of running an automated experiment.

### 5. Detect convergence

The optimization loop runs until it detects convergence:

a. Track the improvement from each adopted experiment. Plot the cumulative improvement curve.

b. Convergence criteria: 3 consecutive experiments produce <2% improvement on their primary metric.

c. When convergence is detected:
- Reduce monitoring frequency from daily to weekly
- Report: "Pricing has reached its local maximum. Current performance: churn rate {X}%, NRR {Y}%, ARPU ${Z}. Further gains require strategic changes (new plans, new segments, product changes) rather than parameter optimization."
- Continue weekly monitoring to detect if market conditions shift (competitor pricing changes, customer mix changes) that would open new optimization space.

### 6. Evaluate sustainability

This level runs continuously. Monthly review:

a. Are the churn reduction gains from Scalable sustaining? Compare current month's churn rate to the Baseline experiment's control group churn rate.

b. Is AI lift positive? Calculate: total metric improvement from autonomously adopted experiments. If zero after 3 months, the system is maintaining but not improving — which is acceptable if metrics are at a good level.

c. Is the system safe? Check: number of guardrail breaches, number of auto-reverts, support ticket volume. If guardrail breaches increase over time, tighten the safety bounds.

d. If metrics are sustaining or improving, the play is durable. If metrics decay, the agent diagnoses the cause: market shift, product change, competitive pressure, seasonal effect. If the cause is external, pricing optimization alone cannot fix it — escalate to strategic review.

## Time Estimate

- 20 hours: Pricing health monitor setup (dashboard, anomaly detection, daily/weekly workflows)
- 15 hours: Autonomous optimization loop configuration (monitor, diagnose, experiment, evaluate, report phases)
- 10 hours: Executive dashboard build
- 5 hours: Guardrail configuration and testing
- 100 hours: Ongoing monitoring, experiment management, and optimization over 6 months (~4 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, anomaly detection | Free up to 1M events/mo; ~$0.00005/event after ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Billing, subscription management, metered pricing | 2.9% + $0.30/txn; Billing $0.50/invoice ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Optimization loop scheduling, webhook pipelines, reporting | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app pricing change notifications, retention offers | From $29/seat/mo; Proactive Support Plus $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation | API: $3/MTok input, $15/MTok output ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Loops | Lifecycle emails, executive summaries | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core detect-diagnose-experiment-evaluate-implement loop that makes Durable self-optimizing
- `pricing-health-monitor` — continuous monitoring of pricing KPIs with anomaly detection and weekly digests
- `dashboard-builder` — executive-level pricing intelligence dashboard with convergence tracking
