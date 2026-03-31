---
name: technical-seo-audit-optimization-baseline
description: >
  Technical SEO Audit & Optimization — Baseline Run. Automate weekly crawl audits
  and fix pipelines. Establish continuous indexation and CWV monitoring.
  Measure organic traffic lift from sustained technical hygiene.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "Organic traffic increases >= 20% and average position improves >= 5 ranks over 8 weeks"
kpis: ["Organic clicks (GSC)", "Average position (GSC)", "Pages indexed / pages submitted", "Core Web Vitals pass rate", "Critical issues per crawl"]
slug: "technical-seo-audit-optimization"
install: "npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization"
drills:
  - technical-seo-crawl-audit
  - technical-seo-fix-pipeline
  - technical-seo-regression-monitor
  - posthog-gtm-events
  - threshold-engine
---

# Technical SEO Audit & Optimization — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Weekly automated crawl audits catch new issues within 7 days of introduction. The agent autonomously fixes LOW and MEDIUM severity issues and flags HIGH/CRITICAL for human review. Organic traffic from Google Search increases >= 20% and average position for target keywords improves >= 5 ranks over 8 weeks compared to the Smoke Test baseline.

## Leading Indicators

- Weekly crawl reports show zero net-new CRITICAL issues (regressions are caught and fixed same week)
- Indexation ratio (indexed / submitted in GSC) stays above 90%
- Core Web Vitals remain in "Good" range on all monitored pages week over week
- GSC impressions trend upward for 4 consecutive weeks
- Average click-through rate improves as titles and descriptions are optimized

## Instructions

### 1. Configure SEO event tracking in PostHog

Run the `posthog-gtm-events` drill to set up the event taxonomy for technical SEO monitoring:

- `seo_crawl_completed`: fires when a weekly crawl finishes. Properties: `pages_crawled`, `critical_count`, `high_count`, `medium_count`, `low_count`, `new_issues`, `resolved_issues`
- `seo_fix_deployed`: fires when a fix batch is deployed. Properties: `fix_category`, `issues_fixed`, `urls_affected`
- `seo_indexation_check`: fires daily. Properties: `pages_indexed`, `pages_submitted`, `indexation_rate`
- `seo_cwv_check`: fires weekly. Properties: `url`, `lcp`, `cls`, `inp`, `performance_score`
- `seo_traffic_check`: fires daily. Properties: `total_clicks`, `total_impressions`, `avg_ctr`, `avg_position`, `clicks_change_pct`

Build a PostHog dashboard: indexation trend, traffic trend, CWV scores over time, issue count per crawl.

### 2. Automate weekly crawl audits

Run the `technical-seo-crawl-audit` drill as an automated weekly workflow via n8n:

1. Schedule a cron trigger for Sunday 2am (or any low-traffic period)
2. The drill crawls the full site, runs all checks, and produces the audit report
3. Compare each week's report against the previous week: flag new issues as regressions
4. Log the crawl results as a `seo_crawl_completed` event in PostHog
5. If new CRITICAL or HIGH issues are detected, send an immediate alert

The agent autonomously fixes LOW and MEDIUM issues from each weekly crawl (metadata improvements, image alt text, URL structure). HIGH and CRITICAL issues are queued for human review with the specific fix recommendation.

### 3. Automate the fix pipeline

Run the `technical-seo-fix-pipeline` drill in continuous mode:

1. After each weekly crawl, the agent picks up all LOW and MEDIUM issues and implements fixes
2. For each fix: implement the change, deploy, verify the fix resolved the issue, submit affected URLs for re-indexing
3. Log each fix as a `seo_fix_deployed` event in PostHog
4. HIGH and CRITICAL issues: the agent prepares the fix and creates a review request with before/after details

**Human action required:** Review HIGH and CRITICAL fix recommendations weekly. Approve, modify, or reject each one. The agent will implement approved fixes and track their impact.

### 4. Set up regression monitoring

Run the `technical-seo-regression-monitor` drill to create always-on monitors:

- robots.txt monitoring every 6 hours
- Indexation and traffic monitoring daily via GSC
- Core Web Vitals monitoring weekly via PageSpeed Insights
- Sitemap health monitoring weekly

Configure alert routing: CRITICAL alerts go to Slack immediately, HIGH alerts within 1 hour, MEDIUM/LOW in daily/weekly digests.

This catches problems caused by deployments, CMS changes, or infrastructure updates before they impact rankings.

### 5. Optimize high-impression, low-CTR pages

Using GSC data from the daily monitoring:

1. Identify pages with >= 1,000 monthly impressions but CTR < 2%
2. These pages rank but don't get clicks — the title and description need improvement
3. The agent generates optimized titles (under 60 chars, keyword-first) and meta descriptions (under 155 chars, with clear value proposition)
4. Deploy as part of the weekly fix pipeline
5. Track CTR changes over the next 4 weeks per page

### 6. Evaluate against threshold

Run the `threshold-engine` drill at the 8-week mark. Compare against the Smoke Test baseline:

- Organic clicks from GSC: target >= 20% increase
- Average position for target keywords: target >= 5 rank improvement
- Indexation ratio: must remain >= 90%
- CWV: all monitored pages must remain in "Good" range

If PASS: proceed to Scalable. The automated pipeline is working and producing measurable ranking improvements.
If FAIL: diagnose — is traffic increasing but not fast enough (stay at Baseline longer)? Are regressions wiping out gains (tighten monitoring)? Are the right pages being prioritized (review Impact Score weighting)?

## Time Estimate

- PostHog event setup: 2 hours
- Automated crawl pipeline setup: 3 hours
- Regression monitor setup: 3 hours
- Weekly review and approval of HIGH/CRITICAL fixes: 1 hour/week x 8 weeks = 8 hours
- Threshold evaluation and analysis: 2 hours
- Buffer for debugging and iteration: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Screaming Frog SEO Spider | Weekly automated crawls | $259/year — https://www.screamingfrog.co.uk/seo-spider/pricing/ |
| Google Search Console | Indexation tracking, search analytics, re-indexing | Free — https://search.google.com/search-console |
| Google PageSpeed Insights | Weekly Core Web Vitals monitoring | Free — https://pagespeed.web.dev/ |
| Ahrefs | Ranking data for Impact Score calculation | $99-199/mo — https://ahrefs.com/pricing |
| PostHog | SEO health dashboard and event tracking | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Scheduling weekly crawls, daily monitors, fix automation | Free (self-hosted) or $20/mo — https://n8n.io/pricing |
| Anthropic Claude API | Generating optimized titles, descriptions, fix recommendations | ~$2-5/mo — https://anthropic.com/pricing |

## Drills Referenced

- `technical-seo-crawl-audit` — weekly automated crawl producing issue reports
- `technical-seo-fix-pipeline` — automated fix implementation with human approval for high-severity issues
- `technical-seo-regression-monitor` — always-on monitoring for robots.txt, indexation, CWV, sitemap health
- `posthog-gtm-events` — SEO event taxonomy and dashboard setup
- `threshold-engine` — 8-week evaluation against organic traffic and ranking targets
