---
name: sms-outreach-sequence
description: Build and launch a multi-step SMS outreach sequence to solution-aware prospects
category: SMS
tools:
  - Twilio
  - n8n
  - Attio
  - Clay
fundamentals:
  - sms-provider-send
  - sms-phone-number-provisioning
  - sms-opt-out-management
  - sms-delivery-tracking
  - sms-conversation-routing
  - clay-enrichment-waterfall
  - attio-contacts
  - n8n-scheduling
---

# SMS Outreach Sequence

Build and deploy a multi-step SMS outreach sequence targeting solution-aware B2B prospects. This drill handles number provisioning, message copy, send scheduling, reply handling, and CRM logging.

## Input

- Prospect list in Attio with verified mobile phone numbers (from `build-prospect-list` drill)
- ICP definition with pain points and value props (from `icp-definition` drill)
- SMS provider account with A2P 10DLC registration complete (from `sms-phone-number-provisioning` fundamental)

## Steps

### 1. Verify phone numbers are mobile

Before any sends, verify your prospect list contains mobile numbers, not landlines. Use Clay's phone type enrichment or Twilio Lookup API:

```bash
curl "https://lookups.twilio.com/v2/PhoneNumbers/+1234567890?Fields=line_type_intelligence" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

Filter to `type: "mobile"` only. Landlines cannot receive SMS. Update Attio: set `phone_type=mobile` or `phone_type=landline` for each contact. Remove landlines from the SMS campaign list.

Target: minimum 70% mobile coverage on your prospect list. If below 70%, enrich additional phone numbers via Clay waterfall before proceeding.

### 2. Write the SMS sequence

Write a 3-message sequence. SMS must be concise (under 160 chars per segment to avoid multi-segment billing). The tone is conversational and founder-direct. No marketing language. No ALL CAPS. No exclamation points.

**Message 1 (Day 1): Pain-aware opener**
```
Hi {{first_name}}, this is [Founder] from [Company]. Saw {{company}} is {{pain_signal}}. We help teams like yours {{value_prop}}. Worth a quick chat? Reply STOP to opt out.
```
- Under 160 characters after merge fields resolve
- References something specific (signal, company event, role)
- Soft CTA (question, not command)
- Includes opt-out language (required on first contact)

**Message 2 (Day 3): Value proof**
```
{{first_name}}, quick follow-up. We helped [similar_company] {{specific_result}} in {{timeframe}}. Happy to share how — just reply YES for a 10-min call.
```
- Social proof with specific result
- Lower-friction CTA (reply YES)
- Under 160 characters

**Message 3 (Day 6): Breakup with booking link**
```
Last note, {{first_name}}. If timing's off, no worries. If you'd like to chat: {{cal_link}}. Either way, wishing {{company}} well.
```
- Graceful exit
- Direct booking link
- No guilt trip

### 3. Build the send workflow in n8n

Create an n8n workflow with these nodes:

1. **Cron trigger** — runs daily at 9am (adjustable per timezone segment)
2. **Attio query** — fetch contacts where `sms_campaign_status=active` AND `sms_next_step_date=today` AND `sms_opted_out!=true`
3. **Timezone check** — verify current time is between 8am-6pm in contact's timezone. If outside window, reschedule to next valid window.
4. **Merge field resolution** — pull personalization data from Attio: first_name, company, pain_signal, cal_link
5. **SMS send** — use `sms-provider-send` fundamental to send the message for the current sequence step
6. **Status update** — update Attio: `sms_last_sent_date`, `sms_current_step`, `sms_next_step_date`
7. **Error handler** — if send fails, log error in Attio, retry once after 1 hour, then mark as `sms_send_failed` if second attempt fails

### 4. Configure reply handling

Wire up the `sms-conversation-routing` fundamental:
- Inbound replies hit n8n webhook
- Sentiment classification runs via Anthropic
- POSITIVE replies create an Attio deal and stop the sequence
- OPT_OUT replies trigger `sms-opt-out-management` and stop the sequence
- NEGATIVE replies stop the sequence and mark contact for 90-day cooldown

### 5. Set sending limits

- Maximum 50 SMS per day per number (stay well under carrier thresholds)
- Maximum 1 message per prospect per 48 hours (minimum spacing between sequence steps)
- Pause all sends if delivery rate drops below 90% for 24 hours
- Never send on weekends unless the prospect's profile indicates weekend activity

### 6. Monitor deliverability

Use `sms-delivery-tracking` fundamental to route all status callbacks to PostHog. Monitor:
- Delivery rate (target: >95%)
- Opt-out rate (alarm if >5% of sends)
- Reply rate by sequence step
- Error rate by error code

## Output

- Active SMS sequence running via n8n with daily sends
- All delivery events flowing to PostHog
- All contact updates synced to Attio
- Reply routing classifying and handling inbound messages

## Triggers

Daily cron via n8n. Sequence runs until all 3 steps complete, prospect replies, or prospect opts out.
