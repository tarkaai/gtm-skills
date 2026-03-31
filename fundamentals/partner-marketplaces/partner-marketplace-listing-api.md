---
name: partner-marketplace-listing-api
description: Create, update, and manage app listings on partner ecosystem marketplaces via their APIs and developer portals
tool: Salesforce AppExchange / HubSpot App Marketplace / Shopify App Store / Slack App Directory / Zapier / Make
difficulty: Setup
---

# Partner Marketplace Listing API

Programmatically create and manage app/integration listings across partner ecosystem marketplaces. These are platforms where users of a partner product discover integrations and complementary tools -- distinct from software review directories (G2, Capterra) and template marketplaces (Notion, Figma).

## Prerequisites

- A working integration with the partner platform (API-based or native)
- Developer account on each target marketplace
- App listing assets: logo (512x512 PNG), screenshots (1280x800), demo video URL, description copy
- UTM parameter strategy for attribution

## Salesforce AppExchange

### Create a listing

Listings are managed through the AppExchange Publishing Console (APC). The Partner API automates metadata management.

**Step 1 -- Register as a Salesforce Partner:**
```
Navigate to: https://partners.salesforce.com
Create a Salesforce Partner Community account.
Complete the ISV partner onboarding.
```

**Step 2 -- Create the app listing via Partner API:**
```
POST https://appexchange.salesforce.com/api/v1/listings
Authorization: Bearer {SF_PARTNER_TOKEN}
Content-Type: application/json

{
  "name": "Your Product Name",
  "tagline": "One-line value prop (max 80 chars)",
  "description": "Full HTML description. Include: what the integration does, who it's for, key features, and setup steps.",
  "category": "Sales / Analytics / Marketing / etc.",
  "pricing": {
    "model": "free_trial",
    "starting_price": 49,
    "trial_days": 14
  },
  "listing_url": "https://yourproduct.com/integrations/salesforce?utm_source=appexchange&utm_medium=partner-marketplace&utm_campaign=listing",
  "media": {
    "logo_url": "https://yourcdn.com/logo-512.png",
    "screenshots": [
      {"url": "https://yourcdn.com/sf-screenshot-1.png", "caption": "Dashboard synced with Salesforce"},
      {"url": "https://yourcdn.com/sf-screenshot-2.png", "caption": "Automated workflow setup"},
      {"url": "https://yourcdn.com/sf-screenshot-3.png", "caption": "Reports in Salesforce"}
    ],
    "video_url": "https://youtube.com/watch?v=sf-demo-id"
  },
  "supported_editions": ["Professional", "Enterprise", "Unlimited"],
  "install_url": "https://login.salesforce.com/packaging/installPackage.apexp?p0={package_id}"
}
```

**Step 3 -- Submit for security review:**
AppExchange requires a security review before listing goes live. Submit via the Partner Console. Review takes 4-8 weeks for first submission.

### Update listing content

```
PATCH https://appexchange.salesforce.com/api/v1/listings/{listing_id}
Authorization: Bearer {SF_PARTNER_TOKEN}

{
  "description": "Updated description with new keywords",
  "media": {
    "screenshots": [/* updated screenshot array */]
  }
}
```

### Retrieve analytics

```
GET https://appexchange.salesforce.com/api/v1/listings/{listing_id}/analytics?period=30d
Authorization: Bearer {SF_PARTNER_TOKEN}
```

Returns: `page_views`, `install_clicks`, `installs_completed`, `uninstalls`, `reviews_count`, `avg_rating`.

## HubSpot App Marketplace

### Create a listing

**Step 1 -- Register as a HubSpot App Partner:**
```
Navigate to: https://developers.hubspot.com
Create a developer account.
Create an app in the developer portal.
```

**Step 2 -- Configure app listing via Developer Portal API:**
```
POST https://api.hubspot.com/developer/v2/apps
Authorization: Bearer {HUBSPOT_DEV_TOKEN}
Content-Type: application/json

{
  "name": "Your Product Name",
  "description": "What your integration does with HubSpot. Focus on CRM use cases.",
  "supportUrl": "https://yourproduct.com/support",
  "websiteUrl": "https://yourproduct.com/integrations/hubspot?utm_source=hubspot-marketplace&utm_medium=partner-marketplace&utm_campaign=listing",
  "logoUrl": "https://yourcdn.com/logo-512.png",
  "screenshots": [
    "https://yourcdn.com/hs-screenshot-1.png",
    "https://yourcdn.com/hs-screenshot-2.png"
  ],
  "categories": ["CRM", "Sales Enablement"],
  "pricing": {
    "type": "freemium",
    "pricingUrl": "https://yourproduct.com/pricing"
  }
}
```

**Step 3 -- Submit for listing review:**
HubSpot reviews all marketplace submissions. Ensure your app passes the HubSpot API certification checklist. Review takes 2-4 weeks.

### Retrieve install analytics

```
GET https://api.hubspot.com/developer/v2/apps/{app_id}/installs
Authorization: Bearer {HUBSPOT_DEV_TOKEN}
```

Returns: `total_installs`, `active_installs`, `uninstalls`, `daily_installs` array.

## Shopify App Store

### Create a listing

**Step 1 -- Register as a Shopify Partner:**
```
Navigate to: https://partners.shopify.com
Create a partner account.
Create an app in the Partners dashboard.
```

**Step 2 -- Configure listing via Partner API:**
```
POST https://partners.shopify.com/api/v1/apps
Authorization: Bearer {SHOPIFY_PARTNER_TOKEN}
Content-Type: application/json

{
  "name": "Your Product Name",
  "tagline": "Short tagline for search results",
  "description": "Detailed description. Shopify heavily weighs keywords in search ranking.",
  "category": "Marketing / Sales / Inventory / etc.",
  "pricing": {
    "model": "recurring",
    "plans": [
      {"name": "Free", "price": 0, "features": ["Feature A", "Feature B"]},
      {"name": "Pro", "price": 29, "features": ["All Free features", "Feature C", "Feature D"]}
    ]
  },
  "listing_url": "https://yourproduct.com/integrations/shopify?utm_source=shopify-appstore&utm_medium=partner-marketplace&utm_campaign=listing",
  "screenshots": ["url1", "url2", "url3", "url4"],
  "demo_url": "https://demo-store.myshopify.com"
}
```

**Step 3 -- Submit for review:**
Shopify reviews all submissions for quality, performance, and merchant value. Review takes 2-6 weeks.

### Retrieve analytics

```
GET https://partners.shopify.com/api/v1/apps/{app_id}/analytics?period=30d
Authorization: Bearer {SHOPIFY_PARTNER_TOKEN}
```

Returns: `page_views`, `installs`, `uninstalls`, `active_installs`, `reviews_count`, `avg_rating`, `revenue`.

## Slack App Directory

### Create a listing

```
POST https://api.slack.com/apps
Authorization: Bearer {SLACK_APP_TOKEN}

{
  "name": "Your Product Name",
  "description": "What your Slack integration does",
  "long_description": "Detailed description with use cases and setup instructions",
  "categories": ["Communication", "Productivity"],
  "listing_url": "https://yourproduct.com/integrations/slack?utm_source=slack-directory&utm_medium=partner-marketplace&utm_campaign=listing",
  "support_url": "https://yourproduct.com/support",
  "privacy_policy_url": "https://yourproduct.com/privacy"
}
```

Slack requires OAuth 2.0 implementation and bot/slash command functionality before directory submission.

## Zapier

### Create a public integration listing

```
Navigate to: https://developer.zapier.com
Create a developer account.
Build your integration using Zapier's CLI or visual builder.
Submit for public listing review.
```

**Zapier Partner API (for analytics):**
```
GET https://developer.zapier.com/api/v1/integrations/{integration_id}/analytics
Authorization: Bearer {ZAPIER_DEV_TOKEN}
```

Returns: `total_users`, `active_zaps`, `zap_runs_30d`, `category_ranking`.

Zapier listings rank by number of active users and Zap templates available. Create 10+ Zap templates to boost ranking.

## Make (formerly Integromat)

### Create a public integration listing

```
Navigate to: https://www.make.com/en/partners
Register as a technology partner.
Build your integration using Make's SDK.
Submit for marketplace inclusion.
```

Make does not expose a public listing management API. All listing management is through the partner portal. Analytics are available in the partner dashboard.

## Listing Optimization Checklist

For every partner marketplace listing:

1. **Keywords in title and description** -- use terms buyers search within that marketplace's search
2. **UTM parameters on all outbound links** -- `utm_source={marketplace}&utm_medium=partner-marketplace&utm_campaign=listing`
3. **Screenshots** -- minimum 3, showing the integration in action within the partner platform
4. **Demo video** -- 60-120 second walkthrough of the integration workflow
5. **Pricing transparency** -- clear pricing model and free trial/freemium option
6. **Setup documentation** -- link to integration setup guide
7. **Support URL** -- dedicated support page for marketplace users

## Error Handling

- **401 Unauthorized**: Developer API token expired. Re-authenticate through the developer portal.
- **403 Forbidden**: App not approved for marketplace listing. Complete certification requirements first.
- **409 Conflict**: Listing already exists. Use `PATCH` to update.
- **429 Rate Limited**: Most partner APIs allow 100-300 requests/minute. Implement exponential backoff.
- **Pending Review**: New submissions go through partner review (2-8 weeks depending on platform). Check status via the developer portal or status API endpoint.
