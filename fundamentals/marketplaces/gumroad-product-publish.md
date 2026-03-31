---
name: gumroad-product-publish
description: Publish a digital product (template, tool, resource) to Gumroad with optimized listing and tracking
tool: Gumroad
product: Gumroad
difficulty: Setup
---

# Gumroad Product Publish

Publish a digital product (template file, tool, resource pack) to Gumroad for distribution. Gumroad handles hosting, payment, and delivery. This fundamental covers the API-based and dashboard-based approaches.

## Prerequisites

- Gumroad account (https://gumroad.com)
- Digital file to distribute (PDF, ZIP, Notion export, Figma file, Airtable share link, etc.)
- Product description and cover image prepared

## Instructions

### 1. Create the product via API

**Endpoint:** `POST https://api.gumroad.com/v2/products`

**Headers:**
```
Authorization: Bearer {GUMROAD_ACCESS_TOKEN}
Content-Type: multipart/form-data
```

**Required parameters:**
```json
{
  "name": "Startup OKR Tracker for Notion",
  "price": 0,
  "description": "Track quarterly OKRs across your startup with automated progress rollups. Includes pre-built views for leadership, team leads, and individual contributors.\n\nGet the full platform: {your-url}?utm_source=gumroad&utm_medium=marketplace&utm_campaign=template-{slug}",
  "preview_url": "https://your-domain.com/template-preview?utm_source=gumroad",
  "url_name": "{template-slug}",
  "tags": ["notion-template", "okr", "startup", "project-management"]
}
```

**File upload:** Attach the template file as `file` in the multipart form data.

**Response (201 Created):**
```json
{
  "success": true,
  "product": {
    "id": "abc123",
    "name": "Startup OKR Tracker for Notion",
    "short_url": "https://gumroad.com/l/abc123",
    "published": false
  }
}
```

### 2. Set the product as free (pay-what-you-want)

For lead-magnet use, set price to $0 with "pay what you want" enabled:

```
PUT https://api.gumroad.com/v2/products/{product_id}
{
  "price": 0,
  "suggest_price": 0,
  "customizable_price": true
}
```

This allows $0 downloads while letting generous users pay more.

### 3. Configure the custom fields for lead capture

Add a required email field (Gumroad collects email by default) and an optional company name field:

```
PUT https://api.gumroad.com/v2/products/{product_id}
{
  "custom_fields": ["Company name (optional)"]
}
```

Every download captures the buyer's email address automatically.

### 4. Upload cover image and preview

**Cover image:** 600x400px minimum. Show the template in use with sample data.

```
PUT https://api.gumroad.com/v2/products/{product_id}
Content-Type: multipart/form-data

thumbnail: [image file]
```

### 5. Publish the product

```
PUT https://api.gumroad.com/v2/products/{product_id}
{
  "published": true
}
```

### 6. Enable Gumroad Discover

To list on Gumroad's built-in marketplace (Discover):

Via dashboard: Product Settings > Discover > Enable. Note: Discover takes a 30% fee on sales made through Discover (vs 10% for direct sales). For free products, this is irrelevant.

### 7. Retrieve download/sales data

**Get product stats:**
```
GET https://api.gumroad.com/v2/products/{product_id}
```

**Get sales (downloads):**
```
GET https://api.gumroad.com/v2/sales?product_id={product_id}&after=2026-03-01&before=2026-03-31
```

Response includes buyer email, timestamp, and custom field values.

### 8. Set up webhook for real-time download notifications

**Endpoint:** `POST https://api.gumroad.com/v2/resource_subscriptions`

```json
{
  "resource_name": "sale",
  "post_url": "https://your-n8n-instance.com/webhook/gumroad-download"
}
```

Gumroad POSTs to your webhook URL on every download with: email, product name, timestamp, custom fields, IP country.

## Error Handling

- **401 Unauthorized:** Regenerate your access token at https://app.gumroad.com/settings/advanced
- **422 Unprocessable:** Check required fields. `name` and file are required for creation.
- **File too large:** Gumroad supports files up to 16GB. If larger, host externally and provide a download link.
- **Product not appearing on Discover:** Ensure Discover is enabled and product has a description, cover image, and at least one tag. New products may take 24-48 hours to appear.

## Pricing

- Gumroad account: Free (no monthly fee)
- Direct sales: 10% + $0.50 per transaction
- Discover marketplace sales: 30% fee
- Free product downloads: No fees charged
- Payouts: Direct deposit (free), PayPal (2%), instant (3%)
