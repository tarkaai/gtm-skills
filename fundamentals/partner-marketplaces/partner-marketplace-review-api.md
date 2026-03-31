---
name: partner-marketplace-review-api
description: Monitor, respond to, and request reviews on partner ecosystem marketplace listings
tool: Salesforce AppExchange
difficulty: Config
---

# Partner Marketplace Review API

Monitor incoming reviews, respond to them programmatically, and trigger review request workflows for partner ecosystem marketplace listings. Reviews directly impact marketplace search ranking and conversion rates.

## Prerequisites

- Active listings on 1+ partner marketplaces (output from `partner-marketplace-listing-api`)
- Developer/partner API credentials for each marketplace
- CRM (Attio, HubSpot, Salesforce, Pipedrive, or Clarify) with customer data for review targeting

## Salesforce AppExchange

### Fetch reviews

```
GET https://appexchange.salesforce.com/api/v1/listings/{listing_id}/reviews?page=1&per_page=50&sort=newest
Authorization: Bearer {SF_PARTNER_TOKEN}
```

Response:
```json
{
  "reviews": [
    {
      "id": "rev_123",
      "author": "John D.",
      "company": "Acme Corp",
      "rating": 5,
      "title": "Great integration",
      "body": "Easy setup and reliable sync...",
      "created_at": "2026-03-15T10:00:00Z",
      "responded": false
    }
  ],
  "total": 42,
  "avg_rating": 4.6
}
```

### Respond to a review

```
POST https://appexchange.salesforce.com/api/v1/listings/{listing_id}/reviews/{review_id}/response
Authorization: Bearer {SF_PARTNER_TOKEN}

{
  "body": "Thank you for the feedback, John. We're glad the integration is working well for Acme. If you ever need help, reach out to support@yourproduct.com."
}
```

## HubSpot App Marketplace

### Fetch reviews

```
GET https://api.hubspot.com/developer/v2/apps/{app_id}/reviews?limit=50
Authorization: Bearer {HUBSPOT_DEV_TOKEN}
```

Response includes: `reviews[]` with `author`, `rating`, `body`, `created_at`, `response` (null if not yet responded).

### Respond to a review

```
POST https://api.hubspot.com/developer/v2/apps/{app_id}/reviews/{review_id}/response
Authorization: Bearer {HUBSPOT_DEV_TOKEN}

{
  "body": "Thanks for the review! We're happy to hear the HubSpot integration is saving your team time."
}
```

## Shopify App Store

### Fetch reviews

```
GET https://partners.shopify.com/api/v1/apps/{app_id}/reviews?page=1&limit=50&sort=newest
Authorization: Bearer {SHOPIFY_PARTNER_TOKEN}
```

Response includes: `reviews[]` with `author_store`, `rating`, `body`, `created_at`, `reply` (null if not replied).

### Reply to a review

```
POST https://partners.shopify.com/api/v1/apps/{app_id}/reviews/{review_id}/reply
Authorization: Bearer {SHOPIFY_PARTNER_TOKEN}

{
  "body": "Thanks for the feedback! We just released an update that addresses the setup speed you mentioned."
}
```

Shopify allows one reply per review. Edits require deleting the existing reply first.

## Slack App Directory

Slack App Directory does not expose a review API. Reviews are visible on the listing page but must be monitored manually or via web scraping.

**Via Clay Claygent fallback:**
```
Prompt: "Go to https://slack.com/apps/{app_id}. Scroll to the Reviews section. Extract all reviews: author name, rating (stars), review text, date. Return as JSON array."
```

## Review Monitoring Workflow

Set up an n8n cron (daily, 8am) that:

1. Calls the review API for each marketplace listing
2. Filters for reviews where `responded == false` or `reply == null`
3. For negative reviews (1-3 stars): send immediate Slack alert with review text and recommended response
4. For positive reviews (4-5 stars): queue for response within 48 hours
5. Log all new reviews to Attio as notes on the marketplace campaign record

## Review Request Workflow

To systematically build review volume:

1. Query Attio for customers who: (a) have been active 30+ days, (b) use the specific integration, (c) have not been asked for a review in the last 90 days
2. Send a review request email via Loops or Instantly with a direct link to the marketplace review page
3. Track: emails sent, review page clicks (via UTM), reviews posted (via review API delta)
4. Cadence: request reviews from 5-10 customers per week. Never batch-blast.

**Review request link format per marketplace:**
- AppExchange: `https://appexchange.salesforce.com/appxReviews?listingId={listing_id}`
- HubSpot: `https://ecosystem.hubspot.com/marketplace/apps/{app_slug}/reviews/new`
- Shopify: `https://apps.shopify.com/{app_handle}/reviews/new`

## Error Handling

- **404 Not Found**: Review may have been deleted by the author or platform moderation.
- **403 Forbidden**: Response privileges require verified vendor status on the marketplace.
- **Rate limit**: Most review APIs share rate limits with the main listing API. Batch review fetches.
- **Review removed**: If a positive review disappears, it may have been flagged. Do not re-request from the same customer.

## Alternative Tools

- **Birdeye**: Aggregates reviews across platforms, supports response from a single dashboard
- **Podium**: Review management with automated request sequences
- **ReviewTrackers**: Multi-platform review monitoring with sentiment analysis
- **Trustpilot**: B2B review platform with API for review collection and management
- **Delighted**: NPS + review request automation
