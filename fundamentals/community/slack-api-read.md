---
name: slack-api-read
description: Read messages, channels, and user profiles from Slack workspaces via the Slack Web API
tool: Slack
product: API
difficulty: Setup
---

# Slack API Read

Read messages, channels, threads, and user profiles from Slack workspaces where you are a member. This fundamental covers all read operations needed for community engagement monitoring.

## Authentication

Slack uses OAuth 2.0 tokens. You need either:

**User Token (`xoxp-...`):** Acts as you. Required for reading channels in workspaces you joined as a personal account. Needed for most community engagement scenarios where you joined a public Slack community.

**Bot Token (`xoxb-...`):** Acts as a bot in a workspace you own or where a bot was installed. Useful for monitoring your own community, not for third-party community engagement.

For community engagement in third-party Slack communities, you typically use the Slack web interface or a user token from a Slack app you created in your own workspace with the appropriate scopes.

**Required scopes (user token):**
- `channels:read` - list public channels
- `channels:history` - read messages in public channels
- `groups:read` - list private channels you belong to
- `groups:history` - read messages in private channels
- `users:read` - read user profiles
- `search:read` - search messages
- `team:read` - read workspace info

Store token as `SLACK_USER_TOKEN` in environment.

## Core Operations

### List channels in a workspace

```
GET https://slack.com/api/conversations.list
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
Query parameters:
  types: public_channel,private_channel
  limit: 200
  exclude_archived: true
```

Response includes channel name, id, member count, topic, purpose, and num_members. Page through results using `cursor` from `response_metadata.next_cursor`.

### Read channel history

```
GET https://slack.com/api/conversations.history
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
Query parameters:
  channel: {CHANNEL_ID}
  limit: 100
  oldest: {UNIX_TIMESTAMP}  (optional: only messages after this time)
  latest: {UNIX_TIMESTAMP}  (optional: only messages before this time)
```

Returns messages with text, user ID, timestamp, reactions, and thread metadata. For threaded conversations, use `conversations.replies`.

### Read thread replies

```
GET https://slack.com/api/conversations.replies
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
Query parameters:
  channel: {CHANNEL_ID}
  ts: {THREAD_TS}  (timestamp of the parent message)
  limit: 100
```

### Search messages across workspace

```
GET https://slack.com/api/search.messages
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
Query parameters:
  query: "{keyword}"
  sort: timestamp
  sort_dir: desc
  count: 20
```

Search supports operators:
- `in:#channel-name` - limit to specific channel
- `from:@username` - messages from a specific user
- `has:link` - messages containing links
- `before:2026-03-01` / `after:2026-03-01` - date range
- `"exact phrase"` - exact phrase match

### Get user profile

```
GET https://slack.com/api/users.info
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
Query parameters:
  user: {USER_ID}
```

Returns display name, real name, title, status, timezone, and profile image.

### Get workspace info

```
GET https://slack.com/api/team.info
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
```

Returns workspace name, domain, member count, and icon.

## Alternative Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Slack API (direct)** | OAuth user token, full API access | Workspaces where you have a token |
| **Common Room** | Aggregates Slack activity across communities | Multi-community monitoring at scale |
| **Orbit (now LF)** | Community analytics platform with Slack integration | Community health tracking |
| **Linen.dev** | Makes Slack conversations searchable/indexable | Discovering content in public Slack communities |
| **n8n Slack node** | Built-in Slack integration for automation | Workflow automation with Slack data |

## Rate Limits

Slack API uses tiered rate limits:
- **Tier 1 (special):** 1 request per minute (e.g., `search.messages`)
- **Tier 2:** 20 requests per minute (e.g., `conversations.history`)
- **Tier 3:** 50 requests per minute (e.g., `conversations.list`)
- **Tier 4:** 100 requests per minute (e.g., `users.info`)

When rate limited, the response includes a `Retry-After` header. Implement exponential backoff.

## Error Handling

- `not_authed` / `invalid_auth`: Token is missing or expired. Re-authenticate.
- `channel_not_found`: You are not a member of this channel or it does not exist. Join the channel first.
- `missing_scope`: Token lacks required permissions. Add the scope to your Slack app and re-authorize.
- `ratelimited`: Back off for the duration specified in `Retry-After` header.
- `account_inactive`: The workspace has been deactivated or you were removed. Remove from monitoring list.
