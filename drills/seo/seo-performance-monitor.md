---
name: seo-performance-monitor
description: Track rankings, indexation, CTR, and organic traffic across all programmatic SEO pages
category: SEO
tools:
  - Google Search Console
  - Ahrefs
  - PostHog
  - n8n
fundamentals:
  - google-search-console-api
  - ahrefs-rank-tracking
  - posthog-dashboards
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-scheduling
---

# SEO Performance Monitor

This drill creates an always-on monitoring system for programmatic SEO pages. It tracks indexation, rankings, organic traffic, CTR, and conversions at the individual page level and surfaces anomalies that need attention.

## Input

- List of published page URLs and their target keywords (from `keyword-matrix-builder` output)
- Google Search Console access for the site
- Ahrefs API access
- PostHog tracking installed on all pages

## Steps

### 1. Set up page-level tracking in PostHog

Using `posthog-custom-events`, configure events for each programmatic page:

- `seo_page_viewed`: fires on page load. Properties: `page_url`, `target_keyword`, `category`, `modifier`, `referrer`, `utm_source`
- `seo_page_engaged`: fires on scroll depth >50% OR time on page >30 seconds. Properties: same as above plus `scroll_depth`, `time_on_page`
- `seo_page_converted`: fires when the CTA is clicked or form is submitted. Properties: same as above plus `conversion_type` (form_submit, demo_book, signup)

Use PostHog autocapture for basic pageview tracking. Add custom events for engagement and conversion.

### 2. Build the SEO dashboard in PostHog

Using `posthog-dashboards`, create a dashboard with these panels:

- **Total organic traffic**: line chart, last 30 days, filtered to `utm_source=google` or referrer contains `google.com`
- **Pages indexed vs total pages**: number comparison. Pull indexed count from GSC API.
- **Top 20 pages by organic traffic**: table sorted by pageview count
- **Conversion rate by page**: table showing `seo_page_converted / seo_page_viewed` per URL
- **Engagement rate**: percentage of pageviews that triggered `seo_page_engaged`
- **Traffic by category/modifier**: breakdown chart showing which page groups drive the most traffic

### 3. Configure GSC data pull via n8n

Using `n8n-workflow-basics` and `n8n-scheduling`, create a daily workflow:

1. **Pull search analytics from GSC** using `google-search-console-api`:
   - Query: last 7 days, dimensions = [page, query], filtered to your programmatic page URL pattern
   - Extract: clicks, impressions, CTR, position per page per query
2. **Pull indexation status** using GSC URL Inspection API:
   - Sample 50 random pages from your published list each day (to stay within rate limits)
   - Log which pages are indexed, crawled-not-indexed, or not discovered
3. **Store results**: write to PostHog as custom events (`seo_gsc_ranking`, `seo_gsc_indexation`) so they appear on your dashboard
4. **Alert on anomalies**:
   - If indexation rate drops below 80%, send alert
   - If average position for any keyword moves >10 positions in a week, send alert
   - If total organic clicks drop >20% week-over-week, send alert

### 4. Configure Ahrefs rank tracking via n8n

Using `ahrefs-rank-tracking`, create a weekly n8n workflow:

1. Pull organic keywords for your domain filtered to programmatic page URLs
2. Compare current positions to last week's positions
3. Identify: keywords gained (new rankings), keywords improved (position up), keywords declined (position down), keywords lost (fell out of top 100)
4. Log gains/losses as PostHog events (`seo_ranking_change`)
5. Generate a weekly ranking summary: total keywords ranked, average position, movement trends

### 5. Build the conversion tracking funnel

Using `posthog-custom-events`, build a funnel:

`seo_page_viewed` -> `seo_page_engaged` -> `seo_page_converted`

Segment by: category, modifier, landing page URL, device type. Identify which page patterns convert best and which have engagement but no conversion (opportunity for CTA optimization).

### 6. Set up automated reporting

Using `n8n-workflow-basics`, create a weekly report workflow that:

1. Pulls the last 7 days of data from PostHog and GSC
2. Computes: total organic sessions, new pages indexed, average position change, total conversions, conversion rate
3. Compares to prior week and prior month
4. Formats as a summary and sends to Slack or email

## Output

- Live PostHog dashboard showing all SEO metrics
- Daily GSC data sync with indexation and ranking alerts
- Weekly Ahrefs rank tracking with gain/loss reports
- Weekly automated performance summary
- Anomaly alerts for indexation drops, ranking changes, and traffic declines

## Triggers

- Dashboard: always-on, updated in real-time by PostHog
- GSC sync: daily via n8n cron
- Ahrefs sync: weekly via n8n cron
- Reporting: weekly via n8n cron
- Alerts: triggered immediately when thresholds are breached
