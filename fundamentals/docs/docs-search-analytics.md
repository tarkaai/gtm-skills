---
name: docs-search-analytics
description: Track and extract what users search for within docs site search and identify content gaps
tool: Algolia / Mintlify / PostHog
difficulty: Config
---

# Docs Search Analytics

Extract search queries from your docs site's internal search to identify what users are looking for, what they cannot find, and where content gaps exist. This data drives documentation content strategy.

## Option 1: Algolia DocSearch (most common)

Many docs platforms (Mintlify, Docusaurus, GitBook) use Algolia for site search.

**Authentication:**
```
X-Algolia-Application-Id: {APP_ID}
X-Algolia-API-Key: {ANALYTICS_API_KEY}
Base URL: https://analytics.algolia.com/2
```

**Pull top searches (last 30 days):**
```
GET /searches?index={index_name}&limit=100&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
```

Response includes: `search`, `count`, `nbHits` (number of results returned).

**Pull searches with no results:**
```
GET /searches/noResults?index={index_name}&limit=100&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
```

These are the highest-priority content gaps: users searched for something and found nothing.

**Pull click-through rate per search:**
```
GET /searches?index={index_name}&limit=100&clickAnalytics=true&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
```

Response adds: `clickThroughRate`, `clickPositions`. Low CTR on high-volume searches means the existing content does not match user intent.

## Option 2: PostHog Custom Event Tracking

If your docs platform does not expose search analytics natively, instrument via PostHog.

**Track search events:**
```javascript
// On search input submission
posthog.capture('docs_search_submitted', {
  query: searchQuery,
  results_count: resultCount,
  page_url: window.location.href
});

// On search result click
posthog.capture('docs_search_result_clicked', {
  query: searchQuery,
  clicked_url: resultUrl,
  click_position: resultIndex,
  page_url: window.location.href
});
```

**Query search data via PostHog API:**
```
POST https://app.posthog.com/api/projects/{project_id}/query
Authorization: Bearer {POSTHOG_API_KEY}

{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT properties.query, count() as search_count, avg(properties.results_count) as avg_results FROM events WHERE event = 'docs_search_submitted' AND timestamp > now() - interval 30 day GROUP BY properties.query ORDER BY search_count DESC LIMIT 100"
  }
}
```

**Find zero-result searches:**
```sql
SELECT properties.query, count() as search_count
FROM events
WHERE event = 'docs_search_submitted'
  AND properties.results_count = 0
  AND timestamp > now() - interval 30 day
GROUP BY properties.query
ORDER BY search_count DESC
LIMIT 50
```

## Option 3: Mintlify Analytics

Mintlify provides built-in search analytics via its dashboard API.

**Authentication:**
```
Authorization: Bearer {MINTLIFY_API_KEY}
```

**Pull search analytics:**
```
GET /api/analytics/search?startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
```

Returns top searches, no-result searches, and search-to-page-view conversion rate.

## Output Format

Produce a structured report:

```json
{
  "period": "2026-03-01 to 2026-03-30",
  "total_searches": 1245,
  "unique_queries": 342,
  "top_searches": [
    {"query": "authentication", "count": 89, "results": 5, "ctr": 0.62},
    {"query": "rate limits", "count": 67, "results": 3, "ctr": 0.45}
  ],
  "zero_result_searches": [
    {"query": "webhook retry", "count": 34},
    {"query": "batch api", "count": 28}
  ],
  "low_ctr_searches": [
    {"query": "error codes", "count": 45, "results": 2, "ctr": 0.11}
  ]
}
```

Zero-result and low-CTR queries are the input for content gap analysis and new page creation.

## Error Handling

- **Algolia 403:** API key lacks analytics permissions. Generate a new key with Analytics scope.
- **PostHog returns empty:** Verify the search tracking JavaScript is firing. Check the event name matches exactly.
- **Low search volume:** If total searches < 50/month, the site may not have enough traffic yet. Focus on GSC search query data instead.
