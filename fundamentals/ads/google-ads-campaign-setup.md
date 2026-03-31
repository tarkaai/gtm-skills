---
name: google-ads-campaign-setup
description: Create a Google Ads campaign with proper structure via the Google Ads API
tool: Google
product: Google Ads
difficulty: Intermediate
---

# Set Up a Google Ads Campaign

## Prerequisites
- Google Ads account with API access
- Conversion tracking configured (see `google-ads-conversion-tracking`)
- Keywords researched (see `google-ads-keyword-research`)

## Steps

1. **Create a campaign via API.** Use the Google Ads API:
   ```
   POST /customers/<id>/campaigns:mutate
   {
     "operations": [{
       "create": {
         "name": "Q1 Search - SaaS CTOs",
         "advertising_channel_type": "SEARCH",
         "status": "PAUSED",
         "campaign_budget": "<budget-resource-name>",
         "bidding_strategy_type": "MAXIMIZE_CONVERSIONS"
       }
     }]
   }
   ```
   Campaign types: SEARCH (text ads on results), DISPLAY (banner ads), PERFORMANCE_MAX (automated across all properties).

2. **Set geographic targeting.** Configure location targeting via the API: country, region, city, or radius. Set daily budget to $20-50/day for testing.

3. **Create ad groups.** Group ads by theme (one ad group per product feature or pain point):
   ```
   POST /customers/<id>/adGroups:mutate
   { "operations": [{ "create": { "name": "CRM Features", "campaign": "<campaign-resource>", "type": "SEARCH_STANDARD" } }] }
   ```

4. **Add keywords.** Add keywords to each ad group via the API (see `google-ads-keyword-research`):
   ```
   POST /customers/<id>/adGroupCriteria:mutate
   { "operations": [{ "create": { "keyword": { "text": "best CRM for startups", "match_type": "PHRASE" } } }] }
   ```

5. **Create Responsive Search Ads.** Provide up to 15 headlines and 4 descriptions via the API. Google mixes and matches to find the best combinations.

6. **Launch and monitor.** Activate the campaign (`status: ENABLED`) and monitor via API queries. Track impressions, clicks, conversions, and CPA daily for the first week.
