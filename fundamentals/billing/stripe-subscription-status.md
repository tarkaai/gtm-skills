---
name: stripe-subscription-status
description: Query subscription status, past-due state, and cancellation schedule from Stripe API
tool: Stripe
difficulty: Setup
---

# Stripe Subscription Status

## Prerequisites

- Stripe account with API access (secret key)
- Active subscriptions to query

## Query a Single Subscription

```bash
curl https://api.stripe.com/v1/subscriptions/sub_XXXXX \
  -u sk_live_YOUR_KEY:
```

Key fields for payment failure recovery:
- `status`: `active`, `past_due`, `unpaid`, `canceled`, `incomplete`, `incomplete_expired`, `trialing`, `paused`
- `latest_invoice`: the most recent invoice object (expand for payment details)
- `cancel_at_period_end`: boolean, whether auto-cancel is scheduled
- `cancel_at`: timestamp when the subscription will cancel (if scheduled)
- `days_until_due`: number of days to pay after invoice creation
- `default_payment_method`: the payment method on file

## List All Past-Due Subscriptions

```bash
curl "https://api.stripe.com/v1/subscriptions?status=past_due&limit=100" \
  -u sk_live_YOUR_KEY:
```

This returns all subscriptions where the most recent invoice payment failed and Stripe is still retrying. These are your active recovery targets.

## Expand Invoice and Payment Details

To get full failure context in a single API call:

```bash
curl "https://api.stripe.com/v1/subscriptions/sub_XXXXX?expand[]=latest_invoice.payment_intent&expand[]=default_payment_method" \
  -u sk_live_YOUR_KEY:
```

This returns the subscription with its latest invoice, the payment intent (including failure reason), and the payment method details (card brand, last 4, expiry).

## Subscription Lifecycle for Payment Failures

1. Invoice created -> payment attempted -> `charge.failed` event
2. Subscription moves to `past_due` status
3. Stripe retries per retry schedule (Smart Retries or custom)
4. If all retries fail:
   - If configured: subscription moves to `unpaid` (access revoked, can be reactivated)
   - If configured: subscription moves to `canceled` (permanent)
   - Default: stays `past_due` until manual intervention

## Batch Query: Subscriptions At Risk

Query all subscriptions that are past due or have upcoming payment that is likely to fail (card expiring soon):

```javascript
// Past-due subscriptions (payment already failed)
const pastDue = await stripe.subscriptions.list({
  status: 'past_due',
  limit: 100,
  expand: ['data.latest_invoice', 'data.default_payment_method']
});

// Subscriptions with expiring cards (proactive prevention)
const expiringSoon = await stripe.paymentMethods.list({
  type: 'card',
  limit: 100
});
const atRisk = expiringSoon.data.filter(pm => {
  const expiryDate = new Date(pm.card.exp_year, pm.card.exp_month - 1);
  const daysUntilExpiry = (expiryDate - new Date()) / (1000 * 60 * 60 * 24);
  return daysUntilExpiry > 0 && daysUntilExpiry <= 30;
});
```

## Error Handling

- `resource_missing`: subscription does not exist (may have been deleted)
- `rate_limit`: Stripe allows 100 reads/sec in live mode; use pagination for large lists
- Expand requests count against rate limits more heavily; batch queries should paginate at 100/page

## Alternative Tools

| Tool | Status Query | Documentation |
|------|-------------|---------------|
| Stripe | `GET /v1/subscriptions` | [stripe.com/docs/api/subscriptions](https://stripe.com/docs/api/subscriptions) |
| Paddle | `GET /subscriptions` | [developer.paddle.com](https://developer.paddle.com) |
| Chargebee | `GET /subscriptions` | [apidocs.chargebee.com](https://apidocs.chargebee.com) |
| Recurly | `GET /subscriptions` | [docs.recurly.com](https://docs.recurly.com) |
| Braintree | Subscription search API | [developer.paypal.com/braintree](https://developer.paypal.com/braintree/docs) |
