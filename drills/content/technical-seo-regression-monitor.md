---
name: technical-seo-regression-monitor
description: Continuously monitor for new technical SEO regressions and alert before they impact rankings
category: SEO
tools:
  - Google Search Console
  - Google PageSpeed Insights
  - n8n
  - PostHog
fundamentals:
  - google-search-console-api
  - pagespeed-insights-api
  - robots-txt-management
  - posthog-anomaly-detection
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
---

# Technical SEO Regression Monitor

This drill creates an always-on monitoring system that detects new technical SEO problems before they impact rankings. Deployments, CMS changes, plugin updates, and infrastructure modifications can silently break SEO. This monitor catches regressions within hours instead of weeks.

## Input

- Baseline audit report from `technical-seo-crawl-audit` (the "known good" state)
- Google Search Console access
- n8n instance for scheduling
- PostHog for dashboarding and alerting

## Steps

### 1. Set up daily robots.txt monitor (n8n cron)

Using `n8n-scheduling`, create a workflow that runs every 6 hours:

1. Fetch `https://example.com/robots.txt` using `robots-txt-management`
2. Compare the content hash against the last known good version (stored in n8n static data or a simple key-value store)
3. If changed:
   - Diff the old vs. new content
   - Check: Are any previously-allowed important paths now blocked?
   - Check: Is the sitemap reference still present?
   - If a critical path is blocked: send CRITICAL alert immediately
   - If only minor changes: log and send INFO alert
4. Store the new content as the latest version

### 2. Set up daily indexation monitor (n8n cron)

Using `n8n-scheduling` and `google-search-console-api`, create a daily workflow:

1. Pull indexation status for 50 high-value pages (homepage, key landing pages, top traffic pages)
2. Compare against yesterday's status:
   - Pages that were indexed and are now NOT indexed: CRITICAL alert
   - Pages that are CRAWLED_NOT_INDEXED for 7+ consecutive days: HIGH alert
   - New pages that haven't been discovered after 14 days: MEDIUM alert
3. Pull aggregate search analytics (last 7 days vs. previous 7 days):
   - Total clicks drop > 20%: CRITICAL alert
   - Average position increase (worse) > 5 positions for key terms: HIGH alert
   - Total impressions drop > 30%: HIGH alert (may indicate deindexation)
4. Log all data points as PostHog events (`seo_indexation_check`, `seo_traffic_check`) for trend analysis

### 3. Set up weekly Core Web Vitals monitor (n8n cron)

Using `n8n-scheduling` and `pagespeed-insights-api`, create a weekly workflow:

1. Test the top 10 pages by traffic with PageSpeed Insights (mobile strategy)
2. Compare performance scores against the baseline:
   - Any page drops from "Good" to "Needs Improvement" or "Poor" on LCP/CLS/INP: HIGH alert
   - Overall performance score drops > 15 points: HIGH alert
   - Performance score drops > 30 points: CRITICAL alert
3. Store all scores as PostHog events (`seo_cwv_check`) with properties: url, lcp, cls, inp, performance_score
4. If regression detected, extract the specific Lighthouse audit recommendations that changed (new render-blocking resources, larger images, etc.)

### 4. Set up sitemap health monitor (n8n cron)

Using `n8n-scheduling`, create a weekly workflow:

1. Fetch and parse the sitemap
2. Test a random sample of 20 URLs from the sitemap:
   - Any URLs returning 4xx or 5xx: HIGH alert (sitemap contains dead URLs)
   - Any URLs returning 3xx: MEDIUM alert (sitemap contains redirects)
3. Compare URL count against previous week:
   - Count drops by > 10%: HIGH alert (pages may have been accidentally removed)
   - Count increases by > 50% in one week: INFO alert (verify new pages are intentional)
4. Cross-reference with GSC submitted vs. indexed count

### 5. Build the SEO health dashboard in PostHog

Using `posthog-dashboards`, create a dashboard with these panels:

- **Indexation trend**: line chart of indexed page count over last 90 days (from daily GSC checks)
- **Organic traffic trend**: line chart of total clicks from GSC over last 90 days
- **Core Web Vitals trend**: multi-line chart showing LCP, CLS, INP for top 10 pages over time
- **Performance score trend**: line chart of average Lighthouse score across monitored pages
- **Regression alerts**: event feed of all alerts triggered in the last 30 days
- **Pages at risk**: table of pages with declining rankings or degraded CWV

### 6. Configure alert routing

Set up alert destinations based on severity:

- **CRITICAL**: Immediate Slack message to #seo-alerts channel + email to site owner. Include: what changed, which URLs are affected, estimated traffic impact, recommended immediate action.
- **HIGH**: Slack message within 1 hour. Include: what changed, affected URLs, recommended fix.
- **MEDIUM**: Daily digest. Aggregate all medium alerts into a single daily summary.
- **LOW/INFO**: Weekly digest included in the SEO performance report.

### 7. Maintain the baseline

After each fix is verified (via `technical-seo-fix-pipeline`), update the baseline:

1. Re-run the relevant audit checks on fixed pages
2. Update the "known good" reference data (robots.txt hash, indexation status, CWV scores)
3. This prevents old fixed issues from triggering false positive alerts

## Output

- Always-on monitoring covering: robots.txt, indexation, Core Web Vitals, sitemap health, organic traffic
- Severity-based alerts routed to the appropriate channel
- PostHog dashboard showing SEO health trends over time
- Baseline reference data that updates after each verified fix

## Triggers

- robots.txt monitor: every 6 hours
- Indexation + traffic monitor: daily
- Core Web Vitals monitor: weekly
- Sitemap health monitor: weekly
- Dashboard: always-on, updated by event ingestion
