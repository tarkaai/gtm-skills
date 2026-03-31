---
name: ahrefs-keyword-research
description: Discover long-tail keywords with search volume, difficulty, and SERP data via the Ahrefs API
tool: Ahrefs
product: Ahrefs
difficulty: Config
---

# Ahrefs Keyword Research API

Use the Ahrefs API to discover long-tail keywords for programmatic SEO. Find keywords your ICP searches, assess difficulty, and identify patterns for template-based page generation.

## Authentication

All Ahrefs API requests require an API token passed as a query parameter or header:

```
Authorization: Bearer {AHREFS_API_TOKEN}
```

API tokens are available on Lite ($99/mo, 10K units), Standard ($199/mo, 150K units), Advanced ($399/mo, 500K units), or Enterprise ($999/mo, 2M units) plans.

## Core Operations

### Keywords Explorer — Get keyword ideas from seed terms

```
GET https://api.ahrefs.com/v3/keywords-explorer/google/keyword-ideas
Authorization: Bearer {token}
Content-Type: application/json

Query params:
  select=keyword,volume,keyword_difficulty,cpc,global_volume,traffic_potential
  where=volume>50 AND keyword_difficulty<40
  keywords=crm+for+startups,sales+automation+tool,cold+email+software
  country=us
  limit=1000
  offset=0
  order_by=volume:desc
```

Response fields: `keyword`, `volume` (monthly searches), `keyword_difficulty` (0-100), `cpc` (cost per click in USD), `global_volume`, `traffic_potential` (estimated clicks if you rank #1).

### Get SERP overview for a keyword

```
GET https://api.ahrefs.com/v3/keywords-explorer/google/serp-overview
Authorization: Bearer {token}

Query params:
  keyword=crm+for+startups
  country=us
  select=position,title,url,domain_rating,backlinks,traffic
```

Use this to assess competition: if top 10 results have domain rating >70 and 100+ backlinks, the keyword is too competitive for a new site.

### Get keyword metrics in bulk

```
POST https://api.ahrefs.com/v3/keywords-explorer/google/keywords-metrics
Authorization: Bearer {token}
Content-Type: application/json

{
  "keywords": ["crm for startups", "crm for real estate", "crm for agencies"],
  "country": "us",
  "select": ["keyword", "volume", "keyword_difficulty", "cpc", "traffic_potential"]
}
```

Use this to validate a list of programmatic page targets. Batch up to 500 keywords per request.

### Content Explorer — Find content gaps

```
GET https://api.ahrefs.com/v3/content-explorer/search
Authorization: Bearer {token}

Query params:
  query="best crm for" -site:example.com
  select=url,title,organic_traffic,referring_domains,word_count
  order_by=organic_traffic:desc
  limit=100
```

Finds existing content ranking for your target patterns. Helps identify which variations have proven search demand.

## Rate Limits

- 60 requests per minute across all endpoints
- Monthly unit allowances vary by plan (10K to 2M)
- Each request costs 1-5 units depending on endpoint and rows returned

## Error Handling

- `401 Unauthorized`: Invalid or expired API token.
- `429 Too Many Requests`: Rate limit exceeded. Wait 60 seconds.
- `402 Payment Required`: Monthly unit quota exhausted. Upgrade plan or wait for next billing cycle.
- `400 Bad Request`: Check parameter formatting. Keywords must be URL-encoded.

## Pricing

- Lite: $99/mo (10,000 API units)
- Standard: $199/mo (150,000 API units)
- Advanced: $399/mo (500,000 API units)
- Enterprise: $999/mo (2,000,000 API units)
- Pricing page: https://ahrefs.com/api/pricing

## Alternatives

If Ahrefs is not available, these tools provide similar keyword research APIs:
- **SEMrush API** ($129.95/mo+): `api.semrush.com` — similar keyword data, different unit model
- **Moz API** ($99/mo+): `api.moz.com` — keyword difficulty and SERP data
- **Serpstat API** ($69/mo+): keyword research and rank tracking
- **Keywords Everywhere API** ($1/1000 credits): lightweight keyword metrics
- **DataForSEO** ($0.002/request): pay-per-use keyword and SERP data
