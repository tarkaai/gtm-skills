---
name: linkedin-ads-campaign-setup
description: Create a LinkedIn advertising campaign via the Marketing API with proper structure and tracking
tool: LinkedIn Ads
difficulty: Intermediate
---

# Set Up a LinkedIn Ads Campaign

## Prerequisites
- LinkedIn Campaign Manager account with Marketing API access
- LinkedIn Insight Tag installed on your website

## Steps

1. **Install the LinkedIn Insight Tag.** Add the JavaScript snippet to your website for conversion tracking. Retrieve the tag code via the LinkedIn Marketing API or Campaign Manager.

2. **Create a Campaign Group via API.** Organize related campaigns:
   ```
   POST /v2/adCampaignGroups
   { "account": "urn:li:sponsoredAccount:<id>", "name": "Q1 2025 - Product Launch", "status": "ACTIVE" }
   ```

3. **Create a Campaign via API.** Choose your objective and ad format:
   ```
   POST /v2/adCampaigns
   {
     "account": "urn:li:sponsoredAccount:<id>",
     "campaignGroup": "urn:li:sponsoredCampaignGroup:<id>",
     "name": "SaaS Decision Makers - Lead Gen",
     "type": "SPONSORED_UPDATES",
     "objectiveType": "LEAD_GENERATION",
     "dailyBudget": {"amount": "100", "currencyCode": "USD"},
     "biddingStrategy": "MAXIMUM_DELIVERY"
   }
   ```

4. **Define your target audience.** Set targeting parameters in the campaign (see `linkedin-ads-audience-targeting`). Filter by industry, company size, job function, and seniority.

5. **Create ad creative via API.** Write headline (under 70 chars), ad copy (under 150 chars), and upload image/video. Create the ad:
   ```
   POST /v2/adCreatives
   { "campaign": "urn:li:sponsoredCampaign:<id>", "type": "SPONSORED_STATUS_UPDATE" }
   ```

6. **Launch and monitor.** Activate the campaign and start with a small budget ($50-100/day). Increase once you verify performance via the Analytics API.
