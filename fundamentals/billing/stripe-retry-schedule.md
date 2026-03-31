---
name: stripe-retry-schedule
description: Query and configure Stripe's automatic payment retry schedule and smart retries
tool: Stripe
product: Stripe
difficulty: Config
---

# Stripe Payment Retry Schedule

## Prerequisites

- Stripe account with billing/subscriptions enabled
- API access with secret key

## Query Current Retry Settings

Retrieve the current retry configuration via the Stripe Billing settings API:

```bash
curl https://api.stripe.com/v1/billing_portal/configurations \
  -u sk_live_YOUR_KEY:
```

Or check subscription-specific retry behavior:

```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXXXX \
  -u sk_live_YOUR_KEY:
```

The `latest_invoice` object contains `next_payment_attempt` (timestamp of next retry) and `attempt_count` (number of attempts so far).

## Configure Smart Retries

Stripe Smart Retries use ML to pick the optimal retry time. Enable via Dashboard or API:

```bash
# Enable Smart Retries (via Stripe Dashboard API settings)
# Dashboard > Settings > Billing > Subscriptions and emails > Manage failed payments
# Toggle "Use Smart Retries" ON
```

Smart Retries analyzes:
- Time of day when the card is most likely to succeed
- Day of month (post-payday patterns)
- Historical success patterns for the card network
- Failure code classification (permanent vs. transient)

## Configure Retry Schedule (if not using Smart Retries)

Set a custom retry schedule via the Stripe Dashboard or automate via the API:

Default schedule: retry at 1 day, 3 days, 5 days, 7 days after initial failure.

To override, use the Stripe Billing settings:
```bash
# Configure via Stripe Billing portal
# Dashboard > Settings > Billing > Subscriptions and emails
# Set: "Retry up to X times over Y days"
```

## Query Retry Status for a Specific Invoice

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX \
  -u sk_live_YOUR_KEY:
```

Key fields:
- `status`: `open` (payment pending), `paid`, `uncollectible`, `void`
- `attempt_count`: number of payment attempts so far
- `next_payment_attempt`: Unix timestamp of next scheduled retry (null if no more retries)
- `auto_advance`: whether Stripe will auto-advance to next retry

## Mark Invoice Uncollectible (after exhausting retries)

```bash
curl https://api.stripe.com/v1/invoices/in_XXXXX/mark_uncollectible \
  -u sk_live_YOUR_KEY: \
  -X POST
```

Use this when all retries AND manual recovery attempts have failed. This voids the invoice and can trigger subscription cancellation.

## Error Handling

- If Smart Retries are off and you set too-aggressive retries (hourly), Stripe may rate-limit
- Monitor retry success rate: query `GET /v1/invoices?status=open&created[gte]=TIMESTAMP` weekly
- If retry success rate drops below 30%, review whether the retry cadence aligns with customer payment cycles

## Alternative Tools

| Tool | Retry Mechanism | Documentation |
|------|----------------|---------------|
| Stripe | Smart Retries (ML-based) | [stripe.com/docs/billing/revenue-recovery](https://stripe.com/docs/billing/revenue-recovery) |
| Paddle | Automatic retry with configurable schedule | [developer.paddle.com](https://developer.paddle.com) |
| Chargebee | Smart Dunning with configurable retries | [chargebee.com/docs](https://www.chargebee.com/docs) |
| Recurly | Revenue Optimization Engine | [docs.recurly.com](https://docs.recurly.com) |
| Braintree | Configurable retry logic | [developer.paypal.com/braintree](https://developer.paypal.com/braintree/docs) |
