---
name: comparison-page-health-monitor
description: Monitor ranking positions, organic traffic, conversion rates, and content freshness across all comparison pages with anomaly alerting
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
  - posthog-anomaly-detection
  - n8n-workflow-basics
  - n8n-scheduling
---

# Comparison Page Health Monitor

This drill creates a dedicated monitoring layer for comparison and alternative pages. It tracks ranking positions for competitor keywords, organic traffic per page, conversion rates, and content freshness. It surfaces pages that need attention — declining rankings, outdated content, or underperforming CTAs — so the `autonomous-optimization` and `content-refresh-pipeline` drills can act on them.

## Input

- Published comparison pages with their target keywords (from `competitor-keyword-research` output)
- PostHog tracking configured on all comparison pages (from `comparison-page-creation`)
- Google Search Console and Ahrefs API access
- n8n instance

## Steps

### 1. Build the comparison page dashboard in PostHog

Using `posthog-dashboards`, create a dedicated dashboard:

**Traffic panels:**
- Total organic traffic to `/compare/*` pages — line chart, last 30 days
- Traffic per comparison page — table sorted by sessions, with week-over-week change
- Traffic by page type (1:1 comparison vs alternatives vs category roundup)

**Conversion panels:**
- Conversion rate per page: `comparison_cta_clicked / comparison_page_viewed`
- Feature table engagement rate: `comparison_table_scrolled / comparison_page_viewed`
- CTA funnel: `comparison_page_viewed` -> `comparison_table_scrolled` -> `comparison_cta_clicked`

**SEO panels:**
- Average ranking position by competitor keyword (data from GSC sync)
- Pages indexed vs total published
- New keywords gained this week (from Ahrefs sync)

**Freshness panel:**
- Days since last content update per page
- Pages with competitor data older than 90 days (flagged as stale)

### 2. Configure daily GSC sync

Build an n8n workflow using `n8n-scheduling` (daily cron):

1. Use `google-search-console-api` to pull search analytics for the last 7 days:
   - Filter: `page` contains `/compare/`
   - Dimensions: page, query
   - Metrics: clicks, impressions, CTR, position
2. For each comparison page, compute:
   - Primary keyword position (the target keyword from `competitor-keyword-research`)
   - Secondary keyword positions (related keywords)
   - Total impressions and clicks
3. Compare against the previous week's data
4. Classify each page:
   - **Improving**: primary keyword position improved by 3+ spots
   - **Stable**: position changed <3 spots
   - **Declining**: position worsened by 3+ spots
   - **Lost**: dropped out of top 100
5. Log results as PostHog events: `comparison_ranking_check` with properties `page_url`, `target_keyword`, `position`, `position_change`, `status`

### 3. Configure weekly Ahrefs sync

Build an n8n workflow using `n8n-scheduling` (weekly cron):

1. Use `ahrefs-rank-tracking` to pull organic keyword data for comparison page URLs
2. Identify new keywords each page ranks for (keywords not in previous week's data)
3. Identify keywords lost (ranked last week, not this week)
4. Calculate total keyword footprint: how many unique keywords do comparison pages rank for?
5. Log as PostHog events: `comparison_keyword_footprint` with properties `total_keywords`, `keywords_gained`, `keywords_lost`

### 4. Set anomaly alerts

Using `posthog-anomaly-detection`, configure alerts:

| Alert | Trigger | Action |
|-------|---------|--------|
| Traffic drop | Any comparison page organic traffic drops >30% WoW | Flag for content refresh |
| Ranking crash | Primary keyword position drops >10 spots in one week | Flag for immediate review |
| Conversion drop | Page conversion rate drops below 0.5% for 2+ weeks | Flag for CTA optimization |
| Stale content | Page not updated in >90 days AND competitor data has changed | Flag for competitive intelligence update |
| New opportunity | A new competitor keyword reaches >200 monthly volume in Ahrefs | Queue new comparison page creation |

Route alerts to n8n which logs them as PostHog events and sends Slack notifications.

### 5. Generate weekly health report

Build an n8n workflow (weekly cron) that:

1. Aggregates all comparison page metrics for the week
2. Computes:
   - Total organic sessions across all comparison pages
   - Total conversions (CTA clicks)
   - Blended conversion rate
   - Average ranking position across all target keywords
   - Pages improving vs stable vs declining
   - Content freshness score (% of pages updated in last 90 days)
3. Generates a summary using Claude:
   - Top 3 performing pages and why
   - Bottom 3 pages and recommended action
   - New opportunities detected
   - Competitive landscape changes detected
4. Posts the report to Slack and logs to Attio

## Output

- Live PostHog dashboard for comparison page performance
- Daily GSC ranking data synced to PostHog
- Weekly Ahrefs keyword footprint tracking
- Anomaly alerts for traffic, ranking, conversion, and freshness issues
- Weekly health report with actionable recommendations

## Triggers

- Dashboard: always-on, real-time PostHog data
- GSC sync: daily via n8n cron
- Ahrefs sync: weekly via n8n cron
- Anomaly alerts: triggered immediately when thresholds are breached
- Health report: weekly via n8n cron
