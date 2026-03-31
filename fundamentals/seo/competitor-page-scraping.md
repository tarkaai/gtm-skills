---
name: competitor-page-scraping
description: Scrape competitor product pages, pricing pages, and feature lists to extract structured competitive data
tool: Firecrawl
difficulty: Config
---

# Competitor Page Scraping

Scrape competitor websites to extract structured competitive intelligence: features, pricing, positioning, and product capabilities. This data feeds comparison page content and automated competitive updates.

## Authentication

Firecrawl requires an API key passed as a Bearer token:

```
Authorization: Bearer {FIRECRAWL_API_KEY}
```

API keys are available on Free (500 credits/mo), Hobby ($19/mo, 3K credits), Standard ($99/mo, 50K credits), and Scale ($399/mo, 500K credits) plans.

## Core Operations

### Scrape a single competitor page

```
POST https://api.firecrawl.dev/v1/scrape
Authorization: Bearer {FIRECRAWL_API_KEY}
Content-Type: application/json

{
  "url": "https://competitor.com/pricing",
  "formats": ["markdown", "extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "product_name": {"type": "string"},
        "plans": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "price_monthly": {"type": "string"},
              "price_annual": {"type": "string"},
              "features": {"type": "array", "items": {"type": "string"}}
            }
          }
        },
        "positioning_statement": {"type": "string"},
        "target_audience": {"type": "string"}
      }
    }
  }
}
```

### Crawl a competitor's product/features section

```
POST https://api.firecrawl.dev/v1/crawl
Authorization: Bearer {FIRECRAWL_API_KEY}
Content-Type: application/json

{
  "url": "https://competitor.com/features",
  "limit": 20,
  "includePaths": ["/features/*", "/product/*", "/solutions/*"],
  "excludePaths": ["/blog/*", "/docs/*"],
  "formats": ["markdown", "extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "page_title": {"type": "string"},
        "feature_name": {"type": "string"},
        "feature_description": {"type": "string"},
        "use_cases": {"type": "array", "items": {"type": "string"}},
        "integrations_mentioned": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

Check crawl status:
```
GET https://api.firecrawl.dev/v1/crawl/{crawl_id}
Authorization: Bearer {FIRECRAWL_API_KEY}
```

### Monitor a competitor page for changes

```
POST https://api.firecrawl.dev/v1/scrape
Authorization: Bearer {FIRECRAWL_API_KEY}
Content-Type: application/json

{
  "url": "https://competitor.com/pricing",
  "formats": ["markdown"]
}
```

Store the markdown output with a timestamp. On subsequent scrapes, diff the current markdown against the stored version. If the diff is non-empty, the page changed. Parse the diff to identify what changed (pricing, features, positioning).

## Rate Limits

- Free: 500 credits/month, 10 requests/minute
- Hobby: 3,000 credits/month, 20 requests/minute
- Standard: 50,000 credits/month, 50 requests/minute
- Scale: 500,000 credits/month, 100 requests/minute
- Each scrape costs 1 credit. Each crawl page costs 1 credit.

## Error Handling

- `401 Unauthorized`: Invalid API key.
- `429 Too Many Requests`: Rate limit exceeded. Back off and retry after 60 seconds.
- `402 Payment Required`: Credit quota exhausted.
- `408 Request Timeout`: Page took too long to load. Retry once with `timeout: 60000`.
- `403 Forbidden`: Site blocks scraping. Try adding `headers: {"User-Agent": "Mozilla/5.0"}` or switch to a different competitor data source (G2, Crunchbase).

## Pricing

- Free: $0/mo (500 credits)
- Hobby: $19/mo (3,000 credits)
- Standard: $99/mo (50,000 credits)
- Scale: $399/mo (500,000 credits)
- Pricing page: https://www.firecrawl.dev/pricing

## Alternatives

- **Jina AI Reader** (free for basic use): `r.jina.ai/{url}` — returns markdown of any URL, no API key needed for low volume
- **ScrapingBee** ($49/mo+): Headless browser API with proxy rotation
- **Browserbase** ($49/mo+): Headless browser infrastructure, Playwright-compatible
- **Apify** ($49/mo+): Web scraping platform with pre-built competitor monitoring actors
- **Diffbot** ($299/mo+): Structured data extraction from any web page, automatic schema detection
