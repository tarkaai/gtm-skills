---
name: reachdesk-send-gift
description: Send a physical gift, eGift, or branded swag to a prospect via the Reachdesk API
tool: Reachdesk
product: Reachdesk
difficulty: Config
---

# Reachdesk — Send Gift

Send a curated physical gift, eGift card, or branded item to a recipient via the Reachdesk API. Reachdesk excels at international gifting with localized gift catalogs and regional warehouses.

## Authentication

Reachdesk uses API key authentication. Obtain your key from the Reachdesk admin panel under Integrations > API.

All requests require:
```
Authorization: Bearer {{REACHDESK_API_KEY}}
Content-Type: application/json
```

Base URL: `https://api.reachdesk.com/v1/`

## Send a Gift

```
POST https://api.reachdesk.com/v1/sends
Authorization: Bearer {{REACHDESK_API_KEY}}
Content-Type: application/json

{
  "recipient": {
    "first_name": "{{first_name}}",
    "last_name": "{{last_name}}",
    "email": "{{email}}",
    "company": "{{company}}",
    "title": "{{title}}",
    "address": {
      "line1": "{{address_line1}}",
      "line2": "{{address_line2}}",
      "city": "{{city}}",
      "state": "{{state}}",
      "postal_code": "{{zip}}",
      "country": "{{country_code}}"
    }
  },
  "gift_id": "{{gift_id}}",
  "message": "{{personalized_note}}",
  "campaign_id": "{{campaign_id}}",
  "metadata": {
    "contact_id": "{{contact_id}}",
    "signal_type": "{{signal_type}}"
  }
}
```

### Required Fields
- `recipient.first_name`, `recipient.last_name`, `recipient.email` — Identity.
- `gift_id` — Item from the Reachdesk marketplace. Retrieve from `GET /v1/gifts`.
- `recipient.address` — Required for physical gifts. eGifts deliver via email.

### Optional Fields
- `campaign_id` — Group sends for campaign-level analytics.
- `message` — Personalized handwritten-style note included with the gift.
- `metadata` — Custom key-value pairs for tracking and attribution.

## List Available Gifts

```
GET https://api.reachdesk.com/v1/gifts
Authorization: Bearer {{REACHDESK_API_KEY}}
```

Filter by `?country={{country_code}}` for localized gift options. Reachdesk curates region-specific catalogs so gifts are locally sourced and culturally appropriate.

## Address Confirmation (MagicLink)

For physical gifts where you lack the recipient's address, use address confirmation:

```
POST https://api.reachdesk.com/v1/sends
{
  "recipient": {
    "email": "{{email}}",
    "first_name": "{{first_name}}"
  },
  "gift_id": "{{gift_id}}",
  "address_confirmation": true,
  "message": "{{personalized_note}}"
}
```

This sends the recipient an email asking them to confirm their delivery address before the gift ships. Useful when you have email but not physical address.

## Check Send Status

```
GET https://api.reachdesk.com/v1/sends/{{send_id}}
Authorization: Bearer {{REACHDESK_API_KEY}}
```

Returns: `pending_address`, `processing`, `shipped`, `delivered`, `failed`.

## Error Handling

| HTTP Code | Meaning | Recovery |
|-----------|---------|----------|
| 400 | Missing required fields | Validate request body |
| 401 | Invalid API key | Check key in admin panel |
| 404 | Gift ID not in catalog | Re-fetch available gifts for the recipient's country |
| 422 | Address validation failed | Use address confirmation flow instead |
| 429 | Rate limited | Back off and retry |

## Pricing

Plans start at ~$20,000/year. Per-send cost includes the gift item value + fulfillment fee. Reachdesk warehouses globally (US, UK, EU, APAC) which keeps shipping costs lower for international sends.

https://www.reachdesk.com/pricing
