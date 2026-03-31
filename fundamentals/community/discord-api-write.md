---
name: discord-api-write
description: Post messages, replies, and reactions in Discord channels via the Discord API
tool: Discord
product: API
difficulty: Setup
---

# Discord API Write

Post messages, thread replies, and reactions in Discord server channels. Used for community engagement -- answering questions, sharing resources, and participating in forum threads.

## Authentication

Same as `discord-api-read`. Requires a bot token with write permissions.

**Required bot permissions (integer: 2048 + 64 + 32768):**
- `SEND_MESSAGES` (2048) - post in text channels
- `ADD_REACTIONS` (64) - add emoji reactions
- `SEND_MESSAGES_IN_THREADS` (32768) - post in threads and forum posts
- `CREATE_PUBLIC_THREADS` (optional, 2048) - start new threads
- `ATTACH_FILES` (optional, 32768) - upload files

**Base URL:** `https://discord.com/api/v10`

## Core Operations

### Post a message to a channel

```
POST /channels/{CHANNEL_ID}/messages
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
  Content-Type: application/json
Body:
{
  "content": "Your message text here"
}
```

Supports Discord Markdown:
- `**bold**`, `*italic*`, `~~strikethrough~~`, `__underline__`
- `` `code` `` and ` ```language\ncode block``` `
- `> quote` and `>>> multiline quote`
- Links auto-embed; suppress with `<https://example.com>`
- User mentions: `<@USER_ID>`
- Channel mentions: `<#CHANNEL_ID>`
- Role mentions: `<@&ROLE_ID>`

### Reply to a message

```
POST /channels/{CHANNEL_ID}/messages
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
  Content-Type: application/json
Body:
{
  "content": "Your reply text",
  "message_reference": {
    "message_id": "{ORIGINAL_MESSAGE_ID}"
  }
}
```

### Create a forum thread post

```
POST /channels/{FORUM_CHANNEL_ID}/threads
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
  Content-Type: application/json
Body:
{
  "name": "Thread title here",
  "message": {
    "content": "First message in the thread"
  },
  "applied_tags": ["{TAG_ID_1}", "{TAG_ID_2}"]
}
```

Forum channels are common in developer and community Discord servers. Creating a well-tagged forum post is equivalent to creating a new discussion thread.

### Reply to a thread

Threads are channels. Use the standard message endpoint:
```
POST /channels/{THREAD_ID}/messages
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
  Content-Type: application/json
Body:
{
  "content": "Your thread reply"
}
```

### Add a reaction

```
PUT /channels/{CHANNEL_ID}/messages/{MESSAGE_ID}/reactions/{EMOJI}/@me
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
```

For standard emoji, URL-encode the emoji character: `%F0%9F%91%8D` (thumbs up).
For custom server emoji: `emoji_name:emoji_id`.

### Edit a message

```
PATCH /channels/{CHANNEL_ID}/messages/{MESSAGE_ID}
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
  Content-Type: application/json
Body:
{
  "content": "Updated message text"
}
```

You can only edit messages sent by your bot.

## Alternative Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Discord API (direct)** | REST API with bot token | Full control |
| **discord.js** | Node.js library | Rich bot interactions |
| **discord.py** | Python library | Script-based automation |
| **n8n Discord node** | Built-in integration | Workflow automation |
| **Make (Integromat)** | Visual automation | Multi-step workflows |

## Rate Limits

Write operations have strict rate limits:
- `POST /channels/{id}/messages`: 5 messages per 5 seconds per channel
- `PUT .../reactions/...`: 1 reaction per 250ms
- Global: 50 requests per second across all endpoints

Community engagement rate: limit to 5-10 messages per server per day to avoid being flagged as a spam bot by moderators.

## Error Handling

- `403 Forbidden`: Bot lacks `SEND_MESSAGES` permission in this channel. Check channel-specific permission overrides.
- `404 Not Found`: Channel or message does not exist. Verify IDs.
- `50006 Cannot execute action on a DM channel`: Tried to use a guild-only operation in DMs.
- `50035 Invalid Form Body`: Message content validation failed (too long, invalid format). Discord messages max at 2000 characters.
- `429 Too Many Requests`: Rate limited. Respect `Retry-After` header.
- `40058 Cannot send messages in a non-text channel`: Tried to post in a voice or category channel. Verify channel type is 0 (text) or 11/12 (thread).

## Community Engagement Guidelines

When using a bot for engagement in third-party servers:
- **Get moderator approval** before adding a bot to someone else's server. Most community servers do not allow random bots.
- **Use a personal account** for organic engagement in third-party communities. Bot accounts are for your own server or servers that explicitly allow your bot.
- **For third-party engagement**, the agent should draft responses that a human posts from their personal Discord account. The agent handles research, drafting, and scheduling; the human handles actual posting.
- **Forum channels** are the best engagement surface. Answer questions with detailed, helpful responses.
- **Respect slow mode** settings. Many community channels have slow mode (1 message per X seconds) to prevent spam.
