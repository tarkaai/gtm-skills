---
name: sms-conversation-routing
description: Route inbound SMS replies to CRM deals, classify sentiment, and trigger follow-up workflows
tool: Twilio
difficulty: Config
---

# SMS Conversation Routing

When a prospect replies to an outbound SMS, classify the reply, update the CRM, and trigger the appropriate next step. This fundamental handles the inbound side of SMS outreach.

## Inbound Reply Processing Pipeline

### Step 1: Receive the inbound webhook

Configure your SMS provider to POST inbound messages to an n8n webhook endpoint. The webhook receives:
- Sender phone number (`From`)
- Message body (`Body`)
- Timestamp
- Media attachments (if MMS)

### Step 2: Match to CRM contact

Query Attio API to find the contact matching the sender's phone number:

```bash
curl -X POST "https://api.attio.com/v2/objects/people/records/query" \
  -H "Authorization: Bearer $ATTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "phone_numbers": {"contains": "+1234567890"}
    }
  }'
```

If no match found, create a new contact record with the phone number and tag as `source:sms-inbound-unknown`.

### Step 3: Classify reply sentiment

Use the Anthropic API to classify the reply:

```javascript
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 100,
  messages: [{
    role: "user",
    content: `Classify this SMS reply to a B2B sales outreach message into exactly one category:
    - POSITIVE: interested, wants to learn more, agrees to meet
    - NEGATIVE: not interested, wrong person, do not contact
    - QUESTION: asking for more info before deciding
    - OPT_OUT: explicitly requesting to stop messages (STOP, unsubscribe, etc.)
    - NEUTRAL: acknowledgment without clear intent

    Reply text: "${replyBody}"

    Return ONLY the category name.`
  }]
});
```

### Step 4: Route by classification

| Classification | Action |
|---------------|--------|
| POSITIVE | Create Attio deal at "Interested" stage. Send Cal.com booking link via SMS. Notify founder on Slack. Stop automated sequence. |
| NEGATIVE | Mark contact as `sms_not_interested=true` in Attio. Stop automated sequence. Do not re-contact via SMS for 90 days. |
| QUESTION | Queue for manual founder reply within 2 hours. Send Slack alert with the question and contact context. |
| OPT_OUT | Trigger opt-out workflow (see `sms-opt-out-management` fundamental). Confirm opt-out via SMS. Update suppression list. |
| NEUTRAL | Continue automated sequence. Log the reply in Attio. |

### Step 5: Log events

Fire PostHog events for every inbound reply:
```javascript
posthog.capture({
  distinctId: contactId,
  event: 'sms_replied',
  properties: {
    campaign_id: campaignId,
    sentiment: classification,
    reply_body_length: replyBody.length,
    time_to_reply_hours: hoursFromSend,
    sequence_step: stepNumber
  }
});
```

### Step 6: Update CRM

Update the Attio contact record:
- `last_sms_reply_date`: current timestamp
- `sms_reply_sentiment`: classification result
- `sms_sequence_status`: "replied" (stops further automated sends)
- Add a note with the full reply text and classification

## Two-Way Conversation Support

For POSITIVE and QUESTION replies, the founder may need to continue the conversation via SMS. Ensure:
1. All subsequent messages from the same number route to the same conversation thread in your SMS provider
2. The founder can reply directly from the SMS provider dashboard or Attio integration
3. Every message in the thread is logged in Attio for context continuity
