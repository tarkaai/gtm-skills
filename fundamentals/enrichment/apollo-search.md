---
name: apollo-search
description: Search Apollo's database for prospects matching your ICP
tool: Apollo
difficulty: Beginner
---

# Search for Prospects in Apollo

## Prerequisites
- Apollo account with API access or Clay integration
- Defined ICP with firmographic and demographic criteria

## Steps

1. **Access Apollo search.** Use Apollo's People Search or Company Search. If using Clay, add an Apollo enrichment column -- Clay connects to Apollo's API automatically. If using Apollo directly, go to the Search tab.

2. **Set company filters.** Filter by: Industry (use Apollo's industry taxonomy), Employee Count (e.g., 11-50, 51-200), Location (country, state, or city), Annual Revenue range, Technologies used, and Keywords in company description.

3. **Set person filters.** Filter by: Job Title (use keywords like "VP", "Head of", "Director"), Department (Engineering, Marketing, Sales), Seniority Level (C-Suite, VP, Director, Manager), and years in current role.

4. **Use boolean search for titles.** Apollo supports boolean title search. Example: "(CTO OR VP Engineering OR Head of Platform) AND NOT (intern OR assistant)". This gives you more control than simple keyword matching.

5. **Save your search.** Save the search as a Saved List in Apollo for re-running later. Name it with the campaign and date (e.g., "Q1-SaaS-DevTools-VPEng"). Apollo will notify you when new prospects match your saved search.

6. **Export results.** Export up to 25 contacts per search on the free plan, or use API/Clay integration for higher volume. Always verify emails before outreach (see `fundamentals/enrichment/clay-email-verification`).
