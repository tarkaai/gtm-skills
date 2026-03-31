---
name: twitter-x-dms
description: Send and monitor direct messages on Twitter/X via API or automation tools
tool: X
product: X Organic
difficulty: Config
---

# Twitter/X Direct Messages

Send and receive DMs on Twitter/X programmatically. Used for cold outreach, warm follow-ups, and lead conversations on X.

## Option A: X API v2 (Direct)

### Authentication

Requires OAuth 2.0 User Access Token with `dm.write` and `dm.read` scopes. App-Only auth is NOT supported for DMs.

```
Authorization: Bearer {USER_ACCESS_TOKEN}
Content-Type: application/json
```

### Send a DM to a Specific User

```
POST https://api.x.com/2/dm_conversations/with/{participant_user_id}/messages

{
  "text": "Your message text here"
}
```

- `participant_user_id`: The numeric X user ID of the recipient (not the @handle).
- Creates a new 1:1 conversation if one does not exist; otherwise appends to the existing conversation.
- Response returns `dm_conversation_id` and `dm_event_id`.

### Send a DM to an Existing Conversation

```
POST https://api.x.com/2/dm_conversations/{dm_conversation_id}/messages

{
  "text": "Follow-up message"
}
```

### Retrieve DM Events

```
GET https://api.x.com/2/dm_events?dm_event_fields=id,text,created_at,sender_id,dm_conversation_id&event_types=MessageCreate
```

Returns recent DM events. Use `pagination_token` for older messages.

### Rate Limits

- Send DMs: 200 per 15-minute window per user (Basic tier). Higher on Pro.
- Read DM events: 100 requests per 15-minute window.
- DM text limit: 10,000 characters.

### Pricing

- X API Basic: $200/mo (sufficient for low-volume cold DM plays).
- X API Pro: $5,000/mo (for high-volume automation).
- Pay-per-use: Available for new signups as of Feb 2026. Per-request pricing varies by operation.

### Resolve @handle to User ID

```
GET https://api.x.com/2/users/by/username/{username}
```

Returns `data.id` which is the numeric user ID required for DM endpoints.

## Option B: PhantomBuster Twitter Message Sender

For teams without X API access or who prefer a no-code approach.

### Setup

1. Create a PhantomBuster account.
2. Navigate to Automations > Twitter > Twitter Message Sender.
3. Connect your X account via session cookie.
4. Provide a Google Sheet URL or CSV with target X profile URLs or @handles.
5. Write your message template. Supports variables: `{firstName}`, `{companyName}`.
6. Set processing rate: 10 accounts per launch, 5-8 launches per day.

### Limitations

- Cannot verify in advance whether a profile has DMs open. Closed DMs = undeliverable.
- X rate limits apply: exceeding them risks account suspension.
- PhantomBuster pricing: Starter $56/mo, Pro $128/mo, Team $352/mo.

### n8n Integration

PhantomBuster has an n8n node. Trigger a Phantom launch from an n8n workflow:

```
POST https://api.phantombuster.com/api/v2/agents/launch
Authorization: X-Phantombuster-Key {API_KEY}

{
  "id": "{PHANTOM_AGENT_ID}",
  "argument": {
    "spreadsheetUrl": "https://docs.google.com/spreadsheets/d/{SHEET_ID}",
    "message": "Your templated message"
  }
}
```

## Option C: Typefully / Hypefury (Scheduled DMs)

Some X content tools support scheduled DM workflows triggered by engagement events (e.g., someone replies to a post). These are limited but useful for warm DM follow-ups after content engagement.

## Error Handling

- **403 Forbidden**: Recipient has DMs closed or has blocked you. Skip and log.
- **429 Too Many Requests**: Rate limit hit. Back off for the duration in the `x-rate-limit-reset` header.
- **400 Bad Request**: Message text is empty or exceeds 10,000 characters.
- **Recipient not found**: The user ID is invalid or the account is suspended. Remove from list.

## Best Practices for Cold DMs

- Only DM users who have DMs open (check profile before sending if using API).
- Keep cold DMs under 280 characters. Shorter = higher read rate.
- Do not include links in the first DM. Links trigger spam filters.
- Personalize using the recipient's recent post content or bio.
- Maximum 20-30 cold DMs per day to avoid account restrictions.
