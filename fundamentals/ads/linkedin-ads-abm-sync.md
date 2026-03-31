---
name: linkedin-ads-abm-sync
description: Upload ABM target company lists to LinkedIn via the Marketing API for precision-targeted advertising
tool: LinkedIn
product: LinkedIn Ads
difficulty: Intermediate
---

# Sync ABM Lists to LinkedIn Ads

## Prerequisites
- LinkedIn Campaign Manager account
- ABM target company list (from Attio or Clay)
- LinkedIn Marketing API access

## Steps

1. **Prepare your ABM list.** Create a CSV with company names (required), company domains (recommended), and optionally company LinkedIn page URLs. Export from Attio using the MCP or API.

2. **Upload via LinkedIn Marketing API.** Use the API to create a matched audience:
   ```
   POST /v2/dmpSegments
   { "name": "Q1 Target Accounts", "type": "COMPANY", "destinations": [{"destination": "LINKEDIN"}] }
   ```
   Then upload the company list. LinkedIn matches companies to profiles -- this takes 24-48 hours. Aim for 80%+ match rate.

3. **Improve match rate.** If match rate is low, add more data points: include both company name variations and domains. Re-upload with enriched data.

4. **Automate Attio-to-LinkedIn sync.** Build an n8n workflow: Schedule Trigger (weekly) -> Attio MCP (export target account list) -> Code node (format as CSV) -> HTTP Request (upload to LinkedIn Marketing API). This keeps your LinkedIn audience in sync with your CRM.

5. **Create targeted campaigns.** Use the matched audience in campaign targeting via the API. Layer job function and seniority filters on top to reach only decision-makers at target accounts.

6. **Measure ABM campaign performance.** Track via the LinkedIn API: impressions, engagement, and pipeline generated from target accounts. Sync to PostHog via n8n for unified reporting alongside organic metrics.
