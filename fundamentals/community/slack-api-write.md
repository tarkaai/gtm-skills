---
name: slack-api-write
description: Post messages, replies, and reactions in Slack channels via the Slack Web API
tool: Slack API
difficulty: Setup
---

# Slack API Write

Post messages, thread replies, and reactions to Slack channels. Used for community engagement — responding to questions, sharing resources, and participating in discussions.

## Authentication

Same as `slack-api-read`. Requires a user token (`xoxp-...`) with write scopes:

**Required scopes:**
- `chat:write` - post messages
- `reactions:write` - add emoji reactions
- `files:write` - upload files (optional, for sharing screenshots or docs)

Store token as `SLACK_USER_TOKEN` in environment.

## Core Operations

### Post a message to a channel

```
POST https://slack.com/api/chat.postMessage
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
  Content-Type: application/json
Body:
{
  "channel": "{CHANNEL_ID}",
  "text": "Your message text here",
  "unfurl_links": true,
  "unfurl_media": true
}
```

Supports Slack's mrkdwn formatting:
- `*bold*`, `_italic_`, `~strikethrough~`
- `` `code` `` and ` ```code block``` `
- Bullet lists with `- ` or `* `
- Links: `<https://example.com|display text>`
- User mentions: `<@USER_ID>`
- Channel mentions: `<#CHANNEL_ID>`

### Reply to a thread

```
POST https://slack.com/api/chat.postMessage
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
  Content-Type: application/json
Body:
{
  "channel": "{CHANNEL_ID}",
  "text": "Your reply text",
  "thread_ts": "{PARENT_MESSAGE_TS}"
}
```

Always reply in threads when responding to existing discussions. Top-level messages in active channels get buried quickly.

### Add a reaction

```
POST https://slack.com/api/reactions.add
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
  Content-Type: application/json
Body:
{
  "channel": "{CHANNEL_ID}",
  "timestamp": "{MESSAGE_TS}",
  "name": "thumbsup"
}
```

Reactions are low-effort engagement signals. Use them to acknowledge messages before crafting a full response.

### Update a message

```
POST https://slack.com/api/chat.update
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
  Content-Type: application/json
Body:
{
  "channel": "{CHANNEL_ID}",
  "ts": "{MESSAGE_TS}",
  "text": "Updated message text"
}
```

### Schedule a message

```
POST https://slack.com/api/chat.scheduleMessage
Headers:
  Authorization: Bearer {SLACK_USER_TOKEN}
  Content-Type: application/json
Body:
{
  "channel": "{CHANNEL_ID}",
  "text": "Your scheduled message",
  "post_at": {UNIX_TIMESTAMP}
}
```

Useful for posting during peak activity hours in different timezones.

## Alternative Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Slack API (direct)** | REST API with user token | Full control over posting |
| **n8n Slack node** | Built-in integration, no code | Automated posting workflows |
| **Zapier Slack** | No-code automation | Simple triggers and actions |
| **Make (Integromat)** | Visual automation | Complex multi-step workflows |
| **Slack CLI** | Command-line interface | Script-based automation |

## Rate Limits

Write operations have stricter limits:
- `chat.postMessage`: 1 message per second per channel, burst up to 1 per second
- `reactions.add`: Tier 3 (50 per minute)
- `chat.scheduleMessage`: Tier 3 (50 per minute)

Posting too frequently in a community channel will trigger spam detection by community moderators even if API limits are not hit. Limit to 2-3 messages per community per day maximum.

## Error Handling

- `channel_not_found`: Channel ID is wrong or you are not a member. Verify channel ID.
- `not_in_channel`: You must join the channel before posting. Use `conversations.join` first.
- `msg_too_long`: Messages over 40,000 characters are rejected. Split into multiple messages.
- `restricted_action`: Workspace admin has restricted posting in this channel. Check channel permissions.
- `is_archived`: Channel is archived and read-only. Remove from active engagement list.
- `too_many_attachments`: Limit file uploads to 10 per message.

## Community Engagement Guidelines

When posting via API in third-party communities:
- **Never automate introductory posts.** First messages in a new community should be manually crafted.
- **Match the community's tone.** Read 50+ messages before posting.
- **Respect channel topics.** Post product questions in #tools or #recommendations, not #general.
- **Thread replies are preferred** over top-level messages in most communities.
- **No unsolicited DMs.** Only DM someone after a public conversation where they expressed interest.
