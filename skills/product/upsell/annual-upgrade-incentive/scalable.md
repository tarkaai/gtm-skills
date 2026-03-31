---
name: annual-upgrade-incentive-scalable
description: >
  Monthly to Annual Conversion — Scalable Automation. A/B test discount tiers, offer timing,
  and channel mix. Run pricing experiments on annual vs monthly economics. Segment-specific
  offers at 10x the Baseline volume.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=12% conversion rate at 500+ monthly impressions with positive net revenue per conversion"
kpis: ["Annual conversion rate at scale", "Net revenue per annual conversion", "LTV lift (annual vs monthly cohort at 90 days)", "Experiment win rate", "Segment-specific conversion rates"]
slug: "annual-upgrade-incentive"
install: "npx gtm-skills add product/upsell/annual-upgrade-incentive"
drills:
  - ab-test-orchestrator
  - pricing-experiment-runner
  - upgrade-prompt
---

# Monthly to Annual Conversion — Scalable Automation

> **Stage:** Product -> Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Annual upgrade offers running at 500+ impressions per month across all monthly subscriber segments. Rigorous A/B testing of discount tiers, offer timing, copy, and surfaces. Pricing experiments validating the economics of annual vs monthly billing. Segment-specific offers (by tenure, plan, usage level) replacing the one-size-fits-all discount. Conversion rate >=12% sustained at this volume with positive net revenue per conversion (discount cost < LTV uplift from annual commitment).

## Leading Indicators

- Experiment velocity: at least 2 completed A/B tests per month (confirms the testing cadence is active)
- Each segment has a winning offer variant (confirms personalization is working)
- Annual cohort 60-day retention measurably higher than monthly cohort (confirms the retention thesis at scale)
- Net revenue per annual conversion is positive and trending upward (confirms economics are sound)

## Instructions

### 1. Launch systematic A/B testing of offer variants

Run the `ab-test-orchestrator` drill to test the variables that most impact annual conversion. Test one variable at a time, in this priority order:

**Test 1: Discount tier**
- Control: current discount (e.g., 2 months free / ~17% off)
- Variant A: 1 month free (~8% off)
- Variant B: 3 months free (~25% off)
- Variant C: No discount, value framing only ("Lock in your rate for 12 months — never worry about price increases")
- Primary metric: `annual_upgrade_completed` rate. Secondary metric: net revenue per conversion (higher discount = more conversions but less revenue per conversion — find the optimum).
- Minimum sample: 100 impressions per variant. Using PostHog feature flags, assign monthly subscribers randomly to variants. Run for 2-4 weeks or until statistical significance.

**Test 2: Offer timing relative to billing cycle**
- Control: 3-7 days before renewal
- Variant A: Immediately after a successful monthly charge ("You just paid $X. Annual would have been $Y — save $Z next time")
- Variant B: Mid-cycle when engagement peaks (e.g., day 15 of billing period, when users are most active)
- Primary metric: CTR and conversion rate. Users may respond differently to offers depending on their mental proximity to payment.

**Test 3: Offer surface and copy**
- Control: In-app modal with pricing comparison
- Variant A: In-app inline banner on billing page only
- Variant B: Dedicated email with savings calculator link
- Variant C: In-app tooltip on the plan badge in navigation
- Primary metric: conversion rate. Secondary: offer fatigue rate per surface.

**Test 4: Social proof and urgency framing**
- Control: Standard savings message
- Variant A: Social proof: "[N] customers switched to annual this month"
- Variant B: Urgency: "This offer expires in 7 days" (with real expiry enforced)
- Variant C: Loss aversion: "You've spent $X extra this year on monthly billing"
- Primary metric: conversion rate.

For each test, follow the `ab-test-orchestrator` drill rigorously: calculate sample size before launching, do not peek at results early, and document the full hypothesis-result-decision cycle.

### 2. Run pricing experiments on annual economics

Run the `pricing-experiment-runner` drill to validate the annual billing economics:

**Experiment: Optimal annual price point**
- Hypothesis: "If we set the annual price at 10 months' worth of monthly (instead of the standard 12-month commitment with 2 months free), conversion rate will increase by 5pp without reducing per-user revenue, because 10x framing is clearer than percentage discounts."
- Create a new Stripe Price object for annual at the test price point
- Use PostHog feature flags to route a segment of monthly subscribers to the test price
- Track conversion rate AND 90-day retention to ensure the price point does not attract low-commitment users
- Minimum experiment duration: 60 days (full annual billing cycle observation)

**Guardrails for pricing experiments:**
- Auto-revert if annual conversion rate drops >50% vs control (the test price is too high)
- Auto-revert if 30-day regret rate (annual-to-monthly downgrade) exceeds 10% (the commitment was not genuine)
- Human approval required for any price change affecting existing annual subscribers

### 3. Build segment-specific offers

Run the `upgrade-prompt` drill Steps 1-4, creating separate offer configurations per segment:

**By tenure (months on monthly billing):**
- 1-3 months: Lighter offer — focus on value lock-in, minimal discount. These users are still evaluating the product. Aggressive discounts may attract uncommitted users.
- 3-6 months: Standard offer — the "sweet spot" segment. They have validated the product and are likely to stay. Full discount tier.
- 6-12 months: Premium offer — they are already loyal. Use loss aversion framing ("You've paid $X extra by staying monthly") rather than discounts.
- 12+ months: Direct ask with no discount — "You've been monthly for over a year. Switch to annual for predictable billing." These users chose monthly deliberately; a discount is unlikely to change their mind, but a framing change might.

**By plan tier:**
- Starter/lower plans: Standard percentage or months-free offer
- Pro/higher plans: Emphasize price lock and rate protection (higher-plan users are more sensitive to price increases)
- Team plans: Emphasize per-seat savings at annual ("Your team of 8 saves $X per year on annual billing")

**By usage level:**
- Power users (top 20% by usage): "You clearly love [product] — lock in your rate"
- Regular users: Standard discount offer
- Low-usage users: Do NOT offer annual — they are more likely to churn, and an annual commitment from a low-usage user increases refund risk

Configure each segment's offer in Intercom (using user properties for targeting) and Loops (using audience segments for email). Track `offer_variant` in PostHog to measure segment-specific conversion rates.

### 4. Scale impression volume

Expand the trigger coverage to reach 500+ monthly impressions:

- Activate all tested trigger types (renewal proximity, billing page visit, usage milestone) simultaneously with frequency capping enforced
- Add new trigger: **Post-support-resolution** — after a support ticket is resolved positively (CSAT 4-5), send a Loops email 3 days later with the annual offer. Positive support experiences create goodwill.
- Add new trigger: **Feature adoption burst** — when a monthly subscriber adopts a new feature and uses it 5+ times in a week, trigger an in-app offer tying annual commitment to continued access
- Monitor impression volume weekly. If <500/mo, lower the tenure threshold for milestone triggers or expand the billing page trigger to the account settings page

### 5. Measure unit economics

For every annual conversion, calculate and track:

```
net_revenue_per_conversion = (
  annual_price_charged
  - discount_given
  - (monthly_price * 12)            // baseline: what they would have paid monthly for 12 months
  + (monthly_price * extra_retained_months)  // bonus: additional months retained because of annual lock-in
)
```

Pull `extra_retained_months` from PostHog retention analysis: compare the annual-converted cohort's retention curve against the monthly cohort's retention curve. At 90 days, measure the gap.

If net revenue per conversion is negative (discount exceeds LTV uplift), reduce the discount tier for segments where the math does not work. If it is positive and growing, the play is ready for Durable.

### 6. Evaluate against threshold

After 2 months of scaled operation:

- **Primary metric:** >=12% conversion rate at 500+ monthly impressions
- **Economic metric:** Net revenue per annual conversion is positive
- **Retention metric:** Annual cohort 90-day retention is measurably higher than monthly cohort

**Pass:** All 3 conditions met. Proceed to Durable.
**Fail:** Conversion rate below threshold. Focus A/B testing on the weakest segment. If economics are negative, reduce discount tiers. If retention is not better for annual, investigate whether annual converts are genuinely more committed or just attracted by the discount.

## Time Estimate

- 10 hours: Design and launch 4 A/B tests (2-3 hours per test setup, staggered over 8 weeks)
- 6 hours: Set up and monitor pricing experiment in Stripe + PostHog
- 8 hours: Build segment-specific offer configurations (2 hours per segment)
- 6 hours: Expand triggers and scale impression volume
- 6 hours: Unit economics tracking, analysis, and optimization
- 4 hours: Weekly review and experiment evaluation (0.5 hours/week over 8 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | A/B testing via feature flags, experiments, funnels, retention analysis | Free tier: 1M events/mo + 1M flag requests/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app offer delivery with segment targeting | Advanced $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email offers with audience segmentation | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Trigger orchestration, frequency capping, experiment routing | Self-hosted free; Cloud from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Stripe | Pricing experiments, annual subscription management | Billing Starter 0.5% recurring + 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| Attio | Experiment logging, campaign tracking | Free for 3 users; Plus $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific monthly cost at Scalable:** $150-350/mo (mainly Intercom Advanced + Loops; PostHog experiments may exceed free tier at scale).

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on discount tiers, timing, surfaces, and copy
- `pricing-experiment-runner` — manages the Stripe pricing experiment with guardrails and auto-revert
- `upgrade-prompt` — builds segment-specific offer configurations with contextual targeting
