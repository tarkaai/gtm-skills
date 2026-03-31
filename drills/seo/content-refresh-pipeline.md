---
name: content-refresh-pipeline
description: Detect underperforming programmatic SEO pages and automatically refresh content to recover or improve rankings
category: SEO
tools:
  - Google Search Console
  - Ahrefs
  - Anthropic
  - Webflow
  - n8n
fundamentals:
  - google-search-console-api
  - ahrefs-rank-tracking
  - webflow-cms-bulk
  - n8n-workflow-basics
  - n8n-scheduling
---

# Content Refresh Pipeline

This drill detects programmatic SEO pages that are underperforming or declining, diagnoses why, and automatically refreshes their content to recover or improve rankings. It is the SEO-specific optimization loop that feeds into the broader `autonomous-optimization` drill at Durable level.

## Input

- Published programmatic pages tracked by `seo-performance-monitor`
- GSC search analytics data (clicks, impressions, CTR, position per page)
- Ahrefs ranking data (position changes, new/lost keywords)
- The original keyword matrix with target keywords and content variables

## Steps

### 1. Identify pages needing refresh

Using `google-search-console-api` and `ahrefs-rank-tracking`, run a weekly scan to categorize every published page:

**Priority 1 — Declining pages:**
- Position worsened by >5 spots in the last 30 days
- Clicks dropped >30% month-over-month
- These pages had traction and are losing it. Urgent refresh.

**Priority 2 — Stuck pages:**
- Ranking positions 11-30 for >60 days (page 2-3, never made it to page 1)
- High impressions but low CTR (below 2%)
- These pages are close to ranking but need a push.

**Priority 3 — Not indexed:**
- Published >30 days ago but still not indexed in GSC
- These pages may have thin content, duplicate content, or crawl issues.

**Priority 4 — Low engagement:**
- Ranking on page 1 but engagement rate <20% (from PostHog `seo_page_engaged` events)
- High bounce rate indicates the content doesn't match search intent.

### 2. Diagnose the issue per page

For each flagged page, run a diagnostic:

**For declining pages:**
- Check if competitors published better content (use Ahrefs SERP overview for the target keyword)
- Check if the page's content is now outdated (dates, statistics, product references)
- Check if Google's algorithm changed (look for broad patterns across all pages declining simultaneously)

**For stuck pages:**
- Compare word count and depth vs top 3 ranking pages
- Check if the page has internal links pointing to it (thin internal linking = weak signals)
- Check meta title and description — is the title click-worthy?

**For not-indexed pages:**
- Check for duplicate content with other pages in the batch (compare H1, first paragraph, meta description)
- Check page load speed (slow pages may not be crawled)
- Verify the page is in the sitemap and not blocked by robots.txt

**For low-engagement pages:**
- Analyze search query vs page content alignment — is the page answering the right question?
- Check if the CTA is relevant to the visitor's intent

### 3. Generate refreshed content

For each page flagged for refresh, generate updated content using Claude (Anthropic API):

```
System prompt: You are refreshing an underperforming SEO page.
Current target keyword: {target_keyword}
Current ranking position: {position}
Issue diagnosed: {diagnosis}
Top-ranking competitor content summary: {competitor_summary}

Rewrite the page content to:
- Address the diagnosed issue specifically
- Be more comprehensive than the current top 3 results
- Include updated data, examples, and statistics for 2026
- Improve the introduction to better match search intent
- Strengthen H2 headings to include related keywords: {related_keywords}
- Add or improve the FAQ section based on "People Also Ask" data
- Keep the same URL slug and target keyword

Output as HTML. Target 1,000-1,800 words.
```

**For not-indexed pages:** Strip and simplify. Reduce to 600-800 words of highly unique content. Remove anything that looks templated or duplicated.

**For low-CTR pages:** Rewrite the meta title and meta description to be more compelling:
- Title: include the target keyword, add a benefit or number, keep under 60 characters
- Description: include a clear value proposition and call to action, keep under 155 characters

### 4. Publish updated content

Using `webflow-cms-bulk`, update the CMS item for each refreshed page:

- Update `body-content` with the new HTML
- Update `meta-title` and `meta-description` if they changed
- Update `last-refreshed` timestamp to today's date
- Publish the site after all updates

### 5. Track refresh impact

After publishing refreshes, monitor each page for 14-28 days:

- Log the refresh event in PostHog: `seo_page_refreshed` with properties: `url`, `target_keyword`, `issue_type`, `refresh_date`
- After 14 days, compare: position change, CTR change, click change, engagement change
- Score the refresh: **success** (improved on the flagged metric), **neutral** (no significant change), **failure** (metric worsened)
- Store refresh outcomes to improve future diagnosis and content generation

### 6. Automate the pipeline (Scalable+ levels)

Using `n8n-workflow-basics` and `n8n-scheduling`, create a weekly n8n workflow:

1. Pull GSC and Ahrefs data
2. Run the identification logic (Step 1)
3. Run diagnostics (Step 2)
4. Generate refreshed content via Anthropic API (Step 3)
5. Quality-check: verify uniqueness, keyword inclusion, length
6. Update Webflow CMS items (Step 4)
7. Publish the site
8. Log all refreshes to PostHog
9. Send a summary of pages refreshed to Slack

## Output

- Weekly list of pages flagged for refresh, categorized by priority
- Refreshed content published for flagged pages
- Impact tracking per refresh (14-day post-refresh comparison)
- Historical refresh log showing what works and what does not

## Triggers

- Weekly: automated scan and refresh cycle via n8n
- On-demand: triggered by anomaly alerts from `seo-performance-monitor`
- Post-algorithm-update: triggered manually when a Google algorithm update is detected and rankings shift broadly
