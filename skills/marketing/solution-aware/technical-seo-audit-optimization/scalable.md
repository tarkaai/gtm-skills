---
name: technical-seo-audit-optimization-scalable
description: >
  Technical SEO Audit & Optimization — Scalable Automation. Expand monitoring to
  cover every page. Automate all fix categories including performance. Scale to
  handle site growth without proportional effort.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Scalable Automation"
time: "40 hours over 3 months"
outcome: ">= 50% YoY organic traffic growth and top-10 rankings maintained for all target keywords over 6 months"
kpis: ["Organic traffic (YoY change)", "Keywords in top 10", "Indexation ratio", "Average Lighthouse score", "Mean time to fix (MTTF) for regressions", "Issues auto-resolved vs. human-resolved"]
slug: "technical-seo-audit-optimization"
install: "npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization"
drills:
  - technical-seo-crawl-audit
  - technical-seo-fix-pipeline
  - dashboard-builder
  - seo-performance-monitor
  - threshold-engine
---

# Technical SEO Audit & Optimization — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

The agent manages technical SEO for a growing site without proportional effort increase. All fix categories — including infrastructure and performance — are automated with safe rollback. The monitoring system covers every indexed page, not just the top 10-20. The site achieves >= 50% year-over-year organic traffic growth and maintains top-10 rankings for all target keywords over 6 months.

## Leading Indicators

- Mean Time to Fix (MTTF) for new regressions < 48 hours
- Auto-fix success rate > 80% (fixes that resolve the issue without human intervention)
- Monitored page coverage = 100% of indexed pages
- Weekly crawl shows decreasing total issue count month over month
- New pages published to the site are automatically indexed within 7 days
- Lighthouse performance score average across all pages > 80

## Instructions

### 1. Expand crawl and monitoring coverage to full site

Upgrade the `technical-seo-crawl-audit` drill configuration:

1. Increase Screaming Frog crawl to cover ALL pages (not capped at top-N)
2. For sites with > 5,000 pages: run a full crawl weekly and a critical-pages-only crawl daily
3. Add JavaScript rendering to the crawl config (catch issues with SPAs and dynamically rendered content)
4. Expand PageSpeed Insights monitoring to test 50 pages per week (rotating through the full page inventory so every page is tested at least once per month)

Upgrade the `dashboard-builder` drill:

1. Increase indexation monitoring from 50 pages/day to all high-value pages (top 200 by traffic)
2. Add deployment hook: trigger an immediate crawl of changed pages whenever a deployment completes (n8n webhook listening to the CI/CD pipeline)
3. Add competitive monitoring: weekly Ahrefs check for competitor ranking changes on your target keywords

### 2. Automate all fix categories

Expand the `technical-seo-fix-pipeline` drill to handle HIGH issues autonomously (not just LOW/MEDIUM):

1. **Redirect chain resolution**: Agent detects chains with 3+ hops, implements direct redirects, verifies, and rolls back if any page returns an error within 24 hours
2. **Canonical fixes**: Agent detects mismatches, determines the correct canonical, implements the fix, and monitors indexation for 7 days (auto-reverts if the page drops out of the index)
3. **Performance fixes**: Agent identifies the highest-impact Lighthouse recommendations, implements them (image compression, JS deferral, CSS optimization), re-tests, and keeps the change only if the performance score improves
4. **Structured data expansion**: Agent generates JSON-LD for every page type on the site, validates, deploys, and monitors GSC for rich result impressions

**Human action required:** CRITICAL issues still require human approval. The agent prepares the fix, shows before/after, and estimates risk. Human approves or modifies.

Implement safe rollback for all automated fixes:
1. Before every change, store the current state (original file, original config)
2. After deployment, monitor the affected metrics for 48 hours
3. If any monitored metric degrades by > 10%, auto-revert and alert

### 3. Scale new-page indexation

As the site grows (new blog posts, new landing pages, new product pages):

1. When a new page is published, the agent automatically:
   - Adds it to the sitemap (via `sitemap-generation`)
   - Submits it for indexing via GSC API
   - Validates its structured data
   - Tests Core Web Vitals
   - Adds internal links from 2-3 related pages (to accelerate crawl discovery)
2. Track time-to-index for each new page. Target: indexed within 7 days.
3. If a page isn't indexed after 14 days, diagnose: check content quality, link equity, crawl logs.

### 4. Build the full SEO performance tracking system

Run the `seo-performance-monitor` drill to create a comprehensive organic search dashboard:

1. Daily GSC data sync: clicks, impressions, CTR, position by page and by keyword
2. Weekly Ahrefs sync: keyword rankings, new/lost keywords, backlink changes
3. Full PostHog dashboard with organic traffic funnels:
   - `organic_visit` -> `page_engaged` (scroll > 50% or 30s on page) -> `cta_clicked` -> `lead_converted`
4. Track organic traffic attribution to leads and pipeline (connect PostHog to Attio via n8n)
5. Weekly automated report: organic traffic, ranking changes, indexation health, CWV scores, fixes applied, pipeline impact

### 5. Optimize crawl budget

For sites with > 1,000 pages:

1. Analyze GSC crawl stats: which pages are being crawled most frequently? Are high-value pages being crawled often enough?
2. Block crawl waste: update robots.txt to disallow low-value parameter URLs, internal search results, tag pages with thin content
3. Prioritize crawl budget: ensure the sitemap lists pages in priority order, add `<priority>` values that reflect business value
4. Monitor: are your most important pages being recrawled within 7 days of updates?

### 6. Evaluate against threshold

Run the `threshold-engine` drill at the 6-month mark:

- Organic traffic: target >= 50% year-over-year growth
- Target keywords in top 10: target = 100% of primary keywords
- Indexation ratio: must remain >= 95%
- Average Lighthouse score across all pages: target >= 80
- MTTF for regressions: target < 48 hours

If PASS: proceed to Durable. The technical SEO system is self-running and producing growth.
If FAIL: identify the bottleneck. If traffic is growing but not fast enough, the issue may be content/backlinks rather than technical SEO (this play has done its job). If rankings are volatile, investigate algorithm-specific issues. If regressions are frequent, tighten the deployment monitoring.

## Time Estimate

- Expand monitoring and crawl coverage: 6 hours
- Automate HIGH-severity fix pipeline with rollback: 8 hours
- New-page indexation automation: 4 hours
- Full SEO performance tracking setup: 6 hours
- Crawl budget optimization: 4 hours
- Weekly review and oversight: 1 hour/week x 12 weeks = 12 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Screaming Frog SEO Spider | Full-site weekly crawl + daily critical crawl | $259/year — https://www.screamingfrog.co.uk/seo-spider/pricing/ |
| Google Search Console | Indexation, search analytics, crawl stats | Free — https://search.google.com/search-console |
| Google PageSpeed Insights | CWV monitoring across all pages | Free — https://pagespeed.web.dev/ |
| Ahrefs | Ranking tracking, competitive monitoring, backlink data | $199/mo (Standard) — https://ahrefs.com/pricing |
| PostHog | SEO health dashboard, organic traffic funnels | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Scheduling crawls, monitors, fix automation, deployment hooks | Free (self-hosted) or $20/mo — https://n8n.io/pricing |
| Anthropic Claude API | Auto-generating fixes, metadata optimization, content analysis | ~$5-15/mo — https://anthropic.com/pricing |

## Drills Referenced

- `technical-seo-crawl-audit` — full-site automated crawl with JavaScript rendering
- `technical-seo-fix-pipeline` — fully automated fix implementation with safe rollback
- `dashboard-builder` — deployment-triggered and scheduled regression detection
- `seo-performance-monitor` — comprehensive organic search performance tracking and reporting
- `threshold-engine` — 6-month evaluation against traffic growth and ranking targets
