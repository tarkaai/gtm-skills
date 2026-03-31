---
name: competitor-keyword-research
description: Identify competitor brand keywords, "vs" queries, and "alternative to" queries that represent high-intent comparison search traffic
category: SEO
tools:
  - Ahrefs
  - Google Search Console
  - Clay
fundamentals:
  - ahrefs-keyword-research
  - google-search-console-api
  - clay-table-setup
  - clay-company-search
---

# Competitor Keyword Research

This drill identifies every keyword pattern where prospects search for competitors by name and produces a prioritized list of comparison page targets. These keywords represent solution-aware buyers actively evaluating options — the highest conversion-intent organic traffic available.

## Input

- Your product category (e.g., "CRM", "project management", "cold email")
- A seed list of 3-10 direct competitors (names and domains)
- Optional: existing GSC data showing competitor-related queries you already appear for

## Steps

### 1. Build the competitor list

Start with your known competitors. Expand the list using `ahrefs-keyword-research`:

- Query Content Explorer for pages ranking for "{product category} alternatives" — extract every product name mentioned
- Query Content Explorer for "{product category} vs" — extract all comparison pairs
- Use `clay-company-search` to find additional competitors: search Clay for companies in your product category with >100 employees or >$1M funding

Target: 15-30 competitors. Include direct competitors (same category, same buyer), indirect competitors (different approach to the same problem), and adjacent tools (partial overlap in functionality).

### 2. Map keyword patterns per competitor

For each competitor, research these keyword patterns using `ahrefs-keyword-research`:

| Pattern | Example | Intent |
|---------|---------|--------|
| `{competitor} alternative` | "Salesforce alternative" | Actively seeking to switch |
| `{competitor} alternatives` | "Salesforce alternatives" | Comparing multiple options |
| `{competitor} vs {your brand}` | "Salesforce vs HubSpot" | Direct head-to-head evaluation |
| `{your brand} vs {competitor}` | "HubSpot vs Salesforce" | Same, reversed |
| `{competitor} vs` | "Salesforce vs" | Looking for any comparison |
| `{competitor} pricing` | "Salesforce pricing" | Evaluating cost, may be dissatisfied |
| `{competitor} review` | "Salesforce review" | Validating or questioning current choice |
| `{competitor} competitors` | "Salesforce competitors" | Market landscape research |
| `best {category} for {use case}` | "best CRM for startups" | Category comparison, not brand-specific |

For each pattern, pull: `volume`, `keyword_difficulty`, `traffic_potential`, `cpc`.

### 3. Score and prioritize

Use `clay-table-setup` to create a Clay table with one row per keyword target. Calculate a priority score:

```
priority = (traffic_potential * 0.4) + ((100 - keyword_difficulty) * 0.3) + (cpc * 10 * 0.2) + (brand_familiarity * 0.1)
```

- `traffic_potential`: estimated clicks if you rank top 3
- `keyword_difficulty`: lower is better (easier to rank)
- `cpc`: proxy for commercial intent (higher CPC = buyer is closer to purchase)
- `brand_familiarity`: 10 if the competitor is well-known in your market, 5 if moderately known, 1 if niche

Sort by priority score. The top 20-30 keywords are your first batch of comparison pages.

### 4. Map page types

Assign each keyword to a page type:

| Page Type | URL Pattern | When to Use |
|-----------|-------------|-------------|
| 1:1 comparison | `/compare/{competitor}-vs-{your-brand}` | Competitor has >500 monthly volume for "vs" queries |
| Alternatives page | `/compare/{competitor}-alternatives` | Competitor has >200 monthly volume for "alternative" queries |
| Category roundup | `/compare/best-{category}-for-{use-case}` | Multiple competitors in one use case with combined volume >300 |

### 5. Identify content angles per page

For each page target, note the content angle the page must address:

- **Why are searchers looking?** (dissatisfied with competitor? evaluating for first time? upgrading?)
- **What do they need to see?** (feature comparison table, pricing comparison, user reviews, migration guide)
- **What is our strongest differentiation?** (price, features, ease of use, support, specific use case fit)

Store these notes in the Clay table — they become the content brief for each comparison page.

## Output

A Clay table (or JSON/CSV export) with one row per comparison page target, containing:
- `target_keyword`, `page_type`, `url_slug`
- `competitor_name`, `search_volume`, `keyword_difficulty`, `cpc`, `traffic_potential`
- `priority_score`
- `content_angle` (why searchers look, what they need, our differentiation)
- `related_keywords` (other queries this page should also target)

This dataset is the direct input to the `comparison-page-creation` drill.

## Triggers

- Run once at play start to build the initial keyword target list
- Re-run monthly to discover new competitors and trending queries
- Re-run when a new competitor enters your market
