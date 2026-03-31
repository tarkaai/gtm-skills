---
name: directory-analytics-scraping
description: Pull listing analytics, ranking positions, and competitive data from software directories
tool: G2
product: G2
difficulty: Config
---

# Directory Analytics Scraping

Pull performance metrics, category rankings, and competitive intelligence from software directories. This fundamental covers both API-based analytics retrieval and structured scraping for directories without robust analytics APIs.

## G2 Analytics API

### Profile performance

**Endpoint:** `GET https://seller.g2.com/api/v1/products/{product_id}/analytics`

```
Headers:
  Authorization: Bearer {G2_API_TOKEN}

Query parameters:
  period: "30d"  # Options: 7d, 30d, 90d, 12m
  metrics: "views,clicks,comparisons,reviews"
```

**Response:**
```json
{
  "period": "30d",
  "metrics": {
    "profile_views": 1245,
    "comparison_views": 387,
    "clicks_to_website": 89,
    "review_count": 3,
    "average_rating": 4.6,
    "category_rank": 12,
    "category_total": 156,
    "satisfaction_score": 92
  },
  "daily": [
    { "date": "2026-03-01", "views": 42, "clicks": 3 },
    { "date": "2026-03-02", "views": 38, "clicks": 2 }
  ]
}
```

### Category ranking position

**Endpoint:** `GET https://seller.g2.com/api/v1/products/{product_id}/rankings`

```
Query parameters:
  category_id: "category-123"
```

Returns your product's position on the G2 Grid (Leader, High Performer, Contender, Niche), satisfaction score, market presence score, and rank within each quadrant.

### Competitor comparison

**Endpoint:** `GET https://seller.g2.com/api/v1/products/{product_id}/competitors`

Returns list of products frequently compared to yours, with their review counts, ratings, and relative ranking positions.

## Capterra Analytics (Gartner Digital Markets)

### Campaign performance

**Endpoint:** `GET https://api.gartnerdigitalmarkets.com/v1/campaigns/{campaign_id}/performance`

```
Headers:
  Authorization: Bearer {CAPTERRA_API_TOKEN}

Query parameters:
  date_from: "2026-03-01"
  date_to: "2026-03-31"
```

**Response:**
```json
{
  "impressions": 8500,
  "clicks": 127,
  "ctr": 0.015,
  "spend": 508.00,
  "avg_cpc": 4.00,
  "conversions": 12,
  "cost_per_conversion": 42.33
}
```

### Listing performance (organic)

**Endpoint:** `GET https://api.gartnerdigitalmarkets.com/v1/products/{product_id}/analytics`

Returns: organic views, organic clicks, review count, average rating, category position.

## Product Hunt Analytics

### Post performance via GraphQL

```graphql
{
  post(slug: "your-product") {
    id
    name
    votesCount
    commentsCount
    reviewsCount
    dailyRank
    weeklyRank
    featuredAt
    createdAt
    topics { edges { node { name } } }
    makers { id name }
  }
}
```

### Historical performance (requires Pro plan)

```graphql
{
  post(slug: "your-product") {
    analytics {
      views
      clicks
      weeklyVotes
      referralTraffic
    }
  }
}
```

## Clay-Based Competitive Monitoring

For directories without robust APIs, use Clay to monitor competitors.

### Set up competitive tracking table

1. Create a Clay table with columns: `directory`, `competitor_name`, `competitor_url`, `rating`, `review_count`, `last_checked`
2. Add rows for each competitor on each directory
3. Use Claygent to scrape competitor profiles:

**Claygent prompt:**
```
Visit {competitor_url} on {directory}. Extract:
- Current star rating
- Total review count
- Most recent review date
- Category position/ranking if visible
- Key features listed
- Pricing shown
Return as JSON.
```

4. Schedule the table to refresh weekly via Clay's scheduling feature or n8n trigger

### Track ranking changes

Create a separate Clay table tracking your own rankings over time:
- Columns: `directory`, `category`, `rank_position`, `rating`, `review_count`, `date_checked`
- Append a new row weekly (do not overwrite)
- This builds a time series for trend analysis

## n8n Analytics Aggregation Workflow

Build an n8n workflow that pulls analytics from all directories into a single dataset:

1. **Trigger:** Weekly cron (Monday 8am)
2. **HTTP Request nodes:** One per directory API (G2, Capterra, Product Hunt, TrustRadius)
3. **Merge node:** Combine all responses into a unified schema:

```json
{
  "directory": "g2",
  "date": "2026-03-30",
  "views": 1245,
  "clicks": 89,
  "reviews_new": 3,
  "avg_rating": 4.6,
  "rank_position": 12,
  "rank_category_size": 156
}
```

4. **PostHog node:** Send aggregated metrics as `directory_analytics_weekly` event
5. **Attio node:** Update the campaign record with latest metrics
6. **Slack node:** Post a summary to the marketing channel

## Error Handling

- **Analytics lag:** Most directories update analytics with a 24-48 hour delay. Do not query for today's data.
- **Scraping blocks:** If Clay scraping gets blocked, reduce frequency and rotate user agents. Prefer official APIs when available.
- **Missing metrics:** Not all directories expose all metrics. Track what is available and note gaps.
- **API changes:** Directory APIs change frequently. Pin API versions when possible and monitor for deprecation notices.
