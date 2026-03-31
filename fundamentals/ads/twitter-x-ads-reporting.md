---
name: twitter-x-ads-reporting
description: Pull campaign metrics, cost data, and conversion attribution from the X Ads API
tool: X
product: X Ads
difficulty: Config
---

# Twitter/X Ads Reporting

Query the X Ads API for campaign performance data, feed it into PostHog dashboards, and calculate ROAS.

## Campaign-Level Stats

```
GET /12/stats/accounts/{account_id}?entity=CAMPAIGN&entity_ids={CAMPAIGN_ID}&granularity=DAY&metric_groups=ENGAGEMENT,BILLING,WEB_CONVERSION&start_time=2026-04-01T00:00:00Z&end_time=2026-04-08T00:00:00Z&placement=ALL_ON_TWITTER
```

## Line Item (Ad Group) Stats

```
GET /12/stats/accounts/{account_id}?entity=LINE_ITEM&entity_ids={LINE_ITEM_ID_1},{LINE_ITEM_ID_2}&granularity=DAY&metric_groups=ENGAGEMENT,BILLING,WEB_CONVERSION&start_time=2026-04-01T00:00:00Z&end_time=2026-04-08T00:00:00Z
```

## Promoted Tweet Stats

```
GET /12/stats/accounts/{account_id}?entity=PROMOTED_TWEET&entity_ids={PT_ID_1},{PT_ID_2}&granularity=DAY&metric_groups=ENGAGEMENT,BILLING&start_time=2026-04-01T00:00:00Z&end_time=2026-04-08T00:00:00Z
```

## Metric Groups

| Group | Metrics | Use |
|-------|---------|-----|
| `ENGAGEMENT` | impressions, engagements, url_clicks, follows, likes, retweets, replies, video_views_25/50/75/100 | Volume and engagement quality |
| `BILLING` | billed_charge_local_micro, billed_engagements | Cost tracking |
| `WEB_CONVERSION` | conversion_purchases, conversion_sign_ups, conversion_site_visits, conversion_custom | Attribution |
| `MOBILE_CONVERSION` | mobile_conversion_installs, mobile_conversion_purchases | App campaign attribution |

## Calculating Key Metrics

### Cost Per Click (CPC)
```
CPC = billed_charge_local_micro / url_clicks / 1000000
```

### Cost Per Lead (CPL)
```
CPL = billed_charge_local_micro / conversion_sign_ups / 1000000
```

### Click-Through Rate (CTR)
```
CTR = url_clicks / impressions
```

Target CTR for B2B: >0.5% (keyword targeting), >0.3% (interest/follower targeting).

### Return on Ad Spend (ROAS)
```
ROAS = (attributed_revenue) / (billed_charge_local_micro / 1000000)
```

Revenue attribution requires connecting X's `twclid` click parameter to your CRM deal values. Capture `twclid` from the landing page URL, store it in PostHog and Attio, then match conversions to deal close amounts.

## Syncing to PostHog

Build an n8n workflow that runs daily:

1. **Trigger**: n8n Cron node, 6:00 AM daily
2. **Fetch stats**: HTTP Request node calling the X Ads stats endpoints above for yesterday's date
3. **Transform**: Code node that calculates CPC, CPL, CTR from raw metrics
4. **Send to PostHog**: HTTP Request node posting custom events:

```
POST https://us.i.posthog.com/capture/
Content-Type: application/json

{
  "api_key": "{POSTHOG_PROJECT_KEY}",
  "event": "twitter_ads_daily_stats",
  "distinct_id": "twitter-ads-{campaign_id}",
  "properties": {
    "campaign_id": "{CAMPAIGN_ID}",
    "campaign_name": "{NAME}",
    "date": "2026-04-01",
    "impressions": 15000,
    "url_clicks": 120,
    "ctr": 0.008,
    "spend_usd": 45.50,
    "cpc_usd": 0.38,
    "conversions": 5,
    "cpl_usd": 9.10
  }
}
```

This enables PostHog dashboards that combine ad platform data with on-site conversion data for full-funnel visibility.

## Granularity Options

- `DAY`: Daily breakdown. Use for daily monitoring and trend detection.
- `HOUR`: Hourly breakdown. Use for detecting time-of-day performance patterns.
- `TOTAL`: Aggregated total for the date range. Use for summary reporting.

Maximum date range: 90 days per request.

## Rate Limits

- Stats endpoints: 100 requests per 15-minute window per ads account
- Maximum 20 entity IDs per request
- For large accounts, batch requests by entity ID groups of 20

## Error Handling

- `INVALID_DATE_RANGE`: Start time after end time, or range exceeds 90 days. Adjust dates.
- `ENTITY_NOT_FOUND`: Campaign or line item ID does not exist. Re-fetch active entity IDs.
- `METRIC_GROUP_NOT_AVAILABLE`: Some metric groups not available for all entity types. Check compatibility.
- `429 Too Many Requests`: Rate limit exceeded. Implement exponential backoff.
