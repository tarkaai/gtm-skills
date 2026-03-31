---
name: sms-opt-out-management
description: Handle opt-out requests, TCPA compliance, and consent tracking for SMS outreach
tool: Twilio / Salesmsg / OpenPhone (Quo)
difficulty: Config
---

# SMS Opt-Out Management

Manage opt-out (STOP) handling, consent records, and TCPA compliance for outbound SMS campaigns. Non-compliance risks $500-$1,500 per unsolicited message in TCPA fines.

## TCPA Requirements for B2B Cold SMS

1. **Prior express consent** is required for non-marketing informational texts. For marketing texts, **prior express written consent** is required.
2. B2B cold SMS to business numbers is a gray area. Mitigate risk by:
   - Sending only to business-registered mobile numbers
   - Including opt-out instructions in every first message
   - Honoring STOP requests immediately (within seconds, not hours)
   - Maintaining a suppression list
   - Keeping messages relevant and non-promotional in tone
3. Never send before 8am or after 9pm in the recipient's local timezone.

## Twilio (Default)

### Automatic STOP handling

Twilio's Messaging Service has built-in Advanced Opt-Out enabled by default. When a recipient replies STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, or QUIT, Twilio:
- Automatically replies with a confirmation message
- Blocks future messages to that number from your Messaging Service
- Returns error `21610` if you attempt to send to an opted-out number

Verify opt-out is enabled:
```bash
curl "https://messaging.twilio.com/v1/Services/$TWILIO_MESSAGING_SERVICE_SID" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Check `use_inbound_webhook_on_number` and ensure opt-out handling is not overridden.

### Query opt-out list

There is no direct API to list all opted-out numbers. Instead, attempt a send and catch error `21610`, or maintain your own suppression list synced from webhook events.

### Webhook for opt-out events

Configure a status callback URL on your Messaging Service. When a STOP is received, Twilio fires a webhook with `OptOutType=STOP`. Capture this in n8n and:
1. Mark the contact as `sms_opted_out=true` in Attio
2. Add the phone number to your suppression list
3. Log a `sms_opt_out` event in PostHog with properties: phone_number_hash, campaign_id, opt_out_keyword

### Re-opt-in

If a contact replies START or UNSTOP, Twilio automatically re-enables messaging and fires a webhook with `OptOutType=START`. Update the contact record in Attio accordingly.

## Salesmsg

Opt-out handled automatically. Salesmsg maintains a global do-not-contact list per account. When someone texts STOP, they are blocked from all future messages. Access the suppression list via dashboard > Contacts > Opted Out.

## OpenPhone (Quo)

Opt-out handling is automatic for registered A2P numbers. STOP replies trigger carrier-level blocking. Quo surfaces opt-out events in the conversation thread.

## Suppression List Management

Regardless of provider, maintain a master suppression list in your CRM (Attio):

1. Create a custom attribute `sms_opted_out` (boolean) on the Person object
2. Create a custom attribute `sms_opt_out_date` (date) on the Person object
3. Before every SMS send, query Attio to verify the contact has `sms_opted_out != true`
4. Sync the suppression list bidirectionally: provider opt-outs update Attio, Attio manual opt-outs update the provider (where API allows)

## Pre-Send Compliance Checklist

Before sending any SMS in this play, verify:
- [ ] A2P 10DLC registration is active and approved
- [ ] STOP handling is enabled on the messaging service
- [ ] First message to any new contact includes "Reply STOP to opt out"
- [ ] Sending window is 8am-9pm in recipient's timezone
- [ ] Contact is not on the suppression list
- [ ] Phone number is a mobile number (landlines cannot receive SMS)
