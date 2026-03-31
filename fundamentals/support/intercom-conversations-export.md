---
name: intercom-conversations-export
description: Export support conversations and ticket data from Intercom via API for analysis
tool: Intercom
difficulty: Setup
---

# Export Conversations from Intercom

Pull support conversations (tickets) from Intercom's REST API for downstream analysis, churn correlation, and product feedback extraction.

## Prerequisites
- Intercom account with API access token (full access scope: `read conversations`, `read contacts`, `read admins`)
- Conversations already flowing through Intercom Messenger or email integration

## API Endpoints

### List all conversations (paginated)

```
GET https://api.intercom.io/conversations
Authorization: Bearer {access_token}
Accept: application/json
```

Query parameters:
- `per_page`: 20 (max 150)
- `starting_after`: cursor for pagination

Response includes: `id`, `created_at`, `updated_at`, `state` (open/closed/snoozed), `priority`, `statistics` (time_to_assignment, time_to_first_close, time_to_last_close, median_time_to_reply), `contacts` (the user), `tags`, `conversation_rating`.

### Search conversations with filters

```
POST https://api.intercom.io/conversations/search
{
  "query": {
    "operator": "AND",
    "value": [
      {"field": "created_at", "operator": ">", "value": 1711929600},
      {"field": "state", "operator": "=", "value": "closed"},
      {"field": "contact_ids", "operator": "=", "value": "{contact_id}"}
    ]
  },
  "pagination": {"per_page": 50}
}
```

Use this to pull conversations for a specific user or time range. Filter by `state`, `created_at`, `updated_at`, `contact_ids`, `teammate_ids`, `tag_ids`.

### Get a single conversation with full thread

```
GET https://api.intercom.io/conversations/{id}
```

Returns the full conversation including all `conversation_parts` (messages, notes, assignments, state changes). Each part has: `part_type`, `body` (HTML), `author` (user or admin), `created_at`.

### Get conversation tags

Tags are returned in the conversation object under `tags.tags[]`. Each tag has `id`, `name`, `applied_at`, `applied_by`.

### Get CSAT rating

The `conversation_rating` object on each conversation includes: `rating` (1-5), `remark` (customer comment), `created_at`, `contact` (who rated).

## Pagination

Intercom uses cursor-based pagination. Loop until `pages.next` is null:

```
response = GET /conversations?per_page=150
while response.pages.next:
    response = GET /conversations?per_page=150&starting_after={response.pages.next.starting_after}
```

## Rate Limits

- 1000 API calls per minute for most plans
- Use search endpoint with date filters rather than listing all conversations
- Cache results locally; only pull new/updated conversations since last sync

## Error Handling

- `401`: Token expired or insufficient scopes. Re-authenticate.
- `429`: Rate limited. Back off exponentially (1s, 2s, 4s).
- `404`: Conversation deleted. Skip and continue.

## Output Schema

For downstream analysis, normalize each conversation to:

```json
{
  "conversation_id": "123",
  "contact_id": "456",
  "contact_email": "user@company.com",
  "company_id": "789",
  "created_at": "2025-01-15T10:30:00Z",
  "closed_at": "2025-01-15T14:20:00Z",
  "state": "closed",
  "tags": ["bug", "billing"],
  "rating": 3,
  "rating_remark": "Took a while to resolve",
  "message_count": 8,
  "time_to_first_reply_seconds": 120,
  "time_to_resolution_seconds": 13800,
  "first_message_body": "I can't export my data..."
}
```

Store normalized data in PostHog as `support_ticket_closed` events or in your CRM (Attio) as activity records on the contact.
