---
name: cluster-gap-analysis
description: Identify missing subtopics, weak internal links, and ranking gaps within an existing content cluster
category: SEO
tools:
  - Google Search Console
  - Ahrefs
  - PostHog
  - n8n
fundamentals:
  - google-search-console-api
  - ahrefs-keyword-research
  - ahrefs-rank-tracking
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
---

# Cluster Gap Analysis

This drill audits an existing content cluster to find gaps: subtopics you should cover but have not, internal links that are missing or broken, cluster articles that underperform, and new keyword opportunities that emerged since the cluster was built. It feeds back into `topic-cluster-mapping` and `cluster-content-production` for expansion.

## Input

- Published content cluster: pillar page URL + all cluster article URLs
- Original cluster map from `topic-cluster-mapping` (with target keywords per article)
- GSC access and Ahrefs access for the domain
- PostHog tracking active on all cluster pages

## Steps

### 1. Audit keyword coverage

Use `ahrefs-keyword-research` to pull the current keyword universe for your pillar topic:

```
GET /v3/keywords-explorer/google/keyword-ideas
keywords={pillar_keyword}
where=volume>30
limit=1000
```

Compare every returned keyword against your existing cluster map. Classify each keyword as:

- **Covered**: an existing cluster article targets this keyword or a close variant
- **Gap**: no existing article targets this keyword, and it has volume >= 50 and KD <= 50
- **Emerging**: keyword appeared in Ahrefs suggestions that was not present in the previous quarter's pull

Store gaps and emerging keywords in the cluster map with `status: "gap"`.

### 2. Analyze ranking performance per cluster article

Use `google-search-console-api` to pull 30-day search analytics for each cluster article URL:

```
POST /searchAnalytics/query
{
  "startDate": "{30_days_ago}",
  "endDate": "{today}",
  "dimensions": ["page", "query"],
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "page",
      "operator": "contains",
      "expression": "/blog/{pillar_slug}"
    }]
  }]
}
```

For each article, compute:
- **Primary keyword position**: where does it rank for its target keyword?
- **Impression share**: impressions for the target keyword vs total impressions for that keyword (GSC does not give competitor data, use Ahrefs SERP overview to estimate)
- **Click-through rate**: clicks / impressions for the target keyword
- **Keyword cannibalization**: are multiple cluster articles ranking for the same query? If so, the one with lower CTR is cannibalizing.

Categorize each article:
- **Strong** (position 1-5, CTR > 3%): leave alone
- **Close** (position 6-20, CTR > 1%): optimize meta title/description for CTR, add more depth
- **Weak** (position 21-50): needs content refresh or internal linking boost
- **Missing** (not indexed or position > 50): investigate indexation, content quality, or thin content

### 3. Audit internal linking completeness

For each cluster article, verify:

1. It links back to the pillar page (check the article HTML for a link to the pillar URL)
2. The pillar page links to it (check the pillar HTML for a link to this article URL)
3. It links to 2-3 adjacent cluster articles as defined in the cluster map
4. No internal links are broken (404s)

Score internal linking completeness per article: `(actual_links / required_links) * 100`. Flag any article below 80%.

Use `ahrefs-rank-tracking` site explorer to check internal link counts:

```
GET /v3/site-explorer/internal-backlinks
target={article_url}
```

### 4. Identify content freshness issues

For each cluster article, check:

- `last_modified` date: if older than 6 months, flag for refresh
- Referenced statistics or data: if they cite year-specific data (e.g., "2025 survey"), flag as outdated
- Referenced tools or products: if any mentioned tool has been discontinued or significantly changed, flag

### 5. Compute cluster health score

Aggregate article-level metrics into a cluster health score:

```
cluster_health = (
  (articles_indexed / total_articles) * 25 +
  (articles_position_1_to_10 / total_articles) * 25 +
  (avg_internal_link_completeness) * 25 +
  (articles_fresh / total_articles) * 25
)
```

Grades:
- 80-100: healthy cluster, focus on expansion
- 60-79: maintenance needed, fix gaps before expanding
- Below 60: cluster needs significant repair before adding new content

### 6. Generate recommendations

Based on the analysis, produce a prioritized action list:

1. **New articles to write** (from gap analysis in Step 1): ranked by priority score
2. **Articles to refresh** (from Steps 2 and 4): with specific diagnosis
3. **Internal links to add** (from Step 3): specific page pairs and anchor text
4. **Cannibalization to resolve** (from Step 2): merge or differentiate affected articles
5. **Pillar page updates** (from Step 1): new sections to add for newly discovered subtopics

### 7. Automate as a recurring workflow (Scalable+ levels)

Using `n8n-workflow-basics` and `n8n-scheduling`, create a monthly n8n workflow:

1. Pull GSC and Ahrefs data for all cluster URLs
2. Run Steps 1-5 programmatically
3. Generate the recommendations list
4. Post the cluster health report to Slack
5. Create tasks in the content queue for recommended actions

## Output

- Cluster health score (0-100)
- List of keyword gaps (new subtopics to write)
- List of articles needing refresh (with diagnosis)
- List of missing internal links (with suggested anchor text)
- Cannibalization report (if applicable)
- Prioritized action list

## Triggers

- Monthly: automated gap analysis via n8n (Scalable+ levels)
- On-demand: after a Google algorithm update or significant ranking shifts
- Quarterly: full re-mapping triggered, feeding back to `topic-cluster-mapping`
