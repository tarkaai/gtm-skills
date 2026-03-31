---
name: tremendous-send-reward
description: Send a digital gift card or reward to a recipient via the Tremendous API
tool: Tremendous
difficulty: Setup
---

# Tremendous — Send Reward

Send a digital gift card, prepaid Visa, or charitable donation to a recipient via the Tremendous REST API. Tremendous is the most cost-effective option for digital gifts — no platform fee, you pay only the face value of the reward.

## Authentication

Tremendous uses Bearer token authentication. Generate an API key from Settings > API keys in your Tremendous dashboard.

- **Sandbox:** `https://testflight.tremendous.com/api/v2/`
- **Production:** `https://www.tremendous.com/api/v2/`

All requests require:
```
Authorization: Bearer {{TREMENDOUS_API_KEY}}
Content-Type: application/json
```

## Create an Order (Send a Reward)

```
POST https://www.tremendous.com/api/v2/orders
Authorization: Bearer {{TREMENDOUS_API_KEY}}
Content-Type: application/json

{
  "payment": {
    "funding_source_id": "{{funding_source_id}}"
  },
  "rewards": [
    {
      "value": {
        "denomination": 50.00,
        "currency_code": "USD"
      },
      "delivery": {
        "method": "EMAIL",
        "meta": {
          "sender_name": "{{sender_name}}",
          "sender_message": "{{personalized_note}}"
        }
      },
      "recipient": {
        "name": "{{first_name}} {{last_name}}",
        "email": "{{email}}"
      },
      "products": ["{{product_id}}"],
      "campaign_id": "{{campaign_id}}"
    }
  ]
}
```

### Required Fields
- `funding_source_id` — Your balance or payment method. Get via `GET /api/v2/funding_sources`.
- `denomination` — Gift card face value in the specified currency.
- `recipient.email` — Where to deliver the digital gift.
- `products` — Array of product IDs (specific brands). Use `["OKMHM2X2OHYV"]` for "recipient's choice" (lets them pick from 1000+ brands).

### Optional Fields
- `campaign_id` — Group sends under a campaign for reporting. Create via `POST /api/v2/campaigns`.
- `delivery.meta.sender_message` — Personalized note displayed to recipient.

## List Available Products (Gift Card Brands)

```
GET https://www.tremendous.com/api/v2/products
Authorization: Bearer {{TREMENDOUS_API_KEY}}
```

Returns 1000+ brands. Filter by country: `?country=US`. Each product has `id`, `name`, `min_value`, `max_value`, `currency_codes`.

## Check Reward Status

```
GET https://www.tremendous.com/api/v2/rewards/{{reward_id}}
Authorization: Bearer {{TREMENDOUS_API_KEY}}
```

Returns status: `PENDING`, `DELIVERED`, `REDEEMED`, `EXPIRED`.

## List Funding Sources

```
GET https://www.tremendous.com/api/v2/funding_sources
Authorization: Bearer {{TREMENDOUS_API_KEY}}
```

Returns available payment methods. Fund your balance via ACH, wire, or credit card in the dashboard.

## Webhooks

Register webhooks at `POST /api/v2/webhooks` to receive real-time events:
- `REWARDS.DELIVERY.SUCCEEDED` — Gift card email delivered
- `REWARDS.REDEEMED` — Recipient redeemed the gift
- `ORDERS.CREATED` — New order placed

## Error Handling

| HTTP Code | Meaning | Recovery |
|-----------|---------|----------|
| 400 | Invalid request body | Check required fields and data types |
| 401 | Invalid API key | Regenerate key in dashboard |
| 402 | Insufficient funds | Add funds to your balance |
| 422 | Validation error (e.g., denomination below product minimum) | Check product min/max values |
| 429 | Rate limited (10 req/sec default) | Back off; request higher limits for bulk sends |

## Rate Limits

Default: 10 requests/second. For bulk sends, batch multiple rewards into a single order (up to 1000 rewards per order).

## Pricing

No platform fee. No subscription. You pay only the face value of rewards sent. Venmo, PayPal, and bank transfers incur a 4-6% processing fee. Gift cards and prepaid Visa are free to send (no markup).

https://www.tremendous.com/pricing
