---
name: slack-discord-keyword-monitoring
description: Monitor Slack and Discord communities for keyword matches and route alerts to an engagement queue
tool: Common Room
product: Community
difficulty: Config
---

# Slack/Discord Keyword Monitoring

Set up automated keyword monitoring across Slack workspaces and Discord servers to detect engagement opportunities in real time. When a community member asks a question, mentions a competitor, or describes a pain point your product solves, an alert fires to your engagement queue.

## Architecture

```
Slack/Discord communities
  -> Polling or webhook ingestion
  -> Keyword matching + filtering
  -> Priority classification
  -> Alert delivery (Slack/email)
```

## Method 1: n8n Polling (Free, works everywhere)

### Slack Polling Workflow

Using the `n8n-workflow-basics` and `n8n-scheduling` fundamentals:

```
Schedule Trigger (every 30 minutes)
  -> Slack Node (conversations.history):
     Channel: {CHANNEL_ID}
     Limit: 50
     Oldest: {{$now.minus(30, 'minutes').toUnixTimestamp()}}
  -> (Repeat for each monitored channel, run in parallel)
  -> Merge Node (combine all results)
  -> Function Node (keyword match):
     For each message:
       Check message.text against keyword lists:
         pain_keywords: ["struggling with", "anyone know how to", "frustrated", "looking for a tool"]
         buying_keywords: ["recommend", "alternative to", "best tool for", "anyone use"]
         competitor_keywords: ["{competitor1}", "{competitor2}", "switching from"]
       If match found, include: {channel, message_ts, text, user, matched_keywords, keyword_group}
  -> IF Node (filter):
     - message.user != your_user_id (skip your own messages)
     - message has text (skip file-only or join messages)
  -> Switch Node (classify priority):
     - buying_keywords match -> "high"
     - pain_keywords match -> "medium"
     - competitor_keywords match -> "low"
  -> Slack Node (alert to internal channel):
     Channel: #community-engagement-queue
     Message:
       [{priority}] {keyword_group} in #{channel_name}
       > {message_text_preview}
       Keywords: {matched_keywords}
       Link: {slack_message_permalink}
       Respond within: {2h for high / 6h for medium / 24h for low}
```

### Discord Polling Workflow

Same structure, but use HTTP Request nodes to call Discord API:

```
Schedule Trigger (every 30 minutes)
  -> HTTP Request Node:
     GET https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=50&after={LAST_MESSAGE_ID}
     Headers: Authorization: Bot {DISCORD_BOT_TOKEN}
  -> (Repeat for each monitored channel)
  -> Merge + Keyword Match + Filter + Classify + Alert (same as Slack flow)
```

Store `LAST_MESSAGE_ID` in n8n static data to avoid processing duplicates.

## Method 2: Common Room (Paid, multi-platform)

Common Room aggregates activity across Slack, Discord, GitHub, Twitter, and forums into a single feed.

1. **Connect sources:** In Common Room settings, add your Slack workspaces and Discord servers.
2. **Create keyword alerts:**
   - Navigate to Signals > Keyword Alerts
   - Add keyword groups: pain points, buying intent, competitor mentions
   - Set notification destination: Slack webhook or email
3. **Configure member enrichment:** Common Room auto-enriches community members with LinkedIn, GitHub, and company data. This helps prioritize responses to ICP-matching members.

**Pricing:** Common Room offers a free tier for small communities. Paid plans start at $500/mo for larger deployments (https://www.commonroom.io/pricing).

## Method 3: Syften (Paid, real-time alerts)

Syften monitors Slack, Discord, Reddit, Hacker News, and forums for keyword mentions.

1. Create a Syften account at https://syften.com
2. Add keyword filters for each keyword group
3. Select platforms: Slack, Discord
4. Add specific workspace/server names
5. Configure webhook delivery to n8n or email

**Pricing:** Plans start at $19/mo for basic monitoring (https://syften.com/pricing).

## Keyword List Design

### Pain-point keywords
Phrases people use when describing a problem you solve:
- "how do I [problem verb]"
- "anyone else struggling with [problem]"
- "is there a way to [desired outcome]"
- "tired of [manual process]"
- "can't figure out [task]"

### Buying-intent keywords
Signals that someone is actively evaluating tools:
- "looking for a [category] tool"
- "recommend a [category]"
- "best [category] for [use case]"
- "alternative to [competitor]"
- "anyone use [competitor]"
- "switching from [competitor]"
- "what do you use for [workflow]"

### Competitor keywords
Direct mentions of competitors:
- Competitor product names
- "[competitor] vs"
- "[competitor] pricing"
- "[competitor] review"

## Output

- Alerting pipeline that fires within 30 minutes of a keyword match
- Alerts classified by priority (high/medium/low) and keyword group
- Each alert includes: message text, community, channel, author, link, and recommended response time

## Error Handling

- **Token expiry:** Slack user tokens can expire. Set up a weekly token validation check.
- **Channel access lost:** If you are removed from a channel or workspace, the poll will return errors. Log and alert on non-200 responses.
- **Keyword false positives:** Review alert quality weekly. Add negative keywords to reduce noise (e.g., exclude messages containing "hiring" or "job" if those trigger false matches).
- **Duplicate alerts:** Use message timestamps or IDs as deduplication keys. Store the last processed ID per channel.
