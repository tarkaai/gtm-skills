---
name: giftsenda-send-gift
description: Send a curated gift internationally via the Giftsenda API with delivery in 200+ countries
tool: Giftsenda
product: Giftsenda
difficulty: Config
---

# Giftsenda — Send Gift

Send a curated physical gift to a recipient in 200+ countries via the Giftsenda API. Giftsenda specializes in international corporate gifting with locally sourced gift options, making it ideal when your prospects are globally distributed.

## Authentication

Giftsenda uses API key authentication. Obtain your key from the Giftsenda developer dashboard.

```
Authorization: Bearer {{GIFTSENDA_API_KEY}}
Content-Type: application/json
```

Base URL: `https://api.giftsenda.com/v1/`

## Send a Gift

```
POST https://api.giftsenda.com/v1/gifts/send
Authorization: Bearer {{GIFTSENDA_API_KEY}}
Content-Type: application/json

{
  "recipient": {
    "first_name": "{{first_name}}",
    "last_name": "{{last_name}}",
    "email": "{{email}}",
    "company": "{{company}}",
    "address": {
      "line1": "{{address_line1}}",
      "city": "{{city}}",
      "state": "{{state}}",
      "postal_code": "{{zip}}",
      "country": "{{country_code}}"
    }
  },
  "gift_id": "{{gift_id}}",
  "message": "{{personalized_note}}",
  "campaign_id": "{{campaign_id}}"
}
```

### Required Fields
- `recipient.first_name`, `recipient.last_name`, `recipient.email` — Identity.
- `gift_id` — Item from the Giftsenda catalog. Retrieved via `GET /v1/gifts`.
- `recipient.address` — Delivery address. Required for physical gifts.

## Browse Gift Catalog

```
GET https://api.giftsenda.com/v1/gifts?country={{country_code}}&category={{category}}
Authorization: Bearer {{GIFTSENDA_API_KEY}}
```

Returns locally sourced gifts for the specified country. Categories include: gourmet food, wine, flowers, gift baskets, branded items. Each item includes `id`, `name`, `price`, `currency`, `delivery_estimate`.

## Track Delivery

```
GET https://api.giftsenda.com/v1/gifts/send/{{send_id}}/status
Authorization: Bearer {{GIFTSENDA_API_KEY}}
```

Returns: `processing`, `dispatched`, `in_transit`, `delivered`, `failed`.

## Error Handling

| HTTP Code | Meaning | Recovery |
|-----------|---------|----------|
| 400 | Invalid request | Check required fields |
| 401 | Invalid API key | Regenerate in dashboard |
| 404 | Gift not available in recipient's country | Re-query catalog for that country |
| 422 | Address validation failed | Verify address format for the recipient's country |

## Pricing

Pay-as-you-go with no platform fee for project-based gifting. Subscription plan: $333/month (billed annually) for year-round gifting with rebates. Gift prices vary by item and destination country — typically $30-$150 per gift.

https://www.giftsenda.com/request-pricing
