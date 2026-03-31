---
name: posthog-web-analytics
description: Query PostHog Web Analytics API for page-level traffic, bounce rate, session duration, and conversion data
tool: PostHog
product: PostHog
difficulty: Setup
---

# PostHog Web Analytics

Pull website performance data from PostHog's Web Analytics module to measure brand and conversion impact. This fundamental provides page-level metrics that brand refresh plays use to measure before/after impact.

## Prerequisites

- PostHog JS snippet installed on all website pages
- Web Analytics enabled in PostHog project settings (Settings > Web Analytics > Enable)
- At least 1 week of data for baseline metrics

## Query Web Analytics via PostHog API

### Page-level metrics

```
POST https://us.i.posthog.com/api/projects/{PROJECT_ID}/query/

Authorization: Bearer {POSTHOG_PERSONAL_API_KEY}
Content-Type: application/json

{
  "query": {
    "kind": "WebOverviewQuery",
    "dateRange": {
      "date_from": "-30d",
      "date_to": null
    },
    "compare": true
  }
}
```

Returns: visitors, pageviews, sessions, session duration, bounce rate, with period-over-period comparison.

### Top pages by traffic

```
{
  "query": {
    "kind": "WebTopPagesQuery",
    "dateRange": {
      "date_from": "-30d"
    },
    "limit": 50
  }
}
```

### Top entry pages (first page visited)

```
{
  "query": {
    "kind": "WebTopPagesQuery",
    "dateRange": {
      "date_from": "-30d"
    },
    "limit": 20,
    "includeScrollDepth": true,
    "doPathCleaning": true
  }
}
```

### Traffic sources

```
{
  "query": {
    "kind": "WebTopSourcesQuery",
    "dateRange": {
      "date_from": "-30d"
    }
  }
}
```

## Custom HogQL Queries for Brand Metrics

### Conversion rate by page

```sql
SELECT
  properties.$current_url AS page,
  count(DISTINCT person_id) AS visitors,
  countIf(event = 'form_submit' OR event = 'signup_started') AS conversions,
  round(conversions / visitors * 100, 2) AS conversion_rate
FROM events
WHERE timestamp >= now() - interval 30 day
  AND event IN ('$pageview', 'form_submit', 'signup_started')
GROUP BY page
ORDER BY visitors DESC
LIMIT 30
```

### Before/after comparison (brand refresh impact)

```sql
SELECT
  if(timestamp < toDateTime('2026-04-15'), 'before', 'after') AS period,
  count(DISTINCT person_id) AS unique_visitors,
  countIf(event = '$pageview') AS pageviews,
  countIf(event = 'form_submit') AS form_submissions,
  round(form_submissions / unique_visitors * 100, 2) AS conversion_rate,
  avg(session_duration) AS avg_session_seconds
FROM events
WHERE timestamp >= toDateTime('2026-04-01')
  AND timestamp <= toDateTime('2026-04-29')
GROUP BY period
```

Replace `2026-04-15` with your brand refresh launch date.

### Bounce rate by landing page

```sql
SELECT
  properties.$current_url AS landing_page,
  count(DISTINCT $session_id) AS sessions,
  countIf(session_page_count = 1) AS bounced_sessions,
  round(bounced_sessions / sessions * 100, 2) AS bounce_rate
FROM events
WHERE timestamp >= now() - interval 30 day
  AND event = '$pageview'
  AND properties.$is_first_pageview = true
GROUP BY landing_page
HAVING sessions >= 50
ORDER BY sessions DESC
```

## Session Recording Analysis

For qualitative brand audit data, query session recordings:

```
GET https://us.i.posthog.com/api/projects/{PROJECT_ID}/session_recordings/?date_from=-7d&limit=50&events=[{"id":"$pageview","properties":[{"key":"$current_url","value":"/","operator":"exact"}]}]
```

Watch recordings of homepage visitors to observe: where they look first, what they click, where they drop off, and whether the messaging hierarchy matches their scroll behavior.

## Error Handling

- `401 Unauthorized`: API key invalid or lacks project access. Generate a new personal API key in PostHog settings.
- `400 Bad Request`: HogQL syntax error. Validate query syntax.
- `429 Rate Limit`: PostHog rate-limits to 240 requests/minute. Add delays between batch queries.
