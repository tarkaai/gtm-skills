---
name: topic-cluster-mapping
description: Research and map pillar topics to cluster subtopics using keyword data, SERP analysis, and ICP intent signals
category: SEO
tools:
  - Ahrefs
  - Google Search Console
  - Anthropic
  - Clay
fundamentals:
  - ahrefs-keyword-research
  - google-search-console-api
  - clay-table-setup
---

# Topic Cluster Mapping

This drill produces a structured cluster map: one pillar topic with 10-30 cluster subtopics, each validated by keyword data. The map defines what to write, how pieces connect, and which subtopics to prioritize first. It feeds directly into the `cluster-content-production` drill and the `blog-seo-pipeline` drill.

## Input

- Product category and ICP description (who you serve, what problems they have)
- 1-3 candidate pillar topics (broad head terms your product owns authority on)
- Optional: existing GSC data showing queries your site already ranks for
- Optional: competitor domains for gap analysis

## Steps

### 1. Validate pillar topic candidates

For each candidate pillar topic, use `ahrefs-keyword-research` to pull:

```
GET /v3/keywords-explorer/google/keyword-ideas
keywords={pillar_topic}
where=volume>100
order_by=traffic_potential:desc
limit=500
```

A valid pillar topic has:
- Monthly search volume >= 500 for the head term
- At least 20 related keyword suggestions with volume >= 50
- A mix of informational ("what is X", "how to X") and commercial ("best X", "X vs Y") intent
- Relevance to your ICP's buying journey (solution-aware stage = they know the category, comparing options)

If a candidate has fewer than 20 viable subtopics, it is too narrow. If it has 200+, consider splitting into multiple pillars.

### 2. Generate the subtopic universe

From the Ahrefs keyword suggestions in Step 1, extract every distinct subtopic. Group by intent type:

**Informational (top of cluster):**
- "what is {pillar}" / "how does {pillar} work"
- "how to {action} with {pillar}"
- "{pillar} best practices" / "{pillar} strategy"
- "{pillar} examples" / "{pillar} case studies"

**Comparative (middle of cluster):**
- "{pillar} vs {alternative}"
- "best {pillar} tools" / "best {pillar} software"
- "{pillar} for {industry/role}"
- "{pillar} pros and cons"

**Transactional (bottom of cluster):**
- "{pillar} pricing" / "{pillar} cost"
- "{pillar} template" / "{pillar} checklist"
- "{pillar} tutorial" / "{pillar} getting started"

Use `clay-table-setup` to create a Clay table storing each subtopic row: `subtopic`, `target_keyword`, `search_volume`, `keyword_difficulty`, `intent_type`, `priority_score`, `pillar_topic`, `status`.

### 3. Expand with SERP gap analysis

For your top 10 subtopics by search volume, use `ahrefs-keyword-research` Content Explorer:

```
GET /v3/content-explorer/search
query="{subtopic}" -site:{your_domain}
order_by=organic_traffic:desc
limit=20
```

For each competitor article ranking for your subtopic:
- Note their H2 structure (what sections they cover)
- Note their word count and depth
- Identify subtopics they cover that you have NOT yet listed

Add any net-new subtopics discovered to your Clay table.

### 4. Score and prioritize subtopics

For each subtopic, calculate a priority score:

```
priority = (search_volume * 0.3) + ((100 - keyword_difficulty) * 0.3) + (intent_weight * 0.2) + (gap_score * 0.2)
```

Where:
- `search_volume`: raw monthly volume
- `keyword_difficulty`: Ahrefs KD (lower = better)
- `intent_weight`: transactional=100, comparative=70, informational=40
- `gap_score`: 100 if no competitor covers it well, 50 if competitors exist but are thin, 0 if strong competition

Sort by priority. The top 8-12 subtopics are your first cluster batch.

### 5. Map the internal linking architecture

Define the link relationships between pillar and cluster pages:

**Pillar page links OUT to:**
- Every cluster subtopic page (one link per subtopic in a structured hub section)

**Each cluster page links:**
- Back to the pillar page (contextual link in the introduction or conclusion)
- To 2-3 adjacent cluster pages (by proximity in intent: informational links to related informational, comparative links to adjacent comparisons)

Document the link map as a directed graph in the Clay table:
- Add a `links_to` column with comma-separated slugs of pages each subtopic should link to
- Add a `links_from` column tracking inbound internal links

### 6. Define the pillar page structure

The pillar page is the hub. It must:
- Target the broad head term (e.g., "content marketing strategy")
- Be 3,000-5,000 words covering the topic comprehensively
- Include a section for each cluster subtopic with a summary paragraph and link to the full cluster article
- Have a table of contents for navigation
- Include a lead capture CTA (email signup, checklist download, or demo booking)

Draft the pillar page outline: H1, table of contents, section H2s (one per cluster subtopic), CTA placement, FAQ section.

## Output

- A Clay table (or structured JSON/CSV) with:
  - Pillar topic and its target keyword metrics
  - 10-30 cluster subtopics with keyword data, intent type, priority score
  - Internal linking map (who links to whom)
  - Pillar page outline
- Subtopics ranked by priority for production order

## Triggers

- Run once per pillar topic at play start (Smoke level)
- Re-run quarterly to discover new subtopics and re-score priorities
- Triggered by `cluster-gap-analysis` when new opportunities are detected
