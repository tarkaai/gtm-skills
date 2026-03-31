---
name: annual-upgrade-incentive-baseline
description: >
  Monthly to Annual Conversion — Baseline Run. Always-on annual upgrade offer system
  with event tracking, multi-channel delivery, and funnel measurement across subscriber segments.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: ">=15% conversion rate on annual offers sustained over 3 consecutive weeks"
kpis: ["Annual offer conversion rate", "Annual upgrade MRR", "Offer CTR by channel", "Monthly-to-annual retention lift (30-day)"]
slug: "annual-upgrade-incentive"
install: "npx gtm-skills add product/upsell/annual-upgrade-incentive"
drills:
  - posthog-gtm-events
  - annual-conversion-health-monitor
  - activation-optimization
---

# Monthly to Annual Conversion — Baseline Run

> **Stage:** Product -> Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Always-on annual upgrade offer system running across 2+ triggers (renewal proximity, billing page visit, usage milestone). Full PostHog event tracking from offer impression through Stripe subscription change. Conversion rate >=15% sustained over 3 consecutive weeks. Clear data on which trigger types and discount tiers produce the highest conversion. Early retention signal: annual cohort retains at a higher rate than monthly cohort at 30 days post-conversion.

## Leading Indicators

- Offer impressions flowing daily at a consistent rate (confirms always-on triggers are firing)
- Conversion funnel has no >50% drop-off at any single step (confirms the checkout flow is not broken)
- Annual cohort 7-day retention is equal to or higher than monthly cohort (early signal of the retention thesis)
- No spike in the offer-fatigued cohort (confirms frequency capping is working)

## Instructions

### 1. Configure comprehensive event tracking

Run the `posthog-gtm-events` drill to establish the annual conversion event taxonomy. Define these events and ensure they fire from every offer surface:

| Event | When | Required Properties |
|-------|------|---------------------|
| `annual_offer_shown` | Offer rendered in-app or email delivered | `trigger_type`, `discount_tier`, `offer_channel`, `plan_current`, `months_on_monthly`, `offer_variant` |
| `annual_offer_clicked` | User clicks CTA | `trigger_type`, `discount_tier`, `offer_channel`, `plan_current` |
| `annual_offer_dismissed` | User explicitly dismisses offer | `trigger_type`, `offer_channel`, `dismiss_reason` (X button, "not now", etc.) |
| `annual_offer_started` | User reaches annual checkout/confirmation page | `trigger_type`, `plan_current`, `annual_price_shown` |
| `annual_upgrade_completed` | Stripe webhook confirms subscription changed to annual | `trigger_type`, `discount_tier`, `annual_revenue`, `discount_amount`, `months_on_monthly`, `previous_monthly_price` |
| `annual_upgrade_reverted` | User switches back to monthly within 30 days | `days_on_annual`, `revert_reason` (if captured) |

Set person properties on conversion: `billing_interval = annual`, `annual_conversion_date`, `annual_discount_tier`. These enable cohort analysis of annual vs monthly subscriber behavior.

### 2. Deploy the health monitor

Run the `annual-conversion-health-monitor` drill to build the measurement layer:

1. Create the annual conversion funnel per trigger type and channel
2. Build the health dashboard with 8 panels (offer volume, CTR, funnel, revenue, retention comparison, fatigue, discount performance, tenure performance)
3. Create the 5 performance cohorts (annual-converted, annual-offer-fatigued, annual-high-intent, annual-eligible-unseen, annual-regret-risk)
4. Configure daily degradation detection with Slack alerting

This gives you the data infrastructure to measure everything from this point forward.

### 3. Expand to multiple triggers

Using the Smoke test winner as the foundation, add 1-2 more trigger types. For each new trigger:

**Renewal proximity trigger** (if not already deployed from Smoke):
- Build an n8n workflow that queries Stripe for monthly subscribers whose next billing date is 3-7 days away
- Send a Loops transactional email: "Your next charge of $X is on [date]. Switch to annual now and save $Y (2 months free)."
- Deploy an Intercom in-app banner for the same users when they log in

**Billing page trigger:**
- Using Intercom in-app messages, show an inline comparison when any monthly subscriber visits the billing/plan page
- Format: side-by-side monthly vs annual pricing with the savings highlighted
- Include social proof: "[N] customers switched to annual this month"

**Usage milestone trigger:**
- Using PostHog cohorts, identify monthly subscribers who hit 90 days active, 6 months active, or a product-specific milestone
- Trigger a celebratory Loops email: "You've been using [product] for 90 days. Lock in your rate with annual billing and save."

For each trigger, ensure all 6 events fire with the correct `trigger_type` property.

### 4. Optimize the conversion funnel

Run the `activation-optimization` drill adapted for the annual conversion funnel. Analyze the funnel from `annual_offer_shown` to `annual_upgrade_completed`:

1. Identify the biggest drop-off step. Common issues:
   - **Offer shown -> Offer clicked** (low CTR): The offer copy is not compelling or the timing is wrong. Test different value framings.
   - **Offer clicked -> Offer started** (drop at checkout): The checkout page is confusing or the user expected a simpler switch. Simplify: ideally a single "Confirm switch to annual" button, not a full checkout flow.
   - **Offer started -> Upgrade completed** (abandoned checkout): Price shock, unclear proration, or payment friction. Show exact charges, explain what happens to their current billing period, and pre-fill payment info from their existing subscription.

2. For each drop-off, implement the fix and measure the impact over 1 week before moving to the next.

### 5. Implement frequency capping and suppression

Prevent offer fatigue:
- Maximum 1 in-app offer per 7-day period per user (even if multiple triggers fire)
- Maximum 1 email offer per 14-day period per user
- Suppress all offers for users in the `annual-offer-fatigued` cohort (dismissed 3+ times in 30 days)
- Never show annual offers to users who converted to annual (obvious, but verify the suppression works)
- Never show annual offers within 7 days of a user filing a support ticket (bad timing)

Log `annual_offer_suppressed` events with `reason` property to monitor suppression rates. If >30% of eligible impressions are suppressed, triggers are overlapping too aggressively.

### 6. Evaluate against threshold

After 3 weeks of always-on operation, run evaluation:

- **Primary metric:** Conversion rate (annual_upgrade_completed / annual_offer_shown) >= 15% sustained over 3 consecutive weeks
- **Supporting metrics:** At least 2 trigger types producing conversions. Annual cohort 30-day retention >= monthly cohort 30-day retention.

**Pass:** >=15% conversion rate for 3 consecutive weeks. Proceed to Scalable.
**Fail:** <15% conversion rate. Diagnose: Which trigger type has the highest conversion? Which step has the biggest drop-off? Is the discount tier wrong (too small to motivate, or so large it attracts price-sensitive users who churn anyway)? Fix and re-run.

## Time Estimate

- 4 hours: Configure event tracking and verify all 6 events fire correctly
- 4 hours: Deploy health monitor (dashboard, cohorts, degradation detection)
- 6 hours: Build and deploy 2 additional trigger types with offers
- 4 hours: Funnel optimization (identify and fix biggest drop-off)
- 2 hours: Frequency capping and suppression rules

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, dashboards | Free tier: 1M events/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app offer delivery, billing page banners | Essential $29/seat/mo; Advanced $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email offer delivery for renewal and milestone triggers | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Renewal proximity detection, frequency capping, suppression logic | Self-hosted free; Cloud from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Stripe | Subscription management, annual billing switch | Billing Starter 0.5% on recurring + 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| Attio | Campaign tracking, degradation alert logging | Free for 3 users; Plus $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific monthly cost at Baseline:** $50-150/mo (mainly Intercom + Loops if not already in stack; n8n and PostHog likely within free tiers).

## Drills Referenced

- `posthog-gtm-events` — establishes the 6-event taxonomy for annual conversion tracking
- `annual-conversion-health-monitor` — builds the dashboard, cohorts, and degradation detection layer
- `activation-optimization` — identifies and fixes the biggest funnel drop-off to maximize conversion rate
