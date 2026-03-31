---
name: pricing-page-optimization-smoke
description: >
  Self-Serve Pricing Optimization — Smoke Test. Audit the current pricing page,
  instrument conversion tracking, run a single A/B test on copy or layout, and
  measure whether any lift in plan selection or checkout conversion is detectable.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥5% lift in pricing page to checkout conversion rate"
kpis: ["Pricing page conversion rate", "Plan selection mix", "ARPU (new subscribers)"]
slug: "pricing-page-optimization"
install: "npx gtm-skills add product/upsell/pricing-page-optimization"
drills:
  - posthog-gtm-events
  - lead-capture-surface-setup
  - threshold-engine
---

# Self-Serve Pricing Optimization — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

A single pricing page variant produces a measurable lift (≥5%) in the conversion rate from pricing page view to completed checkout. You have baseline data on plan selection distribution and new-subscriber ARPU.

## Leading Indicators

- PostHog events firing correctly for every step of the pricing funnel (page view, plan click, checkout start, payment entered, subscription created)
- At least 100 unique pricing page visitors during the test window
- Variant and control groups are receiving roughly equal traffic

## Instructions

### 1. Instrument the pricing page funnel

Run the `posthog-gtm-events` drill to define and implement these events on the pricing page:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `pricing_page_viewed` | Page load | `source` (referrer category), `utm_source`, `utm_campaign` |
| `plan_card_clicked` | User clicks a plan's CTA button | `plan_name`, `plan_price`, `billing_interval` (monthly/annual) |
| `checkout_started` | Checkout modal or page loads | `plan_name`, `plan_price`, `billing_interval` |
| `payment_method_entered` | User submits payment form | `plan_name`, `payment_method_type` |
| `subscription_created` | Stripe webhook confirms subscription | `plan_name`, `plan_price`, `billing_interval`, `stripe_subscription_id` |
| `pricing_faq_expanded` | User clicks a FAQ accordion item | `faq_topic` |
| `plan_comparison_toggled` | User switches monthly/annual toggle | `from_interval`, `to_interval` |

Verify all events fire by loading the pricing page in an incognito window, clicking through the full funnel, and checking PostHog Live Events. Every event must appear with correct properties before proceeding.

### 2. Collect 3 days of baseline data

Let the instrumented pricing page run for at least 3 days without changes. Record baseline metrics:

- Pricing page to checkout conversion rate
- Plan selection distribution (percentage choosing each tier)
- Monthly vs. annual selection rate
- Checkout abandonment rate (started checkout but did not complete)
- ARPU of new subscribers

Store these baselines in a PostHog notebook or as an Attio note on the pricing project record.

### 3. Design a single pricing page variant

Identify the biggest drop-off in the funnel from Step 2. Common targets:

- **If conversion rate is low but plan clicks are healthy:** The checkout flow has friction. Test a simplified checkout (fewer fields, inline payment form).
- **If plan clicks are low:** Visitors do not see enough value. Test rewriting plan card headlines to lead with outcomes instead of feature lists.
- **If plan mix is skewed to the cheapest tier:** The mid-tier is not differentiated. Test highlighting the recommended plan with a visual badge and a "most popular" label.
- **If annual selection is low:** The annual discount is not compelling. Test showing the savings amount explicitly ("Save $120/year").

Pick ONE variant. Do not test multiple changes simultaneously.

### 4. Deploy the variant as a lead capture surface

Run the `lead-capture-surface-setup` drill to deploy the variant on the pricing page. Use PostHog feature flags to split traffic 50/50 between the control (current page) and the variant. Ensure the flag is user-level sticky (each visitor always sees the same version).

**Human action required:** Review the variant's visual design and copy before enabling the feature flag. Confirm the checkout flow works end-to-end for the variant.

### 5. Evaluate against threshold

After 7 days or 200+ visitors per variant (whichever comes first), run the `threshold-engine` drill to measure:

- **Primary metric:** Pricing page to checkout conversion rate. Threshold: ≥5% lift (variant vs. control).
- **Guardrail metric:** Checkout abandonment rate must not increase by more than 10pp.
- **Secondary metrics:** Plan mix shift, ARPU change.

If PASS (≥5% lift, guardrail not breached): Record the winning variant details in Attio. Proceed to Baseline.
If FAIL: Analyze PostHog session recordings for 10 visitors in the variant group to identify why the change did not work. Design a new variant targeting a different drop-off point. Re-run this level.

## Time Estimate

- 1.5 hours: event instrumentation and verification
- 0.5 hours: baseline data collection setup
- 1.5 hours: variant design and feature flag configuration
- 1.5 hours: analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, session recordings, funnels | Free up to 1M events/mo, then $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — instrument the pricing page conversion funnel with standardized events
- `lead-capture-surface-setup` — deploy the pricing page variant with tracking and CRM routing
- `threshold-engine` — evaluate whether the ≥5% conversion lift threshold was met
