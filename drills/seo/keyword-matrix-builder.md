---
name: keyword-matrix-builder
description: Research and build a structured keyword matrix for template-based programmatic page generation
category: SEO
tools:
  - Ahrefs
  - Google Search Console
  - Clay
fundamentals:
  - ahrefs-keyword-research
  - google-search-console-api
  - clay-table-setup
---

# Keyword Matrix Builder

This drill produces a structured keyword matrix: a spreadsheet-like dataset where each row is a page to create, with columns for the keyword, modifiers, search volume, difficulty, and content variables. This matrix feeds directly into the `programmatic-page-generator` drill.

## Input

- Your product or service category (e.g., "CRM", "project management", "invoicing")
- Your ICP definition (who you serve and what problems they have)
- Optional: existing GSC data showing queries you already rank for

## Steps

### 1. Identify the head term and pattern

Every programmatic SEO campaign starts with a pattern. The pattern is: `{head term} + {modifier}`. Examples:

- "best CRM for {industry}" -- modifiers: startups, real estate, agencies, nonprofits, healthcare
- "{tool} alternative" -- modifiers: Salesforce, HubSpot, Pipedrive, Monday
- "{tool} vs {tool}" -- modifiers: pairs of competitors
- "how to {action} in {tool}" -- modifiers: specific workflows
- "{job title} {tool}" -- modifiers: roles that use the product

Use `ahrefs-keyword-research` to validate the head term has search demand. Query the Keywords Explorer with your seed terms. Look for patterns in the suggestions where the same template repeats with different modifiers.

### 2. Expand the modifier list

For each pattern, build an exhaustive modifier list:

**For industry/vertical modifiers:**
Use `clay-table-setup` to create a Clay table. Use the Claygent to research: "List all industries and business types that use {product category}." Cross-reference with `ahrefs-keyword-research` — query `{head term} for` and collect all suggested completions.

**For competitor/alternative modifiers:**
Query Ahrefs Content Explorer for pages ranking for "{product category} alternative" and "{product category} vs". Extract all competitor names mentioned.

**For action/workflow modifiers:**
Use `google-search-console-api` to pull your existing Search Analytics data filtered to queries containing your brand or product terms. Look for query patterns where users search for specific actions or use cases.

**For location modifiers (if applicable):**
Generate from a reference list of cities, states, or countries relevant to your market.

Target: 50-500 modifiers per pattern. Each modifier becomes one page.

### 3. Validate search demand per combination

Use `ahrefs-keyword-research` bulk metrics endpoint to validate every `{head term} + {modifier}` combination:

- Pull `volume`, `keyword_difficulty`, and `traffic_potential` for each
- Filter out combinations with volume < 10/month (not worth a page)
- Filter out combinations with keyword_difficulty > 60 (too competitive for programmatic pages)
- Sort remaining by traffic_potential descending

### 4. Score and prioritize

For each validated keyword, calculate a priority score:

```
priority = (traffic_potential * 0.6) + ((100 - keyword_difficulty) * 0.3) + (cpc * 10 * 0.1)
```

- `traffic_potential` rewards high-traffic opportunities
- `(100 - keyword_difficulty)` rewards easier keywords
- `cpc * 10` is a proxy for commercial intent (higher CPC = more valuable traffic)

Rank all keywords by priority score. The top 20% are your first batch.

### 5. Define content variables per page

For each keyword in the matrix, define the variables that change per page:

| Variable | Source | Example |
|----------|--------|---------|
| target_keyword | Ahrefs | "best crm for startups" |
| slug | Derived | "best-crm-for-startups" |
| h1 | Template | "Best CRM for Startups in 2026" |
| meta_title | Template | "Best CRM for Startups — Compare Top Tools \| Brand" |
| meta_description | Template | "Compare the top CRM tools for startups..." |
| modifier | Extracted | "startups" |
| category | Mapped | "CRM" |
| search_volume | Ahrefs | 2400 |
| keyword_difficulty | Ahrefs | 28 |
| related_keywords | Ahrefs | ["crm for small business", "startup tools"] |
| internal_link_targets | Matrix | ["/solutions/crm-for-agencies", "/solutions/crm-for-nonprofits"] |

### 6. Build internal linking map

Programmatic pages must cross-link to each other to build topical authority. For each page in the matrix:

- Link to 3-5 related pages from the same pattern (e.g., "CRM for startups" links to "CRM for small businesses", "CRM for agencies")
- Link to the parent category page (e.g., "/solutions/crm")
- Link from the parent category page to each child page

Store the internal link targets as a column in the matrix.

## Output

A structured dataset (JSON, CSV, or Clay table) with one row per page, containing:
- target_keyword, slug, h1, meta_title, meta_description
- modifier, category, search_volume, keyword_difficulty, priority_score
- related_keywords, internal_link_targets
- content_template_id (which template to use for generation)

This dataset is the direct input to the `programmatic-page-generator` drill.

## Triggers

- Run once at play start to build the initial matrix
- Re-run monthly to discover new modifiers and keywords
- Re-run quarterly for full matrix refresh including difficulty re-scoring
