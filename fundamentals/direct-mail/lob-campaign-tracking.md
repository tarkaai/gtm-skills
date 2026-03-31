---
name: lob-campaign-tracking
description: Track postcard delivery status and scan events via the Lob API
tool: Lob
product: Lob
difficulty: Config
---

# Lob Campaign Tracking

After sending postcards, track their delivery status through the Lob API. Lob provides USPS Intelligent Mail barcode tracking for letter-class mail, including postcards. Use this data to know when mail was delivered and correlate with inbound responses.

## Retrieve a Single Postcard

```bash
curl https://api.lob.com/v1/postcards/psc_abc123 \
  -u "$LOB_API_KEY:"
```

### Response (tracking fields)

```json
{
  "id": "psc_abc123",
  "tracking_events": [
    {
      "id": "evnt_xyz",
      "type": "certified",
      "name": "In Transit",
      "time": "2026-04-02T14:30:00.000Z"
    },
    {
      "id": "evnt_abc",
      "type": "certified",
      "name": "Processed for Delivery",
      "time": "2026-04-04T08:15:00.000Z"
    }
  ],
  "expected_delivery_date": "2026-04-05",
  "send_date": "2026-04-01"
}
```

## Tracking Event Types

- `In Local Area` — Mail is in the destination postal area
- `In Transit` — Mail is moving through USPS network
- `Processed for Delivery` — Mail is at the destination post office, out for delivery soon
- `Re-Routed` — Mail was redirected (address forwarding)
- `Returned to Sender` — Undeliverable, returned

## List All Postcards (with filtering)

```bash
curl "https://api.lob.com/v1/postcards?limit=50&date_created=%7B%22gte%22%3A%222026-03-01%22%7D" \
  -u "$LOB_API_KEY:"
```

Filter parameters:
- `limit` — Number of results (max 100)
- `offset` — Pagination offset
- `date_created` — Filter by creation date range (use `gte`, `lte`)
- `metadata[campaign_id]` — Filter by custom metadata (if set at send time)

## Webhook Events

Configure webhooks in the Lob dashboard to receive real-time delivery updates:

Dashboard URL: https://dashboard.lob.com/webhooks

Events you can subscribe to:
- `postcard.created` — Postcard entered the print queue
- `postcard.rendered_pdf` — PDF rendered, ready for printing
- `postcard.rendered_thumbnails` — Thumbnails generated
- `postcard.deleted` — Postcard canceled before printing
- `postcard.delivered` — Postcard marked as delivered by USPS
- `postcard.in_transit` — Postcard is in transit
- `postcard.in_local_area` — Postcard arrived in destination area
- `postcard.re-routed` — Postcard was rerouted
- `postcard.returned_to_sender` — Postcard returned to sender

### Webhook Payload

```json
{
  "id": "evt_abc123",
  "event_type": {
    "id": "postcard.delivered",
    "enabled_for_test": true
  },
  "body": {
    "id": "psc_abc123",
    "tracking_events": [ ... ]
  },
  "date_created": "2026-04-05T09:00:00.000Z"
}
```

## Integration with n8n

Set up an n8n webhook node to receive Lob delivery events. When a `postcard.delivered` event fires:
1. Parse the postcard ID from the webhook payload
2. Look up the contact in Attio by the stored postcard ID
3. Update the contact's `direct_mail_status` field to "delivered"
4. Update `direct_mail_delivered_date` to the event timestamp
5. Start a 3-7 day timer — if no response by then, the postcard likely did not convert

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Process tracking data |
| 401 | Invalid API key | Check credentials |
| 404 | Postcard not found | Check the postcard ID |

## Pricing

- Tracking is included with every postcard send at no additional cost
- Webhooks are free to configure

## Notes

- USPS tracking for postcards is less granular than package tracking — you may only get 2-3 events total
- `expected_delivery_date` is an estimate; actual delivery can vary by 1-2 days
- Use the delivery date to set follow-up timers in your CRM — trigger a digital follow-up (email/LinkedIn) 3-5 days after confirmed delivery
- Attach `metadata` to postcards at send time (e.g., `metadata[campaign_id]=dm-q2-2026`) to make filtering and reporting easier
