---
name: clay-company-search
description: Use Clay to find companies matching your ICP criteria
tool: Clay
product: Clay
difficulty: Beginner
---

# Find Companies in Clay

## Prerequisites
- Clay account with credits
- Defined ICP with firmographic criteria (industry, size, funding stage, geography)

## Steps

1. **Use the Find Companies source.** Create a new table and select "Find Companies" as your data source. This searches across Clay's aggregated company database.

2. **Apply ICP filters.** Set filters matching your ICP: Industry (e.g., SaaS, Fintech), Employee Count (e.g., 10-200), Location (e.g., United States), Funding Stage (e.g., Series A-B), Technologies Used (e.g., uses Stripe, runs on AWS).

3. **Refine with keyword filters.** Add keyword filters on company description to narrow results. Example: "developer tools" or "API platform" to find companies in your niche.

4. **Set result limits.** Start with 50 companies for Smoke-level testing. Increase to 200-500 for Baseline campaigns. Never pull more than you can actually outreach to.

5. **Validate the list.** Scan the first 20 results manually. Check that companies genuinely match your ICP. If hit rate is below 70%, tighten your filters.

6. **Export or enrich.** Either export the company list to CSV for manual review, or directly add enrichment columns to find contacts at these companies (see `fundamentals/enrichment/clay-people-search`).
