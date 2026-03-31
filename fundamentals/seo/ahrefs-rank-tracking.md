---
name: ahrefs-rank-tracking
description: Monitor keyword ranking positions over time via the Ahrefs Rank Tracker API
tool: Ahrefs
difficulty: Config
---

# Ahrefs Rank Tracking API

Track keyword positions over time to measure SEO performance. Monitor ranking changes, detect drops, and identify pages gaining or losing visibility.

## Authentication

```
Authorization: Bearer {AHREFS_API_TOKEN}
```

Rank Tracker requires Ahrefs Standard ($199/mo) or higher.

## Core Operations

### Get current rankings for your domain

```
GET https://api.ahrefs.com/v3/site-explorer/organic-keywords
Authorization: Bearer {token}

Query params:
  target=example.com
  country=us
  select=keyword,position,volume,traffic,url,best_position,best_position_timestamp
  where=position<=50
  order_by=traffic:desc
  limit=1000
  offset=0
```

Response fields: `keyword`, `position` (current SERP position), `volume`, `traffic` (estimated monthly organic traffic from this keyword), `url` (ranking page), `best_position` (highest rank achieved), `best_position_timestamp`.

### Get ranking history for specific keywords

```
GET https://api.ahrefs.com/v3/rank-tracker/positions-history
Authorization: Bearer {token}

Query params:
  target=example.com
  keywords=crm+for+startups,crm+for+agencies
  country=us
  date_from=2026-01-01
  date_to=2026-03-30
```

Returns daily position data per keyword. Use to chart ranking trends and detect algorithm impacts.

### Get new and lost keywords

```
GET https://api.ahrefs.com/v3/site-explorer/organic-keywords-new
Authorization: Bearer {token}

Query params:
  target=example.com
  country=us
  date_from=2026-03-01
  date_to=2026-03-30
  select=keyword,position,volume,traffic,url,first_seen
  limit=500
```

Similarly, use `/organic-keywords-lost` to find keywords you dropped out of the top 100.

### Get page-level organic traffic

```
GET https://api.ahrefs.com/v3/site-explorer/top-pages
Authorization: Bearer {token}

Query params:
  target=example.com
  country=us
  select=url,organic_traffic,organic_keywords,value
  order_by=organic_traffic:desc
  limit=200
```

Use to identify which programmatic pages drive the most traffic and which need optimization.

## Rate Limits

- 60 requests per minute
- Subject to monthly API unit allocation

## Error Handling

- `401 Unauthorized`: Invalid API token.
- `429 Too Many Requests`: Rate limit. Implement 60-second backoff.
- `403 Forbidden`: Endpoint requires a higher plan tier.

## Pricing

Included in Ahrefs subscription. See `ahrefs-keyword-research` fundamental for plan details.
Pricing page: https://ahrefs.com/pricing

## Alternatives

- **SEMrush Position Tracking** ($129.95/mo+): Daily rank tracking with API access
- **AccuRanker** ($116/mo+): Dedicated rank tracker with API, fast daily updates
- **SERPWatcher by Mangools** ($29.90/mo+): Budget rank tracking
- **DataForSEO SERP API** ($0.002/request): Pay-per-use rank checking
- **Nightwatch** ($39/mo+): Rank tracking with API and white-label reporting
