---
name: discord-api-read
description: Read messages, channels, and member profiles from Discord servers via the Discord API
tool: Discord
product: API
difficulty: Setup
---

# Discord API Read

Read messages, channels, threads, and member profiles from Discord servers. Used for monitoring community discussions, identifying engagement opportunities, and tracking activity.

## Authentication

Discord uses two authentication methods:

**Bot Token:** Create a bot application at https://discord.com/developers/applications. The bot must be invited to the server with appropriate permissions. Bot tokens look like: `MTIzNDU2Nzg5...`.

**User Token (self-bot):** Your personal Discord token. Using this for automation violates Discord TOS and risks account termination. Use bot tokens instead.

For monitoring third-party communities where you cannot add a bot, use the Discord search UI or tools like Common Room that aggregate publicly available data.

**Required bot permissions (integer: 68608):**
- `VIEW_CHANNEL` (1024) - see channels
- `READ_MESSAGE_HISTORY` (65536) - read messages
- `GUILD_MEMBERS` intent - read member list (privileged, requires Discord approval for bots in 100+ servers)

Store token as `DISCORD_BOT_TOKEN` in environment.

**Base URL:** `https://discord.com/api/v10`

## Core Operations

### List server channels

```
GET /guilds/{GUILD_ID}/channels
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
```

Returns all channels with name, id, type (0=text, 2=voice, 4=category, 15=forum), topic, and position. Filter to type 0 (text) and 15 (forum) for community engagement.

### Read channel messages

```
GET /channels/{CHANNEL_ID}/messages
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
Query parameters:
  limit: 100  (max 100)
  before: {MESSAGE_ID}  (pagination: get messages before this ID)
  after: {MESSAGE_ID}  (get messages after this ID)
```

Returns messages with content, author info, timestamp, reactions, and referenced message (if a reply). Page backward using `before` parameter with the oldest message ID from the previous batch.

### Read forum channel threads

```
GET /channels/{CHANNEL_ID}/threads/archived/public
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
Query parameters:
  limit: 100
```

For active threads:
```
GET /guilds/{GUILD_ID}/threads/active
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
```

### Read thread messages

Threads are channels. Use the same messages endpoint:
```
GET /channels/{THREAD_ID}/messages
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
Query parameters:
  limit: 100
```

### Get member profile

```
GET /guilds/{GUILD_ID}/members/{USER_ID}
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
```

Returns nickname, roles, join date, and avatar. For the user's global profile:
```
GET /users/{USER_ID}
Headers:
  Authorization: Bot {DISCORD_BOT_TOKEN}
```

### Search messages (bot limitation)

Discord bots cannot use the search endpoint. Workarounds:
- **Common Room / Orbit:** These platforms index Discord messages and provide search.
- **Custom indexing:** Read all messages from target channels periodically and build a local search index.
- **Discord search UI:** Manual search via the Discord client for ad-hoc queries.

## Alternative Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Discord API (direct)** | REST API with bot token | Servers where you can add a bot |
| **Common Room** | Aggregates Discord activity | Multi-server monitoring, search |
| **Orbit (LF)** | Community analytics | Member engagement tracking |
| **discord.js / discord.py** | SDK libraries | Building custom monitoring bots |
| **n8n Discord node** | Built-in integration | Workflow automation |

## Rate Limits

Discord uses per-route rate limits:
- **Global:** 50 requests per second
- **Per route:** Varies. `GET /channels/{id}/messages` allows ~5 requests per 5 seconds.
- Rate limit info is returned in headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

Implement rate limit handling:
1. Check `X-RateLimit-Remaining` before each request.
2. If 0, wait until `X-RateLimit-Reset` timestamp.
3. If you receive 429, respect the `Retry-After` header.

## Error Handling

- `401 Unauthorized`: Token is invalid or expired. Re-check bot token.
- `403 Forbidden`: Bot lacks permissions in this channel/server. Check bot role permissions.
- `404 Not Found`: Channel or guild does not exist, or bot is not a member. Verify IDs.
- `429 Too Many Requests`: Rate limited. Wait for `Retry-After` seconds.
- `50001 Missing Access`: Bot cannot see this channel. Ensure the bot role has `VIEW_CHANNEL` permission for the specific channel or category.
