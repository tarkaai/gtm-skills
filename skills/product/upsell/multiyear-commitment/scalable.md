---
name: multiyear-commitment-scalable
description: >
  Multi-Year Deal Incentives — Scalable Automation. Test offer tiers (discount levels, term lengths,
  perks), segment offers by account profile, add 2-year terms, and optimize the funnel for maximum
  committed ARR per account.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: "≥15% conversion rate at 200+ accounts offered; committed ARR ≥20% of total"
kpis: ["Offer conversion rate by tier", "Committed ARR penetration", "Retention lift (committed vs. monthly)", "Revenue per offered account", "Channel conversion comparison"]
slug: "multiyear-commitment"
install: "npx gtm-skills add product/upsell/multiyear-commitment"
drills:
  - ab-test-orchestrator
  - pricing-experiment-runner
  - upgrade-prompt
---

# Multi-Year Deal Incentives — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Find the 10x multiplier for the commitment program. At Baseline you proved the pipeline works at a single discount level. At Scalable you test multiple offer tiers, add 2-year terms, segment offers by account profile, and A/B test every variable to maximize committed ARR. The goal is to increase committed ARR penetration from whatever Baseline achieved to 20%+ of total ARR while maintaining or improving the retention lift.

## Leading Indicators

- Experiment velocity: at least 2 completed A/B tests per month
- Offer tier conversion spread: variant tiers outperforming Standard by >3pp
- 2-year term uptake: any non-zero percentage choosing 2-year over annual
- Segment-specific conversion rates diverging (proves segmentation adds value)
- No increase in committed account churn (discounts are not attracting poor-fit customers)

## Instructions

### 1. A/B test offer tiers

Run the `ab-test-orchestrator` drill to test the 3 offer tiers defined in the `multiyear-offer-engine` drill:

- **Control (Standard):** 2 months free (17%), no perks
- **Variant A (Enhanced):** 3 months free (25%), priority support upgrade
- **Variant B (Premium):** 3 months free (25%), priority support + dedicated CSM session

Use PostHog feature flags to assign Ready-tier accounts to one of 3 groups. Each group sees their tier's offer across all channels (in-app, email). Run until each group has 70+ accounts (minimum for statistical significance at this conversion rate).

Primary metric: `multiyear_offer_converted` rate by tier.
Secondary metrics: time-to-conversion, retention at 90 days post-commitment, support ticket volume.
Guardrail: if committed account churn in any tier exceeds 5% within 90 days, pause that tier.

After significance: adopt the winning tier as the new default. If Enhanced or Premium wins, calculate whether the additional discount/perk cost is justified by the conversion lift.

### 2. Test 2-year commitment terms

Run the `pricing-experiment-runner` drill to introduce 2-year pricing:

1. Create 2-year price objects in Stripe with rate lock guarantee (Step 2 of the drill)
2. Using PostHog feature flags, show the 2-year option alongside the annual option for 50% of Ready-tier accounts
3. Track: what percentage choose 2-year vs. annual vs. stay monthly
4. Hypothesis: "If we offer a 2-year option with rate lock, 10-20% of converters will choose 2-year, increasing average commitment length by 3+ months"

This is a pricing experiment with higher stakes. Follow the drill's guardrails: minimum 2 billing cycles, auto-revert if churn spikes, weekly monitoring.

### 3. Segment the offer by account profile

Run the `upgrade-prompt` drill adapted for commitment offers. Different accounts respond to different value propositions:

**By account size:**
- Small accounts (1-3 seats, <$100/mo): lead with savings percentage ("save 25%")
- Mid accounts (4-10 seats, $100-500/mo): lead with dollar savings ("save $1,200/year")
- Large accounts (10+ seats, >$500/mo): lead with rate lock ("protect against price increases") and route to sales

**By usage pattern:**
- Growing accounts (usage up >30% in 90 days): lead with rate lock — "lock in today's price as your team grows"
- Stable accounts (consistent usage): lead with savings — "you clearly love [product], save by going annual"
- Power users (feature breadth >80%): lead with perks — "get priority support for your advanced workflows"

Using `intercom-in-app-messages`, create segment-specific offer copy. Using `loops-sequences`, create segment-specific email sequences. Use PostHog feature flags to assign the segment-appropriate messaging.

Track conversion rate by segment. The segment that converts highest gets the most offer volume at Durable.

### 4. Optimize the funnel at each step

Using `ab-test-orchestrator`, systematically test one funnel variable at a time:

**Offer placement test:**
- Control: billing page banner
- Variant: settings page banner
- Variant: in-app modal on login (for admins only)

**Email sequence test:**
- Control: 3-email sequence over 12 days
- Variant: 2-email sequence over 7 days (shorter, more urgent)

**CTA copy test:**
- Control: "Switch to annual — save [X]%"
- Variant: "Lock in your rate — save $[amount]/year"

**Timing test:**
- Control: offer immediately when entering Ready tier
- Variant: wait until the account's next billing date is within 7 days

Run each test to significance before moving to the next. Each test should take 2-3 weeks with sufficient Ready-tier volume.

### 5. Evaluate against threshold

After 6 weeks of testing and optimization:

1. Calculate overall conversion rate across all accounts offered (regardless of tier/segment)
2. Calculate committed ARR as a percentage of total ARR
3. Compare retention: committed accounts vs. monthly accounts at 90 days post-commitment

Pass threshold: **15% or higher conversion rate across 200+ accounts offered, AND committed ARR reaches 20% or more of total ARR.**

If PASS: The commitment program scales. Proceed to Durable to hand optimization to the autonomous agent.

If FAIL: Focus on the highest-impact lever:
- If conversion rate is close but penetration is low → the Ready-tier definition is too narrow. Lower the readiness threshold and test.
- If penetration is close but conversion rate is low → the offer is not compelling enough. Test deeper discounts or better perks.
- If both are far off → the product's monthly value prop may be stronger. Consider whether commitment is the right play for your customer base, or pivot to a different LTV driver (seat expansion, usage-based pricing).

## Time Estimate

- 8 hours: set up 3-way offer tier A/B test (feature flags, Intercom variants, Loops variants)
- 6 hours: create 2-year Stripe prices and pricing experiment infrastructure
- 8 hours: build segment-specific offers (copy, targeting rules, PostHog cohorts)
- 8 hours: run 3-4 funnel optimization tests (2 hours each to set up and analyze)
- 10 hours: monitor experiments, analyze results, document learnings (spread over 6 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, funnels | Free up to 1M events/mo; Experiments included |
| Stripe | Multi-year prices, Checkout sessions | 2.9% + $0.30/txn |
| Intercom | Segment-specific in-app offers | Starter $74/mo; https://www.intercom.com/pricing |
| Loops | Segment-specific email sequences | $49/mo for 5K contacts; https://loops.so/pricing |
| n8n | Experiment orchestration workflows | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Attio | Deal tracking, segment data | $29/seat/mo; https://attio.com/pricing |

## Drills Referenced

- `ab-test-orchestrator` — runs offer tier, placement, copy, and timing experiments with statistical rigor
- `pricing-experiment-runner` — manages the 2-year pricing experiment with Stripe guardrails and auto-revert
- `upgrade-prompt` — contextual prompt delivery system adapted for segment-specific commitment offers
