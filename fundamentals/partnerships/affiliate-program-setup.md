---
name: affiliate-program-setup
description: Create and configure an affiliate or reseller tracking program in your chosen platform
tool: Rewardful
product: Rewardful
difficulty: Setup
---

# Affiliate Program Setup

## Prerequisites

- Stripe or Paddle account connected for payment tracking
- Product with a self-serve signup or checkout flow
- Admin access to your chosen affiliate platform

## Tool Options

| Tool | Best For | Pricing |
|------|----------|---------|
| Rewardful | Stripe-native SaaS affiliate tracking | Starter $49/mo up to $7,500 affiliate revenue ([rewardful.com/pricing](https://www.rewardful.com/pricing)) |
| FirstPromoter | SaaS with tiered commission needs | Starter $49/mo up to $5,000 affiliate revenue ([firstpromoter.com/pricing](https://firstpromoter.com/pricing)) |
| PartnerStack | Enterprise partner ecosystem management | Custom pricing, no free tier ([partnerstack.com/pricing](https://partnerstack.com/pricing)) |
| Tapfiliate | Multi-channel affiliate programs | Essential $89/mo ([tapfiliate.com/pricing](https://tapfiliate.com/pricing)) |
| Reflio | Open-source, self-hosted option | Free self-hosted; cloud from $0 ([reflio.com](https://reflio.com)) |

## Steps

### Rewardful (Default for Stripe-based SaaS)

1. **Create a Rewardful account and connect Stripe.**

   ```
   # After signup at rewardful.com, connect Stripe via OAuth
   # Rewardful uses Stripe Connect to track all referred payments automatically
   ```

2. **Create a campaign.** A campaign defines the commission structure for a group of affiliates.

   ```
   POST https://api.rewardful.com/v1/campaigns
   Authorization: Bearer {REWARDFUL_API_KEY}
   Content-Type: application/json

   {
     "name": "Reseller Program",
     "commission_type": "percentage",
     "commission_amount": 20,
     "cookie_duration": 90,
     "minimum_payout_amount": 50,
     "recurring": true,
     "recurring_duration_months": 12,
     "currency": "USD"
   }
   ```

   Response includes `campaign_id` — store this for affiliate creation.

3. **Install the tracking snippet.** Add the Rewardful JavaScript to your marketing site and signup flow:

   ```html
   <script>(function(w,r){w._rwq=r;w[r]=w[r]||function(){(w[r].q=w[r].q||[]).push(arguments)}})(window,'rewardful');</script>
   <script async src='https://r.wdfl.co/rw.js' data-rewardful='{REWARDFUL_CAMPAIGN_ID}'></script>
   ```

   This captures the `?via=` parameter from affiliate links and attributes signups to the referring affiliate.

4. **Configure the affiliate portal.** Rewardful provides a hosted portal where affiliates can see their stats, grab links, and request payouts. Customize it with your branding:

   ```
   PUT https://api.rewardful.com/v1/campaigns/{campaign_id}
   {
     "portal_title": "Partner Program",
     "portal_description": "Track your referrals and commissions",
     "portal_logo_url": "https://yourdomain.com/logo.png"
   }
   ```

### FirstPromoter (Alternative)

1. **Create account and connect Stripe.**

   ```
   # Connect via FirstPromoter dashboard → Integrations → Stripe
   # Or use the API:
   POST https://firstpromoter.com/api/v1/integrations/stripe
   Authorization: Bearer {FIRSTPROMOTER_API_KEY}
   ```

2. **Create a campaign.**

   ```
   POST https://firstpromoter.com/api/v1/campaigns
   Authorization: Bearer {FIRSTPROMOTER_API_KEY}
   Content-Type: application/json

   {
     "name": "Reseller Program",
     "commission_type": "percentage",
     "default_commission": 20,
     "cookie_duration": 90,
     "recurring_commissions": true
   }
   ```

3. **Install tracking script.**

   ```html
   <script src="https://cdn.firstpromoter.com/fprom.js"></script>
   <script>
     $FPROM.init("{FIRSTPROMOTER_CAMPAIGN_ID}", ".yourdomain.com");
   </script>
   ```

## Error Handling

- If Stripe connection fails: verify webhook endpoint is reachable and API key has read access to Subscriptions and Charges
- If tracking script not firing: check browser console for CORS errors; ensure the script loads before the signup form
- If referrals not attributing: verify the `?via=` or `?ref=` parameter is present in the URL and the cookie is being set (check Application → Cookies in browser dev tools)

## Output

- A configured affiliate program with tracking installed
- Hosted affiliate portal for partners to self-serve
- Stripe webhook integration for automatic commission calculation
