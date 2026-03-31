---
name: billing-event-streaming
description: Stream billing events (subscriptions, invoices, usage) from Stripe to PostHog for analytics
tool: Stripe
product: Stripe
difficulty: Config
---

# Billing Event Streaming

Pipe billing events from your payment processor into PostHog so you can correlate revenue data with product behavior. This enables analysis like "users who hit usage tier X churn at Y% within 30 days" or "ARPU by activation cohort."

## Architecture

Stripe emits webhook events. An n8n workflow receives them and forwards them to PostHog as custom events with billing properties attached to the user.

## Step 1: Configure Stripe Webhook

```bash
curl https://api.stripe.com/v1/webhook_endpoints \
  -u "$STRIPE_SECRET_KEY:" \
  -d "url=https://your-n8n.example.com/webhook/stripe-billing" \
  -d "enabled_events[]=customer.subscription.created" \
  -d "enabled_events[]=customer.subscription.updated" \
  -d "enabled_events[]=customer.subscription.deleted" \
  -d "enabled_events[]=invoice.paid" \
  -d "enabled_events[]=invoice.payment_failed" \
  -d "enabled_events[]=customer.subscription.trial_will_end" \
  -d "enabled_events[]=billing.meter.usage_reported"
```

Store the `webhook_secret` (starts with `whsec_`) for signature verification.

## Step 2: n8n Webhook Receiver

Build an n8n workflow:

1. **Trigger:** Webhook node listening on `/webhook/stripe-billing`
2. **Verify signature:** Function node that verifies `stripe-signature` header against `whsec_` secret
3. **Extract data:** Map Stripe event fields to PostHog properties:
   - `event.type` -> `billing_event_type`
   - `event.data.object.customer` -> use to look up PostHog `distinct_id`
   - `event.data.object.plan.amount` / 100 -> `plan_amount_usd`
   - `event.data.object.plan.interval` -> `billing_interval`
   - `event.data.object.status` -> `subscription_status`
4. **Send to PostHog:** HTTP Request node

## Step 3: PostHog Capture

Send billing events to PostHog via the Capture API:

```bash
curl -X POST "https://us.i.posthog.com/capture/" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "phc_xxx",
    "distinct_id": "user_xxx",
    "event": "billing_subscription_updated",
    "properties": {
      "plan_name": "pro",
      "plan_amount_usd": 49,
      "billing_interval": "month",
      "subscription_status": "active",
      "mrr_change": 49,
      "previous_plan": "free",
      "change_type": "upgrade"
    }
  }'
```

Key events to track:

| Stripe Event | PostHog Event | Key Properties |
|-------------|---------------|----------------|
| `customer.subscription.created` | `billing_subscription_created` | plan_name, plan_amount_usd, trial_end |
| `customer.subscription.updated` | `billing_subscription_updated` | change_type (upgrade/downgrade), mrr_change |
| `customer.subscription.deleted` | `billing_subscription_canceled` | cancel_reason, mrr_lost |
| `invoice.paid` | `billing_invoice_paid` | amount_usd, period_start, period_end |
| `invoice.payment_failed` | `billing_payment_failed` | failure_reason, attempt_count |

## Step 4: Set Person Properties

In addition to events, update PostHog person properties so you can segment:

```bash
curl -X POST "https://us.i.posthog.com/capture/" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "phc_xxx",
    "distinct_id": "user_xxx",
    "event": "$set",
    "properties": {
      "$set": {
        "current_plan": "pro",
        "mrr": 49,
        "billing_interval": "month",
        "subscription_status": "active",
        "plan_start_date": "2026-03-01"
      }
    }
  }'
```

## Error Handling

- If PostHog capture fails, queue the event in n8n and retry (do not lose billing data)
- If Stripe webhook delivery fails 3 times, Stripe disables the endpoint — monitor via `GET /v1/webhook_endpoints`
- Validate `distinct_id` mapping: if a Stripe customer cannot be matched to a PostHog user, log it for manual resolution

## Tool Options

| Source | Destination | Bridge |
|--------|-------------|--------|
| Stripe | PostHog | n8n webhook workflow |
| Chargebee | PostHog | Chargebee webhooks + n8n |
| Paddle | PostHog | Paddle Notifications + n8n |
| Recurly | PostHog | Recurly webhooks + n8n |
| Any | PostHog | Segment (if already using) |
