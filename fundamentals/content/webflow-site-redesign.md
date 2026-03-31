---
name: webflow-site-redesign
description: Programmatically update Webflow site pages, styles, and content via the Webflow CMS and Designer API
tool: Webflow
product: Webflow
difficulty: Advanced
---

# Webflow Site Redesign

Update website pages, CMS content, styles, and components programmatically via the Webflow API and CLI. Use this for brand refreshes where you need to update copy, images, and page structure across multiple pages without manual Designer work.

## Authentication

Webflow API v2 uses Bearer tokens:
```
Authorization: Bearer {WEBFLOW_API_TOKEN}
```

Generate tokens at: Webflow Dashboard > Site Settings > Integrations > API Access.

Scopes needed: `sites:read`, `sites:write`, `pages:read`, `pages:write`, `cms:read`, `cms:write`.

## List Sites and Pages

```
GET https://api.webflow.com/v2/sites
```

```
GET https://api.webflow.com/v2/sites/{site_id}/pages
```

Returns page IDs, slugs, titles, and metadata.

## Update Page Content (Static Pages)

```
PATCH https://api.webflow.com/v2/pages/{page_id}

{
  "title": "New Page Title",
  "seo": {
    "title": "New SEO Title | Brand Name",
    "description": "Updated meta description reflecting new brand positioning."
  },
  "openGraph": {
    "title": "New OG Title",
    "description": "Updated OG description",
    "titleCopied": false,
    "descriptionCopied": false
  }
}
```

Note: The API can update page metadata but not visual layout. For layout changes, use the Webflow Designer CLI or manual updates.

## Update CMS Items (Blog, Case Studies, etc.)

### List collections
```
GET https://api.webflow.com/v2/sites/{site_id}/collections
```

### List items in a collection
```
GET https://api.webflow.com/v2/collections/{collection_id}/items
```

### Update a CMS item
```
PATCH https://api.webflow.com/v2/collections/{collection_id}/items/{item_id}

{
  "fieldData": {
    "name": "Updated Title",
    "slug": "updated-slug",
    "hero-headline": "New brand-aligned headline",
    "hero-subheadline": "Updated subheadline with new value proposition",
    "cta-text": "Get Started Free",
    "cta-url": "/signup?utm_source=website&utm_medium=hero"
  }
}
```

Field names must match your Webflow collection schema exactly. Fetch collection schema first:
```
GET https://api.webflow.com/v2/collections/{collection_id}
```

### Publish changes
```
POST https://api.webflow.com/v2/sites/{site_id}/publish

{
  "publishToWebflowSubdomain": false,
  "customDomains": ["www.yoursite.com"]
}
```

## Bulk Update Workflow

For a brand refresh affecting many pages:

1. Export all CMS items: `GET /collections/{id}/items?limit=100&offset=0`
2. Transform content programmatically (update headlines, CTAs, descriptions to match new brand voice)
3. PATCH each item with updated fieldData
4. Publish the site

Use n8n for the batch workflow:
- HTTP Request node to fetch all items
- Code node to apply brand voice rules (e.g., replace old tagline with new, update CTA copy)
- Loop node to PATCH each item
- Final HTTP Request to publish

## Webflow CLI (for style and layout changes)

```bash
npm install -g @webflow/cli
webflow login
webflow pull --site {site_id}  # Download site as local files
# Edit CSS variables, component markup
webflow push --site {site_id}  # Push changes
```

For CSS variable updates (brand colors, fonts):
```css
:root {
  --brand-primary: #F06543;
  --brand-secondary: #2A9E96;
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

## Alternative: Framer

Framer uses a different API. For Framer sites, update content via:
- Framer CMS API: `POST https://api.framer.com/v1/sites/{site_id}/cms/items`
- Similar structure: list collections, update items, publish

## Alternative: Next.js / Static Sites

For headless/static sites, the "redesign" happens in the codebase:
1. Update brand tokens (colors, fonts, spacing) in CSS/Tailwind config
2. Update copy in content files or CMS (Contentful, Sanity, etc.)
3. Deploy via CI/CD

## Error Handling

- `404 Page Not Found`: Invalid page_id. Re-fetch page list.
- `422 Validation Error`: Field name mismatch or invalid field value. Check collection schema.
- `429 Rate Limit`: Webflow allows 60 requests/minute on paid plans. Add 1-second delays between batch updates.
- `409 Conflict`: Concurrent edit detected. Retry after 2 seconds.
