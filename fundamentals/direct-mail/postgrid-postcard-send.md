---
name: postgrid-postcard-send
description: Send a physical postcard to a recipient via the PostGrid Print & Mail API
tool: Lob
difficulty: Setup
---

# PostGrid Postcard Send

Alternative to Lob for sending physical postcards via API. PostGrid supports US, Canada, UK, EU, and Australia. Useful if you need international direct mail or prefer PostGrid's pricing model.

## Authentication

- Obtain your API key from the PostGrid dashboard at https://app.postgrid.com
- Test keys operate in a sandbox (no mail sent)
- Live keys trigger real printing and mailing
- Include the API key in the `x-api-key` header with every request

## API Endpoint

```
POST https://api.postgrid.com/print-mail/v1/postcards
```

## Request Format

```bash
curl -X POST https://api.postgrid.com/print-mail/v1/postcards \
  -H "x-api-key: $POSTGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": {
      "firstName": "{{first_name}}",
      "lastName": "{{last_name}}",
      "addressLine1": "{{address_line1}}",
      "addressLine2": "{{address_line2}}",
      "city": "{{city}}",
      "provinceOrState": "{{state}}",
      "postalOrZip": "{{zip}}",
      "countryCode": "US"
    },
    "from": {
      "firstName": "{{sender_first_name}}",
      "lastName": "{{sender_last_name}}",
      "addressLine1": "{{sender_address}}",
      "city": "{{sender_city}}",
      "provinceOrState": "{{sender_state}}",
      "postalOrZip": "{{sender_zip}}",
      "countryCode": "US"
    },
    "size": "4x6",
    "frontHTML": "<html><body><h1>Hello {{first_name}}</h1><p>{{body_copy}}</p></body></html>",
    "backHTML": "<html><body><p>{{back_message}}</p></body></html>",
    "mailingClass": "first_class",
    "mergeVariables": {
      "first_name": "{{first_name}}",
      "body_copy": "{{body_copy}}",
      "back_message": "{{back_message}}"
    }
  }'
```

## Postcard Sizes

- `4x6` — Standard (cheapest)
- `6x9` — Jumbo
- `6x11` — Extra large

## Mailing Classes

- `first_class` — 2-5 business days delivery
- `standard_class` — 5-14 business days delivery (cheaper)

## Response

```json
{
  "id": "postcard_abc123",
  "status": "ready",
  "to": { ... },
  "from": { ... },
  "sendDate": "2026-04-01",
  "expectedDeliveryDate": "2026-04-05",
  "url": "https://pg-assets.com/postcards/postcard_abc123.pdf"
}
```

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Postcard created | Store `id` in CRM |
| 401 | Invalid API key | Check `POSTGRID_API_KEY` |
| 400 | Invalid request body | Check address format, required fields |
| 422 | Address validation failed | Verify address separately first |
| 429 | Rate limited | Back off and retry |

## Pricing

- Postcards start at $0.82/piece (includes printing + postage)
- Starter tier: up to 500 mailings/month
- Volume pricing available for higher quantities
- Pricing page: https://www.postgrid.com/pricing/

## Notes

- PostGrid supports international mailing natively — useful for prospects outside the US
- Templates can use `{{variableName}}` merge variables in both frontHTML and backHTML
- Use test API keys during development — sandbox mode simulates the full flow
- Store the postcard `id` in your CRM for delivery tracking
