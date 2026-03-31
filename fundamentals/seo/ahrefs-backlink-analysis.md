---
name: ahrefs-backlink-analysis
description: Pull backlink profiles, new/lost backlinks, and referring domain data via the Ahrefs Site Explorer API
tool: Ahrefs
product: Ahrefs
difficulty: Config
---

# Ahrefs Backlink Analysis API

Retrieve backlink data for any domain or URL: referring domains, new and lost backlinks, anchor text distribution, and domain rating history. Essential for tracking guest post backlink acquisition, monitoring competitor link-building, and measuring the SEO impact of earned placements.

## Authentication

```
Authorization: Bearer {AHREFS_API_TOKEN}
```

Requires Ahrefs Standard ($199/mo) or higher for full backlink data access.

## Core Operations

### Get backlink profile summary

```
GET https://api.ahrefs.com/v3/site-explorer/overview
Authorization: Bearer {token}

Query params:
  target=example.com
  mode=domain   # or "exact" for specific URL, "prefix" for URL prefix
  select=domain_rating,backlinks,referring_domains,organic_traffic,organic_keywords
```

Response fields: `domain_rating` (0-100), `backlinks` (total count), `referring_domains` (unique linking domains), `organic_traffic`, `organic_keywords`.

### Get all backlinks to a target

```
GET https://api.ahrefs.com/v3/site-explorer/all-backlinks
Authorization: Bearer {token}

Query params:
  target=example.com/blog/guest-post-article
  mode=exact
  select=url_from,domain_rating_source,anchor,first_seen,last_seen,http_code,is_dofollow
  where=is_dofollow=true
  order_by=domain_rating_source:desc
  limit=500
  offset=0
```

Use `mode=exact` to check backlinks to a specific guest post URL you placed. Use `mode=domain` to see all backlinks across your domain.

### Get new backlinks (recently acquired)

```
GET https://api.ahrefs.com/v3/site-explorer/new-backlinks
Authorization: Bearer {token}

Query params:
  target=example.com
  mode=domain
  date_from=2026-03-01
  date_to=2026-03-30
  select=url_from,url_to,domain_rating_source,anchor,first_seen,is_dofollow
  order_by=first_seen:desc
  limit=200
```

Run this weekly to detect when guest post backlinks go live. Match `url_from` against your media target list to attribute backlinks to specific pitches.

### Get lost backlinks

```
GET https://api.ahrefs.com/v3/site-explorer/lost-backlinks
Authorization: Bearer {token}

Query params:
  target=example.com
  mode=domain
  date_from=2026-03-01
  date_to=2026-03-30
  select=url_from,url_to,domain_rating_source,anchor,last_seen,reason
  limit=200
```

`reason` field values: `broken` (page removed), `noindex`, `redirect`, `link_removed`. Monitor lost backlinks from guest posts to detect when editors remove your links.

### Get referring domains

```
GET https://api.ahrefs.com/v3/site-explorer/referring-domains
Authorization: Bearer {token}

Query params:
  target=example.com
  mode=domain
  select=domain,domain_rating,backlinks,first_seen,last_seen
  order_by=domain_rating:desc
  limit=500
```

Use to track unique referring domains from guest posting. Each new referring domain from a DA 30+ site is a meaningful SEO signal.

### Get competitor backlink sources

```
GET https://api.ahrefs.com/v3/site-explorer/all-backlinks
Authorization: Bearer {token}

Query params:
  target=competitor.com
  mode=domain
  select=url_from,domain_rating_source,anchor,url_to,is_dofollow
  where=domain_rating_source>=30
  order_by=domain_rating_source:desc
  limit=500
```

Find where competitors have guest posts published. Extract `url_from` domains as high-probability targets for your own guest posting pitches.

## Rate Limits

- 60 requests per minute across all endpoints
- Monthly unit allowances vary by plan
- Backlink endpoints cost 2-5 units per request depending on result size

## Error Handling

- `401 Unauthorized`: Invalid or expired API token.
- `429 Too Many Requests`: Rate limit exceeded. Implement exponential backoff starting at 60 seconds.
- `402 Payment Required`: Monthly unit quota exhausted.
- `400 Bad Request`: Verify target URL encoding and mode parameter value.

## Pricing

Included in Ahrefs subscription. Backlink data requires Standard ($199/mo) or higher.
- Standard: $199/mo (150,000 API units)
- Advanced: $399/mo (500,000 API units)
- Pricing page: https://ahrefs.com/pricing

## Alternatives

- **SEMrush Backlink Analytics API** ($249.95/mo+): Similar backlink data, different unit model
- **Moz Link Explorer API** ($99/mo+): Domain Authority, backlink data, spam score
- **Majestic API** ($49.99/mo+): Trust Flow, Citation Flow, backlink history
- **DataForSEO Backlinks API** ($0.002/request): Pay-per-use backlink data
- **Ubersuggest API** ($29/mo+): Basic backlink data, budget option
