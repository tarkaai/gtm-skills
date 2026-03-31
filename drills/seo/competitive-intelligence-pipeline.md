---
name: competitive-intelligence-pipeline
description: Automated pipeline that monitors competitor product changes, pricing updates, and new market entrants and updates comparison pages accordingly
category: SEO
tools:
  - Firecrawl
  - Anthropic
  - n8n
  - Webflow
  - Ahrefs
  - Attio
fundamentals:
  - competitor-page-scraping
  - ahrefs-keyword-research
  - webflow-cms-bulk
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Competitive Intelligence Pipeline

This drill creates an always-on competitive monitoring system that detects when competitors change their product, pricing, or positioning and automatically updates your comparison pages. It also discovers new competitors entering your market.

## Input

- Published comparison pages tracked by `seo-performance-monitor`
- Competitor list from `competitor-keyword-research` with URLs for each competitor's pricing page, features page, and changelog
- n8n instance with Firecrawl and Anthropic API credentials configured
- Webflow CMS collection containing comparison page content

## Steps

### 1. Set up competitor page snapshots

Build an n8n workflow that runs weekly:

1. For each competitor in your list, use `competitor-page-scraping` to scrape their:
   - Pricing page
   - Features/product page
   - Changelog or "what's new" page (if available)
2. Store the scraped markdown in a persistent store (Airtable, Notion, or local JSON file) with: `competitor_name`, `page_url`, `scraped_date`, `content_markdown`
3. On each subsequent scrape, compare current markdown against the previous snapshot
4. If the diff exceeds a threshold (>5% content change), classify the change:
   - **pricing_change**: price numbers, plan names, or feature-per-plan allocations changed
   - **feature_change**: new feature announced, feature removed, or capability description updated
   - **positioning_change**: tagline, hero copy, or target audience description changed
   - **minor_change**: formatting, typos, or non-substantive edits (ignore these)

### 2. Generate comparison page updates

When a substantive change is detected, use Claude (Anthropic API) to generate updates:

```
System prompt: A competitor has updated their product information. Generate the specific
content changes needed for our comparison page.

Competitor: {competitor_name}
Change type: {change_type}
Previous content: {previous_snapshot}
New content: {current_snapshot}
Diff summary: {diff_text}

Our current comparison page content: {current_comparison_page_content}

Generate:
1. Updated rows for the feature comparison table (only rows that changed)
2. Updated prose sections that reference the changed information
3. A brief changelog note: "Last updated: {date} — {one-sentence summary of what changed}"

Do NOT rewrite the entire page. Only output the specific sections that need updating.
Output as HTML fragments keyed by section ID.
```

### 3. Discover new competitors

Build an n8n workflow that runs monthly:

1. Use `ahrefs-keyword-research` to query Content Explorer for recent pages (last 30 days) ranking for:
   - "{your product category} alternative"
   - "best {your product category}"
   - "{your product category} vs"
2. Extract product names from titles and URLs
3. Compare against your existing competitor list
4. For any new name appearing 3+ times: flag as a new competitor
5. Use `competitor-page-scraping` to gather initial data on the new competitor
6. Log the new competitor in Attio using `attio-notes`: create a note with the competitor's name, website, positioning, and estimated market presence
7. Add to the comparison page generation queue

### 4. Auto-update comparison pages

Build an n8n workflow triggered by change detection (Step 1 output):

1. Receive the change event: competitor name, change type, generated updates
2. Using `webflow-cms-bulk`, update the CMS item for the affected comparison page:
   - Replace changed table rows
   - Update prose sections
   - Set `last-updated` field to today
   - Add the changelog note
3. Publish the site
4. Log the update to PostHog: `comparison_page_auto_updated` with properties `competitor`, `change_type`, `sections_updated`

**Guardrails:**
- **Never auto-publish pricing changes.** Pricing updates require human verification. Flag for review and queue the update.
- **Never auto-publish if >30% of the page content would change.** Flag for human review.
- **Rate limit:** maximum 5 auto-updates per day across all comparison pages.

### 5. Track update impact

After each auto-update, monitor for 14 days:
- Compare organic traffic, CTR, and conversion rate before vs after the update
- If traffic or conversion drops >15% post-update, revert the change and alert the team
- Log update outcomes to build a learning database: which types of updates improve performance vs harm it

## Output

- Weekly competitor page snapshots with change detection
- Auto-generated comparison page updates when competitors change
- Monthly new competitor discovery reports
- Audit trail of every auto-update with impact measurement
- Attio records for new competitors

## Triggers

- Competitor monitoring: weekly via n8n cron
- New competitor discovery: monthly via n8n cron
- Page updates: triggered by change detection events
- Impact evaluation: 14 days after each update
