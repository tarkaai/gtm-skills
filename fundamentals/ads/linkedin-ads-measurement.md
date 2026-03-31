---
name: linkedin-ads-measurement
description: Set up conversion tracking and analyze LinkedIn Ads performance via the Marketing API
tool: LinkedIn
product: LinkedIn Ads
difficulty: Intermediate
---

# Measure LinkedIn Ads Performance

## Prerequisites
- LinkedIn Insight Tag installed on your website
- LinkedIn Marketing API access

## Steps

1. **Verify Insight Tag installation.** Use the LinkedIn API to check tag status. The Insight Tag JavaScript snippet must be on all pages for conversion tracking to work.

2. **Set up conversion actions via API.** Define conversions using the Marketing API:
   ```
   POST /v2/conversions
   {
     "name": "Demo Requested",
     "type": "LEAD",
     "attributionType": "LAST_TOUCH_BY_CAMPAIGN",
     "conversionMethod": "PIXEL",
     "postClickAttributionWindowSize": 7,
     "viewThroughAttributionWindowSize": 1
   }
   ```
   Define conversions for: demo requested, sign-up completed, content downloaded.

3. **Query campaign performance via API.** Pull metrics:
   ```
   GET /v2/adAnalytics?campaigns=urn:li:sponsoredCampaign:<id>&dateRange.start.year=2025
   ```
   Key metrics: impressions, clicks, CTR, conversions, cost per conversion.

4. **Segment performance by audience.** Compare metrics across job functions, seniority levels, and company sizes via the API breakdown parameters to find your best-performing segments.

5. **Track down-funnel metrics.** Connect LinkedIn leads to Attio (via n8n) to measure which LinkedIn leads become pipeline and revenue. Calculate ROAS: total ad spend vs revenue from LinkedIn-sourced deals.

6. **Build unified reporting.** Sync LinkedIn ad performance data to PostHog via n8n. This lets you see LinkedIn ads alongside organic metrics in one dashboard. Run weekly reviews: pause campaigns with CPA > 2x target, increase budget on winners.
