---
name: google-ads-youtube-reporting
description: Pull YouTube video campaign performance metrics (views, VTR, CPV, conversions) via Google Ads API
tool: Google
product: Google Ads
difficulty: Config
---

# Google Ads YouTube Reporting

Retrieve performance data for YouTube Video campaigns: views, view rate (VTR), cost per view (CPV), video played to 25%/50%/75%/100%, conversions, and cost per conversion.

## Prerequisites

- Active YouTube Video campaign in Google Ads
- Google Ads API access with OAuth 2.0
- Conversion tracking configured (see `google-ads-conversion-tracking`)

## Core Operations

### Campaign-level video metrics

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT campaign.name, campaign.id, metrics.cost_micros, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.average_cpv, metrics.conversions, metrics.cost_per_conversion, metrics.video_quartile_p25_rate, metrics.video_quartile_p50_rate, metrics.video_quartile_p75_rate, metrics.video_quartile_p100_rate, metrics.clicks, metrics.ctr, segments.date FROM campaign WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date DURING LAST_7_DAYS ORDER BY segments.date DESC"
}
```

### Ad group performance

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT ad_group.name, ad_group.id, metrics.cost_micros, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.average_cpv, metrics.conversions, metrics.cost_per_conversion, metrics.video_quartile_p25_rate, metrics.video_quartile_p100_rate FROM ad_group WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.video_views DESC"
}
```

### Per-ad creative performance

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.video_ad.video.asset, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.average_cpv, metrics.conversions, metrics.cost_per_conversion, metrics.video_quartile_p25_rate, metrics.video_quartile_p50_rate, metrics.video_quartile_p75_rate, metrics.video_quartile_p100_rate, metrics.clicks, metrics.ctr FROM ad_group_ad WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.video_views DESC"
}
```

### Audience segment performance

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT ad_group_criterion.display_name, ad_group_criterion.type, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.average_cpv, metrics.conversions, metrics.cost_per_conversion FROM ad_group_criterion WHERE campaign.advertising_channel_type = 'VIDEO' AND ad_group_criterion.type IN ('PLACEMENT', 'TOPIC', 'CUSTOM_AUDIENCE', 'USER_INTEREST') AND segments.date DURING LAST_30_DAYS ORDER BY metrics.conversions DESC"
}
```

### Placement-level performance (where your ads ran)

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT detail_placement_view.display_name, detail_placement_view.placement, detail_placement_view.placement_type, metrics.impressions, metrics.video_views, metrics.video_view_rate, metrics.average_cpv, metrics.conversions FROM detail_placement_view WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.impressions DESC LIMIT 100"
}
```

This reveals which specific YouTube channels and videos your ads appeared on. Essential for discovering high-performing placements to target directly and low-quality placements to exclude.

### Conversion breakdown by action type

```
POST https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "query": "SELECT campaign.name, segments.conversion_action, segments.conversion_action_name, metrics.conversions, metrics.conversions_value, metrics.cost_per_conversion FROM campaign WHERE campaign.advertising_channel_type = 'VIDEO' AND segments.date DURING LAST_30_DAYS AND metrics.conversions > 0 ORDER BY metrics.conversions DESC"
}
```

## Key YouTube Ad Metrics

| Metric | Definition | B2B Benchmark |
|--------|-----------|---------------|
| `video_views` | Views (30s watched or full video, or click) | N/A |
| `video_view_rate` | Views / Impressions | 15-30% for skippable |
| `average_cpv` | Cost per view | $0.02-0.10 B2B |
| `video_quartile_p25_rate` | % who watched 25% | 60-80% |
| `video_quartile_p50_rate` | % who watched 50% | 40-60% |
| `video_quartile_p75_rate` | % who watched 75% | 25-45% |
| `video_quartile_p100_rate` | % who watched 100% | 15-35% |
| `conversions` | Conversion actions tracked | Depends on CPA target |
| `cost_per_conversion` | Spend / Conversions | $20-100 B2B |
| `ctr` | Clicks / Impressions | 0.5-2% |

## Computed Metrics (agent should calculate)

- **Cost per qualified lead:** (Total spend) / (Leads that match ICP). Target: < 3x your search ads CPL.
- **View-to-click rate:** Clicks / Video views. How many viewers take action after watching.
- **Completion-to-conversion rate:** Conversions / Video completions. Quality signal for the CTA.
- **Effective CPM (eCPM):** (Total spend / Impressions) x 1000. Compare to LinkedIn/Meta CPMs.

## Error Handling

- `REQUEST_ERROR`: GAQL query syntax error. Validate query fields and segments compatibility.
- `AUTHORIZATION_ERROR`: Refresh OAuth token. Ensure the authenticated user has read access to the customer account.
- `QUERY_ERROR`: Some metric+segment combinations are invalid. Remove segments or metrics and retry.
- Rate limits: 15,000 requests per day. Use searchStream for bulk queries (streaming, not paginated).

## Pricing

- Free (included with Google Ads API access)
- Docs: https://developers.google.com/google-ads/api/docs/reporting/overview

## Alternatives

- **Google Ads UI reports**: Manual export from the Ads interface. No API needed, but not automatable.
- **Supermetrics**: Pull Google Ads data into sheets/dashboards ($29-$239/mo)
- **Funnel.io**: Marketing data aggregation, Google Ads connector ($380/mo+)
- **Windsor.ai**: Multi-touch attribution with Google Ads integration ($19-$99/mo)
- **Whatagraph**: Marketing reporting with Google Ads connector ($199/mo+)
