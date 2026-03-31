---
name: meta-ads-audiences
description: Create custom, lookalike, and interest-based audiences via the Meta Marketing API
tool: Meta
product: Meta Ads
difficulty: Intermediate
---

# Build Meta Ads Audiences

## Prerequisites
- Meta Business Manager with Marketing API access
- Meta Pixel installed for website visitor audiences
- Customer email list for custom audiences

## Steps

1. **Create a Custom Audience from website visitors.** Use the Marketing API:
   ```
   POST /act_<ad-account-id>/customaudiences
   {
     "name": "Pricing Page Visitors - Last 14 Days",
     "subtype": "WEBSITE",
     "rule": {"url": {"i_contains": "/pricing"}, "retention_days": 14}
   }
   ```

2. **Create a Custom Audience from customer list.** Upload a CSV of customer emails via the API. Meta matches to Facebook/Instagram profiles (typically 40-70% match rate). Hash emails with SHA-256 before uploading for privacy compliance.

3. **Create Lookalike Audiences.** Select your best customers as the source:
   ```
   POST /act_<ad-account-id>/customaudiences
   { "name": "Lookalike - Best Customers 1%", "subtype": "LOOKALIKE", "origin_audience_id": "<source-id>", "lookalike_spec": {"country": "US", "ratio": 0.01} }
   ```
   1% is most similar, 5-10% is broader.

4. **Use interest and behavior targeting.** For B2B: layer interests (SaaS, Entrepreneurship), behaviors (Small business owners), and demographics in your ad set targeting configuration.

5. **Exclude audiences.** Exclude existing customers and recent converters in the ad set targeting to avoid wasting spend:
   ```json
   { "targeting": { "exclusions": { "custom_audiences": [{"id": "<customers-audience-id>"}] } } }
   ```

6. **Refresh audiences.** Re-upload customer lists monthly and update website visitor windows via the API to keep audiences current. Automate with an n8n workflow that exports customers from Attio and uploads to Meta weekly.
