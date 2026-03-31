---
name: meta-ads-campaign-setup
description: Create a Meta (Facebook/Instagram) ad campaign via the Marketing API
tool: Meta Ads
difficulty: Intermediate
---

# Set Up a Meta Ads Campaign

## Prerequisites
- Meta Business Manager account with Marketing API access
- Meta Pixel and CAPI configured (see `meta-ads-pixel-capi`)

## Steps

1. **Create a campaign via Marketing API.** Use the Meta Marketing API:
   ```
   POST /act_<ad-account-id>/campaigns
   { "name": "Q1 SaaS Lead Gen", "objective": "OUTCOME_LEADS", "status": "PAUSED", "special_ad_categories": [] }
   ```
   For B2B: use OUTCOME_LEADS with lead forms, or OUTCOME_SALES pointing to your landing page.

2. **Set campaign structure.** Campaign (budget) -> Ad Set (audience, placement) -> Ad (creative). Set daily budget:
   ```
   POST /act_<ad-account-id>/adsets
   { "name": "Engineering Leaders", "campaign_id": "<id>", "daily_budget": 5000, "billing_event": "IMPRESSIONS", "optimization_goal": "LEAD_GENERATION" }
   ```

3. **Configure targeting.** Set audience targeting on the ad set (see `meta-ads-audiences`):
   ```json
   { "targeting": { "interests": [{"id": "6003020834693"}], "age_min": 25, "age_max": 55, "geo_locations": {"countries": ["US"]} } }
   ```

4. **Create ads via API.** Upload creative and create ads:
   ```
   POST /act_<ad-account-id>/ads
   { "name": "Ad Variant A", "adset_id": "<id>", "creative": {"creative_id": "<creative-id>"}, "status": "PAUSED" }
   ```
   Write primary text (under 125 chars for mobile), headline, and description. Add CTA: LEARN_MORE, SIGN_UP, GET_QUOTE.

5. **Launch and monitor.** Activate the campaign and monitor via the Insights API:
   ```
   GET /act_<id>/insights?fields=impressions,clicks,ctr,actions,cost_per_action_type
   ```

6. **Automate reporting.** Build an n8n workflow that pulls Meta ad performance daily via the Marketing API and syncs to PostHog for unified GTM reporting.
