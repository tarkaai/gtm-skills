---
name: multiyear-offer-engine
description: Build and deliver contextual multi-year commitment offers based on account health, usage maturity, and renewal timing
category: Conversion
tools:
  - PostHog
  - Stripe
  - Intercom
  - Loops
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-feature-flags
  - stripe-subscription-management
  - stripe-pricing-tables
  - intercom-in-app-messages
  - loops-sequences
  - n8n-workflow-basics
  - n8n-triggers
  - attio-deals
  - attio-custom-attributes
---

# Multi-Year Offer Engine

This drill builds the system that determines WHICH accounts should receive a multi-year commitment offer, WHAT offer variant to present (discount level, term length, perks), and HOW to deliver it (in-app, email, or sales-assisted). The engine scores readiness, constructs personalized offers, surfaces them at the right moment, and tracks the full funnel from impression to signed commitment.

## Input

- PostHog tracking active with at least 60 days of per-account usage data
- Stripe configured with monthly subscription prices (the drill creates annual/multi-year price objects)
- Intercom for in-app offer delivery
- Loops for email offer delivery
- Attio CRM for deal tracking
- n8n for orchestration workflows

## Steps

### 1. Define commitment readiness signals

Using `posthog-custom-events`, instrument the behavioral signals that predict a customer is ready to commit long-term. These signals differ from churn risk signals — you are looking for STABILITY and EXPANSION, not risk:

| Signal | PostHog Event | Weight | Reasoning |
|--------|--------------|--------|-----------|
| Tenure > 6 months | Account age calculation | +20 | Survived early churn window |
| Usage growth | `usage_volume_spike` (positive trend 3+ months) | +25 | Growing accounts have more to lose |
| Team expansion | `team_invite_sent` count > 2 in 90 days | +15 | Multi-user accounts are stickier |
| Feature breadth | Unique feature events > 60% of available features | +20 | Deep adoption = high switching cost |
| Low churn risk | `churn_risk_score` < 25 | +15 | No point offering commitment to at-risk accounts |
| Renewal approaching | Days to renewal end < 60 | +20 | Natural decision point |
| Billing page visits | `billing_page_viewed` in last 14 days | +10 | Actively thinking about their plan |
| Support satisfaction | NPS > 7 or CSAT > 4.0 | +10 | Satisfied customers commit |

Compute a `commitment_readiness_score` per account (0-135). Classify:

- **Ready (score >= 70):** Present offer immediately
- **Warming (score 40-69):** Queue for next renewal window
- **Not ready (score < 40):** Do not offer. Focus on value delivery first.

### 2. Create multi-year price objects in Stripe

Using `stripe-pricing-tables`, create annual and multi-year prices for each existing monthly plan. Tag with metadata for experiment tracking:

```bash
# Annual price (2 months free = ~17% discount)
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "unit_amount=49900" \
  -d "currency=usd" \
  -d "recurring[interval]=year" \
  -d "metadata[commitment_type]=annual" \
  -d "metadata[discount_pct]=17" \
  -d "metadata[equivalent_monthly]=4158"

# 2-year price (4 months free = ~17% discount, locked rate)
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "unit_amount=99800" \
  -d "currency=usd" \
  -d "recurring[interval]=year" \
  -d "recurring[interval_count]=2" \
  -d "metadata[commitment_type]=2year" \
  -d "metadata[discount_pct]=17" \
  -d "metadata[rate_lock]=true"
```

Create 3 offer tiers to test:

| Tier | Annual Discount | Multi-Year Discount | Perks |
|------|----------------|-------------------|-------|
| Standard | 2 months free (17%) | 4 months free (17%) + rate lock | None |
| Enhanced | 3 months free (25%) | 6 months free (25%) + rate lock | Priority support upgrade |
| Premium | 3 months free (25%) | 6 months free (25%) + rate lock | Priority support + dedicated CSM session |

### 3. Build the readiness scoring workflow

Using `n8n-workflow-basics`, create a daily n8n workflow:

1. Query PostHog for all active accounts with their readiness signals (Step 1 query)
2. Compute `commitment_readiness_score` per account
3. Classify into readiness tiers
4. Using `attio-custom-attributes`, update each account in Attio with: `commitment_readiness_score`, `commitment_readiness_tier`, `recommended_offer_tier`, `days_to_renewal`
5. Using `attio-deals`, for accounts that moved into "Ready" tier, create a deal in the "Expansion" pipeline at "Offer Queued" stage
6. For accounts with ARR > $5,000, route to the account owner for sales-assisted outreach instead of self-serve
7. Log `commitment_readiness_scored` event in PostHog per account

### 4. Design the offer surfaces

Build 3 delivery channels. Use PostHog feature flags to assign each Ready account to one channel for testing.

**In-app (self-serve):** Using `intercom-in-app-messages`, show a banner or modal when a Ready account's admin visits the billing page or the account settings page:

- Headline: "Lock in your rate — save [X]% with an annual plan"
- Body: Show current monthly cost, annual cost, and savings in dollars (not just percentage)
- CTA: "Switch to annual" → links to Stripe Checkout session with the annual price
- Dismiss behavior: if dismissed, do not show again for 30 days

**Email (automated):** Using `loops-sequences`, send a 3-email sequence to Ready accounts:

- Email 1 (Day 0): "You've been with us [X] months — here's how to save [Y]%"
  - Content: usage summary, savings calculation, one-click upgrade link (Stripe Checkout URL)
- Email 2 (Day 5, if no action): "Quick math: [monthly cost] x 12 = [$X]. Annual plan = [$Y]. You save [$Z]."
  - Content: framing around what they could do with the savings
- Email 3 (Day 12, if no action): "Last chance: this offer expires in [N] days"
  - Content: deadline + link. After this, cool down for 90 days.

**Sales-assisted (high-value):** Using `attio-deals`, create a deal and assign to the account owner with a context brief:

- Account health summary (readiness score, usage trend, feature adoption)
- Recommended offer tier
- Talking points: their specific usage data, what they would save, rate lock protection against price increases
- The AE calls or emails the decision-maker directly

### 5. Build the conversion pipeline

Using `n8n-triggers`, create a webhook workflow that fires when a customer completes a multi-year subscription change in Stripe:

1. Stripe webhook `customer.subscription.updated` fires with `billing_cycle_anchor` change
2. Verify the new price has `metadata[commitment_type]` = annual or 2year
3. Using `attio-deals`, move the deal to "Won" stage. Record: commitment term, discount tier, ARR impact
4. Using `posthog-custom-events`, emit `multiyear_commitment_converted` with properties: `account_id`, `commitment_term`, `discount_pct`, `offer_channel` (in-app, email, sales), `previous_mrr`, `new_arr`, `ltv_increase`
5. Using `loops-sequences`, send a confirmation email with: what changed, their new rate, when it renews, and a thank-you

### 6. Track the full offer funnel

Using `posthog-custom-events`, instrument the complete funnel:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `multiyear_offer_qualified` | Account enters Ready tier | `account_id`, `readiness_score`, `recommended_tier` |
| `multiyear_offer_shown` | Offer rendered in-app or email sent | `account_id`, `channel`, `offer_tier`, `discount_pct` |
| `multiyear_offer_clicked` | User clicked CTA | `account_id`, `channel`, `offer_tier` |
| `multiyear_offer_started` | Checkout session created | `account_id`, `commitment_term`, `offer_tier` |
| `multiyear_offer_converted` | Subscription updated to annual/multi-year | `account_id`, `commitment_term`, `discount_pct`, `arr_impact` |
| `multiyear_offer_dismissed` | User dismissed the offer | `account_id`, `channel`, `dismiss_reason` |

Build a PostHog funnel: `qualified` → `shown` → `clicked` → `started` → `converted`. Track conversion rate at each step and by channel.

## Output

- A daily scoring workflow that identifies commitment-ready accounts
- Multi-year price objects in Stripe with 3 discount tiers
- 3 offer delivery channels (in-app, email, sales-assisted) with full tracking
- Conversion pipeline from offer to signed commitment
- Full funnel instrumentation for optimization

## Triggers

Scoring runs daily via n8n cron. Offer delivery triggers immediately when an account enters the Ready tier. Conversion pipeline fires on Stripe webhook. Re-run scoring calibration monthly.
