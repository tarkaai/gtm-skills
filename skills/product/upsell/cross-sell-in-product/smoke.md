---
name: cross-sell-in-product-smoke
description: >
  Related Product Cross-Sell — Smoke Test. Map your product catalog to behavioral
  triggers and deploy one contextual cross-sell surface to validate that users engage
  when shown a related product at the right moment.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=15% CTR on cross-sell surface among triggered users"
kpis: ["Cross-sell surface CTR", "Surface dismissal rate", "Trigger accuracy (% of shown users who were genuinely ready)"]
slug: "cross-sell-in-product"
install: "npx gtm-skills add product/upsell/cross-sell-in-product"
drills:
  - threshold-engine
---

# Related Product Cross-Sell — Smoke Test

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

One in-product cross-sell surface is live for your highest-opportunity related product, targeted at users whose behavior indicates readiness. At least 15% of triggered users who see the surface click through. This validates that contextual, behavior-triggered cross-sell works for your product catalog.

## Leading Indicators

- Trigger cohort populates with 20+ users within the first 3 days (trigger threshold is not too narrow)
- Dismissal rate stays below 40% (the surface feels relevant, not intrusive)
- At least 1 user who clicked through starts the second product's activation flow during the test window
- Zero support tickets about the cross-sell surface feeling spammy

## Instructions

### 1. Map your product catalog to triggers

Run the the cross sell catalog mapping workflow (see instructions below) drill scoped to your top 3 cross-sell products. Specifically:

- Complete Step 1 (build adopter vs. non-adopter cohorts in PostHog for each product)
- Complete Step 2 (identify the behavioral predictors that separate multi-product users from single-product users)
- Complete Step 3 (set trigger thresholds for each product)
- Complete Step 4 (backtest triggers against 90 days of historical data)
- Complete Step 6 (rank products by expected impact)

Pick the single highest-scoring product for this Smoke test. You need a product where: the trigger converts at >=10% historically, there are >=50 users in the trigger cohort today, and the product has a clear in-app entry point.

### 2. Build one cross-sell discovery surface

Run the the addon discovery surface build workflow (see instructions below) drill scoped to the ONE product you selected. Specifically:

- Complete Step 1 (use the trigger map from Step 1 above — do not re-derive it)
- Complete Step 2 (instrument `addon_discovery_impression`, `addon_discovery_clicked`, `addon_activation_started`, `addon_activated` events in PostHog, replacing "addon" references with your cross-sell product slug)
- Complete Step 3 (build ONE contextual surface — a tooltip if the trigger behavior happens at a specific UI location, or a banner if it is a cumulative behavior like "exported 10+ times")
- Skip Steps 4-5 (no n8n automation or sales routing at Smoke level — trigger detection is manual or via PostHog feature flags)
- Complete Step 6 (implement fatigue controls: suppress after 2 dismissals)

The surface copy must reference the user's actual behavior and the cross-sell product's benefit in that context. Not "Try our Analytics product" but "You exported 47 reports this month — Analytics turns these into live dashboards."

**Human action required:** Review the surface copy and placement before enabling. Trigger the behavior yourself to verify the surface appears at the right moment and PostHog events fire in Live Events. Enable for a test group of 20-50 users who match the trigger criteria.

### 3. Observe for 5-7 days

Monitor PostHog daily:
- How many users saw the surface (impressions)?
- How many clicked through (CTR)?
- How many dismissed it?
- Did any user start or complete activation of the cross-sell product?

Do not modify the surface during the observation window. If the surface is technically broken (zero impressions, events not firing), fix the technical issue and restart the clock.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure: >=15% CTR on the cross-sell surface among triggered users. If PASS, proceed to Baseline. If FAIL, diagnose:

- CTR below 5%: Surface copy or placement is wrong. Users see it but ignore it. Rewrite copy to be more specific to their behavior context.
- CTR 5-14%: Concept works but needs refinement. Test a different surface type (switch from banner to tooltip or vice versa) or adjust the trigger threshold.
- Dismissal rate above 50%: Trigger is too broad. You are showing the product to users who do not need it. Tighten the PostHog cohort criteria.

## Time Estimate

- 2 hours: Run catalog mapping — analyze PostHog data, build cohorts, identify triggers
- 1.5 hours: Build the discovery surface in Intercom with PostHog event instrumentation
- 0.5 hours: Verify events fire, enable for test group
- 2 hours: Monitor results over the week and compile evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage tracking, cohorts, trigger detection | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app tooltip or banner surface | Included in existing plan — https://www.intercom.com/pricing |
| Attio | Store cross-sell eligibility attributes | Included in existing plan — https://attio.com/pricing |

## Drills Referenced

- the cross sell catalog mapping workflow (see instructions below) — analyzes product usage data to map which products to recommend to which users and what behavior triggers readiness
- the addon discovery surface build workflow (see instructions below) — builds the in-product surface that shows users the cross-sell product at the trigger moment
- `threshold-engine` — evaluates whether CTR hit the 15% pass threshold
