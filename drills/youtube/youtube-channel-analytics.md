---
name: youtube-channel-analytics
description: Pull YouTube channel and video performance data, surface trends, and identify optimization opportunities
category: YouTube
tools:
  - YouTube Analytics API
  - YouTube Data API v3
  - PostHog
  - n8n
fundamentals:
  - youtube-analytics-api
  - youtube-data-api-metadata
  - posthog-dashboards
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-scheduling
---

# YouTube Channel Analytics

Build an always-on analytics pipeline that pulls YouTube performance data, syncs it to PostHog, surfaces trends, and identifies which videos and topics drive the most pipeline value. This drill is the measurement backbone of the YouTube Channel SEO play.

## Input

- YouTube channel with OAuth credentials configured
- PostHog instance with API access
- n8n instance for scheduled workflows
- At least 4 published videos (need a baseline for meaningful comparison)

## Steps

### 1. Configure PostHog event schema for YouTube metrics

Using `posthog-custom-events`, define the following events:

```
yt_video_published
  Properties: video_id, title, target_keyword, publish_date, duration_seconds

yt_daily_metrics
  Properties: video_id, date, views, watch_time_minutes, avg_view_duration,
              avg_view_percentage, likes, comments, shares, subscribers_gained, ctr

yt_traffic_source
  Properties: video_id, date, source_type, views, watch_time_minutes

yt_search_term
  Properties: video_id, date, search_query, views, watch_time_minutes

yt_channel_daily
  Properties: date, total_views, total_watch_time, total_subscribers,
              subscribers_gained, subscribers_lost, videos_published
```

### 2. Build the n8n daily sync workflow

Using `n8n-workflow-basics` and `n8n-scheduling`, create a workflow triggered by daily cron (06:00 UTC):

**Step 2a: Pull channel daily metrics**

Using `youtube-analytics-api`, query:
```
GET /v2/reports?ids=channel==MINE
  &startDate={yesterday}&endDate={yesterday}
  &metrics=views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost
  &dimensions=day
```

Send as `yt_channel_daily` event to PostHog.

**Step 2b: Pull per-video daily metrics**

For each video published in the last 90 days:
```
GET /v2/reports?ids=channel==MINE
  &startDate={yesterday}&endDate={yesterday}
  &metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,annotationClickThroughRate
  &filters=video=={VIDEO_ID}
```

Send as `yt_daily_metrics` events to PostHog.

**Step 2c: Pull traffic sources**

```
GET /v2/reports?ids=channel==MINE
  &startDate={yesterday}&endDate={yesterday}
  &metrics=views,estimatedMinutesWatched
  &dimensions=insightTrafficSourceType
```

Send as `yt_traffic_source` events to PostHog. Key sources to track: `YT_SEARCH` (SEO working), `SUGGESTED` (algorithm recommending), `BROWSE` (subscribers' home feed), `EXT_URL` (external referrals).

**Step 2d: Pull search terms**

```
GET /v2/reports?ids=channel==MINE
  &startDate={yesterday}&endDate={yesterday}
  &metrics=views,estimatedMinutesWatched
  &dimensions=insightTrafficSourceDetail
  &filters=insightTrafficSourceType==YT_SEARCH
  &sort=-views&maxResults=100
```

Send as `yt_search_term` events. These reveal exactly which searches are finding your videos — feed this back to keyword research.

### 3. Build the PostHog dashboard

Using `posthog-dashboards`, create a "YouTube Channel Performance" dashboard:

**Panel 1 — Channel overview (last 30 days)**
- Total views (line chart, daily)
- Total watch time hours (line chart, daily)
- Net subscriber change (bar chart, daily)

**Panel 2 — Video leaderboard**
- Table: all videos sorted by views (last 30 days)
- Columns: title, views, avg_view_percentage, likes, comments, subscribers_gained

**Panel 3 — SEO performance**
- YT_SEARCH views as percentage of total views (trend line)
- Top 20 search terms driving traffic (table)
- Search traffic by video (table)

**Panel 4 — Traffic source mix**
- Pie chart: views by traffic source type
- Trend lines: search vs suggested vs browse over time

**Panel 5 — Content effectiveness**
- Scatter plot: avg_view_percentage (x) vs views (y) per video
- Videos in top-right quadrant = high retention + high views = best topics
- Videos in bottom-right = high views but low retention = clickbait or mismatch

**Panel 6 — Conversion tracking**
- CTA click rate per video (from end screen / card CTR)
- Website referral traffic from YouTube (connect PostHog web tracking)

### 4. Set up anomaly alerts

Using `n8n-workflow-basics`, create alert conditions:

- **Search traffic drop**: If YT_SEARCH views drop >30% week-over-week, alert. Possible causes: keyword competition, algorithm change, or video aged out.
- **Retention spike**: If a new video has avg_view_percentage >60%, alert. This video's topic and format should be replicated.
- **Subscriber spike**: If subscribers_gained for any video is >3x the channel average, alert. The topic resonated — consider a follow-up video.
- **CTR drop below 3%**: Alert for any video with impressions >1000 and CTR <3%. Thumbnail or title needs optimization.

### 5. Generate weekly performance report

Using `n8n-scheduling`, create a weekly workflow (Monday 09:00):

1. Pull last 7 days of data from PostHog
2. Compute: total views, watch time hours, net subscribers, top 5 videos, top 10 search terms, traffic source breakdown
3. Compare to prior week: highlight improvements and declines
4. Identify top opportunity: the keyword with the most search impressions but lowest click-through (title/thumbnail optimization opportunity)
5. Format and send the report via Slack or email

## Output

- Daily YouTube data synced to PostHog
- Live dashboard with 6 panels covering channel health, video performance, SEO, traffic, content effectiveness, and conversions
- Anomaly alerts for search drops, retention spikes, subscriber spikes, and CTR issues
- Weekly performance report with trends and optimization recommendations

## Triggers

- Daily sync: n8n cron at 06:00 UTC
- Dashboard: always-on, updated as events arrive
- Alerts: triggered immediately on threshold breach
- Weekly report: Monday 09:00 via n8n cron
