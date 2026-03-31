---
name: ahrefs-content-explorer
description: Search for blogs accepting guest posts and analyze content opportunities via the Ahrefs Content Explorer API
tool: Ahrefs
product: Ahrefs
difficulty: Config
---

# Ahrefs Content Explorer API

Search billions of indexed pages to find blogs that accept guest posts, analyze top-performing content in your niche, and identify content placement opportunities. Content Explorer combines web search with Ahrefs SEO metrics, making it the primary discovery engine for guest posting at scale.

## Authentication

```
Authorization: Bearer {AHREFS_API_TOKEN}
```

Requires Ahrefs Standard ($199/mo) or higher.

## Core Operations

### Search for blogs accepting guest posts

```
GET https://api.ahrefs.com/v3/content-explorer/search
Authorization: Bearer {token}

Query params:
  query="write for us" AND "{your_niche_keyword}"
  select=url,title,domain_rating,organic_traffic,referring_domains,word_count,published_date
  where=domain_rating>=30 AND organic_traffic>=500
  order_by=domain_rating:desc
  limit=200
```

Vary the query to cover all guest post signals:
- `"write for us" AND "saas"` — explicit guest post pages
- `"guest post" AND "marketing automation"` — sites mentioning guest posts
- `"contribute" AND "submit article" AND "B2B"` — contribution guidelines pages
- `"guest author" AND "{topic}"` — sites that have published guest authors before
- `intitle:"guest post by" AND "{niche}"` — live guest posts on target sites

### Analyze a specific blog's content profile

```
GET https://api.ahrefs.com/v3/content-explorer/search
Authorization: Bearer {token}

Query params:
  query=site:targetblog.com
  select=url,title,organic_traffic,referring_domains,word_count,published_date,author
  order_by=organic_traffic:desc
  limit=100
```

Use this to understand what content performs best on a target blog before pitching. Identify: popular topics, average word count, publishing frequency, and whether they have guest authors (check the `author` field for non-staff names).

### Find competitor guest posts

```
GET https://api.ahrefs.com/v3/content-explorer/search
Authorization: Bearer {token}

Query params:
  query="competitor_founder_name" OR "competitor_company" -site:competitor.com
  select=url,title,domain_rating,organic_traffic,published_date,author
  where=domain_rating>=20
  order_by=domain_rating:desc
  limit=200
```

Finds articles by or mentioning competitors on third-party sites. These sites are high-probability guest post targets because they already publish content in your space.

### Discover high-traffic content gaps

```
GET https://api.ahrefs.com/v3/content-explorer/search
Authorization: Bearer {token}

Query params:
  query="{your_topic}" -site:yourdomain.com
  select=url,title,organic_traffic,referring_domains,word_count
  where=organic_traffic>=1000
  order_by=organic_traffic:desc
  limit=100
```

Identify high-traffic articles about your topic on other sites. These topics are proven to drive traffic, making them strong pitch angles for guest posts on the same or similar blogs.

### Get content metrics in bulk

```
POST https://api.ahrefs.com/v3/content-explorer/details
Authorization: Bearer {token}
Content-Type: application/json

{
  "urls": [
    "https://blog1.com/guest-post-guidelines",
    "https://blog2.com/write-for-us",
    "https://blog3.com/contribute"
  ],
  "select": ["url", "domain_rating", "organic_traffic", "referring_domains"]
}
```

Batch-check metrics for a list of candidate blogs. Use to score and tier your target blog list.

## Rate Limits

- 60 requests per minute
- Content Explorer queries cost 2-5 API units per request
- Subject to monthly unit allocation

## Error Handling

- `401 Unauthorized`: Invalid API token.
- `429 Too Many Requests`: Rate limited. Back off 60 seconds.
- `400 Bad Request`: Check query syntax. Boolean operators (AND, OR, NOT) must be uppercase. Use quotes around exact phrases.
- `402 Payment Required`: Unit quota exhausted.

## Pricing

Included in Ahrefs subscription. Content Explorer requires Standard ($199/mo) or higher.
- Pricing page: https://ahrefs.com/pricing

## Alternatives

- **SEMrush Content Marketing API** ($249.95/mo+): Topic research and content audit capabilities
- **BuzzSumo API** ($199/mo+): Content discovery by engagement metrics (shares, links)
- **SparkToro** ($50/mo+): Audience research to find where your ICP reads and engages
- **DataForSEO Content Analysis API** ($0.002/request): Pay-per-use content metrics
- **SimilarWeb API** (custom pricing): Traffic data for any domain, useful for scoring blog targets
