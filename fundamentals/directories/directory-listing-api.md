---
name: directory-listing-api
description: Create, update, and manage product listings on software directories via their APIs and vendor portals
tool: G2
product: G2
difficulty: Setup
---

# Directory Listing API

Programmatically create and manage product listings across software review directories and marketplaces. This fundamental covers the API and vendor portal operations for each major directory.

## G2

G2 vendor operations are managed through the G2 Seller Solutions portal and API.

### Claim and create a profile

**Endpoint:** `POST https://seller.g2.com/api/v1/products`

```
Headers:
  Authorization: Bearer {G2_API_TOKEN}
  Content-Type: application/json

Body:
{
  "product": {
    "name": "Your Product Name",
    "website_url": "https://yourproduct.com?utm_source=g2&utm_medium=directory&utm_campaign=listing",
    "description": "Primary description (max 300 chars). Lead with the problem you solve.",
    "detailed_description": "Full product description with keywords buyers search on G2.",
    "category_ids": ["category-id-1", "category-id-2"],
    "media": {
      "logo_url": "https://yourcdn.com/logo.png",
      "screenshots": [
        {"url": "https://yourcdn.com/screenshot1.png", "caption": "Dashboard overview"},
        {"url": "https://yourcdn.com/screenshot2.png", "caption": "Key workflow"}
      ],
      "video_url": "https://youtube.com/watch?v=demo-video-id"
    },
    "pricing": {
      "model": "subscription",
      "starting_price": 49,
      "currency": "USD",
      "billing_period": "monthly",
      "free_trial": true,
      "freemium": false
    }
  }
}
```

**Response:** `201 Created` with product ID and profile URL.

### Update listing content

**Endpoint:** `PATCH https://seller.g2.com/api/v1/products/{product_id}`

Send only the fields being updated. Common updates: description, screenshots, pricing, feature list.

### Retrieve listing analytics

**Endpoint:** `GET https://seller.g2.com/api/v1/products/{product_id}/analytics?period=30d`

Returns: profile views, comparison views, clicks to website, review count, average rating.

## Capterra (Gartner Digital Markets)

Capterra vendor management is through the Gartner Digital Markets vendor portal.

### Claim profile

1. Navigate to `https://www.capterra.com/vendors/signup`
2. Via API (if available through Gartner Digital Markets API):

**Endpoint:** `POST https://api.gartnerdigitalmarkets.com/v1/products`

```
Headers:
  Authorization: Bearer {CAPTERRA_API_TOKEN}
  Content-Type: application/json

Body:
{
  "product_name": "Your Product Name",
  "short_description": "One-line pitch (max 150 chars)",
  "long_description": "Detailed description with category keywords",
  "website_url": "https://yourproduct.com?utm_source=capterra&utm_medium=directory",
  "logo_url": "https://yourcdn.com/logo.png",
  "screenshots": ["url1", "url2", "url3"],
  "pricing_model": "per_user_monthly",
  "starting_price": 49,
  "free_trial": true,
  "deployment": ["cloud", "saas"],
  "categories": ["category-slug-1"]
}
```

### Set up PPC campaigns

**Endpoint:** `POST https://api.gartnerdigitalmarkets.com/v1/campaigns`

```
Body:
{
  "product_id": "{product_id}",
  "budget_monthly": 500,
  "max_cpc": 5.00,
  "target_categories": ["category-slug-1", "category-slug-2"],
  "landing_url": "https://yourproduct.com/capterra-landing?utm_source=capterra&utm_medium=ppc"
}
```

Minimum spend: $500/month. Floor CPC: $2.00.

## Product Hunt

Product Hunt API v2 uses GraphQL.

### Submit a product

**Endpoint:** `POST https://api.producthunt.com/v2/api/graphql`

```
Headers:
  Authorization: Bearer {PH_API_TOKEN}
  Content-Type: application/json

Body:
{
  "query": "mutation { createPost(input: { name: \"Your Product\", tagline: \"Short tagline under 60 chars\", url: \"https://yourproduct.com?ref=producthunt\", description: \"Longer description of what you built and why.\", thumbnailUrl: \"https://yourcdn.com/ph-thumbnail.png\", topics: [\"SaaS\", \"Developer Tools\"] }) { id slug votesCount } }"
}
```

### Query product analytics

```
{
  "query": "{ post(slug: \"your-product-slug\") { id name votesCount commentsCount reviewsCount dailyRank weeklyRank } }"
}
```

## TrustRadius

### Claim profile

**Endpoint:** `POST https://api.trustradius.com/v1/products`

```
Headers:
  Authorization: Bearer {TR_API_TOKEN}

Body:
{
  "name": "Your Product",
  "description": "Product description",
  "website": "https://yourproduct.com?utm_source=trustradius",
  "category": "category-name",
  "pricing": { "starting_at": 49, "model": "subscription" }
}
```

## GetApp (Gartner Digital Markets)

Same API infrastructure as Capterra. Use the Gartner Digital Markets vendor portal to manage listings across both Capterra and GetApp simultaneously.

## SourceForge

### Claim project

**Endpoint:** `PUT https://sourceforge.net/rest/p/{project_slug}`

```
Headers:
  Authorization: Bearer {SF_API_TOKEN}

Body:
{
  "name": "Your Product",
  "short_description": "One-line description",
  "description": "Full description with keywords",
  "external_homepage": "https://yourproduct.com?utm_source=sourceforge"
}
```

## Listing Optimization Checklist

For every directory listing, ensure:

1. **Keywords in title and description** -- use the terms buyers search for in that directory's search
2. **UTM parameters on all links** -- `utm_source={directory}&utm_medium=directory&utm_campaign=listing`
3. **Screenshots** -- minimum 3, showing the core workflow and key differentiators
4. **Video** -- 60-90 second demo video increases engagement significantly
5. **Pricing transparency** -- directories that show pricing get more qualified clicks
6. **Category selection** -- list in the most specific category, not the broadest
7. **Comparison content** -- fill out all feature comparison fields so you appear in comparison pages

## Error Handling

- **401 Unauthorized**: API token expired or revoked. Re-authenticate through the vendor portal.
- **403 Forbidden**: Profile not claimed. Must verify domain ownership first.
- **409 Conflict**: Product already exists. Use `PATCH` to update instead of `POST`.
- **429 Rate Limited**: Most directory APIs allow 60-120 requests/minute. Implement exponential backoff.
- **Pending Review**: New listings and major updates go through editorial review (24-72 hours). Check status via `GET /products/{id}/status`.
