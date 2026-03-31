---
name: linkedin-ads-abm
description: Run account-based marketing campaigns on LinkedIn targeting specific companies
tool: LinkedIn Ads
difficulty: Advanced
---

# Run ABM Campaigns on LinkedIn

## Prerequisites
- Target account list with at least 100 companies
- LinkedIn Campaign Manager with Matched Audiences enabled
- Budget of at least $3,000/month for meaningful ABM

## Steps

1. **Build your account list.** Export your target account list from your CRM (see `fundamentals/crm/attio-lists`) or enrichment tool. Include company name and domain at minimum. LinkedIn matches on company name to their page database. Clean names for best match rate -- remove "Inc.", "Ltd.", etc.

2. **Upload as Matched Audience.** In Campaign Manager, go to Audiences > Matched Audiences > Upload Company List. Upload your CSV. LinkedIn takes 24-48 hours to process matching. Expect 60-80% match rate. If below 50%, clean your company names and re-upload.

3. **Layer targeting on the account list.** Your Matched Audience includes everyone at those companies. Layer additional targeting: Seniority (Director+), Job Function (the department that buys your product), or specific job titles. This narrows to decision-makers at target accounts.

4. **Create multi-format campaigns.** Run 3 campaign types simultaneously against your ABM list: Sponsored Content (awareness -- educational posts), Lead Gen Forms (conversion -- gated content offers), and Message Ads (direct outreach to high-value contacts). Each format serves a different funnel stage.

5. **Coordinate with outbound.** Sync your ABM ad campaigns with outbound email sequences. When a target account engages with an ad (clicks, form fill), prioritize them for outbound outreach. This "surround sound" approach warms the account before the sales touch.

6. **Measure account-level engagement.** Track metrics per account, not just per campaign. Use LinkedIn's Demographics report to see which companies are clicking. Export this data and match it to your CRM pipeline. The goal is account engagement leading to pipeline, not just ad clicks.
