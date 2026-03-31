---
name: apollo-search
description: Search Apollo's database for prospects matching your ICP
tool: Apollo
product: Apollo
difficulty: Beginner
---

# Search for Prospects in Apollo

## Prerequisites
- Apollo account with API access or Clay integration
- Defined ICP with firmographic and demographic criteria

## Steps

1. **Access Apollo search via API.** Use Apollo's People Search or Company Search API endpoints. If using Clay, add an Apollo enrichment column -- Clay connects to Apollo's API automatically. Direct API access:
   ```
   POST /v1/mixed_people/search
   {
     "person_titles": ["VP Engineering", "CTO"],
     "organization_num_employees_ranges": ["11,50", "51,200"],
     "person_seniorities": ["vp", "c_suite"]
   }
   ```

2. **Set company filters.** Filter by: Industry (use Apollo's industry taxonomy), Employee Count (e.g., 11-50, 51-200), Location (country, state, or city), Annual Revenue range, Technologies used, and Keywords in company description.

3. **Set person filters.** Filter by: Job Title (keywords: "VP", "Head of", "Director"), Department (Engineering, Marketing, Sales), Seniority Level (C-Suite, VP, Director, Manager), and years in current role.

4. **Use boolean search for titles.** Apollo supports boolean title search: `"(CTO OR VP Engineering OR Head of Platform) AND NOT (intern OR assistant)"`. This gives you more control than simple keyword matching.

5. **Save your search.** Save the search as a Saved List in Apollo via the API for re-running later. Name with campaign and date (e.g., "Q1-SaaS-DevTools-VPEng"). Apollo notifies when new prospects match.

6. **Export results.** Use the API to export contacts. Free plan: 25 per search. Paid/Clay integration: higher volume. Always verify emails before outreach (see `clay-email-verification`).
