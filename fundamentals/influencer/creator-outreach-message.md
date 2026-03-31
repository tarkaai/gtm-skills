---
name: creator-outreach-message
description: Send a sponsorship inquiry to a B2B creator via email or platform DM
tool: Instantly
difficulty: Config
---

# Creator Outreach Message

Craft and send a sponsorship inquiry to a B2B micro-influencer. This is a single outreach touch — one message to one creator proposing a paid collaboration.

## Message Structure

Every creator outreach message follows this structure:

1. **Specificity hook** — Reference a specific post or piece of content they created. This proves you actually follow their work.
2. **Who you are** — One sentence: your name, company, what you do.
3. **The ask** — One sponsored post or story about your product/topic. Be specific about format (LinkedIn post, newsletter mention, YouTube mention, tweet thread).
4. **Why them** — Why their audience is a fit. Reference their audience's characteristics.
5. **Compensation** — State a budget range or ask for their rate card. Never leave compensation ambiguous.
6. **Low-friction CTA** — Ask if they are open to it. Link to a Cal.com booking page or ask for their rate card.

## Option 1: Instantly (Cold Email)

Use when you have the creator's email address (from Clay enrichment or public info).

### API Call

```
POST https://api.instantly.ai/api/v2/emails/send
Authorization: Bearer {INSTANTLY_API_KEY}
Content-Type: application/json

{
  "account_id": "{SENDING_ACCOUNT_ID}",
  "to": "creator@example.com",
  "subject": "Sponsor your next {{platform}} post?",
  "body": "Hi {{creator_first_name}},\n\nI loved your recent post about {{specific_post_topic}} — especially the point about {{specific_detail}}.\n\nI'm {{your_name}} from {{company}}. We {{one_line_what_you_do}}.\n\nWould you be open to a paid {{format}} (LinkedIn post / newsletter mention / etc.) about {{topic}}? Your audience of {{audience_description}} is exactly who we're trying to reach.\n\nBudget: ${{budget_range}} for a single post. Happy to work with your standard rates if you have a rate card.\n\nIf you're interested, grab a time here: {{calcom_link}}\n\nBest,\n{{your_name}}",
  "reply_to": "{{your_email}}"
}
```

### Response
```json
{
  "status": "sent",
  "message_id": "msg_abc123",
  "timestamp": "2026-03-30T12:00:00Z"
}
```

### Authentication
- API key from Instantly dashboard → Settings → API Keys
- Ensure sending account is warmed up (use `instantly-warmup` fundamental)

## Option 2: Loops (If Creator Is Already a Contact)

Use when the creator is in your Loops audience (e.g., newsletter subscriber, past contact).

### API Call

```
POST https://app.loops.so/api/v1/transactional
Authorization: Bearer {LOOPS_API_KEY}
Content-Type: application/json

{
  "transactionalId": "creator_sponsorship_inquiry",
  "email": "creator@example.com",
  "dataVariables": {
    "creator_name": "{{creator_first_name}}",
    "specific_post": "{{specific_post_topic}}",
    "your_name": "{{your_name}}",
    "company": "{{company}}",
    "format": "LinkedIn post",
    "budget_range": "$300-500",
    "booking_link": "{{calcom_link}}"
  }
}
```

### Authentication
- API key from Loops dashboard → Settings → API

## Option 3: Passionfroot (Direct Booking)

Use when the creator has a Passionfroot storefront.

1. Navigate to `https://www.passionfroot.me/creators/{creator_handle}`
2. Browse available sponsorship slots (newsletter, social post, video mention)
3. Select the slot type and date
4. Fill in the brief: what you want the creator to cover, key messages, any links to include
5. Submit payment (Passionfroot handles the transaction; 2% fee added)

No API — web-app only.

## Option 4: LinkedIn DM

Use for LinkedIn-native creators when you have a connection or InMail credits.

1. Use `linkedin-organic-dms` fundamental to send a connection request with a note (300 char max): "Hi {{name}}, love your content on {{topic}}. I'd like to discuss a paid collaboration — mind if I send details?"
2. Once connected, send a full DM following the message structure above
3. Keep the DM under 500 words. Link to a Cal.com page for scheduling.

## Error Handling

- **Bounce / invalid email:** Remove creator from list, try alternative contact method (LinkedIn DM, Passionfroot)
- **No response after 5 business days:** Send one follow-up. If no response after follow-up, mark as "not interested" and move on.
- **Creator asks for more than budget:** Log their rate card in Attio for future reference. Either negotiate or move to the next creator on the list.
- **Creator says yes:** Move to `creator-content-brief` fundamental to send the brief.
