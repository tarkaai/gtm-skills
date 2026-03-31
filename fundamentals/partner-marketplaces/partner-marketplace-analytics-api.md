---
name: partner-marketplace-analytics-api
description: Pull listing analytics (views, installs, conversions, rankings) from partner ecosystem marketplace developer portals
tool: Salesforce
product: AppExchange
difficulty: Config
---

# Partner Marketplace Analytics API

Retrieve performance data from partner ecosystem marketplace listings. Each marketplace exposes different metrics through different APIs. This fundamental normalizes the data extraction across platforms so it can be aggregated into a single PostHog dashboard.

## Prerequisites

- Active listings on 1+ partner marketplaces with developer/partner API access
- PostHog instance for centralized metric storage
- n8n instance for scheduling automated data pulls

## Salesforce AppExchange

### Listing analytics

```
GET https://appexchange.salesforce.com/api/v1/listings/{listing_id}/analytics
Authorization: Bearer {SF_PARTNER_TOKEN}
Query params:
  period: 30d | 7d | 90d
  granularity: daily | weekly
```

Response:
```json
{
  "period": "30d",
  "metrics": {
    "page_views": 1240,
    "install_clicks": 87,
    "installs_completed": 42,
    "uninstalls": 3,
    "reviews_count": 18,
    "avg_rating": 4.7,
    "category_rank": 12,
    "search_impressions": 3200
  },
  "daily": [
    {"date": "2026-03-01", "page_views": 45, "install_clicks": 3, "installs_completed": 1}
  ]
}
```

### Conversion funnel

Calculate from the response:
- **Search-to-view rate:** `page_views / search_impressions`
- **View-to-click rate:** `install_clicks / page_views`
- **Click-to-install rate:** `installs_completed / install_clicks`
- **Retention rate:** `(installs_completed - uninstalls) / installs_completed`

## HubSpot App Marketplace

### Install analytics

```
GET https://api.hubspot.com/developer/v2/apps/{app_id}/installs/analytics
Authorization: Bearer {HUBSPOT_DEV_TOKEN}
Query params:
  start: 2026-03-01
  end: 2026-03-30
```

Response:
```json
{
  "total_installs": 156,
  "active_installs": 132,
  "new_installs_period": 28,
  "uninstalls_period": 4,
  "daily_installs": [
    {"date": "2026-03-01", "installs": 2, "uninstalls": 0}
  ]
}
```

### Listing page analytics

HubSpot does not expose listing page view counts via API. Use UTM-tagged outbound links in PostHog to infer marketplace-sourced traffic:

```
PostHog query:
  event = "$pageview"
  properties.utm_source = "hubspot-marketplace"
  date_range = last 30 days
  group_by = day
```

## Shopify App Store

### App analytics

```
GET https://partners.shopify.com/api/v1/apps/{app_id}/analytics
Authorization: Bearer {SHOPIFY_PARTNER_TOKEN}
Query params:
  start_date: 2026-03-01
  end_date: 2026-03-30
```

Response:
```json
{
  "page_views": 2100,
  "installs": 89,
  "uninstalls": 7,
  "active_installs": 342,
  "reviews_count": 23,
  "avg_rating": 4.5,
  "revenue_period": 2580.00,
  "conversion_rate": 0.042
}
```

Shopify provides the richest analytics among partner marketplaces. The `conversion_rate` is view-to-install.

## Zapier

### Integration analytics

```
GET https://developer.zapier.com/api/v1/integrations/{integration_id}/analytics
Authorization: Bearer {ZAPIER_DEV_TOKEN}
Query params:
  period: 30d
```

Response:
```json
{
  "total_users": 890,
  "active_zaps": 1240,
  "zap_runs_30d": 45000,
  "new_users_30d": 67,
  "category_rank": 8,
  "popular_triggers": [
    {"name": "New Record Created", "active_zaps": 450}
  ],
  "popular_actions": [
    {"name": "Create Contact", "active_zaps": 320}
  ]
}
```

Zapier ranks integrations by active user count and available Zap templates. Track `total_users` and `active_zaps` as primary KPIs.

## Slack App Directory

Slack does not expose listing analytics via API. Use these alternatives:

**Method 1 -- OAuth install tracking:**
Track every OAuth install event from your app's backend:
```json
{
  "event": "partner_marketplace_install",
  "properties": {
    "marketplace": "slack",
    "team_id": "{slack_team_id}",
    "team_name": "{slack_team_name}",
    "installer_user_id": "{user_id}",
    "timestamp": "2026-03-15T10:00:00Z"
  }
}
```

**Method 2 -- UTM-tagged website traffic:**
PostHog query for Slack-sourced visits:
```
event = "$pageview"
properties.utm_source = "slack-directory"
date_range = last 30 days
```

## Make (formerly Integromat)

Make partner analytics are available through the partner dashboard only. No public API. Use Clay Claygent scraping as fallback:

```
Prompt: "Go to {make_partner_dashboard_url}. Extract: total scenarios using our integration, new users this month, total active users. Return as JSON."
```

## Normalized Data Schema

After collecting data from each marketplace, normalize into a single PostHog event format:

```json
{
  "event": "partner_marketplace_weekly_metrics",
  "properties": {
    "marketplace": "{marketplace_name}",
    "listing_slug": "{app_slug}",
    "page_views": 0,
    "install_clicks": 0,
    "installs_completed": 0,
    "uninstalls": 0,
    "active_installs": 0,
    "reviews_count": 0,
    "avg_rating": 0.0,
    "category_rank": 0,
    "revenue": 0.0,
    "leads_from_marketplace": 0,
    "week_start": "2026-03-23"
  }
}
```

Send one event per marketplace per week. This enables cross-marketplace comparison in PostHog dashboards.

## Error Handling

- **API not available**: For marketplaces without analytics APIs (Slack, Make), use install event tracking from your app backend + UTM-tagged PostHog data.
- **Data lag**: Some marketplace analytics update with 24-48 hour delay. Schedule data pulls for Tuesday mornings to capture full prior-week data.
- **Metric definitions vary**: "Installs" on Shopify means app installed on a store; on Zapier it means a user connected your integration. Document definitions per marketplace and compare trends within-marketplace, not absolute numbers cross-marketplace.
- **Rate limits**: Most partner APIs allow 100-300 requests/minute. Cache responses and batch queries.
