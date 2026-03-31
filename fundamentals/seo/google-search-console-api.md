---
name: google-search-console-api
description: Query Google Search Console API for indexation status, search queries, CTR, and position data
tool: Google Search Console
difficulty: Setup
---

# Google Search Console API

Query GSC for organic search performance data: which pages are indexed, what queries drive clicks, average position, and click-through rate. This is the foundation for all SEO measurement.

## Authentication

GSC uses OAuth 2.0 via Google Cloud. Set up once:

1. Create a Google Cloud project at `https://console.cloud.google.com/`
2. Enable the Search Console API: `https://console.cloud.google.com/apis/library/searchconsole.googleapis.com`
3. Create OAuth 2.0 credentials (type: Desktop app or Service Account)
4. For service accounts, share GSC property access with the service account email
5. Store credentials as `GOOGLE_APPLICATION_CREDENTIALS` env var pointing to the JSON key file

## Core Operations

### Query search analytics (rankings, CTR, clicks)

```
POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "startDate": "2026-01-01",
  "endDate": "2026-03-30",
  "dimensions": ["query", "page"],
  "rowLimit": 25000,
  "dataState": "final",
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "page",
      "operator": "contains",
      "expression": "/solutions/"
    }]
  }]
}
```

Response fields per row: `clicks`, `impressions`, `ctr`, `position`, `keys` (array matching dimensions).

### Check indexation status

```
POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "inspectionUrl": "https://example.com/solutions/crm-for-startups",
  "siteUrl": "https://example.com/"
}
```

Response includes `inspectionResult.indexStatusResult.coverageState` — values: `SUBMITTED_AND_INDEXED`, `CRAWLED_NOT_INDEXED`, `DISCOVERED_NOT_INDEXED`, `URL_IS_UNKNOWN`.

### Submit URL for indexing

```
POST https://indexing.googleapis.com/v3/urlNotifications:publish
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://example.com/solutions/crm-for-startups",
  "type": "URL_UPDATED"
}
```

Note: The Indexing API is officially for job posting and livestream structured data, but works for requesting crawls. For bulk submissions, use sitemaps instead.

### List sitemaps

```
GET https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps
Authorization: Bearer {access_token}
```

### Submit a sitemap

```
PUT https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
Authorization: Bearer {access_token}
```

Where `feedpath` is the full URL of the sitemap (e.g., `https://example.com/sitemap.xml`).

## Rate Limits

- Search Analytics: 1,200 queries per minute per project
- URL Inspection: 600 inspections per day per property, 2,000 per day per project
- Indexing API: 200 publish requests per day

## Error Handling

- `403 Forbidden`: Service account lacks access to the GSC property. Add it as a user in GSC settings.
- `429 Too Many Requests`: Rate limit hit. Implement exponential backoff starting at 1 second.
- `400 Bad Request`: Check date format (YYYY-MM-DD) and that siteUrl matches the property exactly (including protocol).

## Pricing

Free. No usage charges. Subject to rate limits above.
