---
name: usage-based-pricing-durable
description: >
  Consumption-Based Pricing — Durable Intelligence. Always-on AI agents autonomously optimize
  the usage-based pricing system: detect metric anomalies, generate improvement hypotheses, run
  A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "ARPU lift sustained or improving over 6 months; optimization loop converges with <2% improvement across 3 consecutive experiments"
kpis: ["ARPU trend (6-month)", "Net revenue retention", "Experiment velocity (experiments/month)", "Cumulative AI-driven lift", "Optimization convergence rate"]
slug: "usage-based-pricing"
install: "npx gtm-skills add product/upsell/usage-based-pricing"
drills:
  - autonomous-optimization
  - pricing-health-monitor
---

# Consumption-Based Pricing — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The usage-based pricing system runs autonomously. An AI agent monitors all pricing KPIs daily, detects when metrics plateau or degrade, generates improvement hypotheses, designs and runs A/B experiments, evaluates results, and auto-implements winners. The pricing health monitor tracks ARPU, NRR, churn by plan, and usage-to-revenue efficiency in real time. A weekly usage-revenue optimization report connects usage patterns to billing outcomes, detects pricing model drift, and identifies bill shock risks.

The optimization loop runs the core cycle: detect anomaly -> generate hypothesis -> run experiment -> evaluate -> implement winner. Weekly optimization briefs summarize what changed and why. The loop converges when 3 consecutive experiments produce less than 2% improvement — at that point, the play has reached its local maximum. Further gains require strategic changes (new tiers, new value metrics, market repositioning) rather than tactical optimization.

## Leading Indicators

- Daily anomaly detection running without gaps (no missed monitoring days for 30+ consecutive days)
- Hypothesis generation producing actionable, testable proposals (not vague "improve pricing" suggestions)
- At least 2 experiments reaching statistical significance per month
- Experiment win rate of 30%+ (at least 1 in 3 experiments produces a positive result worth adopting)
- Pricing model drift detection triggering when usage distribution shifts 20%+ from original tier boundaries
- Bill shock alerts catching 70%+ of accounts with >200% invoice growth before the next billing cycle
- Weekly optimization brief posted to Slack every Monday

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core system that makes Durable fundamentally different from Scalable:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use PostHog anomaly detection to check the play's primary KPIs: ARPU, NRR, churn rate by tier, auto-upgrade acceptance rate, upgrade prompt conversion rate, pricing page conversion rate.
2. Compare last 2 weeks against 4-week rolling average.
3. Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase).
4. If normal, log to Attio, no action needed.
5. If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: pull the current pricing configuration from Attio (tier boundaries, price points, auto-upgrade rules, active experiments).
2. Pull 8-week metric history from PostHog dashboards.
3. Run the hypothesis generation fundamental with anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk.
4. Store hypotheses in Attio as notes on the pricing project record.
5. If the top hypothesis has risk = "high" (e.g., changing base price, removing a tier), send a Slack alert for human review and STOP. **Human action required:** Approve or reject high-risk hypotheses.
6. If risk = "low" or "medium", proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis.
2. Design the experiment: create a PostHog feature flag that splits traffic between control and variant.
3. Implement the variant using the appropriate mechanism — for alert copy changes, update Intercom templates via `intercom-in-app-messages`; for tier boundary changes, create new Stripe prices via `stripe-pricing-tables`; for pricing page changes, deploy via PostHog feature flags.
4. Set experiment duration: minimum 14 days or until 200+ samples per variant.
5. Log the experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog.
2. Run the experiment evaluation fundamental with control vs. variant data.
3. Decision: **Adopt** (implement the winner permanently), **Iterate** (generate a new hypothesis building on results, return to Phase 2), **Revert** (disable variant, restore control, return to Phase 1), or **Extend** (keep running for another period).
4. Store the full evaluation in Attio.

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week.
2. Calculate net metric change from all adopted changes.
3. Generate a weekly optimization brief: what changed, net KPI impact, distance from estimated local maximum, recommended focus for next week.
4. Post to Slack and store in Attio.

**Guardrails (critical):**
- Maximum 1 active pricing experiment at a time. Never stack experiments.
- If primary metric drops >30% during an experiment, auto-revert immediately.
- Human approval required for: budget changes >20%, targeting changes affecting >50% of traffic, any high-risk hypothesis.
- After a failed experiment, 7-day cooldown before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for strategic review.

### 2. Deploy pricing health monitoring

Run the `pricing-health-monitor` drill. This builds the always-on observation layer:

1. **Build the pricing health dashboard in PostHog:** ARPU trend (30-day rolling), ARPU by plan, NRR (monthly and trailing 12-month), expansion and contraction revenue, churn rate by plan, churn rate by usage band, churn rate by tenure, usage per dollar spent, percentage of customers at plan limits, overage revenue as percentage of total.

2. **Set anomaly detection rules:** ARPU drops >10% MoM (High), NRR below 100% for 2 consecutive months (Critical), churn rate in any tier exceeds 2x its 90-day average (High), customers at plan limit exceed 40% (Medium), overage complaints >5 tickets in 7 days (High), expansion revenue drops >20% MoM (Medium).

3. **Build the daily monitoring workflow:** n8n cron at 07:00 UTC. Query PostHog for all pricing health metrics. Compare against thresholds. Log anomalies in PostHog and Attio. Slack alert on Critical severity.

4. **Build the weekly pricing digest:** n8n cron on Monday 09:00 UTC. Aggregate week's data. Compute WoW changes. Identify top 3 trends. Post structured report to Slack.

5. **Maintain pricing sensitivity cohorts:** Pricing page visitors (active customers viewing pricing 2+ times in 7 days), limit-approaching (80%+ of a plan limit), overage shock (last invoice 50%+ higher than previous), downgrade candidates (usage dropped below current plan threshold for 2+ weeks). Update daily.

6. **Calibrate monthly:** Compare predicted anomalies vs. actual outcomes. Adjust thresholds if false positive rate exceeds 30% or miss rate exceeds 20%. Check if usage distribution has shifted enough to warrant tier boundary re-analysis.

### 3. Deploy usage-revenue optimization reporting

Run the the usage revenue optimization report workflow (see instructions below) drill. This is the play-specific intelligence layer that feeds hypotheses into the autonomous optimization loop:

1. **Compute usage-to-revenue efficiency metrics weekly:** Usage per dollar (UPD), revenue per usage unit (RPU), overage revenue ratio. Track trends: rising UPD across cohorts indicates pricing value leakage.

2. **Track tier migration flow:** Build a migration matrix showing upgrade and downgrade flows between tiers, net flow per tier, auto-upgrade vs. self-serve ratio. Alert if any tier has negative net flow for 3 consecutive weeks.

3. **Detect pricing model drift:** Re-compute usage distribution percentiles (P50, P80, P95) monthly. Compare against the original percentiles that defined tier boundaries. If any percentile shifts 20%+, trigger a `usage-pricing-model-analysis` re-run to assess whether tiers need adjustment.

4. **Monitor bill shock indicators:** Identify accounts with >50% invoice growth. Classify by severity: mild (50-100%), significant (100-200%), shock risk (>200%). Significant accounts get a proactive usage summary email. Shock risk accounts get flagged for immediate outreach.

5. **Generate optimization candidates:** Each weekly report includes 3 ranked findings with recommended experiments. These feed directly into the autonomous optimization loop's hypothesis pipeline.

### 4. Evaluate sustainability

This level runs continuously for 6 months. The play passes if:

- ARPU lift is sustained or improving over the 6-month period (no sustained decline of >5% lasting more than 4 weeks)
- Net revenue retention stays at or above 100%
- The optimization loop is running: at least 2 experiments per month reaching completion
- Cumulative AI-driven lift (total ARPU improvement attributable to experiments) is measurable and positive

The play reaches its **local maximum** when 3 consecutive experiments produce less than 2% improvement. At convergence:
1. Reduce monitoring frequency from daily to weekly.
2. Report: "This play is optimized. Current ARPU is [X]. NRR is [Y]. Further gains require strategic changes (new tiers, new value metrics, new market segments) rather than tactical optimization."
3. Keep the pricing health monitor and bill shock detection running — they protect against degradation even after convergence.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows for all 5 phases, PostHog experiments integration, Attio logging, Slack reporting)
- 15 hours: Pricing health monitor (PostHog dashboard, anomaly rules, daily and weekly n8n workflows, cohort maintenance)
- 10 hours: Usage-revenue optimization report (efficiency queries, migration matrix, drift detection, bill shock monitoring)
- 105 hours: Ongoing operation over 6 months (experiment design and implementation, weekly brief review, monthly calibration, convergence assessment)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, cohorts, session recordings | Free up to 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Metered billing, experiment price variants, subscription management | 0.5% of recurring revenue for Billing ([stripe.com/pricing](https://stripe.com/pricing)) |
| Intercom | In-app messages for experiments, upgrade prompts, bill shock outreach | Essential $29/seat/mo; Proactive add-on $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered emails for experiment variants, proactive usage summaries | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | Claude API usage-based; ~$15/MTok input, $75/MTok output ([anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)) |

**Estimated play-specific cost at this level:** $200-500/mo (Intercom proactive messaging + Loops + Anthropic API for hypothesis/evaluation, scaling with experiment frequency)

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners, report weekly
- `pricing-health-monitor` — Continuous monitoring of ARPU, NRR, churn by plan, usage-to-revenue ratio with daily anomaly detection and weekly digests
- the usage revenue optimization report workflow (see instructions below) — Weekly usage-to-revenue efficiency analysis, tier migration tracking, pricing model drift detection, and bill shock early warning
