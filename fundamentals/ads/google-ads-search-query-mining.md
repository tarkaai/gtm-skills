---
name: google-ads-search-query-mining
description: Extract and analyze actual search queries from Google Ads to find converting terms and new negative keywords
tool: Google Ads
difficulty: Config
---

# Mine Google Ads Search Query Reports

## Prerequisites
- Google Ads account with active Search campaigns (at least 7 days of data)
- Google Ads API access configured

## Steps

1. **Pull the search terms report via API.** Use the Google Ads Query Language (GAQL):
   ```
   SELECT
     search_term_view.search_term,
     search_term_view.status,
     metrics.impressions,
     metrics.clicks,
     metrics.conversions,
     metrics.cost_micros,
     metrics.click_through_rate,
     metrics.conversions_from_interactions_rate,
     segments.keyword.info.text,
     segments.keyword.info.match_type
   FROM search_term_view
   WHERE segments.date DURING LAST_30_DAYS
     AND metrics.impressions > 10
   ORDER BY metrics.conversions DESC
   ```
   This returns every actual query that triggered your ads, with performance data.

2. **Identify high-value converting queries.** Filter for queries with conversions > 0. These are your proven money terms. For each:
   - If it is not already an exact-match keyword, add it as one to capture this traffic at the lowest CPC
   - If it is a long-tail variant of an existing keyword, create a dedicated ad group with tailored ad copy
   - Calculate the actual CPA for each converting query: `cost_micros / conversions / 1_000_000`

3. **Find negative keyword candidates.** Filter for queries with high impressions and clicks but zero conversions:
   - Queries with spend > 2x your target CPA and zero conversions are strong negative keyword candidates
   - Look for pattern clusters: if multiple irrelevant queries share a common word (e.g., "free", "jobs", "tutorial"), add that word as a negative keyword at the campaign level
   - Use `AddNegativeKeywords` API call to add them:
     ```
     POST /customers/<id>/campaignCriteria:mutate
     {
       "operations": [{
         "create": {
           "campaign": "customers/<id>/campaigns/<campaign_id>",
           "negative": true,
           "keyword": {
             "text": "free",
             "match_type": "BROAD"
           }
         }
       }]
     }
     ```

4. **Discover new keyword opportunities.** Look for converting queries that are not in your keyword list at all. These represent demand you are capturing accidentally via broad or phrase match. Add the best ones as exact-match keywords with dedicated ad copy.

5. **Analyze match type performance.** Compare conversion rates across match types for the same root keyword. If exact match converts at 8% but broad match at 1%, tighten match types and shift budget toward exact.

6. **Schedule regular mining.** Run this analysis weekly for the first month of a campaign, then biweekly once stable. Each cycle should produce:
   - 5-15 new negative keywords
   - 2-5 new exact-match keyword additions
   - Updated CPA by query for budget allocation decisions

## Output
- List of converting search queries with CPA
- New exact-match keywords to add
- New negative keywords to add
- Match type performance comparison
