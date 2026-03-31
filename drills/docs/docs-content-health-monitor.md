---
name: docs-content-health-monitor
description: Always-on monitoring of documentation content health — traffic trends, ranking decay, content freshness, and conversion performance per page
category: Docs
tools:
  - Google Search Console
  - Ahrefs
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - google-search-console-api
  - ahrefs-rank-tracking
  - posthog-dashboards
  - posthog-anomaly-detection
  - n8n-workflow-basics
  - n8n-scheduling
  - docs-search-analytics
---

# Docs Content Health Monitor

This drill creates an always-on system that monitors every documentation page's health across four dimensions: traffic, rankings, freshness, and conversions. It surfaces pages that need attention before they decay and identifies high performers to replicate.

## Input

- Docs site with >= 30 published pages and >= 8 weeks of traffic data
- PostHog tracking on all docs pages (from `posthog-gtm-events`)
- GSC and Ahrefs access
- n8n instance for scheduling

## Steps

### 1. Build the docs health dashboard

Using `posthog-dashboards`, create a comprehensive docs performance dashboard:

**Panel 1 — Traffic overview:**
- Total organic docs page views (last 30 days, with 30-day-prior comparison)
- Organic traffic trend (daily line chart, 90-day window)
- Traffic by source: organic search, direct, referral, social

**Panel 2 — Top pages:**
- Top 20 docs pages by organic traffic (table: URL, views, avg time on page, CTA clicks, conversion rate)
- Bottom 20 docs pages by organic traffic (pages that may need refresh or removal)

**Panel 3 — Conversion funnel:**
- docs_page_viewed → docs_cta_clicked → account_created (overall and by page type)
- Conversion rate trend (weekly, 12-week window)
- Total leads from docs this month vs last month

**Panel 4 — Content freshness:**
- Pages not updated in > 90 days (from git commit history or `last_modified` metadata)
- Pages with declining traffic (> 20% drop month-over-month)

**Panel 5 — Search performance:**
- Top docs search queries with zero results (from `docs-search-analytics`)
- Average search-to-click ratio across docs search

### 2. Configure daily health checks via n8n

Using `n8n-workflow-basics` and `n8n-scheduling`, create a daily cron workflow:

**Check 1 — Traffic anomalies:**
Use `posthog-anomaly-detection` to detect:
- Total docs traffic dropped > 15% vs 7-day rolling average → alert
- Any single page lost > 50% of its traffic vs prior week → alert
- Total docs traffic increased > 30% → positive alert (find out what caused it)

**Check 2 — Indexation monitoring:**
Use `google-search-console-api` to sample 20 random docs pages daily:
- Check indexation status
- If any previously-indexed page is now de-indexed → critical alert
- Track overall indexation rate over time

**Check 3 — Ranking decay:**
Use `ahrefs-rank-tracking` weekly:
- Pull position changes for all docs pages
- Flag pages where position dropped > 5 spots
- Flag pages that fell from page 1 to page 2+

### 3. Score every page's health

For each docs page, compute a health score daily:

```
health = (traffic_score * 0.3) + (ranking_score * 0.25) + (freshness_score * 0.2) + (conversion_score * 0.25)
```

Where:
- `traffic_score`: 100 if traffic is stable or growing, 50 if flat, 0 if declining > 20%
- `ranking_score`: 100 if position 1-3, 75 if position 4-10, 50 if position 11-20, 25 if position 21-50, 0 if > 50 or not ranked
- `freshness_score`: 100 if updated in last 30 days, 75 if 30-90 days, 50 if 90-180 days, 25 if 180-365 days, 0 if > 365 days
- `conversion_score`: 100 if conversion rate > 3%, 75 if 2-3%, 50 if 1-2%, 25 if 0.5-1%, 0 if < 0.5%

### 4. Generate weekly health report

Using `n8n-scheduling`, run a weekly report workflow every Monday:

1. Pull health scores for all pages
2. Sort into categories:
   - **Healthy (score > 75):** No action needed. Track.
   - **Watch (score 50-75):** Minor issues. Monitor for another week.
   - **Needs attention (score 25-50):** Flag for refresh or optimization.
   - **Critical (score < 25):** Immediate action required — either refresh, merge with another page, or remove.
3. Compare to last week's report: which pages improved? Which declined?
4. Generate a natural-language summary using Anthropic API:
   - Total docs health score (average across all pages)
   - Top 3 wins this week (pages that improved most)
   - Top 3 risks this week (pages that declined most)
   - Recommended actions for critical pages

5. Post the report to Slack and store in Attio as a note on the docs campaign record

### 5. Trigger refresh workflows

When a page's health score drops below 25 for two consecutive weeks:

1. Automatically add it to the `content-refresh-pipeline` queue
2. Tag the refresh with the diagnosed issue (ranking decay, traffic drop, stale content, low conversion)
3. After refresh is published, reset the monitoring clock and track recovery over 28 days

When docs search analytics show a zero-result query with > 10 searches/month:

1. Automatically add it to the `docs-content-scaling-pipeline` production queue
2. Tag it as "user-requested content gap" with the search query as the target keyword

## Output

- Live PostHog dashboard with all docs health metrics
- Daily anomaly alerts for traffic, indexation, and ranking issues
- Per-page health scores updated daily
- Weekly health report with wins, risks, and recommended actions
- Automatic integration with refresh and content scaling pipelines

## Triggers

- Dashboard: always-on
- Daily checks: n8n cron at 06:00 UTC
- Weekly report: n8n cron every Monday at 08:00 UTC
- Refresh triggers: automatic when health score < 25 for 2 consecutive weeks
- Content gap triggers: automatic when zero-result search exceeds 10/month
