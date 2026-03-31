---
name: marketplace-analytics-scraping
description: Scrape download counts, view stats, and ranking data from template marketplaces using Clay or direct APIs
tool: Clay
difficulty: Config
---

# Marketplace Analytics Scraping

Collect performance data (downloads, views, ratings, rankings) from template and tool marketplaces where your products are listed. Marketplaces vary widely in what analytics they expose -- this fundamental covers API-based extraction where available and Clay-based scraping as fallback.

## Prerequisites

- Active listings on one or more template marketplaces (Notion, Gumroad, Figma, Airtable, Canva, etc.)
- Clay account for scraping marketplaces without APIs
- Listing URLs for each marketplace

## Instructions

### 1. Gumroad -- API-based analytics

Gumroad provides the best API access for download and sales data.

**Get product-level stats:**
```
GET https://api.gumroad.com/v2/products/{product_id}
Authorization: Bearer {GUMROAD_ACCESS_TOKEN}
```

Response includes: `sales_count`, `sales_usd_cents`, `views_count`, `name`, `published`, `url`.

**Get individual downloads:**
```
GET https://api.gumroad.com/v2/sales?product_id={product_id}&after={start_date}&before={end_date}&page={page}
```

Response includes per-download: `email`, `timestamp`, `price`, `quantity`, `referrer`, `ip_country`, custom fields.

**Aggregate weekly:**
```python
# Pseudo-code for weekly aggregation
downloads_this_week = count(sales where timestamp >= week_start)
views_this_week = product.views_count - last_week_snapshot.views_count
conversion_rate = downloads_this_week / views_this_week
```

### 2. Notion Marketplace -- Dashboard scraping

Notion does not expose a public API for marketplace analytics. Use the creator dashboard.

**Via Clay Claygent:**
```
Prompt: "Go to {notion_marketplace_creator_dashboard_url}. Extract: total template duplications (downloads), views this month, and review count. Return as JSON: {downloads, views, reviews, avg_rating}."
```

**Alternative -- manual extraction schedule:** If scraping is unreliable, set up a weekly n8n reminder for a human to log Notion marketplace stats manually into a PostHog event:

```json
{
  "event": "marketplace_weekly_metrics",
  "properties": {
    "marketplace": "notion",
    "template_slug": "{slug}",
    "downloads": 142,
    "views": 1830,
    "reviews": 7,
    "avg_rating": 4.8,
    "week_start": "2026-03-23"
  }
}
```

### 3. Figma Community -- Page scraping

Figma Community shows public stats on each template page: duplicates (downloads), likes, and comments.

**Via Clay Claygent:**
```
Prompt: "Go to {figma_community_template_url}. Extract the number next to the duplicate icon (downloads), the number next to the heart icon (likes), and the number next to the comment icon (comments). Return as JSON: {duplicates, likes, comments}."
```

### 4. Airtable Universe -- Page scraping

Airtable Universe shows copy count on published bases.

**Via Clay Claygent:**
```
Prompt: "Go to {airtable_universe_url}. Extract the copy count displayed on the page. Return as JSON: {copies, description, creator}."
```

### 5. Canva -- Creator dashboard scraping

Canva Creators dashboard shows template usage stats (how many times a template was used in a design).

**Via Clay Claygent:**
```
Prompt: "Go to {canva_creator_dashboard_url}. Extract: template uses this month, total uses, and estimated royalties. Return as JSON: {uses_this_month, total_uses, estimated_royalties}."
```

### 6. Aggregate across marketplaces

After collecting data from each marketplace, normalize into a single schema:

```json
{
  "event": "marketplace_weekly_metrics",
  "properties": {
    "marketplace": "{marketplace_name}",
    "template_slug": "{slug}",
    "downloads": 0,
    "views": 0,
    "reviews": 0,
    "avg_rating": 0,
    "cta_clicks": 0,
    "leads_captured": 0,
    "week_start": "2026-03-23"
  }
}
```

Send each marketplace's data as a separate PostHog event for per-marketplace comparison.

## Error Handling

- **Clay scraping fails:** Marketplace UI may have changed. Update the Claygent prompt with new element descriptions. Fall back to manual weekly logging.
- **Gumroad API rate limit:** 60 requests per minute. Batch queries and cache results.
- **Metrics discrepancy:** Some marketplaces count "views" differently (page loads vs unique visitors). Document the definition per marketplace and compare within-marketplace trends rather than cross-marketplace absolutes.
- **No API available:** For marketplaces without APIs or scrapable dashboards, use UTM-tagged links in PostHog as the primary metric source. PostHog will capture all clicks from the marketplace to your site.

## Pricing

- Clay: Explorer plan $149/mo for Claygent scraping credits ([clay.com/pricing](https://clay.com/pricing))
- Gumroad API: Free with any Gumroad account
- PostHog: Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing))
