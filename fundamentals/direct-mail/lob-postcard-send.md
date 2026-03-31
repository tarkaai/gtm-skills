---
name: lob-postcard-send
description: Send a physical postcard to a recipient via the Lob Print & Mail API
tool: Lob
product: Lob
difficulty: Setup
---

# Lob Postcard Send

Send a physical postcard to a single recipient using the Lob REST API. Lob handles printing, addressing, and USPS mailing. Postcards arrive in 3-7 business days (standard) or 2-3 days (express).

## Authentication

- Obtain your API key from the Lob dashboard at https://dashboard.lob.com
- Test keys start with `test_` (no mail is sent, but you get realistic responses)
- Live keys start with `live_` (real mail is printed and sent)
- Use HTTP Basic Auth: API key as username, empty password

## API Endpoint

```
POST https://api.lob.com/v1/postcards
```

## Request Format

```bash
curl https://api.lob.com/v1/postcards \
  -u "$LOB_API_KEY:" \
  -d "description=Postcard to {{company_name}}" \
  -d "to[name]={{recipient_name}}" \
  -d "to[address_line1]={{address_line1}}" \
  -d "to[address_line2]={{address_line2}}" \
  -d "to[address_city]={{city}}" \
  -d "to[address_state]={{state}}" \
  -d "to[address_zip]={{zip}}" \
  -d "to[address_country]=US" \
  -d "from[name]={{sender_name}}" \
  -d "from[address_line1]={{sender_address}}" \
  -d "from[address_city]={{sender_city}}" \
  -d "from[address_state]={{sender_state}}" \
  -d "from[address_zip]={{sender_zip}}" \
  -d "from[address_country]=US" \
  -d "front=tmpl_{{front_template_id}}" \
  -d "back=tmpl_{{back_template_id}}" \
  -d "size=4x6" \
  -d "merge_variables[first_name]={{first_name}}" \
  -d "merge_variables[company]={{company_name}}" \
  -d "merge_variables[pain_point]={{pain_point}}"
```

Alternatively, pass inline HTML instead of template IDs:

```bash
  -d "front=<html><body><h1>Hello {{first_name}}</h1></body></html>" \
  -d "back=<html><body><p>Your message here</p></body></html>"
```

## Postcard Sizes

- `4x6` — Standard postcard (default, cheapest)
- `6x9` — Jumbo postcard
- `6x11` — Extra-large postcard

## Response

```json
{
  "id": "psc_abc123",
  "description": "Postcard to Acme Corp",
  "to": { "name": "Jane Smith", ... },
  "from": { "name": "Your Company", ... },
  "url": "https://lob-assets.com/postcards/psc_abc123.pdf",
  "expected_delivery_date": "2026-04-08",
  "send_date": "2026-04-01",
  "date_created": "2026-03-30T12:00:00.000Z",
  "tracking_events": []
}
```

## Key Fields in Response

- `id` — Unique postcard ID. Store in CRM for tracking.
- `url` — PDF preview of the printed postcard
- `expected_delivery_date` — Estimated USPS delivery date
- `tracking_events` — Array of delivery tracking events (updated over time)

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Postcard created | Store `id` and `expected_delivery_date` in CRM |
| 401 | Invalid API key | Check `LOB_API_KEY` environment variable |
| 422 | Invalid address or missing fields | Run `lob-address-verify` first, then retry |
| 429 | Rate limited | Back off and retry after 60 seconds |

## Pricing

- Developer plan: $0/mo platform + $0.77/postcard (4x6)
- Small Business plan: $260/mo + $0.51/postcard
- Growth plan: $550/mo + $0.48/postcard
- Pricing page: https://www.lob.com/pricing

## Notes

- Always verify addresses with `lob-address-verify` before sending to avoid wasted spend on undeliverable mail
- Use test keys during development — test mode simulates the full flow without printing or mailing
- Lob auto-validates addresses at send time and will reject obviously invalid ones (returns 422)
- Store the `id` in your CRM (Attio) as a custom field on the contact record for tracking
