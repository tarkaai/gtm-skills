---
name: affiliate-commission-configuration
description: Configure commission structures, tiers, and payout rules for an affiliate or reseller program
tool: Rewardful / FirstPromoter / PartnerStack / Tapfiliate
difficulty: Config
---

# Affiliate Commission Configuration

## Prerequisites

- Affiliate program created (see `affiliate-program-setup`)
- Stripe or Paddle connected with active subscription products
- Clear understanding of your unit economics (LTV, CAC, margin)

## Steps

### 1. Define the commission structure

Choose a commission model based on your economics. The commission must be attractive enough to motivate partners while keeping your CAC below target.

**Percentage of revenue (most common for SaaS):**

```
PUT https://api.rewardful.com/v1/campaigns/{campaign_id}
Authorization: Bearer {REWARDFUL_API_KEY}
Content-Type: application/json

{
  "commission_type": "percentage",
  "commission_amount": 20,
  "recurring": true,
  "recurring_duration_months": 12
}
```

**Flat fee per conversion:**

```
PUT https://api.rewardful.com/v1/campaigns/{campaign_id}
{
  "commission_type": "flat",
  "commission_amount": 50,
  "recurring": false
}
```

**Tiered commissions (FirstPromoter):**

```
POST https://firstpromoter.com/api/v1/campaigns/{campaign_id}/tiers
Authorization: Bearer {FIRSTPROMOTER_API_KEY}

{
  "tiers": [
    { "min_referrals": 0, "max_referrals": 10, "commission_percentage": 15 },
    { "min_referrals": 11, "max_referrals": 50, "commission_percentage": 20 },
    { "min_referrals": 51, "max_referrals": null, "commission_percentage": 25 }
  ]
}
```

### 2. Configure payout rules

```
PUT https://api.rewardful.com/v1/campaigns/{campaign_id}
{
  "minimum_payout_amount": 50,
  "payout_frequency": "monthly",
  "payout_delay_days": 30,
  "payout_method": "paypal"
}
```

Key payout parameters:
- **Minimum payout**: $50 minimum prevents micro-payouts (typical range: $25-100)
- **Payout delay**: 30-day delay protects against refunds and chargebacks
- **Frequency**: Monthly payouts are standard; weekly for high-volume resellers

### 3. Configure cookie and attribution settings

```
PUT https://api.rewardful.com/v1/campaigns/{campaign_id}
{
  "cookie_duration": 90,
  "attribution_model": "first_click",
  "double_reward_protection": true
}
```

- **Cookie duration**: 90 days is standard for B2B SaaS (longer sales cycles)
- **Attribution model**: First-click (original referrer gets credit) or last-click
- **Double reward protection**: Prevents the same customer from generating commission for multiple affiliates

### 4. Set up product-specific commissions (optional)

If you have multiple products or tiers with different margins:

```
POST https://api.rewardful.com/v1/campaigns/{campaign_id}/product_commissions
{
  "product_commissions": [
    { "stripe_product_id": "prod_starter", "commission_amount": 15 },
    { "stripe_product_id": "prod_growth", "commission_amount": 20 },
    { "stripe_product_id": "prod_enterprise", "commission_amount": 25 }
  ]
}
```

## Error Handling

- If commissions not calculating: verify Stripe webhook is delivering `invoice.paid` events to your affiliate platform
- If tiered commissions not upgrading: check that the referral count threshold uses cumulative (all-time) not monthly count
- If payouts failing: verify affiliate has a valid PayPal email or bank account connected

## Output

- Configured commission structure aligned to unit economics
- Payout rules with fraud protection (delay, minimum, double-reward prevention)
- Product-specific commission overrides if needed
