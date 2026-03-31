---
name: structured-data-validation
description: Validate and test Schema.org structured data (JSON-LD) for rich result eligibility
tool: Google
product: Rich Results Test
difficulty: Config
---

# Structured Data Validation

Programmatically validate Schema.org JSON-LD markup on any URL. Check whether pages are eligible for rich results (FAQ snippets, HowTo cards, Product ratings, Breadcrumbs, etc.) and fix validation errors.

## Authentication

The Rich Results Test requires a Google Cloud API key with the "Search Console API" enabled (same key used for GSC).

## Core Operations

### Test a URL for rich results eligibility

```
POST https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run
Content-Type: application/json

{
  "url": "https://example.com/solutions/crm-for-startups"
}
```

Note: For structured data specifically, use the Rich Results API (currently accessible via the Search Console API umbrella):

```
POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
Authorization: Bearer {access_token}

{
  "inspectionUrl": "https://example.com/solutions/crm-for-startups",
  "siteUrl": "https://example.com/"
}
```

The `richResultsResult` field in the response contains detected structured data types and their validation status.

### Validate JSON-LD markup directly (without deploying)

Use the Schema.org Validator API or validate locally:

```bash
# Install schema-dts for TypeScript validation
npm install schema-dts

# Or use the structured-data-testing-tool CLI
npx structured-data-testing-tool --url "https://example.com/solutions/crm-for-startups"
```

CLI output shows each detected schema type, whether it passes validation, and any missing required properties.

### Generate JSON-LD for common page types

#### SoftwareApplication (for SaaS product pages)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Product Name",
  "description": "One-sentence product description",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "description": "Free tier available"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "127"
  }
}
```

#### FAQPage (for comparison/alternative pages)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the best CRM for startups?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The best CRM for startups depends on..."
      }
    }
  ]
}
```

#### BreadcrumbList (for site navigation)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/"},
    {"@type": "ListItem", "position": 2, "name": "Solutions", "item": "https://example.com/solutions/"},
    {"@type": "ListItem", "position": 3, "name": "CRM for Startups"}
  ]
}
```

#### Article (for blog posts)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {"@type": "Person", "name": "Author Name"},
  "datePublished": "2026-03-30",
  "dateModified": "2026-03-30",
  "publisher": {
    "@type": "Organization",
    "name": "Company Name",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  }
}
```

### Inject JSON-LD into pages

Add the JSON-LD script tag to the `<head>` of each page:

```html
<script type="application/ld+json">
{ ... your JSON-LD here ... }
</script>
```

For Next.js / React apps, render dynamically:

```jsx
<Head>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
  />
</Head>
```

For Webflow, inject via custom code in page settings or site-wide head code.

## Rate Limits

- URL Inspection API: 600 inspections per day per property, 2,000 per day per project
- `structured-data-testing-tool` CLI: No rate limits (runs locally)

## Error Handling

- Missing required fields: Schema.org types have required and recommended properties. Check https://schema.org/{Type} for the full spec.
- Invalid nesting: JSON-LD must be valid JSON. Use `JSON.parse()` to validate before deploying.
- Wrong schema type: Google only supports specific types for rich results. Check https://developers.google.com/search/docs/appearance/structured-data/search-gallery

## Pricing

Free. Both the Rich Results Test and Schema.org validation are free.
Reference: https://developers.google.com/search/docs/appearance/structured-data

## Alternatives

- **Schema.org Validator** (free): https://validator.schema.org/
- **Merkle Schema Markup Generator** (free): GUI for generating JSON-LD — https://technicalseo.com/tools/schema-markup-generator/
- **Yoast SEO** (WordPress, free/$99/yr): Automatically generates structured data for WordPress sites
- **RankMath** (WordPress, free/$59/yr): Similar to Yoast with broader schema support
- **Schema App** ($30/mo+): Enterprise structured data management — https://www.schemaapp.com/
