---
name: sms-provider-send
description: Send an SMS message to a single recipient via API
tool: Twilio
product: Twilio
difficulty: Setup
---

# SMS Provider Send

Send a single SMS message to a phone number. This is the atomic send operation that all SMS drills chain together.

## Tool Options

### Twilio (Default Stack)

**API Endpoint:** `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`

**Authentication:** HTTP Basic Auth with Account SID and Auth Token. Store as environment variables `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`.

**Request:**
```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  --data-urlencode "From=$TWILIO_PHONE_NUMBER" \
  --data-urlencode "To=+1234567890" \
  --data-urlencode "Body=Your message here" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

**Response (200):**
```json
{
  "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "queued",
  "to": "+1234567890",
  "from": "+10987654321",
  "body": "Your message here",
  "date_created": "2026-03-30T12:00:00Z",
  "price": null,
  "error_code": null
}
```

**Node.js SDK:**
```javascript
const twilio = require('twilio');
const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const message = await client.messages.create({
  body: 'Your message here',
  from: process.env.TWILIO_PHONE_NUMBER,
  to: '+1234567890',
  statusCallback: 'https://your-webhook.com/sms-status'
});
```

**Error Handling:**
- `21211` — Invalid "To" phone number. Validate E.164 format before sending.
- `21610` — Recipient opted out. Do NOT retry. Mark contact as opted-out in CRM.
- `21612` — "From" number not SMS-capable. Verify number capabilities in Twilio console.
- `30004` — Message blocked by carrier. Likely spam filtering. Review message content for spam triggers.
- `30008` — Unknown error. Retry with exponential backoff (max 3 retries, 5s/15s/45s delays).

### Salesmsg

**API Endpoint:** `POST https://api.salesmessage.com/v1/messages`

**Authentication:** Bearer token via `Authorization: Bearer {api_key}`. Obtain API key from Salesmsg dashboard > Settings > API.

**Request:**
```bash
curl -X POST "https://api.salesmessage.com/v1/messages" \
  -H "Authorization: Bearer $SALESMSG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "+1234567890", "text": "Your message here", "from_number": "+10987654321"}'
```

### OpenPhone (Quo)

**API Endpoint:** `POST https://api.openphone.com/v1/messages`

**Authentication:** Bearer token via API key from Quo dashboard.

**Request:**
```bash
curl -X POST "https://api.openphone.com/v1/messages" \
  -H "Authorization: Bearer $OPENPHONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"from": "phone_number_id", "to": ["+1234567890"], "content": "Your message here"}'
```

### Heymarket

**API Endpoint:** `POST https://api.heymarket.com/v1/messages`

**Authentication:** Bearer token. Obtain from Heymarket > Settings > API Keys.

### SlickText

SlickText does not offer a direct send API for 1:1 outbound. Use their campaign API for bulk sends or integrate via Zapier webhook for individual messages. Better suited for opt-in marketing campaigns than cold outbound.

## Message Constraints

- SMS segment = 160 GSM-7 characters or 70 UCS-2 (Unicode) characters
- Messages exceeding one segment are split and billed as multiple messages
- Keep outbound prospecting messages under 160 characters for cost efficiency and readability
- Include opt-out language in first message to a new contact: "Reply STOP to opt out"

## Pricing Reference

- **Twilio:** $0.0079/SMS + carrier fees (~$0.003-0.005/msg) = ~$0.011-0.013/msg effective (https://www.twilio.com/en-us/sms/pricing/us)
- **Salesmsg:** From $25/mo for 250 credits (https://www.salesmessage.com/features/new-salesmsg-pricing)
- **OpenPhone (Quo):** $15/user/mo includes unlimited SMS; API sends $0.01/msg (https://www.quo.com/blog/quo-pricing/)
- **Heymarket:** Per-user plans starting ~$20/user/mo (https://www.heymarket.com/pricing/)
- **SlickText:** From $29/mo for 500 texts (https://www.slicktext.com/pricing)
