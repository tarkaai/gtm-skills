---
name: qa-question-monitoring
description: Monitor Q&A platforms for new questions matching target keywords and tags via polling or RSS
tool: Stack Exchange API
difficulty: Config
---

# Q&A Question Monitoring

Set up automated monitoring for new questions on Q&A platforms that match your target keywords and tags. This enables responding within hours of a question being posted, which is critical for visibility on Stack Overflow (early answers get the most upvotes).

## Stack Overflow -- Tag-Based Polling

### Via Stack Exchange API

Poll for new questions in your target tags every 30 minutes:

```bash
# Get questions created in the last 30 minutes, tagged with your target tags
curl "https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&tagged=TAG1;TAG2&fromdate=UNIX_TIMESTAMP_30MIN_AGO&site=stackoverflow&key=YOUR_API_KEY&filter=withbody&pagesize=50"
```

Compute `fromdate` as current Unix timestamp minus 1800 (30 minutes).

### Via n8n Workflow

Build a polling workflow:

```
Schedule Trigger (every 30 minutes)
  -> HTTP Request Node:
     URL: https://api.stackexchange.com/2.3/search/advanced
     Params:
       order: desc
       sort: creation
       tagged: your-tag-1;your-tag-2
       fromdate: {{$now.minus(30, 'minutes').toUnixInteger()}}
       site: stackoverflow
       key: YOUR_API_KEY
       filter: withbody
       pagesize: 50
  -> Function Node (filter):
     - Remove questions already seen (check against a stored list of processed question_ids)
     - Remove questions with accepted answers
     - Remove questions from users with <10 reputation (often low quality)
     - Score remaining by: (view_count * 0.3) + (score * 0.3) + (no_accepted_answer * 0.4)
  -> IF Node:
     - High priority: score > 0 AND answer_count == 0 AND question_score >= 0
     - Medium priority: answer_count <= 2 AND no accepted answer
     - Low priority: everything else
  -> Slack Node:
     Channel: #qa-engagement
     Message:
       [PRIORITY] New question on Stack Overflow
       Title: {{title}}
       Tags: {{tags}}
       Score: {{score}} | Views: {{view_count}} | Answers: {{answer_count}}
       URL: {{link}}
       Posted: {{creation_date | toHuman}}
       Action: Answer within {{priority == 'high' ? '2h' : '6h'}}
```

### Store processed IDs

Use n8n's static data or an external store (Redis, Airtable, or a JSON file) to track processed question IDs. This prevents duplicate alerts:

```javascript
// In n8n Function node
const staticData = $getWorkflowStaticData('global');
if (!staticData.seenIds) staticData.seenIds = [];

const newQuestions = items.filter(item => {
  const qid = item.json.question_id;
  if (staticData.seenIds.includes(qid)) return false;
  staticData.seenIds.push(qid);
  // Keep only last 1000 IDs to prevent unbounded growth
  if (staticData.seenIds.length > 1000) staticData.seenIds = staticData.seenIds.slice(-1000);
  return true;
});

return newQuestions;
```

## Stack Overflow -- RSS Feed Monitoring

Stack Overflow provides RSS feeds for tags:

```
https://stackoverflow.com/feeds/tag/TAG_NAME
```

Monitor via n8n's RSS Feed Trigger node:
- Set feed URL to `https://stackoverflow.com/feeds/tag/YOUR_TAG`
- Poll interval: 15 minutes
- Parse title, link, and published date from feed items

RSS is simpler but provides less metadata than the API (no view count, no answer count). Use RSS for quick setup; switch to API polling for production.

## Dev.to -- Tag Monitoring

Poll Dev.to for new articles with help/discuss tags:

```bash
curl "https://dev.to/api/articles?tag=help&top=1&per_page=30" \
  -H "api-key: YOUR_DEV_TO_API_KEY"
```

Or use Dev.to's RSS feeds:

```
https://dev.to/feed/tag/help
https://dev.to/feed/tag/discuss
```

## Quora -- Keyword Monitoring via Search

Since Quora has no API, monitor via Google search:

```bash
# Using SerpAPI -- find new Quora questions in the last day
curl "https://serpapi.com/search.json?engine=google&q=site:quora.com+YOUR+KEYWORDS&tbs=qdr:d&api_key=YOUR_SERPAPI_KEY&num=20"
```

The `tbs=qdr:d` parameter restricts results to the last 24 hours. Run daily.

Alternatively, use Syften ($20-100/mo) which monitors Quora natively and sends webhook alerts.

## Multi-Platform Monitoring Workflow (n8n)

Combine all sources into a single n8n workflow:

```
Schedule Trigger (every 30 minutes)
  -> [Parallel branches]:
     Branch 1: Stack Overflow API poll (tags: your-tags)
     Branch 2: Dev.to API poll (tags: help, discuss)
     Branch 3: SerpAPI Quora search (daily)
  -> Merge Node (combine all results)
  -> Function Node:
     Normalize to common schema:
     {
       platform: "stackoverflow" | "devto" | "quora",
       title: string,
       url: string,
       tags: string[],
       answer_count: number,
       views: number,
       created_at: ISO date,
       priority: "high" | "medium" | "low"
     }
  -> Remove Duplicates (by url)
  -> Filter (remove already-processed)
  -> Slack Alert
```

## Tuning

After 1 week of monitoring, adjust:
- **Too many alerts (>20/day)**: Narrow tags, add negative keywords, increase minimum question score
- **Too few alerts (<3/day)**: Broaden tags, add related tags, include more Stack Exchange sites
- **Low quality alerts**: Increase minimum poster reputation, exclude questions with negative scores
- **Target**: 5-15 actionable questions per day across all platforms

## Error Handling

- **API quota exhausted**: Stack Exchange resets daily at midnight UTC. Switch to RSS feed as fallback.
- **Stale alerts**: Discard questions older than 24 hours (response window has passed for maximum visibility).
- **Duplicate detection failure**: Use URL as the dedup key (more reliable than title matching).
