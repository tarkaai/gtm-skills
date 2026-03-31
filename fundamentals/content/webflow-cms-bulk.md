---
name: webflow-cms-bulk
description: Create and update Webflow CMS items in bulk via API for programmatic page generation
tool: Webflow
product: Webflow
difficulty: Advanced
---

# Webflow CMS Bulk Operations

Create hundreds or thousands of CMS items programmatically via the Webflow API. This is the execution layer for programmatic SEO — taking a keyword matrix and turning it into live pages.

## Authentication

```
Authorization: Bearer {WEBFLOW_API_TOKEN}
```

Generate a site-level API token in Webflow: Site Settings > Integrations > API Access. Token needs CMS read/write permissions.

## Core Operations

### Create a CMS item

```
POST https://api.webflow.com/v2/collections/{collection_id}/items
Authorization: Bearer {token}
Content-Type: application/json

{
  "isArchived": false,
  "isDraft": false,
  "fieldData": {
    "name": "Best CRM for Startups",
    "slug": "best-crm-for-startups",
    "meta-title": "Best CRM for Startups in 2026 | Your Brand",
    "meta-description": "Compare the top CRM tools for startups. Find the right fit for your team size, budget, and workflow.",
    "h1-heading": "Best CRM for Startups",
    "body-content": "<p>Detailed, keyword-optimized content...</p>",
    "target-keyword": "best crm for startups",
    "search-volume": 2400,
    "keyword-difficulty": 28,
    "category": "CRM",
    "modifier": "startups",
    "internal-links": "<a href='/solutions/crm-for-agencies'>CRM for Agencies</a>",
    "last-refreshed": "2026-03-30T00:00:00Z"
  }
}
```

### Bulk create via loop

The Webflow API does not have a native bulk create endpoint. Implement a sequential loop with rate limiting:

```javascript
const RATE_LIMIT_MS = 1100; // Webflow allows ~60 req/min

async function bulkCreateItems(collectionId, items, token) {
  const results = [];
  for (const item of items) {
    const res = await fetch(
      `https://api.webflow.com/v2/collections/${collectionId}/items`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fieldData: item, isDraft: false, isArchived: false })
      }
    );
    if (res.status === 429) {
      // Rate limited — wait and retry
      await new Promise(r => setTimeout(r, 5000));
      // Retry the same item
      continue;
    }
    results.push(await res.json());
    await new Promise(r => setTimeout(r, RATE_LIMIT_MS));
  }
  return results;
}
```

### Update an existing CMS item

```
PATCH https://api.webflow.com/v2/collections/{collection_id}/items/{item_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "fieldData": {
    "body-content": "<p>Updated content...</p>",
    "last-refreshed": "2026-03-30T00:00:00Z"
  }
}
```

### Publish the site after changes

CMS changes are not live until the site is published:

```
POST https://api.webflow.com/v2/sites/{site_id}/publish
Authorization: Bearer {token}
Content-Type: application/json

{
  "publishToWebflowSubdomain": false,
  "customDomains": ["your-domain.com"]
}
```

### List all items in a collection

```
GET https://api.webflow.com/v2/collections/{collection_id}/items?limit=100&offset=0
Authorization: Bearer {token}
```

Paginate with `offset` to retrieve all items.

## CMS Collection Setup for Programmatic SEO

Before bulk creating items, configure the collection with these fields:

| Field | Type | Purpose |
|-------|------|---------|
| name | PlainText | Page title (required by Webflow) |
| slug | PlainText | URL slug (auto-generated if omitted) |
| meta-title | PlainText | SEO title tag |
| meta-description | PlainText | Meta description |
| h1-heading | PlainText | Primary H1 heading |
| body-content | RichText | Main page content |
| target-keyword | PlainText | Primary keyword target |
| search-volume | Number | Monthly search volume |
| keyword-difficulty | Number | Ahrefs KD score |
| category | Option | Grouping category |
| modifier | PlainText | The variable element (e.g., "startups", "agencies") |
| internal-links | RichText | Cross-links to related pages |
| last-refreshed | DateTime | When content was last updated |
| cta-text | PlainText | Custom CTA per page |

## Rate Limits

- 60 requests per minute per site
- 429 responses include `Retry-After` header
- Plan limits: CMS plan = 2,000 items; Business plan = 10,000-20,000 items

## Error Handling

- `401 Unauthorized`: Invalid or expired API token. Regenerate in Webflow settings.
- `404 Not Found`: Collection ID or item ID does not exist. List collections first: `GET /v2/sites/{site_id}/collections`.
- `409 Conflict`: Duplicate slug. Append a suffix or check if item already exists.
- `429 Too Many Requests`: Rate limited. Wait for `Retry-After` seconds.
- `400 Validation Error`: Required field missing or field type mismatch. Check field names match collection schema exactly.

## Pricing

- CMS plan: $23/mo (2,000 CMS items, API access included)
- Business plan: $39/mo (10,000+ CMS items, higher bandwidth)
- Enterprise: Custom pricing (unlimited CMS items)
- Pricing page: https://webflow.com/pricing

## Alternatives

If not using Webflow:
- **Sanity.io** ($0-99/mo): Headless CMS with generous API limits, GROQ query language
- **Contentful** ($0-489/mo): Headless CMS with Content Management API for bulk operations
- **Strapi** (free, self-hosted): Open-source headless CMS with REST/GraphQL API
- **WordPress REST API** (free with hosting): `/wp-json/wp/v2/posts` for bulk page creation
- **Ghost Content API** (free with hosting): `/ghost/api/admin/posts/` for bulk publishing
