---
name: technical-seo-crawl-audit
description: Crawl a website, categorize all technical SEO issues by severity, and produce a prioritized fix list
category: SEO
tools:
  - Screaming Frog SEO Spider
  - Google PageSpeed Insights
  - Google Search Console
  - Ahrefs
fundamentals:
  - screaming-frog-crawl
  - pagespeed-insights-api
  - google-search-console-api
  - robots-txt-management
  - structured-data-validation
  - sitemap-generation
  - ahrefs-rank-tracking
---

# Technical SEO Crawl Audit

This drill performs a comprehensive technical SEO audit of a website. It crawls every page, tests performance, checks indexation, validates structured data, and produces a severity-ranked list of issues with specific fix instructions. The output is a structured audit report that feeds directly into the `technical-seo-fix-pipeline` drill.

## Input

- Target website URL (e.g., `https://example.com`)
- Google Search Console access for the property
- Ahrefs API access (for current ranking data to prioritize fixes on high-value pages)
- Screaming Frog SEO Spider license (or alternative crawler)

## Steps

### 1. Crawl the entire site

Using `screaming-frog-crawl`, run a headless crawl of the target domain:

```bash
"/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher" \
  --crawl "https://example.com" \
  --headless \
  --output-folder "/tmp/seo-audit" \
  --export-tabs "Internal:All,Response Codes:Client Error (4xx),Response Codes:Server Error (5xx),Page Titles:All,Meta Description:All,H1:All,Canonicals:All,Directives:All,Images:All" \
  --bulk-export "All Inlinks,Redirect Chains,Orphan Pages"
```

Wait for crawl completion. Parse the CSV output files.

### 2. Audit robots.txt

Using `robots-txt-management`:

1. Fetch `https://example.com/robots.txt`
2. Check: Does it exist (200 OK)?
3. Check: Does it reference a sitemap?
4. Check: Are important page paths (/, /blog/, /solutions/, /pricing/) allowed for Googlebot?
5. Check: Are low-value paths (/admin/, /api/, /staging/) blocked?
6. Check: Is there a blanket `Disallow: /` that blocks everything?
7. Log each finding as CRITICAL (if blocking important pages), WARNING (if allowing junk pages), or OK.

### 3. Audit the sitemap

Using `sitemap-generation` and `google-search-console-api`:

1. Fetch the sitemap referenced in robots.txt (or try `/sitemap.xml`)
2. Parse: How many URLs are listed?
3. Cross-reference with the crawl: Are all important pages in the sitemap?
4. Cross-reference with GSC: How many sitemap URLs are indexed vs. submitted?
5. Check for stale entries: URLs in the sitemap that return 404 or redirect
6. Check sitemap validity: Valid XML, no URLs over the 50,000 limit, no files over 50MB

Log findings: CRITICAL (sitemap missing or contains errors), WARNING (stale URLs, missing pages), OK.

### 4. Categorize crawl issues

Parse `internal_all.csv` from the Screaming Frog output. For every indexable page, check:

**CRITICAL issues** (block indexing or cause ranking loss):
- HTTP status 4xx or 5xx on pages that have inbound links or rank for keywords
- `Indexability` = "Non-Indexable" on pages that should rank (noindex tag, canonical pointing elsewhere)
- Redirect chains with 3+ hops
- Canonical URL mismatches (self-referencing canonical is missing or points to wrong page)
- robots.txt blocking important pages

**HIGH issues** (degrade ranking potential):
- Missing page titles on indexable pages
- Duplicate page titles across multiple URLs
- Missing meta descriptions on indexable pages
- Missing H1 tags on indexable pages
- Duplicate H1 tags across multiple URLs
- Pages with word count < 300 that are expected to rank
- Broken internal links (links to 4xx pages)

**MEDIUM issues** (sub-optimal but not blocking):
- Page titles too long (>60 chars) or too short (<30 chars)
- Meta descriptions too long (>155 chars) or too short (<70 chars)
- Multiple H1 tags on a single page
- Images missing alt text
- URLs with parameters that create duplicate content
- HTTP pages that should be HTTPS

**LOW issues** (best practice improvements):
- URLs with uppercase characters, underscores, or excessive depth (>4 levels)
- Missing Open Graph tags
- Missing hreflang tags (if multi-language)
- Excessive DOM size (>1,500 elements)

### 5. Audit Core Web Vitals

Using `pagespeed-insights-api`, test the top 20 pages by traffic (from Ahrefs or GSC):

1. For each URL, run PageSpeed Insights with `strategy=mobile`
2. Extract: LCP, INP, CLS, overall performance score, SEO score
3. Flag pages where:
   - LCP > 4000ms: CRITICAL
   - LCP 2500-4000ms: HIGH
   - CLS > 0.25: CRITICAL
   - CLS 0.1-0.25: HIGH
   - INP > 500ms: CRITICAL
   - INP 200-500ms: HIGH
   - Performance score < 50: CRITICAL
   - Performance score 50-75: HIGH
4. Extract the top 3 specific optimization opportunities per page from `lighthouseResult.audits` (e.g., "render-blocking resources", "unused JavaScript", "unoptimized images")

### 6. Audit structured data

Using `structured-data-validation`:

1. For each page type (homepage, product pages, blog posts, comparison pages), test one representative URL
2. Check: Is any JSON-LD structured data present?
3. Check: Does the structured data pass validation (no errors)?
4. Check: Are the correct schema types used for each page type?
5. Identify missing opportunities: pages that could have FAQPage, BreadcrumbList, SoftwareApplication, or Article markup but don't

### 7. Check indexation health via GSC

Using `google-search-console-api`:

1. Pull indexation status for a sample of 50 important pages (homepage, key landing pages, top blog posts)
2. Categorize: SUBMITTED_AND_INDEXED (good), CRAWLED_NOT_INDEXED (investigate), DISCOVERED_NOT_INDEXED (crawl budget issue), URL_IS_UNKNOWN (not submitted)
3. Pull search analytics for the last 28 days: total clicks, impressions, average CTR, average position
4. Identify pages with high impressions but low CTR (<2%): these need title/description optimization
5. Identify pages with declining position over the last 3 months

### 8. Prioritize fixes by impact

Using the `ahrefs-rank-tracking` fundamental, pull the current organic traffic estimate per page. Then score each issue:

**Impact Score** = Issue Severity Weight x Page Traffic Value

Severity weights: CRITICAL = 10, HIGH = 5, MEDIUM = 2, LOW = 1

Sort all issues by Impact Score descending. This ensures you fix the highest-value problems first.

### 9. Produce the audit report

Generate a structured report (JSON or Markdown) with:

```json
{
  "audit_date": "2026-03-30",
  "site": "https://example.com",
  "summary": {
    "pages_crawled": 450,
    "pages_indexed": 380,
    "critical_issues": 12,
    "high_issues": 34,
    "medium_issues": 89,
    "low_issues": 156,
    "avg_performance_score": 62,
    "avg_seo_score": 85
  },
  "issues": [
    {
      "id": "issue-001",
      "severity": "CRITICAL",
      "category": "indexation",
      "description": "Homepage canonical points to /home instead of /",
      "affected_urls": ["https://example.com/"],
      "impact_score": 100,
      "fix": "Update canonical tag on / to self-reference https://example.com/"
    }
  ],
  "core_web_vitals": { ... },
  "structured_data": { ... },
  "indexation_health": { ... }
}
```

## Output

- Complete audit report in JSON format with every issue, its severity, affected URLs, and specific fix instruction
- Issues sorted by Impact Score (severity x page value)
- Core Web Vitals scores for top 20 pages
- Structured data validation results
- Indexation health summary from GSC

## Triggers

- Run manually at Smoke level (one-time audit)
- Run weekly at Baseline level (automated via n8n)
- Run daily at Scalable level (for critical checks only; full audit weekly)
