---
name: reddit-keyword-monitoring
description: Monitor Reddit for keyword mentions using Syften, n8n Reddit node, or direct API polling
tool: Syften / n8n / Reddit API
difficulty: Config
---

# Reddit Keyword Monitoring

Set up real-time or near-real-time monitoring for keywords relevant to your product, competitors, and ICP pain points across Reddit. This fundamental covers three approaches ranked by reliability.

## Option 1: Syften (Recommended for speed and coverage)

Syften monitors Reddit, Hacker News, X, Discourse, Slack communities, Stack Overflow, and more with ~1 minute delay.

### Setup

1. Sign up at https://syften.com (14-day free trial, plans from $19.95/mo)
2. Create a "Project" for your monitoring campaign
3. Add keyword filters — these are the search queries Syften runs continuously

### Configuring Filters

Create filters for each monitoring category:

**Pain point keywords** (what your ICP complains about):
```
Filter: "struggling with [problem]" OR "frustrated with [problem]" OR "looking for [solution category]"
Platforms: Reddit
Subreddits: (leave blank to monitor all, or specify target subreddits)
```

**Competitor mentions**:
```
Filter: "competitor-name" OR "competitor-name alternative" OR "competitor-name vs"
Platforms: Reddit
```

**Product category keywords**:
```
Filter: "[your category] tool" OR "[your category] software" OR "best [your category]"
Platforms: Reddit
```

### Alert Delivery

Configure alerts to deliver via:
- **Webhook** (best for automation): Set up a webhook URL pointing to your n8n instance. Syften sends a POST with `{title, url, text, source, matched_keyword, created_at}`.
- **Slack**: Direct integration for human review before engaging.
- **Email**: Daily digest or real-time alerts.
- **RSS**: For consumption by other tools.

### Pricing

| Plan | Price | Filters | Alerts |
|------|-------|---------|--------|
| Entry | $19.95/mo | 5 filters | Email, Slack, Webhook, RSS |
| Standard | $39.95/mo | 15 filters | Same + priority support |
| Pro | $99.95/mo | 50 filters | Same + API access |

## Option 2: n8n Reddit Node (Self-hosted, free)

Build a polling workflow in n8n that checks target subreddits on a schedule.

### Setup

1. In n8n, add Reddit OAuth2 credentials (Client ID, Client Secret, Username, Password)
2. Create a new workflow with a Schedule Trigger node

### Workflow Pattern

```
Schedule Trigger (every 4 hours)
  → Reddit Node (Search: query="looking for [category]", subreddit="target_sub", sort="new", limit=25)
  → Filter Node (exclude posts older than 4 hours, exclude your own posts)
  → IF Node (check if post score > 1 AND num_comments < 20 — sweet spot for early engagement)
  → Slack Node (send alert with post title, URL, and matched keyword)
```

### Multiple Keyword Monitoring

Chain multiple Reddit Search nodes in parallel, one per keyword group. Merge results and deduplicate by post ID before alerting.

### Advantages

- Free (self-hosted n8n)
- Full control over filtering logic
- Can integrate directly with your response workflow

### Limitations

- Polling delay (4-hour minimum recommended to stay within rate limits)
- Misses fast-moving threads where early comments matter most
- Must manage Reddit API rate limits across all n8n workflows

## Option 3: Direct Reddit API Polling (Lowest level)

Use the `reddit-api-read` fundamental to poll subreddits directly via cron or a script.

### Polling Script Pattern

```python
import praw
import json
from datetime import datetime, timedelta

reddit = praw.Reddit(client_id="ID", client_secret="SECRET",
                     user_agent="Monitor/1.0", username="USER", password="PASS")

KEYWORDS = ["looking for", "alternative to", "best tool for", "struggling with"]
SUBREDDITS = ["SaaS", "startups", "smallbusiness", "Entrepreneur"]
SEEN_FILE = "seen_posts.json"

seen = json.load(open(SEEN_FILE)) if os.path.exists(SEEN_FILE) else []
cutoff = datetime.utcnow() - timedelta(hours=4)

for sub_name in SUBREDDITS:
    for post in reddit.subreddit(sub_name).new(limit=50):
        if post.id in seen:
            continue
        if datetime.utcfromtimestamp(post.created_utc) < cutoff:
            continue
        text = f"{post.title} {post.selftext}".lower()
        matched = [kw for kw in KEYWORDS if kw.lower() in text]
        if matched:
            # Send alert (Slack webhook, email, etc.)
            print(f"MATCH in r/{sub_name}: {post.title} | Keywords: {matched}")
            print(f"  URL: https://reddit.com{post.permalink}")
        seen.append(post.id)

json.dump(seen[-10000:], open(SEEN_FILE, "w"))
```

Run via cron every 4 hours. This is the lowest-cost option but requires the most maintenance.

## Error Handling

- **Rate limited**: Back off and increase polling interval
- **Subreddit not found**: Verify the subreddit name hasn't changed or been banned
- **No results**: Check keyword specificity — too broad returns noise, too narrow returns nothing
- **Syften webhook failures**: Configure retry logic in n8n for webhook ingestion
