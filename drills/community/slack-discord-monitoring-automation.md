---
name: slack-discord-monitoring-automation
description: Set up automated monitoring for relevant Slack/Discord threads using keyword polling and alert routing
category: Community
tools:
  - n8n
  - Slack API
  - Discord API
  - Common Room
fundamentals:
  - slack-discord-keyword-monitoring
  - slack-api-read
  - discord-api-read
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
---

# Slack/Discord Monitoring Automation

Build an automated pipeline that detects engagement opportunities in Slack workspaces and Discord servers as they appear and routes them to a response queue. Replaces manual community browsing with structured, prioritized alerts.

## Input

- Keyword lists from the `slack-discord-reconnaissance` drill
- Ranked community list with key channel IDs from `slack-discord-reconnaissance`
- Internal Slack channel for engagement alerts (e.g., #community-engagement-queue)

## Steps

### 1. Choose monitoring approach

| Approach | Cost | Latency | Best for |
|----------|------|---------|----------|
| **n8n polling + Slack/Discord API** | Free | 15-60 min | Budget-constrained, moderate response time OK |
| **Common Room** | $500+/mo | ~5 min | Multi-platform, rich member enrichment, at scale |
| **Syften + n8n webhook** | $19-100/mo | ~1 min | Fast response, cross-platform |

For Smoke/Baseline: use n8n polling (free). Upgrade to Common Room or Syften at Scalable/Durable.

### 2. Build Slack monitoring workflow in n8n

Using the `slack-discord-keyword-monitoring` fundamental and `n8n-workflow-basics`:

```
Schedule Trigger (every 30 minutes)
  -> Slack Node (conversations.history):
     For each monitored channel (run in parallel):
       Channel: {CHANNEL_ID}
       Limit: 50
       Oldest: {{$now.minus(30, 'minutes').toUnixTimestamp()}}
  -> Merge Node (combine all channel results)
  -> Function Node (keyword match):
     For each message:
       Match against pain_keywords, buying_keywords, competitor_keywords
       Classify match as high/medium/low priority
       Skip messages from your own user ID
       Skip messages that are just emoji reactions or joins
  -> IF Node (has_match == true)
  -> Slack Node (post alert to #community-engagement-queue):
     [{priority}] {keyword_group} match in {workspace} #{channel}
     > {message_preview_first_200_chars}
     Keywords matched: {matched_keywords}
     Link: {slack_message_permalink}
     Author: {display_name} | {title}
     Respond within: {2h for high / 6h for medium / 24h for low}
```

### 3. Build Discord monitoring workflow in n8n

```
Schedule Trigger (every 30 minutes)
  -> HTTP Request Node:
     For each monitored channel (run in parallel):
       GET https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=50&after={LAST_MESSAGE_ID}
       Headers: Authorization: Bot {DISCORD_BOT_TOKEN}
  -> Merge Node
  -> Function Node (keyword match — same logic as Slack)
  -> IF Node (has_match == true)
  -> Slack Node (post alert):
     [{priority}] {keyword_group} match in {server} #{channel}
     > {message_preview}
     Keywords: {matched_keywords}
     Author: {username}
     Link: https://discord.com/channels/{GUILD_ID}/{CHANNEL_ID}/{MESSAGE_ID}
     Respond within: {response_time_by_priority}
```

Store `LAST_MESSAGE_ID` per channel in n8n static data to process only new messages.

### 4. Build the response tracking feedback loop

After someone engages with an alerted thread, track the outcome. Add a daily summary workflow:

```
Schedule Trigger (daily at 9am)
  -> Function Node: Count yesterday's alerts by priority and community
  -> Slack Node: Post to #community-engagement-queue:
     Community Engagement Summary — {date}
     Threads alerted: {total} (high: {h}, medium: {m}, low: {l})
     Threads responded to: {responded}
     Referral sessions (PostHog): {sessions}
     Top community: {highest_volume_community}
     Threads still needing response: {pending_count}
```

Pull response tracking data from the activity log (`community-engagement-tracking` fundamental) and PostHog UTM data.

### 5. Tune keyword filters (weekly for first month)

After 1 week of monitoring, review:
- **Too many alerts (>20/day):** Tighten keywords. Add negative keywords (e.g., "hiring", "job posting"). Restrict to fewer channels.
- **Too few alerts (<3/day):** Broaden keywords. Add new pain-point phrases. Add more communities.
- **Low quality alerts:** Review which keyword groups produce the most false positives. Refine those groups.
- **Missed opportunities:** Browse communities manually and compare with what alerts caught. Add keywords for what was missed.

Target: 5-15 actionable alerts per day across all monitored communities.

## Output

- Automated monitoring pipeline covering Slack and Discord communities
- Internal Slack channel receiving prioritized engagement alerts
- Daily summary of alert volume and response metrics
- Keyword filters tuned to produce 5-15 actionable alerts/day

## Triggers

- Set up once during Baseline level
- Runs continuously (automated)
- Keyword review: weekly for first month, then monthly
- Community list review: monthly (add new communities, drop inactive ones)
