---
name: linkedin-ads-audience-targeting
description: Build precise LinkedIn ad audiences using the Marketing API for B2B targeting
tool: LinkedIn Ads
difficulty: Intermediate
---

# Configure LinkedIn Ads Audience Targeting

## Prerequisites
- LinkedIn Campaign Manager account with Marketing API access
- Defined ICP with firmographic and demographic criteria

## Steps

1. **Define targeting criteria via API.** Use the LinkedIn Marketing API to configure campaign targeting:
   ```
   POST /v2/adCampaigns
   {
     "targeting": {
       "include": {
         "and": [
           {"or": {"industry": ["SOFTWARE", "INTERNET"]}},
           {"or": {"companySize": ["SIZE_11_50", "SIZE_51_200"]}},
           {"or": {"jobFunction": ["ENGINEERING", "PRODUCT_MANAGEMENT"]}},
           {"or": {"seniority": ["VP", "DIRECTOR"]}}
         ]
       }
     }
   }
   ```

2. **Company targeting.** Filter by industry, company size, and optionally specific company names. For ABM, use matched audiences (see `linkedin-ads-abm-sync`).

3. **Person targeting.** Layer job function, seniority level, and specific job titles. Use boolean-style targeting for precision: target "VP of Engineering" OR "Head of Platform" with Director+ seniority.

4. **Exclude audiences.** Exclude competitors' employees, your own company, and current customers via the API exclusion parameters to avoid wasting spend.

5. **Check audience size via API.** Query the audience count endpoint. LinkedIn recommends 50,000-500,000 for Sponsored Content. If too small, broaden criteria; if too large, add more filters.

6. **Create audience variations.** Build and save multiple audience configurations: "ICP - Engineering Leaders", "ICP - Marketing Leaders", "ICP - C-Suite". Test each in separate campaigns to identify which converts best.
