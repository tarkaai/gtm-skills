---
name: technical-seo-audit-optimization-smoke
description: >
  Technical SEO Audit & Optimization — Smoke Test. Run a one-time comprehensive crawl
  audit of the website, fix all critical and high-severity issues, and verify
  indexation and Core Web Vitals improvements.
stage: "Marketing > Solution Aware"
motion: "FounderSocialContent"
channels: "Website, Content"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "Zero critical technical SEO errors and all Core Web Vitals in 'Good' range on top 10 pages"
kpis: ["Critical issues resolved", "Pages indexed in GSC", "Core Web Vitals pass rate", "Average Lighthouse performance score"]
slug: "technical-seo-audit-optimization"
install: "npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization"
drills:
  - technical-seo-crawl-audit
  - technical-seo-fix-pipeline
  - threshold-engine
---

# Technical SEO Audit & Optimization — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

All critical and high-severity technical SEO issues are resolved. Every important page is indexable and indexed in Google Search Console. Core Web Vitals (LCP, INP, CLS) are in the "Good" range on the top 10 pages by traffic. The site has a clean robots.txt, a complete sitemap, and valid structured data on key page types.

## Leading Indicators

- Screaming Frog crawl returns zero 4xx/5xx errors on internal links within 3 days of fixes
- GSC URL Inspection shows "SUBMITTED_AND_INDEXED" for all key pages within 14 days
- PageSpeed Insights performance score >= 75 on mobile for all top 10 pages
- No redirect chains with 3+ hops remain
- Sitemap submission in GSC shows submitted count equals indexed count (within 90%)

## Instructions

### 1. Run the full technical SEO crawl audit

Run the `technical-seo-crawl-audit` drill against the production site. Provide the target URL, GSC credentials, and Ahrefs API token. The drill will:

- Crawl every page on the site using Screaming Frog
- Audit robots.txt for blocking issues
- Audit the sitemap for completeness and errors
- Categorize every issue by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Test Core Web Vitals on the top 20 pages via PageSpeed Insights
- Validate structured data on representative pages
- Check indexation health via GSC
- Produce a prioritized audit report sorted by Impact Score

Review the audit report. Confirm the severity classifications are correct. If any issues are misclassified, adjust before proceeding.

### 2. Implement critical and high-severity fixes

Run the `technical-seo-fix-pipeline` drill with the audit report. At Smoke level, the agent prepares each fix and presents it for review before implementation. The drill will process fixes in this order:

1. **Robots/crawl directive fixes**: Unblock important pages, fix canonical tags, correct meta robots directives
2. **Infrastructure fixes**: Resolve redirect chains, fix broken internal links, ensure HTTPS everywhere
3. **Content/metadata fixes**: Add missing titles, descriptions, and H1 tags. De-duplicate where needed.
4. **Structured data**: Add JSON-LD markup for key page types (homepage, product pages, blog posts)
5. **Performance fixes**: Address Lighthouse recommendations — compress images, defer JS, fix CLS sources

**Human action required:** Review each batch of fixes before deployment. Verify that:
- Canonical changes point to the correct URLs
- Redirect updates don't break existing inbound links
- Generated titles and descriptions accurately represent each page
- Structured data markup is correct for the page content

Deploy each batch. After deployment, the drill will verify each fix and submit affected URLs for re-indexing via GSC.

### 3. Verify improvements

Wait 7-14 days after all fixes are deployed. Then:

1. Re-run the `technical-seo-crawl-audit` drill to confirm issues are resolved
2. Check GSC: are previously non-indexed pages now indexed?
3. Re-run PageSpeed Insights on the top 10 pages: are all CWV in "Good" range?
4. Compare before/after: total critical issues, total indexed pages, average performance score

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: Zero critical technical SEO errors AND all Core Web Vitals in "Good" range on top 10 pages.

If PASS: proceed to Baseline. The site's technical foundation is clean.
If FAIL: identify which issues persist and re-run the fix pipeline on those specific issues. Common blockers: pages that won't index (check content quality), CWV regressions after deployment (check caching config).

## Time Estimate

- Crawl audit setup and execution: 2 hours
- Audit review and fix prioritization: 1 hour
- Fix implementation (agent prepares, human reviews): 3 hours
- Verification and re-audit: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Screaming Frog SEO Spider | Full site crawl and issue detection | $259/year — https://www.screamingfrog.co.uk/seo-spider/pricing/ |
| Google Search Console | Indexation status, search analytics, re-index requests | Free — https://search.google.com/search-console |
| Google PageSpeed Insights | Core Web Vitals and Lighthouse auditing | Free — https://pagespeed.web.dev/ |
| Ahrefs | Current rankings to prioritize high-value page fixes | $99-199/mo — https://ahrefs.com/pricing |
| Anthropic Claude API | Generate missing titles, descriptions, structured data | ~$0.50-2.00 per audit — https://anthropic.com/pricing |

## Drills Referenced

- `technical-seo-crawl-audit` — crawl the site, identify all technical SEO issues, produce prioritized report
- `technical-seo-fix-pipeline` — implement fixes in severity order, verify each fix, request re-indexing
- `threshold-engine` — evaluate pass/fail against zero critical errors and CWV targets
