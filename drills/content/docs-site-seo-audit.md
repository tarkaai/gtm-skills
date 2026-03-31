---
name: docs-site-seo-audit
description: Audit a public documentation site for SEO readiness — indexation, keyword targeting, metadata, internal linking, and conversion paths
category: Docs
tools:
  - Google Search Console
  - Ahrefs
  - PostHog
  - Anthropic
fundamentals:
  - google-search-console-api
  - ahrefs-keyword-research
  - competitor-page-scraping
  - posthog-custom-events
---

# Docs Site SEO Audit

This drill evaluates a public documentation site's readiness to attract organic search traffic and convert visitors. It produces a prioritized list of issues to fix and keyword opportunities to target.

## Input

- Public docs site URL (e.g., `docs.yourcompany.com`)
- Google Search Console access for the docs domain/subdomain
- Product description and ICP (who searches for your docs topics)
- 2-3 competitor docs sites for benchmarking

## Steps

### 1. Crawl the docs site structure

Use `google-search-console-api` to pull the sitemap and all indexed URLs:

```
GET /webmasters/v3/sites/{site_url}/sitemaps
```

Then pull all pages from the sitemap XML. If no sitemap exists, note this as a critical issue.

For each page, extract:
- URL path
- Page title (from `<title>` tag)
- Meta description
- H1 heading
- Word count (body text only)
- Internal link count (links to other docs pages)
- External link count
- Has CTA (signup link, demo link, or lead capture form present: yes/no)

### 2. Check indexation status

Use `google-search-console-api` URL Inspection to check indexation for a sample of pages (50 pages or 20% of total, whichever is larger):

```
POST /v1/urlInspection/index:inspect
{
  "inspectionUrl": "{page_url}",
  "siteUrl": "{site_url}"
}
```

Categorize pages as: indexed, crawled-not-indexed, not-discovered, or blocked.

Flag: if indexation rate is below 80%, there is a structural issue (thin content, noindex tags, robots.txt blocking, orphaned pages).

### 3. Analyze keyword coverage

Use `ahrefs-keyword-research` to pull organic keywords the docs site currently ranks for:

```
GET /v3/site-explorer/organic-keywords
target={docs_domain}
where=position<=100
order_by=traffic:desc
limit=500
```

Group keywords by intent:
- **How-to queries:** "how to {action}" — these convert well from docs
- **API/integration queries:** "{product} API", "{product} webhook", "{product} SDK" — high intent
- **Error/troubleshooting queries:** "{product} error {code}", "fix {issue}" — support deflection + awareness
- **Comparison queries:** "{product} vs {competitor}" — should be on marketing site, not docs

### 4. Identify keyword gaps vs competitors

For each competitor docs site, use `ahrefs-keyword-research`:

```
GET /v3/site-explorer/organic-keywords
target={competitor_docs_domain}
where=position<=20
order_by=traffic:desc
limit=500
```

Compare: keywords competitors rank for that you do not. These are content gaps. Prioritize by:
- Search volume > 50/month
- Relevance to your product's capabilities
- Intent matches docs content (how-to, reference, troubleshooting)

### 5. Audit on-page SEO quality

For each docs page, check:

- **Title tag:** Under 60 characters? Contains target keyword? Unique across all pages?
- **Meta description:** Under 155 characters? Describes the page's value? Contains target keyword?
- **H1:** Matches the title? Only one H1 per page?
- **Content depth:** Word count > 300? (thin pages get de-prioritized by search engines)
- **Internal links:** Page links to >= 2 other docs pages? Page is linked FROM >= 2 other pages?
- **Code blocks:** Are code examples present for technical pages? (code blocks increase time-on-page)

Score each page 0-100 based on these checks.

### 6. Audit conversion paths

For each docs page, check whether there is a path from reading docs to becoming a lead:

- **CTA present:** Does the page have a signup link, "try it" button, or demo booking link?
- **CTA relevance:** Does the CTA match the page content? (API reference page should CTA to "get API key", not "book a demo")
- **CTA placement:** Is it visible without scrolling to the bottom?
- **Navigation to product:** Can a visitor get from docs to pricing/signup in 1-2 clicks?

Flag pages with no conversion path as high-priority fixes.

### 7. Produce the audit report

Output a structured report:

```json
{
  "site": "docs.yourcompany.com",
  "total_pages": 142,
  "indexed_pages": 118,
  "indexation_rate": 0.83,
  "organic_keywords_ranked": 312,
  "estimated_monthly_organic_traffic": 2400,
  "critical_issues": [
    {"issue": "No sitemap.xml found", "impact": "high", "fix": "Generate sitemap and submit to GSC"},
    {"issue": "23 pages have no meta description", "impact": "medium", "fix": "Add meta descriptions"}
  ],
  "keyword_gaps": [
    {"keyword": "webhook retry logic", "competitor": "competitor.com", "volume": 320, "difficulty": 25}
  ],
  "pages_without_cta": 47,
  "average_seo_score": 62,
  "top_opportunities": [
    {"action": "Create page for 'webhook retry logic'", "estimated_traffic": 180, "difficulty": "low"},
    {"action": "Add meta descriptions to 23 pages", "estimated_traffic_lift": 120, "difficulty": "low"}
  ]
}
```

## Output

- SEO health score for the docs site (0-100)
- Prioritized issue list with fix instructions
- Keyword gap list with traffic estimates
- Conversion path audit with missing CTA locations
- Top 10 quick-win opportunities ranked by estimated impact

## Triggers

- Run once at Smoke level to establish baseline
- Re-run quarterly at Baseline+ to track improvements and find new gaps
