---
name: pricing-experiment-baseline
description: >
  Pricing Tests — Baseline Run. Run the winning pricing variant at production scale
  with statistical rigor across 200+ users and automated weekly monitoring.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 2 months"
outcome: ">=5% net revenue retention improvement with 95% statistical significance across 200+ users per variant"
kpis: ["Net revenue retention (NRR)", "Revenue per user", "30-day churn rate by variant", "Checkout conversion rate", "Support ticket volume (pricing-related)"]
slug: "pricing-experiment"
install: "npx gtm-skills add product/upsell/pricing-experiment"
drills:
  - pricing-experiment-runner
  - posthog-gtm-events
  - pricing-health-monitor
---

# Pricing Tests — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The pricing variant that showed directional signal at Smoke is now running as a statistically rigorous experiment across 200+ users per variant. After 2 full billing cycles, you have a confident adopt/iterate/revert decision backed by 95% significance on net revenue retention. The always-on monitoring workflow catches guardrail breaches and auto-reverts if necessary.

## Leading Indicators

- PostHog experiment created with proper sample size calculation (minimum 200 per variant)
- First weekly monitoring report generated automatically by n8n
- Billing event streaming confirmed (Stripe events flowing into PostHog via `billing-event-streaming` fundamental)
- No guardrail breaches in the first 2 weekly checks
- Treatment group's support ticket volume within 2x of control group

## Instructions

### 1. Instrument billing events and pricing-specific tracking

Run the `posthog-gtm-events` drill to set up detailed tracking for this experiment:

Events to configure:
- `pricing_experiment_enrolled` — user assigned to treatment or control (properties: `variant`, `previous_price`, `new_price`, `enrollment_date`)
- `pricing_experiment_invoice_generated` — treatment user's first invoice at the new price (properties: `amount_usd`, `variant`, `plan_name`)
- `pricing_experiment_churned` — user in either group cancels (properties: `variant`, `days_since_enrollment`, `cancel_reason`)
- `pricing_experiment_upgraded` — user in either group moves to a higher plan (properties: `variant`, `from_plan`, `to_plan`, `mrr_change`)
- `pricing_experiment_downgraded` — user in either group moves to a lower plan (properties: same as upgraded)
- `pricing_experiment_support_ticket` — support ticket filed mentioning pricing, billing, or charges (properties: `variant`, `ticket_category`)

Build PostHog funnels:
- Enrollment > First invoice > 30-day retention > 60-day retention (segmented by variant)

### 2. Launch the production experiment

Run the `pricing-experiment-runner` drill with these Baseline-specific parameters:

- Use the same Stripe variant prices from Smoke (or create refined versions if the hypothesis was iterated)
- Create a new PostHog feature flag `pricing-experiment-baseline` with 50/50 split
- Target: all eligible customers on the plan being tested (same exclusions as Smoke: no enterprise, no custom pricing, no accounts <30 days old)
- Calculate required sample size using PostHog's experiment calculator: for a 5% minimum detectable effect on NRR, you need approximately 200+ users per variant
- Set experiment duration: minimum 2 full billing cycles (60 days for monthly billing)
- Build the n8n weekly monitoring workflow that checks all guardrail metrics and posts status reports to Slack

**Human action required:** If the variant pricing differs from Smoke (e.g., adjusted tier boundaries based on Smoke learnings), review the updated Intercom message copy before launch.

### 3. Monitor pricing health throughout the experiment

Run the `pricing-health-monitor` drill to build always-on monitoring:

- Build the "Pricing Health" PostHog dashboard: ARPU trend, ARPU by plan, NRR, expansion revenue, contraction revenue, churn by plan, churn by usage band, usage-to-revenue ratio
- Configure anomaly detection: ARPU drops >10% MoM = High alert; NRR below 100% for 2 consecutive months = Critical; churn rate exceeds 2x the 90-day average = High
- Build the daily monitoring n8n workflow (07:00 UTC): checks all pricing metrics, compares against 30-day rolling averages, logs anomalies to PostHog and Attio, sends Slack alerts for High/Critical
- Build the weekly pricing digest (Monday 09:00 UTC): aggregates all metrics, computes WoW changes, identifies top 3 trends, posts to Slack

This monitoring layer persists beyond the experiment and feeds the Durable level.

### 4. Evaluate and decide

At the end of the 60-day experiment window:

1. Pull experiment results from PostHog: treatment vs. control on NRR, revenue per user, churn rate, support ticket volume
2. Check statistical significance (require 95% confidence)
3. Check practical significance (is the improvement >= 5% NRR lift?)
4. Review secondary metrics: did treatment users file more support tickets? Did checkout conversion change?

Decision framework:
- **Adopt:** NRR improved >= 5% at 95% significance, no guardrail breaches. Migrate all remaining control users to new pricing. Archive old Stripe prices. Update the pricing page.
- **Iterate:** Directionally positive but not significant. Extend the experiment or design a refined variant (adjust tier boundaries, base price, or overage rates). Return to Step 2.
- **Revert:** Treatment performed worse than control, or guardrails were breached. Revert all treatment users to control pricing. Document why the hypothesis was wrong. Return to Smoke with a new hypothesis.

## Time Estimate

- 4 hours: event instrumentation, funnel setup, billing event verification
- 4 hours: experiment launch (Stripe prices, PostHog flag, n8n workflows, Intercom messages)
- 4 hours: pricing health monitor setup (dashboard, anomaly rules, daily/weekly workflows)
- 4 hours: weekly check-ins over 8 weeks (30 min/week)
- 4 hours: final evaluation, decision, migration or revert execution

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, dashboards, anomaly detection | Free up to 1M flag requests/mo; usage-based beyond — [posthog.com/pricing](https://posthog.com/pricing) |
| Stripe | Variant prices, subscription migrations, billing events | 2.9% + $0.30/txn + 0.7% Billing fee — [stripe.com/pricing](https://stripe.com/pricing) |
| n8n | Weekly monitoring, daily anomaly checks, subscription migration | Standard stack (excluded) |
| Intercom | Pricing change communication to treatment users | $29/seat/mo Essential; Proactive Support Plus $99/mo for advanced messaging — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Attio | Store experiment records, anomaly logs, pricing project notes | Standard stack (excluded) |

**Play-specific cost:** ~$0-99/mo (Intercom Proactive Support Plus add-on if advanced in-app messaging is needed; PostHog likely within free tier at 200-400 user experiment scale)

## Drills Referenced

- `pricing-experiment-runner` — manage the full experiment lifecycle: Stripe prices, PostHog flags, n8n migration, guardrail monitoring, adopt/revert execution
- `posthog-gtm-events` — configure pricing experiment event tracking and funnels
- `pricing-health-monitor` — build always-on pricing metric monitoring with anomaly detection and weekly digests
