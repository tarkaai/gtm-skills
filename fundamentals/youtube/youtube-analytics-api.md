---
name: youtube-analytics-api
description: Pull channel and video performance metrics via the YouTube Analytics API
tool: YouTube Analytics API
difficulty: Config
---

# YouTube Analytics API

Retrieve performance data for your YouTube channel and individual videos: views, watch time, traffic sources, audience demographics, and revenue metrics.

## Authentication

Requires OAuth 2.0 with `https://www.googleapis.com/auth/yt-analytics.readonly` scope. Revenue/ad data requires `https://www.googleapis.com/auth/yt-analytics-monetary.readonly`.

## Core Operations

### Channel-level metrics (daily)

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-03-01
  &endDate=2026-03-30
  &metrics=views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments,shares
  &dimensions=day
  &sort=day
Authorization: Bearer {ACCESS_TOKEN}
```

### Per-video metrics

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-01-01
  &endDate=2026-03-30
  &metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares,annotationClickThroughRate
  &dimensions=video
  &sort=-views
  &maxResults=50
  &filters=video=={VIDEO_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

### Traffic sources (where viewers find your videos)

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-03-01
  &endDate=2026-03-30
  &metrics=views,estimatedMinutesWatched
  &dimensions=insightTrafficSourceType
  &sort=-views
Authorization: Bearer {ACCESS_TOKEN}
```

Traffic source types include: `YT_SEARCH`, `SUGGESTED`, `BROWSE`, `EXT_URL`, `NOTIFICATION`, `PLAYLIST`, `END_SCREEN`, `ANNOTATION`, `CAMPAIGN_CARD`, `NO_LINK_EMBEDDED`, `NO_LINK_OTHER`.

### Search terms driving traffic

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-03-01
  &endDate=2026-03-30
  &metrics=views,estimatedMinutesWatched
  &dimensions=insightTrafficSourceDetail
  &filters=insightTrafficSourceType==YT_SEARCH
  &sort=-views
  &maxResults=100
Authorization: Bearer {ACCESS_TOKEN}
```

Returns the actual search queries viewers used to find your videos. Essential for YouTube SEO keyword discovery.

### Audience demographics

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-03-01
  &endDate=2026-03-30
  &metrics=viewerPercentage
  &dimensions=ageGroup,gender
Authorization: Bearer {ACCESS_TOKEN}
```

### Audience retention for a specific video

```
GET https://youtubeanalytics.googleapis.com/v2/reports
  ?ids=channel==MINE
  &startDate=2026-01-01
  &endDate=2026-03-30
  &metrics=audienceWatchRatio
  &dimensions=elapsedVideoTimeRatio
  &filters=video=={VIDEO_ID}
Authorization: Bearer {ACCESS_TOKEN}
```

Returns retention curve: what percentage of viewers are still watching at each point in the video. Drops indicate weak sections.

## YouTube Reporting API (Bulk Data)

For large-scale analysis, use the Reporting API to get daily bulk CSV reports:

### Create a reporting job

```
POST https://youtubereporting.googleapis.com/v1/jobs
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "reportTypeId": "channel_basic_a2",
  "name": "Channel daily metrics"
}
```

### List available reports

```
GET https://youtubereporting.googleapis.com/v1/jobs/{JOB_ID}/reports
Authorization: Bearer {ACCESS_TOKEN}
```

### Download a report

```
GET https://youtubereporting.googleapis.com/v1/media/{REPORT_URL}
Authorization: Bearer {ACCESS_TOKEN}
```

Reports are generated daily and available for 60 days.

## Key Metrics for SEO Plays

| Metric | What it tells you |
|--------|------------------|
| `views` | Total video views |
| `estimatedMinutesWatched` | Total watch time (YouTube's #1 ranking factor) |
| `averageViewDuration` | How long viewers stay (quality signal) |
| `averageViewPercentage` | Retention rate (higher = better recommendations) |
| `subscribersGained` | New subs driven by this video |
| `annotationClickThroughRate` | End screen / card CTR |
| `shares` | Social sharing (virality signal) |

## Error Handling

- `401 Unauthorized`: Refresh OAuth token.
- `403 Forbidden`: Check scope. Monetary metrics require the monetary scope.
- `400 badRequest`: Validate date format (YYYY-MM-DD) and metric/dimension compatibility. Not all metric+dimension combinations are valid.
- `429 rateLimitExceeded`: Retry with exponential backoff.

## Pricing

- Free (OAuth-based, no separate billing)
- Google Cloud project required
- Docs: https://developers.google.com/youtube/analytics

## Alternatives

- **vidIQ**: Channel analytics dashboard + keyword tracking ($5.98-$17.50/mo)
- **TubeBuddy**: Video performance tracking + A/B testing ($2.25-$14.50/mo)
- **Social Blade**: Public channel statistics and growth tracking (free tier available)
- **Tubular Labs**: Enterprise cross-platform video analytics
- **Phyllo API**: Unified creator analytics across platforms
