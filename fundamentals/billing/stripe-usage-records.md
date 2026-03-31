---
name: stripe-usage-records
description: Report metered usage to Stripe Billing via the Meter Events API for usage-based pricing
tool: Stripe
difficulty: Config
---

# Stripe Usage Records

Report customer product usage to Stripe so it can be aggregated into billable charges. This fundamental covers the Meter Events API (the current approach) rather than the legacy Usage Records API.

## Authentication

Stripe API key (secret key) with `billing:write` scope. Set as environment variable `STRIPE_SECRET_KEY`. All requests go to `https://api.stripe.com/v1/`.

## Prerequisites

- A Stripe Meter object created via Dashboard or API (defines how events aggregate: sum, count, max, etc.)
- A Price object linked to the Meter (recurring price with `meter` parameter)
- A Subscription containing that Price, assigned to the customer

## Create a Meter

```bash
curl https://api.stripe.com/v1/billing/meters \
  -u "$STRIPE_SECRET_KEY:" \
  -d "display_name=API Requests" \
  -d "event_name=api_request" \
  -d "default_aggregation[formula]=sum" \
  -d "value_settings[event_payload_key]=request_count"
```

Response includes `id` (e.g., `mtr_xxx`). Store this — you need it to create prices.

## Report a Meter Event

```bash
curl https://api.stripe.com/v1/billing/meter_events \
  -u "$STRIPE_SECRET_KEY:" \
  -d "event_name=api_request" \
  -d "payload[stripe_customer_id]=cus_xxx" \
  -d "payload[request_count]=150" \
  -d "timestamp=$(date +%s)"
```

- `event_name` must match the meter's `event_name`
- `payload[stripe_customer_id]` is required — identifies the customer
- `payload[{value_key}]` must match `value_settings.event_payload_key` on the meter
- `timestamp` is optional (defaults to now); use it for backfilling

## Batch Reporting via n8n

For high-volume reporting, build an n8n workflow:

1. Trigger: cron every 1 hour (or webhook from your app)
2. HTTP Request node: query your product database for usage since last report
3. Loop node: for each customer, POST to `/v1/billing/meter_events`
4. Error handling: retry on 429 (rate limit) with exponential backoff

Rate limit: 1,000 meter events per second per meter. Batch if needed.

## Query Usage Summary

```bash
curl "https://api.stripe.com/v1/billing/meters/mtr_xxx/event_summaries?customer=cus_xxx&start_time=1709251200&end_time=1711929600&value_grouping_window=day" \
  -u "$STRIPE_SECRET_KEY:"
```

Returns daily aggregated usage per customer. Use this to build usage dashboards or validate billing accuracy.

## Error Handling

- `400 invalid_request_error`: Check `event_name` matches a meter, `stripe_customer_id` is valid
- `404 resource_missing`: Meter does not exist
- `429 rate_limit_error`: Back off and retry. Queue events if sustained.
- Events with future timestamps are rejected. Events older than 35 days are rejected.

## Tool Options

| Tool | API | Notes |
|------|-----|-------|
| Stripe | Meter Events API | Native, recommended |
| Chargebee | Metered Billing API | `POST /api/v2/subscriptions/{id}/usages` |
| Recurly | Measured Units API | `POST /v2/subscriptions/{uuid}/add_ons/{code}/usage` |
| Paddle | Usage API | `POST /transactions` with metered items |
| Orb | Events API | Purpose-built for usage-based; `POST /v1/ingest` |
| Metronome | Events API | Real-time metering; `POST /v1/ingest` |
| OpenMeter | CloudEvents-based | Open-source; `POST /api/v1/events` |
