---
name: stripe-payment-failure-webhook
description: Configure Stripe webhooks to receive real-time payment failure events and extract failure metadata
tool: Stripe
product: Stripe
difficulty: Setup
---

# Stripe Payment Failure Webhook

## Prerequisites

- Stripe account with API access (secret key and webhook signing secret)
- An HTTP endpoint to receive webhooks (n8n, custom server, or serverless function)

## Webhook Configuration

### 1. Create the webhook endpoint in Stripe

Via Stripe API:

```bash
curl https://api.stripe.com/v1/webhook_endpoints \
  -u sk_live_YOUR_KEY: \
  -d url="https://your-n8n-instance.com/webhook/stripe-payment-failures" \
  -d "enabled_events[]"="invoice.payment_failed" \
  -d "enabled_events[]"="charge.failed" \
  -d "enabled_events[]"="customer.subscription.updated" \
  -d "enabled_events[]"="payment_intent.payment_failed"
```

Store the returned `webhook_signing_secret` (whsec_...) for signature verification.

### 2. Verify webhook signatures

Every incoming webhook must be verified to prevent spoofing. Use the Stripe SDK:

```javascript
const event = stripe.webhooks.constructEvent(
  request.body,        // raw body (string or Buffer)
  request.headers['stripe-signature'],
  process.env.STRIPE_WEBHOOK_SECRET
);
```

If verification fails, return 400 and log the attempt. Never process unverified webhooks.

### 3. Extract failure metadata from the event payload

For `invoice.payment_failed` events, extract:

```json
{
  "customer_id": "event.data.object.customer",
  "subscription_id": "event.data.object.subscription",
  "invoice_id": "event.data.object.id",
  "amount_due": "event.data.object.amount_due",
  "currency": "event.data.object.currency",
  "attempt_count": "event.data.object.attempt_count",
  "next_payment_attempt": "event.data.object.next_payment_attempt",
  "failure_code": "event.data.object.last_payment_error.code",
  "failure_message": "event.data.object.last_payment_error.message",
  "payment_method_type": "event.data.object.last_payment_error.payment_method.type",
  "payment_method_last4": "event.data.object.last_payment_error.payment_method.card.last4",
  "billing_reason": "event.data.object.billing_reason"
}
```

Key failure codes to classify:
- `card_declined` — generic decline, could be insufficient funds, fraud block, etc.
- `expired_card` — card has passed its expiration date
- `insufficient_funds` — not enough balance
- `authentication_required` — needs 3D Secure / SCA
- `processing_error` — temporary processor issue, likely to succeed on retry

### 4. Respond correctly

Return HTTP 200 within 5 seconds to acknowledge receipt. Process the event asynchronously. If you return a non-2xx status, Stripe retries with exponential backoff for up to 72 hours.

## Error Handling

- If the webhook endpoint is down, Stripe queues events for up to 72 hours
- Monitor webhook delivery health in Stripe Dashboard > Developers > Webhooks
- Set up a Stripe webhook health check: query the Stripe API for pending webhooks weekly
- If failure rate exceeds 5%, check endpoint availability and response times

## Alternative Tools

| Tool | Webhook Event | Documentation |
|------|--------------|---------------|
| Stripe | `invoice.payment_failed` | [stripe.com/docs/api/events](https://stripe.com/docs/api/events) |
| Paddle | `subscription.payment_failed` | [developer.paddle.com/webhooks](https://developer.paddle.com/webhooks) |
| Chargebee | `payment_failed` | [apidocs.chargebee.com](https://apidocs.chargebee.com) |
| Recurly | `failed_payment` | [recurly.com/developers](https://recurly.com/developers) |
| Braintree | `subscription_went_past_due` | [developer.paypal.com/braintree](https://developer.paypal.com/braintree/docs) |
