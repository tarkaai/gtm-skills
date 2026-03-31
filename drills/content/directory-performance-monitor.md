---
name: directory-performance-monitor
description: Track directory listing KPIs, competitor rankings, and review trends with automated weekly reporting
category: Directories
tools:
  - PostHog
  - n8n
  - Attio
  - Clay
fundamentals:
  - directory-analytics-scraping
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Directory Performance Monitor

This drill builds the monitoring and reporting system for the directories-marketplaces play. It tracks views, clicks, reviews, rankings, and competitor movements across all directories -- then surfaces anomalies and trends in a weekly report.

## Input

- Active directory listings (output from `directory-listing-setup` drill)
- PostHog tracking configured for directory traffic (via UTM parameters)
- n8n instance for scheduled data collection
- At least 2 weeks of listing data for trend comparison

## Steps

### 1. Configure PostHog event tracking for directory traffic

Using the `posthog-custom-events` fundamental, ensure all directory-sourced traffic is captured with standard events:

- `directory_listing_view`: Fired when a user visits your site from a directory (detected via UTM params). Properties: `directory_name`, `listing_type` (organic/ppc), `campaign`.
- `directory_listing_click`: Fired on CTA click from a directory-sourced session. Properties: `directory_name`, `cta_type` (signup/demo/pricing).
- `directory_inquiry_submitted`: Fired when a directory-sourced visitor submits a form, books a demo, or starts a trial. Properties: `directory_name`, `inquiry_type`, `lead_value`.

UTM parsing logic: If `utm_source` matches a known directory name AND `utm_medium` equals "directory" or "ppc", classify the session as directory-sourced.

### 2. Build the data collection workflow

Using the `n8n-scheduling` and `n8n-workflow-basics` fundamentals, create an n8n workflow that runs weekly (Monday 7am):

**Step 1 -- Pull directory analytics:**
For each directory, use `directory-analytics-scraping` fundamental to fetch:
- Profile views (last 7 days)
- Clicks to website (last 7 days)
- New reviews (last 7 days)
- Current average rating
- Category rank position

**Step 2 -- Pull PostHog data:**
Query PostHog API for the same period:
- `directory_listing_view` count by directory
- `directory_inquiry_submitted` count by directory
- Conversion rate: inquiries / views

**Step 3 -- Pull competitor data:**
Use Clay-based scraping (via `directory-analytics-scraping`) to check top 5 competitors:
- Their review count change
- Their rating change
- Their rank position change

**Step 4 -- Store in PostHog:**
Send aggregated weekly metrics as a `directory_weekly_metrics` event:
```json
{
  "event": "directory_weekly_metrics",
  "properties": {
    "directory": "g2",
    "views": 312,
    "clicks": 24,
    "inquiries": 3,
    "conversion_rate": 0.0096,
    "reviews_new": 1,
    "avg_rating": 4.6,
    "rank_position": 12,
    "week_start": "2026-03-23"
  }
}
```

**Step 5 -- Store in Attio:**
Update the directory campaign record with latest metrics using `attio-reporting`.

### 3. Build the PostHog dashboard

Using the `posthog-dashboards` fundamental, create a "Directory & Marketplace Performance" dashboard:

**Panel 1 -- Traffic Overview:**
- Trend: total directory views per week (stacked by directory)
- Trend: total directory clicks per week (stacked by directory)
- Number: total inquiries this month

**Panel 2 -- Conversion Funnel:**
- Funnel: directory_listing_view -> directory_listing_click -> directory_inquiry_submitted
- Break down by directory_name

**Panel 3 -- Directory Comparison:**
- Table: directory_name, views, clicks, inquiries, conversion_rate, avg_rating, rank
- Sorted by inquiries descending

**Panel 4 -- Review Velocity:**
- Trend: new reviews per week (stacked by directory)
- Number: total reviews across all directories
- Number: average rating across all directories

**Panel 5 -- Competitor Tracking:**
- Table: competitor_name, their_reviews, their_rating, their_rank, our_rank
- Highlight rows where competitor rank improved

### 4. Set up alerts

Using n8n, configure alerts for:

- **Traffic drop:** Views drop >30% week-over-week on any Tier 1 directory
- **Rating drop:** Average rating falls below 4.0 on any directory
- **Negative review:** Any 1-2 star review posted (trigger immediate response)
- **Competitor surge:** A competitor gains 10+ reviews in a single week (possible review campaign)
- **Rank drop:** Category rank falls 5+ positions on G2 or Capterra

Route alerts to Slack with the specific metrics and recommended action.

### 5. Generate weekly performance report

The n8n workflow generates a report with:

```
# Directory Performance Report — Week of {date}

## Summary
- Total views: {views} ({views_change}% vs last week)
- Total clicks: {clicks} ({clicks_change}% vs last week)
- Inquiries: {inquiries} ({inquiries_change}% vs last week)
- New reviews: {new_reviews}
- Average rating: {avg_rating}

## Top Performing Directories
1. {dir1}: {views1} views, {inquiries1} inquiries, {rate1}% conversion
2. {dir2}: {views2} views, {inquiries2} inquiries, {rate2}% conversion

## Alerts
- {any alerts that fired this week}

## Competitor Movements
- {notable competitor changes}

## Recommended Actions
- {data-driven recommendations}
```

Post to Slack and store in Attio.

## Output

- Weekly automated data collection from all directories
- Real-time PostHog dashboard with directory KPIs
- Automated alerts for anomalies
- Weekly performance report delivered to Slack
- Historical trend data for optimization decisions

## Triggers

- Data collection: weekly via n8n cron
- Alerts: continuous via webhook monitoring
- Dashboard: always-on, refreshes with live data
- Review alerts: daily check for new reviews
