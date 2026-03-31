---
name: sendoso-send-gift
description: Send a physical or digital gift to a prospect via the Sendoso REST API
tool: Sendoso
difficulty: Config
---

# Sendoso — Send Gift

Send a physical gift, eGift card, or branded swag item to a single recipient via the Sendoso REST API. This fundamental handles one send; batch sends iterate over this.

## Authentication

Sendoso uses OAuth 2.0. Obtain credentials from Settings > API in the Sendoso dashboard.

1. Exchange client_id + client_secret for an access token:
```
POST https://app.sendoso.com/oauth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{{SENDOSO_CLIENT_ID}}",
  "client_secret": "{{SENDOSO_CLIENT_SECRET}}"
}
```
2. Use the returned `access_token` as a Bearer token on all subsequent requests.
3. Tokens expire after 2 hours. Refresh before expiry.

## Send a Gift

```
POST https://app.sendoso.com/api/v3/sends
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "send": {
    "gift_id": "{{gift_id}}",
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
    },
    "message": "{{personalized_note}}",
    "variant_id": "{{variant_id}}",
    "team_id": "{{team_id}}",
    "metadata": {
      "campaign_id": "{{campaign_id}}",
      "contact_id": "{{contact_id}}"
    }
  }
}
```

### Required Fields
- `gift_id` — The catalog item to send. Retrieve from `GET /api/v3/gifts`.
- `first_name`, `last_name`, `email` — Recipient identity.
- `address` — Required for physical gifts. Not required for eGift cards (delivered via email).
- `message` — Personalized note included with the gift.

### Optional Fields
- `variant_id` — Specific variant (size, color) of a swag item.
- `metadata` — Arbitrary key-value pairs for attribution tracking.

## List Available Gifts

```
GET https://app.sendoso.com/api/v3/gifts
Authorization: Bearer {{access_token}}
```

Returns the full gift catalog including physical items, eGift cards, branded swag, and charitable donations. Filter by category or price range in query params.

## Check Send Status

```
GET https://app.sendoso.com/api/v3/sends/{{send_id}}
Authorization: Bearer {{access_token}}
```

Returns status: `pending`, `processing`, `shipped`, `delivered`, `failed`, `returned`.

## Error Handling

| HTTP Code | Meaning | Recovery |
|-----------|---------|----------|
| 400 | Invalid address or missing required field | Validate address before sending; check all required fields |
| 401 | Token expired | Refresh the OAuth token |
| 404 | Gift ID not found | Re-fetch catalog with GET /api/v3/gifts |
| 422 | Unprocessable (e.g., eGift to invalid email) | Verify email address; check gift eligibility for recipient country |
| 429 | Rate limited | Back off and retry after the Retry-After header value |

## Pricing

Sendoso platform starts at ~$20,000/year (Essential plan). Per-send costs depend on the gift item selected plus shipping. eGift cards incur no shipping cost. Physical gifts: item cost + $10-15 fulfillment + shipping.

https://www.sendoso.com/compare-plans
