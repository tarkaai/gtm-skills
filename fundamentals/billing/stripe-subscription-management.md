---
name: stripe-subscription-management
description: Create, update, and manage Stripe subscriptions including plan changes, trials, and cancellations
tool: Stripe
difficulty: Config
---

# Stripe Subscription Management

CRUD operations on Stripe subscriptions. Covers creating subscriptions, changing plans (upgrades/downgrades), adding metered components, managing trials, and handling cancellations.

## Authentication

Stripe API key (secret key). Set as `STRIPE_SECRET_KEY`. All requests to `https://api.stripe.com/v1/`.

## Create a Subscription

```bash
curl https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_xxx" \
  -d "items[0][price]=price_xxx" \
  -d "payment_behavior=default_incomplete" \
  -d "expand[]=latest_invoice.payment_intent"
```

For usage-based prices, the subscription starts immediately and usage is billed at end of period.

## Change Plan (Upgrade/Downgrade)

```bash
# List subscription items first
curl "https://api.stripe.com/v1/subscription_items?subscription=sub_xxx" \
  -u "$STRIPE_SECRET_KEY:"

# Update the subscription item to a new price
curl https://api.stripe.com/v1/subscriptions/sub_xxx \
  -u "$STRIPE_SECRET_KEY:" \
  -d "items[0][id]=si_xxx" \
  -d "items[0][price]=price_new_xxx" \
  -d "proration_behavior=create_prorations"
```

`proration_behavior` options: `create_prorations` (charge/credit difference immediately), `none` (change takes effect next billing cycle), `always_invoice` (invoice the proration immediately).

## Add a Metered Component to Existing Subscription

```bash
curl https://api.stripe.com/v1/subscription_items \
  -u "$STRIPE_SECRET_KEY:" \
  -d "subscription=sub_xxx" \
  -d "price=price_metered_xxx"
```

This adds a usage-based line item alongside flat-rate items.

## Cancel a Subscription

```bash
# Cancel at period end (recommended — lets user keep access until paid period ends)
curl https://api.stripe.com/v1/subscriptions/sub_xxx \
  -u "$STRIPE_SECRET_KEY:" \
  -d "cancel_at_period_end=true"

# Cancel immediately
curl -X DELETE "https://api.stripe.com/v1/subscriptions/sub_xxx" \
  -u "$STRIPE_SECRET_KEY:"
```

## Retrieve Subscription Details

```bash
curl "https://api.stripe.com/v1/subscriptions/sub_xxx?expand[]=customer&expand[]=items.data.price" \
  -u "$STRIPE_SECRET_KEY:"
```

Key fields: `status` (active, past_due, canceled, trialing, unpaid), `current_period_end`, `items.data[].price`, `cancel_at_period_end`.

## List All Subscriptions for a Customer

```bash
curl "https://api.stripe.com/v1/subscriptions?customer=cus_xxx&status=active" \
  -u "$STRIPE_SECRET_KEY:"
```

## Apply a Coupon/Discount

```bash
curl https://api.stripe.com/v1/subscriptions/sub_xxx \
  -u "$STRIPE_SECRET_KEY:" \
  -d "coupon=retention_offer_20pct"
```

Useful for retention interventions — apply a discount to an at-risk subscription.

## Error Handling

- `402 card_error`: Payment method failed. Subscription enters `past_due`.
- `404 resource_missing`: Subscription or price does not exist.
- Webhook events to listen for: `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`.

## Tool Options

| Tool | API | Notes |
|------|-----|-------|
| Stripe | Subscriptions API | Most widely used |
| Chargebee | Subscriptions API | Better dunning management |
| Recurly | Subscriptions API | Strong revenue recovery |
| Paddle | Subscriptions API | Handles tax/compliance |
| Braintree | Subscriptions API | PayPal-integrated |
