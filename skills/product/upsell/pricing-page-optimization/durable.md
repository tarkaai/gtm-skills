---
name: pricing-page-optimization-durable
description: >
  Self-Serve Pricing Optimization — Durable Intelligence. Always-on AI agents
  monitor pricing page conversion, detect anomalies, generate experiment hypotheses,
  run A/B tests, auto-implement winners, and converge on the local maximum.
  Autonomous optimization loop finds and maintains peak conversion performance.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Durable Intelligence"
time: "Ongoing — 8 hours setup, then 2 hours/week agent maintenance"
outcome: "Sustained or improving conversion lift over 6 months with <2% improvement between successive experiments signaling convergence"
kpis: ["Pricing page conversion rate", "Plan selection mix", "ARPU (new subscribers)", "Experiment velocity", "Autonomous optimization lift", "Time to convergence"]
slug: "pricing-page-optimization"
install: "npx gtm-skills add product/upsell/pricing-page-optimization"
drills:
  - autonomous-optimization
  - pricing-page-conversion-monitor
  - pricing-health-monitor
---

# Self-Serve Pricing Optimization — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

An always-on AI agent continuously monitors pricing page performance, detects when metrics plateau or degrade, generates hypotheses for improvement, runs controlled A/B experiments, evaluates results, and auto-implements winners. The agent converges on the local maximum — the best achievable pricing page performance given the current market, product, and audience — and maintains it as conditions change. Convergence is defined as 3 consecutive experiments producing <2% improvement.

## Leading Indicators

- Autonomous optimization loop executing without human intervention (daily monitoring, weekly experiments, monthly reports)
- Anomaly detection catching real issues within 24 hours of occurrence
- Experiment pipeline maintaining velocity of 2-4 experiments per month
- Each adopted experiment producing measurable lift (even if diminishing)
- Weekly optimization briefs generating actionable insights, not just status updates

## Instructions

### 1. Deploy the pricing page conversion monitor

Run the `pricing-page-conversion-monitor` drill to build the always-on observation layer:

1. Build the PostHog "Pricing Page Health" dashboard with visitor, conversion, and revenue panels
2. Create the multi-step pricing funnel: `pricing_page_viewed` → `plan_card_clicked` → `checkout_started` → `payment_method_entered` → `subscription_created`
3. Configure anomaly detection rules for conversion rate, plan mix, checkout abandonment, ARPU, and annual selection rate
4. Build the daily n8n monitoring workflow that checks all metrics, pulls session recordings for anomalies, and alerts on High/Critical severity
5. Build the weekly pricing page digest workflow
6. Create dynamic cohorts: comparison shoppers, plan hesitators, downgrade researchers, annual-curious
7. Set up monthly calibration to tune alert thresholds based on precision/recall

This monitor runs continuously and feeds anomaly signals into the autonomous optimization loop.

### 2. Ensure the pricing health monitor is active

Verify the `pricing-health-monitor` drill (set up at Baseline) is still running and calibrated:

- ARPU trend, NRR, churn by plan, and usage-to-revenue panels are current
- Anomaly detection thresholds have been calibrated at least once since Scalable
- Weekly pricing digest is being generated and posted
- Pricing sensitivity cohorts (limit-approaching, overage shock, downgrade candidates) are updating daily

If any component has drifted or stopped, restart and recalibrate before proceeding.

### 3. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the pricing page:

**Monitor phase (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check: pricing page conversion rate, plan selection mix, ARPU, checkout abandonment rate, segment-level conversion rates
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context from Attio: current segment configurations, active experiments, recent pricing changes, last 5 experiment results
- Pull 8-week metric history from the pricing page PostHog dashboard
- Pull 5 session recordings from the anomaly window using `posthog-session-recording`
- Run `hypothesis-generation` with the anomaly data + context + session recording summaries
- Receive 3 ranked hypotheses with expected impact and risk levels
- Store hypotheses in Attio as notes on the pricing project record
- If the top hypothesis has risk = "high" (e.g., changes to actual Stripe pricing, checkout flow restructure): send Slack alert for human review and STOP
- If risk = "low" or "medium" (e.g., copy changes, layout tweaks, CTA color, social proof placement): proceed to Experiment phase

**Experiment phase (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use `posthog-experiments` to create a feature flag splitting traffic between control (current) and variant (hypothesis change)
- Implement the variant change:
  - For pricing page copy/layout: update the variant via feature flag-gated code
  - For plan presentation order: swap plan card positions in the variant
  - For checkout flow: modify form fields or add/remove steps in the variant
  - For Stripe pricing structure: use `pricing-experiment-runner` drill (always requires human approval)
- Set experiment duration: minimum 7 days or until 200+ conversions per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, risk level

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` with control vs. variant data for all metrics (conversion rate, plan mix, ARPU, checkout abandonment)
- Decision tree:
  - **Adopt:** Variant won with 95% confidence and no guardrail breaches. Update production code to use the winning variant. Log the change in Attio. Move to Report phase.
  - **Iterate:** Directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Diagnose phase.
  - **Revert:** Variant lost or a guardrail was breached. Disable the variant. Restore control. Log the failure with the specific failure reason. Return to Monitor phase. Observe the 7-day cooldown before testing the same variable again.
  - **Extend:** Results are promising but sample size is insufficient. Keep running for another period. Set a reminder.
- Store the full evaluation (decision, confidence interval, reasoning, metric deltas) in Attio

**Report phase (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate: net metric change from all adopted changes this week
- Generate a weekly optimization brief using Claude:
  - What changed and why (specific experiment results)
  - Net impact on primary KPIs (conversion rate, ARPU, plan mix)
  - Current distance from estimated local maximum
  - Cumulative lift since Durable level started
  - Recommended focus for next week
- Post the brief to Slack and store in Attio

### 4. Configure guardrails

These guardrails are critical and must be enforced by the n8n orchestration:

- **Rate limit:** Maximum 1 active pricing page experiment at a time. Never stack experiments.
- **Revert threshold:** If pricing page conversion rate drops >30% during any experiment, auto-revert immediately.
- **Revenue protection:** If new-subscriber ARPU drops >20% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Any change to actual Stripe pricing (price points, tier boundaries, billing intervals)
  - Checkout flow changes that affect >50% of traffic
  - Any hypothesis the AI flags as "high risk"
- **Cooldown:** After a reverted experiment, wait 7 days before testing the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause autonomous optimization and flag for human strategic review.
- **Never experiment without baseline data:** If a metric lacks 30+ days of PostHog tracking, instrument it first before running experiments on it.

### 5. Detect convergence

The optimization loop runs indefinitely. However, the agent must detect convergence:

- Track the lift produced by each successive adopted experiment
- When 3 consecutive experiments produce <2% improvement each, the pricing page has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency from 2-4/month to 1/month (maintenance mode)
  3. Generate a convergence report: "Pricing page is optimized. Current conversion rate: [X]%. ARPU: $[Y]. Plan mix: [breakdown]. Further gains require strategic changes (new plans, new audience segments, product changes) rather than tactical optimization."
  4. Post convergence report to Slack and store in Attio
  5. Continue weekly monitoring to detect if market changes break convergence (competitor pricing change, seasonal shift, product update)

If post-convergence monitoring detects a >10% metric shift, re-enter the full daily optimization loop.

## Time Estimate

- 4 hours: pricing-page-conversion-monitor setup
- 2 hours: autonomous-optimization configuration for pricing page
- 2 hours: guardrail and convergence detection setup
- Ongoing: ~2 hours/week for optimization brief review and human-approval gating

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, anomaly detection, session recordings, funnels, dashboards | Free up to 1M events/mo, then $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Billing event streaming, pricing experiment variant prices | 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Orchestration: daily monitor, experiment lifecycle, weekly reports | From €24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | Usage-based ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Experiment audit trail, pricing project records, hypothesis storage | From $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `pricing-page-conversion-monitor` — always-on pricing page funnel monitoring with anomaly detection, session recording context, and dynamic behavioral cohorts
- `pricing-health-monitor` — broader pricing health observation (ARPU, NRR, churn by plan, usage-to-revenue) that provides macro context for the optimization loop
