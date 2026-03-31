---
name: technical-seo-fix-pipeline
description: Systematically implement technical SEO fixes from an audit report, verify each fix, and measure ranking impact
category: SEO
tools:
  - Google Search Console
  - Google PageSpeed Insights
  - n8n
  - Anthropic
fundamentals:
  - google-search-console-api
  - pagespeed-insights-api
  - sitemap-generation
  - robots-txt-management
  - structured-data-validation
  - n8n-workflow-basics
---

# Technical SEO Fix Pipeline

This drill takes the prioritized issue list from `technical-seo-crawl-audit` and systematically implements fixes, verifies each fix worked, and requests re-crawling from Google. It processes issues in Impact Score order — highest-value fixes first.

## Input

- Audit report JSON from `technical-seo-crawl-audit` (with issues sorted by Impact Score)
- Access to the site's codebase or CMS for making changes
- Google Search Console access for submitting URL re-indexing requests

## Steps

### 1. Group fixes by implementation type

Categorize each issue from the audit report into fix batches:

- **Robots/Crawl directives**: robots.txt changes, meta robots tags, canonical fixes → can often be fixed in a single deployment
- **Content/Metadata**: missing titles, descriptions, H1s, thin content → batch by page template or section
- **Infrastructure**: redirect chains, broken links, HTTPS issues → requires server/hosting config
- **Performance**: image optimization, render-blocking resources, unused JS/CSS → requires build pipeline changes
- **Structured data**: missing or invalid JSON-LD → batch by page type/template

Process batches in this order: Robots/Crawl > Infrastructure > Content/Metadata > Structured Data > Performance. This order maximizes indexation fixes first (no point optimizing pages Google cannot see).

### 2. Implement robots.txt and crawl directive fixes

Using `robots-txt-management`:

1. If robots.txt is blocking important pages, update the rules to allow them
2. If robots.txt is missing a sitemap reference, add it
3. Deploy the updated robots.txt
4. Verify: re-fetch robots.txt and confirm the changes are live
5. Test each previously-blocked URL with the `can_fetch("Googlebot", url)` check

Using `sitemap-generation`:

1. If the sitemap is missing pages, regenerate it with all indexable URLs
2. Remove any 404 or redirect URLs from the sitemap
3. Deploy the updated sitemap
4. Submit to GSC using `google-search-console-api`

### 3. Fix redirect chains and broken links

For each redirect chain (3+ hops):
1. Identify the final destination URL
2. Update the original redirect to point directly to the final destination (single hop)
3. Update any internal links that point to the redirect source to point directly to the destination

For each broken internal link (pointing to a 4xx page):
1. If the target page should exist: create or restore it
2. If the target page was moved: update the link to point to the new URL
3. If the target page is genuinely gone: remove the link or replace with a relevant alternative

### 4. Fix canonical and indexation issues

For each canonical mismatch:
1. Determine the correct canonical URL (the version that should rank)
2. Update the `<link rel="canonical">` tag on the page to self-reference correctly
3. If duplicate pages exist, set their canonical to the primary version

For each non-indexable page that should be indexed:
1. If blocked by `noindex` meta tag: remove the `noindex` directive
2. If blocked by canonical pointing elsewhere: fix the canonical (see above)
3. If blocked by `X-Robots-Tag` header: update the server configuration

### 5. Fix content and metadata issues

For missing or duplicate page titles:
1. Generate unique, keyword-rich titles under 60 characters
2. Include the primary target keyword near the beginning
3. Format: "{Primary Keyword} — {Brand}" or "{Primary Keyword}: {Value Proposition}"

For missing meta descriptions:
1. Generate descriptions under 155 characters
2. Include the target keyword and a clear value proposition or call-to-action
3. Each description must be unique across the site

For missing or duplicate H1 tags:
1. Each page gets exactly one H1 that includes the primary keyword
2. H1 should closely match the page title but can be slightly different

For thin content (< 300 words):
1. Expand the page with substantive content: add sections, examples, data
2. If the page has no ranking potential, consider consolidating it into a related page and redirecting

### 6. Implement structured data

Using `structured-data-validation`:

For each page type missing structured data:
1. Generate the appropriate JSON-LD markup (Article, FAQPage, BreadcrumbList, SoftwareApplication)
2. Inject the `<script type="application/ld+json">` tag into the page's `<head>`
3. Validate the markup using the structured data testing tool
4. Verify no validation errors before deploying

### 7. Fix performance issues

For each page with poor Core Web Vitals:
1. Review the specific Lighthouse audit recommendations from the audit report
2. Common fixes by category:
   - **LCP**: compress images, preload hero image, reduce server response time, remove render-blocking CSS/JS
   - **CLS**: set explicit width/height on images and embeds, avoid dynamically injecting content above the fold
   - **INP**: reduce JavaScript execution time, break up long tasks, defer non-critical JS
3. Implement fixes in the build pipeline or page templates
4. Re-test with `pagespeed-insights-api` after deployment

### 8. Verify fixes and request re-indexing

After each batch of fixes is deployed:

1. Re-run the relevant checks from `technical-seo-crawl-audit` on the affected URLs to confirm the issues are resolved
2. Using `google-search-console-api`, submit each fixed URL for re-indexing:
   ```
   POST https://indexing.googleapis.com/v3/urlNotifications:publish
   {"url": "https://example.com/fixed-page", "type": "URL_UPDATED"}
   ```
3. Log each fix: URL, issue type, what was changed, verification result, re-index request timestamp

### 9. Measure fix impact

After 2-4 weeks, pull fresh GSC data:

1. Compare indexation status: how many previously non-indexed pages are now indexed?
2. Compare search analytics: clicks, impressions, CTR, average position for the fixed pages
3. Re-run PageSpeed Insights on performance-fixed pages: compare scores before vs. after
4. Document the impact per fix category in the audit trail

## Output

- Fix log: every change made, which URL, what was changed, verification status
- Re-indexing request log: every URL submitted, timestamp
- Before/after comparison: metrics for each fixed page
- Remaining issues: any issues that could not be fixed (e.g., require human intervention or product changes)

## Triggers

- Run after each `technical-seo-crawl-audit` completes
- At Smoke level: one-time execution, human reviews each fix before deployment
- At Baseline level: weekly execution, agent implements low/medium fixes autonomously, flags high/critical for human review
- At Scalable level: continuous execution, agent implements all fixes autonomously with revert capability
