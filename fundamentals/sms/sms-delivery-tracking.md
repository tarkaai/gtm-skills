---
name: sms-delivery-tracking
description: Track SMS delivery status, read receipts, and response events via webhooks
tool: Twilio / Salesmsg / OpenPhone (Quo)
difficulty: Config
---

# SMS Delivery Tracking

Track the lifecycle of every outbound SMS: queued, sent, delivered, failed, and replied. Route delivery events to PostHog and your CRM for funnel measurement.

## Twilio (Default)

### Status callback webhook

When creating a message, include a `StatusCallback` URL:

```javascript
const message = await client.messages.create({
  body: 'Your message',
  from: process.env.TWILIO_PHONE_NUMBER,
  to: '+1234567890',
  statusCallback: 'https://your-n8n-instance.com/webhook/twilio-sms-status'
});
```

Twilio POSTs to the callback URL as the message progresses through statuses:

| Status | Meaning |
|--------|---------|
| `queued` | Message accepted by Twilio |
| `sent` | Message sent to carrier |
| `delivered` | Carrier confirmed delivery to handset |
| `undelivered` | Carrier rejected or could not deliver |
| `failed` | Twilio could not send (bad number, blocked, etc.) |

**Webhook payload fields:**
- `MessageSid` — unique message ID
- `MessageStatus` — current status
- `To` — recipient number
- `From` — sender number
- `ErrorCode` — if failed/undelivered, the error code
- `ErrorMessage` — human-readable error description

### Inbound reply webhook

Configure the phone number's SMS webhook URL:

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers/$TWILIO_PHONE_NUMBER_SID.json" \
  --data-urlencode "SmsUrl=https://your-n8n-instance.com/webhook/twilio-sms-inbound" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Inbound webhook payload includes `Body` (message text), `From` (sender), `To` (your number), and `NumMedia` (attached media count).

### n8n workflow for event routing

Build an n8n webhook node that receives Twilio status callbacks and:

1. Parses the `MessageStatus` field
2. Fires a PostHog event: `sms_delivered`, `sms_failed`, `sms_replied`
3. Updates the Attio contact record with `last_sms_status` and `last_sms_date`
4. If status is `replied` (inbound message), classify sentiment (positive/negative/neutral) using Claude and update Attio

### Delivery rate calculation

Query PostHog for delivery rate:
```
delivered_count / (delivered_count + undelivered_count + failed_count) * 100
```

Target: >95% delivery rate. Below 90% indicates number quality issues or carrier filtering.

## Salesmsg

Delivery tracking built into dashboard. Webhook integration available via Zapier or native webhooks (Settings > Webhooks). Events: `message.delivered`, `message.failed`, `message.received`. Route to n8n via webhook URL.

## OpenPhone (Quo)

Delivery status visible in conversation threads. Webhook events available via API: configure webhook endpoints at Settings > Webhooks. Events include `message.completed`, `message.failed`, `message.received`.

## Error Codes to Monitor

| Code | Provider | Meaning | Action |
|------|----------|---------|--------|
| 30001 | Twilio | Queue overflow | Reduce send rate |
| 30003 | Twilio | Unreachable destination | Verify number, retry once after 24h |
| 30004 | Twilio | Message blocked | Review content for spam triggers |
| 30005 | Twilio | Unknown destination | Invalid number, remove from list |
| 30006 | Twilio | Landline or unreachable | Mark as non-mobile, exclude from SMS |
| 30007 | Twilio | Carrier content filtering | Rewrite message, avoid links/spam words |
| 21610 | Twilio | Recipient opted out | Honor immediately, update suppression list |
