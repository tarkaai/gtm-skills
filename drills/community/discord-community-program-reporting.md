---
name: discord-community-program-reporting
description: Generate weekly Discord community health reports with member growth, engagement cohort analysis, channel ROI, and lead attribution
category: Community
tools:
  - Discord API
  - PostHog
  - n8n
  - Attio
fundamentals:
  - discord-api-read
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-lists
  - attio-reporting
---

# Discord Community Program Reporting

Generate a structured weekly report on Discord community health, member engagement cohorts, channel-level ROI, and lead attribution. This drill produces the data layer that feeds the `autonomous-optimization` drill at Durable level, enabling the optimization loop to detect metric anomalies specific to Discord community dynamics.

## Input

- Discord server with bot access (from Baseline/Scalable setup)
- PostHog tracking events flowing for community-driven traffic
- Attio records for community-sourced leads
- At least 8 weeks of historical data for trend analysis

## Steps

### 1. Build the weekly data collection workflow

Using the `n8n-scheduling` and `n8n-workflow-basics` fundamentals, create a workflow that runs every Monday at 5am:

```
Schedule Trigger (weekly, Monday 5am)
  -> Discord HTTP Request Node:
     GET /guilds/{GUILD_ID}?with_counts=true
     Extract: approximate_member_count, approximate_presence_count
  -> Discord HTTP Request Node:
     GET /guilds/{GUILD_ID}/members?limit=1000
     Paginate through all members. For each member, extract:
       user_id, joined_at, roles, nickname
     Compute: new_members_this_week = members where joined_at > 7_days_ago
     Compute: members_with_role_changes = members whose roles changed this week
  -> Discord HTTP Request Node:
     For each monitored text/forum channel:
       GET /channels/{CHANNEL_ID}/messages?limit=100&after={LAST_WEEK_FIRST_MESSAGE_ID}
       Count: messages_this_week, unique_authors_this_week, threads_created
       Compute: avg_message_length, messages_with_reactions, messages_with_replies
  -> PostHog HTTP Request Node:
     Query: discord_referral_visit events, last 7 days
     Return: {channel: string, sessions: number, signups: number}
  -> Attio HTTP Request Node:
     Query: Contacts where lead_source = "discord-community", created in last 7 days
     Return: {count: number, pipeline_value: number, qualified: number}
```

### 2. Compute engagement cohort metrics

The workflow computes engagement tiers for all members based on the last 30 days:

| Tier | Definition | Action |
|------|-----------|--------|
| Power users | 20+ messages in 30 days, active in 3+ channels | Track by name. These are potential advocates. Sync to Attio as high-value contacts. |
| Regular contributors | 5-19 messages in 30 days | Maintain engagement. Tag for content collaboration opportunities. |
| Occasional participants | 1-4 messages in 30 days | Monitor for drop-off. Send re-engagement prompts if they go silent for 14+ days. |
| Lurkers | 0 messages in 30 days but still in server | Not a problem. Many lurkers read and visit your site. Track via PostHog referral data. |
| Churned | Left the server this week | Log churn reason if available (from audit log). Track churn rate trend. |

Using the `discord-api-read` fundamental, pull the audit log to detect member departures:
```
GET /guilds/{GUILD_ID}/audit-logs?action_type=20&limit=50
```
Action type 20 = MEMBER_KICK, 22 = MEMBER_BAN_ADD. Members who leave voluntarily do not appear in audit logs but can be detected by comparing member lists week over week.

### 3. Compute channel-level ROI

For each channel, calculate:

```
channel_engagement_score = (messages_this_week * 1) + (threads_created * 3) + (reactions * 0.5)
channel_referral_value = referral_sessions * avg_session_value_from_posthog
channel_efficiency = channel_engagement_score / messages_posted_by_team_this_week
```

Rank channels by `channel_referral_value`. Identify:
- **High ROI channels**: Generate referral traffic relative to team effort invested
- **High engagement, low ROI channels**: Active but not driving site visits (may need better CTAs or link placement)
- **Low engagement channels**: Consider archiving or merging with active channels

### 4. Generate the weekly report

Post to Slack and store in Attio:

```markdown
## Discord Community Report — Week of {date}

### Growth
- Total members: {count} ({+/- change} from last week, {growth_rate}% WoW)
- New members this week: {count}
- Members churned this week: {count}
- Net growth: {new - churned}
- 4-week growth trend: {trend_direction}

### Engagement
- Messages this week: {count} ({+/- change}% WoW)
- Unique active members: {count} ({pct_of_total}% of total)
- Threads created: {count}
- Power users: {count} | Regular: {count} | Occasional: {count} | Lurkers: {count}

### Channel Performance
| Channel | Messages | Unique Authors | Referral Sessions | Signups |
|---------|----------|---------------|-------------------|---------|
| #{name} | {count}  | {count}       | {sessions}        | {signups} |

### Lead Attribution
- Referral sessions from Discord: {total}
- Signups attributed to Discord: {count}
- Qualified leads this week: {count}
- Pipeline value attributed: ${amount}
- Cost per qualified lead: ${total_tool_costs / qualified_leads}

### Anomalies
{List any metrics that deviated >20% from 4-week rolling average}

### Recommendations
{AI-generated recommendations based on the data: channels to invest in, content types to increase, members to personally engage}
```

### 5. Feed into autonomous optimization

The report data feeds the `autonomous-optimization` drill. Specifically:

- **Growth metrics** feed the monitor phase: if new member rate drops >20% vs 4-week avg, trigger diagnosis
- **Engagement cohort shifts** feed hypothesis generation: if power users decline, hypothesize content quality issues
- **Channel ROI data** feeds experiment design: test posting frequency, content type, or CTA placement per channel
- **Lead attribution** feeds evaluation: measure whether optimization experiments improved qualified lead output

Store all weekly report data as structured JSON in Attio notes for the Discord community record. This creates the historical dataset the optimization loop needs for trend analysis.

## Output

- Weekly Discord community health report posted to Slack
- Engagement cohort analysis with member tier classifications
- Channel-level ROI rankings
- Lead attribution summary with pipeline value
- Structured data stored in Attio for trend analysis and autonomous optimization input

## Triggers

- Automated: weekly (every Monday)
- Ad-hoc: before monthly community strategy reviews
- Triggered by `autonomous-optimization` drill when it needs fresh data for hypothesis generation
