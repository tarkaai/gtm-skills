---
name: annual-upgrade-incentive-smoke
description: >
  Monthly to Annual Conversion — Smoke Test. Deploy one annual upgrade offer
  to the highest-intent monthly subscriber segment and measure whether users convert.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 annual conversions from >=20 offer impressions"
kpis: ["Offer CTR", "Offer-to-checkout rate", "Annual conversions count"]
slug: "annual-upgrade-incentive"
install: "npx gtm-skills add product/upsell/annual-upgrade-incentive"
drills:
  - upgrade-prompt
  - threshold-engine
---

# Monthly to Annual Conversion — Smoke Test

> **Stage:** Product -> Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

One annual upgrade offer live on the single highest-intent monthly subscriber segment. At least 20 monthly subscribers see the offer. At least 3 convert to annual billing. This proves that a discount incentive tied to a contextual moment (billing page visit, usage milestone, or renewal proximity) generates annual commitment intent.

## Leading Indicators

- Monthly subscribers encountering the offer trigger at the expected rate (confirms the trigger fires correctly)
- `annual_offer_shown` and `annual_offer_clicked` events appearing in PostHog Live Events (confirms instrumentation)
- At least 1 click within the first 48 hours (early signal before full measurement window)

## Instructions

### 1. Identify the highest-intent annual upgrade trigger

Run the `upgrade-prompt` drill, Step 1, adapted for annual conversion. Pick ONE trigger to test — the one most likely to generate annual commitment:

- **Renewal proximity** (recommended first choice): Monthly subscriber is 3-7 days before their next billing date. The offer appears as an in-app banner or email: "Switch to annual before your next charge and save X months free." This trigger has high intent because the user is already thinking about payment.
- **Usage milestone** (second choice): Monthly subscriber just hit a usage milestone (e.g., 90 days active, 100th action). The offer frames annual as a reward for their commitment: "You've been using [product] for 3 months — lock in your rate and save."
- **Billing page visit** (third choice): Monthly subscriber views the billing or plan page. The offer appears inline on the page showing the annual price comparison.

Do NOT test broad audience triggers at Smoke. Focus on the segment most likely to convert.

### 2. Define the discount offer

Choose ONE discount structure to test:

- **Months free**: "Get 2 months free when you switch to annual" (equivalent to ~17% discount). This is the clearest value proposition — users understand "free months" immediately.
- **Percentage off**: "Save 20% with annual billing" — simpler but less tangible.
- **Price lock**: "Lock in your current rate for 12 months" — works when a price increase is planned or rumored.

Calculate the break-even: if the discount costs you X months of revenue upfront, how many additional months of retention does annual billing need to deliver to be net positive? Typically annual subscribers retain 2-4x longer than monthly, so even a 2-month discount is profitable.

### 3. Deploy the offer

Run the `upgrade-prompt` drill, Steps 2-3 adapted for annual conversion. Deploy using Intercom in-app messages (for billing page or in-product triggers) or Loops transactional email (for renewal proximity triggers). The offer must:

- State the exact savings: "You pay $X/year instead of $Y/year ($Z savings)" — never just the percentage
- Show the discount as a concrete amount: "That's 2 months free"
- Include a single CTA button that links directly to the annual checkout/switch page in Stripe
- Track these PostHog events with properties:

| Event | When | Properties |
|-------|------|------------|
| `annual_offer_shown` | Offer renders or email delivered | `trigger_type`, `discount_tier`, `plan_current`, `months_on_monthly` |
| `annual_offer_clicked` | User clicks the CTA | `trigger_type`, `discount_tier`, `plan_current` |
| `annual_offer_started` | User reaches annual checkout page | `trigger_type`, `plan_current` |
| `annual_upgrade_completed` | Stripe confirms subscription changed to annual | `trigger_type`, `discount_tier`, `annual_revenue`, `discount_amount` |

**Human action required:** Review the offer copy before deploying. Verify the Stripe annual checkout flow works end-to-end (test with a sandbox subscription). Confirm that switching a monthly subscription to annual in Stripe handles proration correctly (either credit remaining monthly period or start annual at next billing date). Deploy to all monthly subscribers who hit the trigger.

### 4. Instrument and verify

Open PostHog Live Events. Trigger the condition yourself (e.g., visit the billing page on a test monthly account, or simulate a renewal proximity event via n8n). Confirm all 4 events appear with correct properties. If any event is missing, fix the instrumentation before proceeding.

Verify in Stripe that a test annual switch:
- Creates the correct annual subscription with the discount applied
- Fires the `annual_upgrade_completed` event via your billing webhook
- Records the correct `annual_revenue` and `discount_amount` properties

### 5. Run for 1 week and evaluate

Let the offer run for 7 days. Do not change the copy, discount, or targeting mid-run.

Run the `threshold-engine` drill to evaluate: query PostHog for `annual_offer_shown` count and `annual_upgrade_completed` count.

**Pass:** >=3 annual conversions from >=20 impressions. Proceed to Baseline.
**Fail:** <3 conversions. Diagnose: Was the trigger firing at the right moment? Was the discount compelling enough? Was the checkout flow frictionless? Did users understand the savings? Revise and re-run.

## Time Estimate

- 1 hour: Identify trigger segment and calculate discount economics
- 1.5 hours: Build the offer (Intercom in-app message or Loops email) and configure PostHog events
- 1 hour: Set up and verify Stripe annual checkout flow with discount
- 0.5 hours: End-to-end instrumentation test
- 1 hour: Review after 48 hours for early signal
- 1 hour: Final evaluation after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app offer delivery | Essential $29/seat/mo; Advanced $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email offer delivery (if using email trigger) | From $49/mo for paid plans ([loops.so/pricing](https://loops.so/pricing)) |
| Stripe | Subscription management, annual checkout | Billing Starter 0.5% on recurring + 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |

**Estimated play-specific cost at Smoke:** $0 incremental (tools already in stack). Stripe fees are per-transaction on conversions that happen.

## Drills Referenced

- `upgrade-prompt` — adapted for annual conversion: defines the trigger taxonomy, builds the contextual offer, and instruments the funnel
- `threshold-engine` — evaluates conversion count against the >=3 pass threshold and recommends next action
