---
name: cross-sell-in-product-baseline
description: >
  Related Product Cross-Sell — Baseline Run. Deploy always-on cross-sell surfaces for
  1-2 products with automated trigger detection, coordinated in-app and email channels,
  and full funnel tracking.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: ">=10% of triggered users activate the cross-sell product within 30 days"
kpis: ["Cross-sell activation rate", "Impression-to-activation funnel conversion", "ARPU lift from cross-sell adopters", "Email vs. in-app channel conversion"]
slug: "cross-sell-in-product"
install: "npx gtm-skills add product/upsell/cross-sell-in-product"
drills:
  - posthog-gtm-events
  - activation-optimization
---

# Related Product Cross-Sell — Baseline Run

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Always-on cross-sell surfaces running for 1-2 products with automated trigger detection via n8n. At least 10% of users who trigger the cross-sell criteria activate the second product within 30 days. The full funnel (impression -> click -> activation start -> activation complete) is tracked and measured.

## Leading Indicators

- n8n trigger detection workflow fires daily and correctly identifies new trigger-qualified users
- In-app surface impressions are steady (not declining, which would signal audience exhaustion)
- Email fallback channel generates incremental activations beyond in-app alone
- ARPU for cross-sell adopters is measurably higher than single-product users
- Fatigue controls are working (dismissal rate stable or declining)

## Instructions

### 1. Set up full event tracking

Run the `posthog-gtm-events` drill to establish the cross-sell event taxonomy. Configure these events:

```
cross_sell_trigger_fired       — user crossed a trigger threshold
cross_sell_impression          — surface rendered for the user
cross_sell_clicked             — user engaged with the surface
cross_sell_activation_started  — user began the second product's setup
cross_sell_activated           — user completed activation of the second product
cross_sell_dismissed           — user dismissed the surface
cross_sell_email_sent          — fallback email dispatched
cross_sell_email_clicked       — user clicked through from email
```

Each event must carry properties: `product_slug`, `surface_type` (tooltip|banner|email), `trigger_behavior`, `user_plan`, `days_since_signup`, `channel` (in-app|email).

Build the PostHog funnel: `cross_sell_impression` -> `cross_sell_clicked` -> `cross_sell_activation_started` -> `cross_sell_activated`. Save as "[Cross-Sell] Activation Funnel" with breakdowns by product and surface type.

### 2. Deploy always-on discovery surfaces

Run the the addon discovery surface build workflow (see instructions below) drill for 1-2 validated products (the Smoke winner plus the next highest-scoring product from the catalog mapping). This time, complete ALL steps:

- Step 1: Use the trigger map from the cross sell catalog mapping workflow (see instructions below) (already validated at Smoke)
- Step 2: Events are configured from Step 1 above
- Step 3: Build both a tooltip AND a banner surface per product to test which performs better
- Step 4: Build the n8n trigger detection workflow — daily cron identifies users who crossed trigger thresholds, activates PostHog feature flags to show the appropriate surface, and enqueues email fallback for users who do not engage in-app within 48 hours
- Step 5: Route high-value expansions (>$200/mo potential) to sales as Attio expansion deals
- Step 6: Implement full fatigue controls (suppress after 2 dismissals per product, max 2 products per user per week, global suppression after 3 cross-product dismissals in a month)

### 3. Optimize the activation funnel

Run the `activation-optimization` drill focused on the cross-sell product's activation flow. Analyze the PostHog funnel to find the biggest drop-off:

- **Impression -> Click drop-off**: Surface copy or placement problem. Test alternative messages.
- **Click -> Activation Start drop-off**: Landing/setup page problem. Simplify the entry experience for existing users (they should not repeat onboarding they already completed).
- **Activation Start -> Activated drop-off**: Product friction. The second product's first-use experience needs improvement — use Intercom product tours to guide users through the initial setup specific to their existing data and workflows.

Run 2-3 targeted improvements at the biggest drop-off point. Measure each change against the baseline funnel conversion rate.

### 4. Evaluate against threshold

Measure after 3 weeks of always-on operation: >=10% of triggered users activated the cross-sell product within 30 days of trigger. If PASS, proceed to Scalable. If FAIL, diagnose:

- Activation rate 5-9%: Directionally positive. Extend the Baseline for 2 more weeks while optimizing the biggest funnel drop-off.
- Activation rate below 5%: Trigger accuracy or product-market fit issue. Re-run the cross sell catalog mapping workflow (see instructions below) with updated data. The trigger may be firing for users who are not genuinely ready.

## Time Estimate

- 4 hours: Configure full event taxonomy, build PostHog funnels and dashboard
- 6 hours: Build discovery surfaces for 1-2 products with tooltip and banner variants
- 4 hours: Build n8n trigger detection workflow with email fallback and sales routing
- 4 hours: Analyze funnel, identify drop-offs, implement 2-3 optimizations
- 2 hours: Monitor results and compile evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app tooltips, banners, product tours | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Fallback cross-sell emails | Free up to 1,000 contacts — https://loops.so/pricing |
| n8n | Trigger detection workflow, email fallback orchestration | Free self-hosted / $20/mo cloud — https://n8n.io/pricing |
| Attio | Cross-sell tracking, expansion deals, sales routing | Included in existing plan — https://attio.com/pricing |

## Drills Referenced

- `posthog-gtm-events` — establishes the cross-sell event taxonomy for consistent tracking
- the addon discovery surface build workflow (see instructions below) — builds always-on in-product surfaces with automated trigger detection, email fallback, and sales routing
- `activation-optimization` — identifies and fixes the biggest drop-off in the cross-sell activation funnel
