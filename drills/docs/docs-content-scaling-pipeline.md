---
name: docs-content-scaling-pipeline
description: Automated pipeline that discovers keyword gaps, generates docs pages, publishes, and monitors performance — scaling docs content production 10x without proportional effort
category: Docs
tools:
  - Ahrefs
  - Google Search Console
  - Anthropic
  - Mintlify / GitBook / ReadMe / Docusaurus / Fumadocs
  - PostHog
  - n8n
fundamentals:
  - ahrefs-keyword-research
  - ahrefs-content-explorer
  - google-search-console-api
  - docs-platform-publishing
  - ai-content-ghostwriting
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-scheduling
---

# Docs Content Scaling Pipeline

This drill automates the documentation content production loop: discover keyword opportunities, generate pages, publish, track performance, and feed results back into discovery. It is the 10x multiplier that takes docs-as-marketing from manually written pages to a continuous content engine.

## Input

- Docs site with at least 20 published pages (baseline content foundation)
- Ahrefs API access for keyword research and competitor monitoring
- GSC access for search query data
- n8n instance for orchestration
- Docs platform repository access for automated publishing

## Steps

### 1. Set up the automated keyword discovery workflow

Using `n8n-workflow-basics` and `n8n-scheduling`, create a weekly n8n workflow:

**Source 1 — GSC query mining:**
Use `google-search-console-api` to pull queries where your docs pages get impressions but low CTR or no clicks:

```
POST /webmasters/v3/sites/{site_url}/searchAnalytics/query
{
  "startDate": "{28_days_ago}",
  "endDate": "{today}",
  "dimensions": ["query", "page"],
  "rowLimit": 500,
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "page",
      "operator": "contains",
      "expression": "/docs/"
    }]
  }]
}
```

Filter for queries with impressions > 10 but clicks < 3. These are topics Google thinks your docs should cover but your pages are not matching the intent well enough.

**Source 2 — Competitor keyword monitoring:**
Use `ahrefs-keyword-research` to pull new keywords your competitor docs sites rank for weekly:

```
GET /v3/site-explorer/organic-keywords
target={competitor_docs_domain}
where=position<=20,volume>=50
order_by=traffic:desc
mode=subdomains
limit=200
```

Compare against your current keyword list. New keywords competitors gained this week are opportunities.

**Source 3 — Docs search analytics:**
If using Algolia or PostHog search tracking, pull zero-result searches (see `docs-search-analytics` fundamental). Each zero-result search is a user explicitly requesting content you do not have.

### 2. Score and queue opportunities

For each discovered keyword opportunity, compute a priority score:

```
priority = (search_volume * 0.25) + ((100 - keyword_difficulty) * 0.25) + (intent_score * 0.25) + (gap_urgency * 0.25)
```

Where:
- `intent_score`: getting-started=100, how-to=80, integration=90, api-reference=60, troubleshooting=50
- `gap_urgency`: competitor already ranks = 100, user searched for it = 90, GSC impressions exist = 70, new keyword = 40

Add scored opportunities to a production queue (Attio list, Airtable, or JSON file in the docs repo).

### 3. Automate page generation

Using `n8n-workflow-basics`, create a workflow triggered when the queue has >= 5 items:

For each queued keyword:

1. Classify page type based on keyword pattern (how-to, integration, API ref, troubleshooting)
2. Pull the top 3 competitor pages for that keyword using `ahrefs-content-explorer`
3. Extract their structure: H2 headings, word count, topics covered
4. Generate the page using `ai-content-ghostwriting` with a prompt that:
   - Targets the specific keyword
   - Covers everything the top 3 competitors cover, plus unique product-specific content
   - Includes real code examples from your product's API
   - Follows your docs site's template for the page type
   - Sets proper frontmatter (title, description, keywords)

**Rate limit:** Generate a maximum of 10 pages per week. Quality matters more than volume.

### 4. Automated quality gate

Before any generated page is published, run an automated quality check:

1. **Keyword check:** Target keyword appears in title, first 100 words, and >= 1 H2
2. **Length check:** Meets minimum word count for page type (see `docs-content-production`)
3. **Code check:** All code blocks have a language specified. No placeholder or pseudo-code.
4. **Link check:** Page links to >= 2 existing docs pages with descriptive anchor text
5. **CTA check:** Page ends with a conversion CTA matching its intent tier
6. **Duplicate check:** First 200 words are < 30% similar to any existing page (prevents cannibalization)

Pages passing all checks go to a review queue. Pages failing any check are regenerated with specific fix instructions.

**Human action required:** Review the quality-gate output weekly. Approve, reject, or edit pages before they are published. As confidence grows over time, reduce review to spot-checks (every 5th page).

### 5. Batch publish and submit

Using `docs-platform-publishing`, publish approved pages:

1. Create pages in the docs repo (branch per batch)
2. Update navigation/sidebar to include new pages
3. Merge the branch
4. Submit new URLs to GSC using `google-search-console-api` URL Inspection
5. Log each published page as a PostHog event: `docs_page_published` with properties `url`, `target_keyword`, `page_type`, `generation_method` (automated)

### 6. Performance feedback loop

Using `posthog-custom-events`, track each automated page's performance at day 14 and day 30:

- Organic page views
- Time on page
- CTA click rate
- Search position for target keyword (from GSC)
- Indexation status

Feed performance data back into the priority scoring model:
- Pages that performed well → increase weight for similar keyword patterns
- Pages that underperformed → diagnose (thin content? wrong intent?) and adjust generation prompts
- Pages not indexed after 30 days → flag for rewrite or consolidation

## Output

- Weekly automated discovery of 10-30 keyword opportunities
- Scored and prioritized production queue
- 5-10 generated pages per week (after quality gate)
- Automated publishing with GSC submission
- 14-day and 30-day performance tracking per page
- Continuous feedback loop improving generation quality over time

## Triggers

- Keyword discovery: weekly via n8n cron (every Monday)
- Page generation: triggered when queue has >= 5 items
- Quality gate: runs automatically after generation
- Publishing: triggered by human approval (initially) or auto-publish (at maturity)
- Performance check: daily for first 30 days post-publish, then weekly
