---
name: linkedin-ads-abm-sync
description: Upload and sync your Account-Based Marketing target company lists to LinkedIn for precision-targeted advertising.
tool: LinkedIn Ads
difficulty: Config
---

# Sync ABM Lists to LinkedIn Ads

### Step-by-step
1. Prepare your ABM list: create a CSV with company names (required), company domains (recommended), and optionally company LinkedIn page URLs.
2. In LinkedIn Campaign Manager, go to Account Assets > Matched Audiences > Create Audience > Upload List > Company/Contact.
3. For company list upload: map the columns (Company Name is required, Domain improves match rate).
4. Upload the CSV and wait for LinkedIn to match — this can take 24-48 hours. Aim for 80%+ match rate.
5. If match rate is low, add more data points: include both company name variations and domains.
6. For Attio-to-LinkedIn sync: build an n8n workflow that exports your target account list from Attio weekly and uploads it to LinkedIn via the Marketing API.
7. Create a campaign using your matched audience: this ensures only employees at your target accounts see the ads.
8. Layer job function/seniority targeting on top of the company list: target only decision-makers at your target accounts.
9. Monitor the matched audience size: if companies are added/removed from your ABM list, re-upload monthly.
10. Measure ABM campaign performance: track impressions, engagement, and pipeline generated from target accounts specifically.
