---
name: community-monitoring-automation
description: Set up automated monitoring for relevant Reddit threads using Syften webhooks or n8n polling
category: Community
tools:
  - Syften
  - n8n
  - Slack
fundamentals:
  - reddit-keyword-monitoring
  - n8n-workflow-basics
  - n8n-triggers
---

# Community Monitoring Automation

This drill builds an automated pipeline that discovers relevant Reddit threads as they appear and routes them to the right person for engagement. The pipeline runs continuously and replaces manual Reddit browsing.

## Input

- Keyword lists from the `community-reconnaissance` drill (pain-point, category, ICP role keywords)
- Ranked subreddit list from the `community-reconnaissance` drill
- Slack channel for engagement alerts (or email if Slack not available)

## Steps

### 1. Choose monitoring approach

Based on your budget and response-time requirements:

| Approach | Cost | Delay | Best for |
|----------|------|-------|----------|
| **Syften + n8n webhook** | $20-100/mo | ~1 min | Fast response matters, multiple platforms |
| **n8n Reddit polling** | Free | 1-4 hours | Budget-constrained, Reddit-only |
| **Direct API script + cron** | Free | 1-4 hours | Technical team, custom filtering |

For most teams, start with n8n Reddit polling (free) and upgrade to Syften when the play reaches Scalable level.

### 2. Set up Syften monitoring (if using Syften)

Using the `reddit-keyword-monitoring` fundamental:

1. Create a Syften project named "Reddit Community Play"
2. Create filters for each keyword group:

**Filter 1 — Pain points:**
```
Keywords: "struggling with [problem]" OR "frustrated with [problem]" OR "can't figure out [problem]"
Platform: Reddit
Subreddits: [your top-tier subreddits, comma-separated]
```

**Filter 2 — Buying intent:**
```
Keywords: "looking for [category]" OR "recommend a [category]" OR "best [category] tool" OR "alternative to [competitor]"
Platform: Reddit
```

**Filter 3 — Competitor mentions:**
```
Keywords: "[competitor1]" OR "[competitor2]" OR "[competitor1] vs" OR "switch from [competitor]"
Platform: Reddit
```

3. Configure webhook delivery pointing to your n8n instance:
   `https://YOUR-N8N.com/webhook/reddit-alerts`

### 3. Build the n8n ingestion workflow

Using the `n8n-workflow-basics` and `n8n-triggers` fundamentals:

**Workflow: Reddit Alert Processor**

```
Webhook Node (receives Syften alert or Reddit poll results)
  → Set Node (normalize fields: title, url, subreddit, matched_keyword, text, score, num_comments, created_utc)
  → IF Node (FILTER):
      - Post age < 6 hours (fresh enough for early engagement)
      - Score > 0 (not downvoted into oblivion)
      - num_comments < 30 (still room for your comment to be visible)
      - NOT from your own Reddit username
  → Switch Node (CATEGORIZE by matched keyword group):
      - "buying_intent" → High priority
      - "pain_point" → Medium priority
      - "competitor_mention" → Medium priority
      - Other → Low priority
  → Slack Node (ALERT):
      Channel: #reddit-engagement
      Message format:
        🎯 [PRIORITY] New thread in r/[subreddit]
        Title: [title]
        Keywords: [matched_keywords]
        Score: [score] | Comments: [num_comments]
        URL: [url]
        Action: Reply within [2h for high priority / 6h for medium / 24h for low]
```

### 4. Set up n8n polling (if not using Syften)

**Workflow: Reddit Keyword Poller**

```
Schedule Trigger Node (every 4 hours)
  → Reddit Node (Search):
      Query: "looking for [category]" OR "best [category]"
      Subreddit: [target subreddit]
      Sort: new
      Limit: 25
  → (Duplicate Reddit Node for each keyword group, run in parallel)
  → Merge Node (combine all results)
  → Remove Duplicates Node (by post ID)
  → Function Node (filter: created_utc > last_run_timestamp)
  → [Continue with same FILTER, CATEGORIZE, ALERT from step 3]
```

To monitor multiple subreddits, either:
- Use a single Reddit Search node without restricting to a subreddit (searches all of Reddit)
- Create parallel Reddit nodes, one per subreddit, and merge results

### 5. Build the response tracking feedback loop

After someone engages with an alerted thread, they should log the outcome. Add a follow-up workflow:

```
Schedule Trigger (daily at 9am)
  → Slack Node: Post daily summary to #reddit-engagement:
      "Yesterday's engagement results:
       - Threads alerted: X
       - Threads responded to: Y
       - Total upvotes earned: Z
       - Referral sessions (from PostHog): W
       Threads still needing response: [list URLs]"
```

The daily summary data comes from the activity log (per `community-engagement-tracking` fundamental) and PostHog UTM tracking.

### 6. Tune keyword filters

After 1 week of monitoring, review alert quality:
- **Too many irrelevant alerts**: Tighten keywords, add negative keywords, restrict to fewer subreddits
- **Missing relevant threads**: Broaden keywords, add new pain-point phrases, add subreddits
- **Alerts arriving too late**: Upgrade from polling to Syften, or increase polling frequency

Target: 5-15 actionable alerts per day. More than 20 creates alert fatigue. Fewer than 3 means keywords are too narrow.

## Output

- Automated monitoring pipeline (Syften + n8n or n8n-only)
- Slack channel receiving categorized, prioritized thread alerts
- Daily engagement summary workflow
- Tuned keyword filters producing 5-15 actionable alerts/day

## Triggers

- Set up once during Baseline or Scalable level
- Runs continuously (automated)
- Keyword review: weekly for first month, monthly thereafter
