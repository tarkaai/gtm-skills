---
name: pricing-page-optimization-baseline
description: >
  Self-Serve Pricing Optimization — Baseline Run. Deploy the winning Smoke variant
  to production, build continuous PostHog funnels and dashboards, run a second
  experiment on plan mix or annual selection, and sustain ≥10% conversion lift
  over 2 weeks of always-on measurement.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥10% sustained lift in pricing page conversion rate over 2 weeks"
kpis: ["Pricing page conversion rate", "Plan selection mix", "ARPU (new subscribers)", "Checkout abandonment rate"]
slug: "pricing-page-optimization"
install: "npx gtm-skills add product/upsell/pricing-page-optimization"
drills:
  - posthog-gtm-events
  - ab-test-orchestrator
  - pricing-health-monitor
---

# Self-Serve Pricing Optimization — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

The Smoke winner is deployed at 100%. A second A/B test targeting the next-biggest funnel drop-off produces an additional lift. Combined conversion improvement ≥10% vs. pre-Smoke baseline is sustained over a full 2-week measurement window. Continuous pricing page monitoring is running.

## Leading Indicators

- PostHog dashboard shows stable or improving daily conversion rate with no regression after Smoke winner rollout
- Second experiment reaches sufficient sample size within the 2-week window
- Checkout abandonment rate is trending down vs. Smoke baseline
- ARPU is stable or increasing (variant is not cannibalizing higher tiers)

## Instructions

### 1. Roll out the Smoke winner to 100%

Using the PostHog feature flag from Smoke, ramp the winning variant to 100% of traffic. Remove the control group. Update the pricing page source code to reflect the winning variant as the new default (so you are no longer dependent on the feature flag for the base experience).

Verify via PostHog that conversion events continue to fire correctly after the rollout. Check 24 hours of data to confirm the conversion rate matches the Smoke test treatment group rate (within normal variance).

### 2. Build production-grade tracking

Run the `posthog-gtm-events` drill to extend the Smoke event taxonomy with these additional events:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `pricing_page_scroll_depth` | User scrolls past 25%, 50%, 75%, 100% of the pricing page | `depth_percent`, `time_on_page_ms` |
| `plan_feature_hover` | User hovers on a feature tooltip or expands a feature description | `plan_name`, `feature_name` |
| `billing_interval_toggled` | User switches between monthly and annual toggle | `from_interval`, `to_interval`, `plan_name` |
| `checkout_field_focused` | User focuses a checkout form field | `field_name`, `plan_name` |
| `checkout_error` | Checkout form validation error or payment failure | `error_type`, `field_name`, `plan_name` |

### 3. Launch the pricing health monitor

Run the `pricing-health-monitor` drill to build:

- A PostHog dashboard with ARPU trend, plan mix distribution, conversion rate by source, and checkout abandonment funnel
- Daily anomaly detection rules: conversion rate drop >15%, ARPU drop >10%, checkout abandonment spike >20pp
- A daily n8n workflow that checks all pricing metrics and alerts on anomalies
- A weekly pricing digest posted to Slack

This monitor runs continuously from Baseline through Durable.

### 4. Run a second A/B test

Run the `ab-test-orchestrator` drill to test the next-highest-impact hypothesis. Common Baseline-level experiments:

- **Checkout flow optimization:** If checkout abandonment >40%, test reducing form fields (remove company name, phone number) or adding inline payment via Stripe Elements.
- **Plan anchoring:** If plan mix is skewed to the cheapest tier, test reordering plans so the recommended plan is visually centered and 20% larger. Test adding a "Best value" badge.
- **Annual incentive:** If annual selection <30%, test showing a crossed-out monthly price next to the annual price with explicit dollar savings ("$49/mo billed monthly" vs "$39/mo billed annually — save $120/year").
- **Social proof:** Test adding customer count ("Join 2,000+ teams") or a testimonial quote near the plan CTAs.

Use PostHog feature flags for the split. Run for 7-14 days or until 300+ visitors per variant. Evaluate using the same statistical rigor as the `ab-test-orchestrator` drill specifies: 95% confidence, minimum detectable effect of 3%.

### 5. Evaluate against threshold

After 2 full weeks, measure the combined impact:

- **Primary metric:** Pricing page to checkout conversion rate. Threshold: ≥10% lift vs. pre-Smoke baseline.
- **Secondary metrics:** ARPU, plan mix (is the recommended plan getting more share?), annual selection rate.
- **Guardrail:** Checkout abandonment must not be higher than Smoke baseline.

If PASS (≥10% sustained lift): Document the full test history — hypotheses, variants, results, adopted winners — in Attio. Proceed to Scalable.
If FAIL: Review the pricing health dashboard for anomalies. Use PostHog session recordings to diagnose the remaining friction. Design a third experiment targeting the specific failure point. Re-run Baseline for another 2-week cycle.

## Time Estimate

- 2 hours: Smoke winner rollout and verification
- 3 hours: extended event instrumentation
- 4 hours: pricing health monitor setup (dashboard, anomaly rules, n8n workflows)
- 5 hours: second A/B test (hypothesis, variant build, monitoring)
- 2 hours: analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, funnels, session recordings, dashboards | Free up to 1M events/mo, then $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Daily monitoring workflows, weekly digest automation | From €24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Stripe | Billing event streaming for revenue metrics | 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — extend pricing page event instrumentation with scroll depth, feature hover, checkout field tracking
- `ab-test-orchestrator` — design, run, and evaluate the second A/B test on plan anchoring, checkout, or annual incentive
- `pricing-health-monitor` — build always-on pricing dashboard, daily anomaly detection, and weekly digest
