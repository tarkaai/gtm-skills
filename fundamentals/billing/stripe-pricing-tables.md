---
name: stripe-pricing-tables
description: Create and manage Stripe pricing tables and checkout sessions for plan selection
tool: Stripe
product: Stripe
difficulty: Setup
---

# Stripe Pricing Tables

Create pricing tables and checkout sessions that let customers self-serve plan selection, upgrades, and downgrades. Covers both the embeddable Pricing Table component and the Checkout Session API for programmatic control.

## Authentication

Stripe API key (publishable key for frontend, secret key for backend). Frontend embeds use `STRIPE_PUBLISHABLE_KEY`. Backend API calls use `STRIPE_SECRET_KEY`.

## Create a Product and Prices

Before building pricing tables, define products and prices:

```bash
# Create a product
curl https://api.stripe.com/v1/products \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Pro Plan" \
  -d "description=Unlimited projects, priority support"

# Create a flat-rate price
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "unit_amount=4900" \
  -d "currency=usd" \
  -d "recurring[interval]=month"

# Create a tiered usage-based price
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "currency=usd" \
  -d "recurring[interval]=month" \
  -d "recurring[usage_type]=metered" \
  -d "billing_scheme=tiered" \
  -d "tiers_mode=graduated" \
  -d "tiers[0][up_to]=1000" \
  -d "tiers[0][unit_amount]=10" \
  -d "tiers[1][up_to]=10000" \
  -d "tiers[1][unit_amount]=8" \
  -d "tiers[2][up_to]=inf" \
  -d "tiers[2][unit_amount]=5" \
  -d "meter=mtr_xxx"
```

## Create a Checkout Session (Programmatic)

```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=subscription" \
  -d "customer=cus_xxx" \
  -d "line_items[0][price]=price_xxx" \
  -d "line_items[0][quantity]=1" \
  -d "success_url=https://app.example.com/billing?session_id={CHECKOUT_SESSION_ID}" \
  -d "cancel_url=https://app.example.com/pricing"
```

Returns a `url` field — redirect the customer there. On success, the subscription is created automatically.

## Create a Customer Portal Session

Let customers manage their own subscriptions (upgrade, downgrade, cancel):

```bash
curl https://api.stripe.com/v1/billing_portal/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_xxx" \
  -d "return_url=https://app.example.com/settings"
```

Configure allowed portal actions in Stripe Dashboard > Settings > Billing > Customer portal: enable plan switching, cancellation, payment method updates.

## Retrieve Current Pricing

```bash
# List all active prices for a product
curl "https://api.stripe.com/v1/prices?product=prod_xxx&active=true&expand[]=data.tiers" \
  -u "$STRIPE_SECRET_KEY:"
```

## Error Handling

- `400 invalid_request_error`: Check price exists and is active
- `402 card_error`: Payment method problem during checkout
- Webhook: listen for `checkout.session.completed` to confirm subscription creation

## Tool Options

| Tool | Approach | Notes |
|------|----------|-------|
| Stripe | Pricing Table embed + Checkout API | Most flexible |
| Chargebee | Hosted checkout pages | Built-in plan comparison |
| Paddle | Overlay checkout | Handles tax automatically |
| LemonSqueezy | Hosted checkout | Simpler setup, fewer options |
| Recurly | Hosted pages + API | Strong enterprise support |
