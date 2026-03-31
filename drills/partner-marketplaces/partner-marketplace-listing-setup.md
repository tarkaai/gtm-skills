---
name: partner-marketplace-listing-setup
description: Research, create, and publish app listings on partner ecosystem marketplaces with keyword-optimized copy and UTM tracking
category: Partner Marketplaces
tools:
  - Clay
  - Attio
  - PostHog
fundamentals:
  - partner-marketplace-listing-api
  - clay-claygent
  - clay-company-search
  - attio-contacts
  - attio-notes
  - posthog-custom-events
  - google-ads-keyword-research
---

# Partner Marketplace Listing Setup

This drill creates and publishes your app/integration listing on partner ecosystem marketplaces (Salesforce AppExchange, HubSpot App Marketplace, Shopify App Store, Slack App Directory, Zapier, Make). Each listing is keyword-optimized for marketplace search and UTM-tagged for attribution.

## Input

- ICP definition: who your buyers are and which partner platforms they already use
- Working integration with at least 1 partner platform (API-based or native)
- App listing assets: logo (512x512 PNG min), 3+ screenshots showing the integration in action within the partner platform, 60-120 second demo video URL
- Product pricing model and free trial/freemium details

## Steps

### 1. Identify target partner marketplaces

Use Clay with the `clay-company-search` fundamental to identify which partner platforms your ICP already uses:

**Claygent prompt:**
```
For companies matching this ICP: {icp_description}
1. What are the top 5 SaaS platforms they use as core infrastructure? (e.g., Salesforce, HubSpot, Shopify, Slack, Zapier)
2. For each platform, does it have a public app/integration marketplace?
3. What is the estimated marketplace traffic for our category on each platform?
4. How many competing integrations exist in our category on each marketplace?
Return: platform name, marketplace URL, estimated category traffic (high/medium/low), competing app count, and our fit score (1-5).
```

Prioritize marketplaces where: (a) your ICP already lives, (b) competition is moderate (5-20 apps, not 0 or 100+), (c) you have a working integration.

### 2. Research marketplace-specific keywords

For each target marketplace, use `clay-claygent` and `google-ads-keyword-research` to identify search terms:

**Claygent prompt per marketplace:**
```
For the {marketplace_name} app marketplace, in the {category} category:
1. What search terms do users type when looking for apps like ours?
2. What titles do the top 5 apps in this category use?
3. What tags or categories do the highest-rated apps use?
4. What phrases appear repeatedly in top-rated reviews? (These indicate what buyers value.)
Return: keyword, estimated search relevance (high/medium/low), current top result for that keyword.
```

Supplement with `google-ads-keyword-research` to find terms people search on Google that lead to marketplace pages (e.g., "best salesforce reporting apps", "hubspot lead scoring integration").

### 3. Write listing copy

For each marketplace, write optimized listing content:

**Title:** `{Primary Keyword} - {Your Product Name}` or `{Your Product Name}: {Primary Benefit}`
- Include the highest-volume keyword from step 2
- Keep under 50 characters for display truncation

**Tagline/Short description (where supported):**
- One sentence: what the integration does + who it's for
- Include secondary keyword

**Full description structure:**
1. Opening paragraph: restate primary keyword + specific outcome the integration delivers
2. Key features: bullet list of 4-6 integration capabilities, each starting with an action verb
3. Who it's for: ICP description in the user's language (job titles, company types)
4. How it works: 3-step quick-start (install, connect, see value)
5. Social proof: number of customers, notable logos (if permitted), aggregate rating from other platforms
6. CTA: link to product website with UTM parameters

**Tags/Categories:** Fill every available tag slot using keyword variants from step 2.

### 4. Prepare visual assets

For each marketplace:

- **Logo:** 512x512 PNG, clean background, recognizable at small sizes
- **Screenshots:** Minimum 3, showing the integration running inside the partner platform. Caption each screenshot with a benefit statement, not a feature label. Example: "See pipeline revenue sync in real-time" not "Dashboard view."
- **Demo video:** 60-120 seconds. Structure: problem (10s) -> solution demo (40-60s) -> CTA (10s). Host on YouTube or Vimeo for embed compatibility.
- **Cover image (if supported):** 1280x800 or marketplace-specific dimensions. Show the product UI integrated with the partner platform.

### 5. Submit listings

Use `partner-marketplace-listing-api` to create listings on each target marketplace. For each:

1. Fill all required and optional fields
2. Set UTM parameters on all outbound links: `?utm_source={marketplace}&utm_medium=partner-marketplace&utm_campaign=listing`
3. Submit for marketplace review
4. Note: review timelines vary by marketplace (2-8 weeks for first submission)

### 6. Configure basic tracking

Using `posthog-custom-events`, set up initial attribution tracking:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `partner_marketplace_visit` | UTM-tagged site visit from a partner marketplace | `marketplace`, `listing_slug`, `utm_campaign` |
| `partner_marketplace_signup` | Trial start or signup from a marketplace-sourced session | `marketplace`, `listing_slug`, `signup_type` |

### 7. Log listings in CRM

Using `attio-contacts`, create a campaign record in Attio for each marketplace listing:

Fields: `marketplace_name`, `listing_url`, `date_submitted`, `review_status` (pending/live/rejected), `listing_title`, `primary_keyword`, `utm_source_value`.

Using `attio-notes`, add the listing copy and keyword research as a note on each record for future optimization reference.

## Output

- 1-3 app listings submitted to partner marketplaces with keyword-optimized copy
- UTM-tagged links for attribution tracking
- PostHog events configured for marketplace-sourced traffic
- CRM records for each listing with submission status

## Triggers

- Run once at Smoke level for the first 1-2 marketplace listings
- Run again when adding new marketplace listings at Scalable level
- Re-run listing copy optimization quarterly at Baseline+
