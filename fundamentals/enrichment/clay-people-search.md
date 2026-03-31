---
name: clay-people-search
description: Find decision-makers and contacts at target companies using Clay
tool: Clay
difficulty: Beginner
---

# Find People in Clay

## Prerequisites
- Clay table with target companies (see `fundamentals/enrichment/clay-company-search`)
- Defined buyer personas (titles, seniority levels)

## Steps

1. **Add a "Find People" enrichment column.** In your company table, add a new column using Clay's "Find People at Company" enrichment. This searches for contacts matching your persona criteria at each company in your table.

2. **Configure persona filters.** Set Title Keywords (e.g., "VP Engineering", "CTO", "Head of Platform"), Seniority (e.g., Director+), and Department (e.g., Engineering, Product). Target 2-3 contacts per company for multi-threading.

3. **Handle multi-contact results.** Clay returns multiple people per company. Use the "Expand rows" feature to create one row per person, or keep the top result only if you want a single point of contact per account.

4. **Enrich contact details.** Once people are found, add enrichment columns for Email (see `fundamentals/enrichment/clay-enrichment-waterfall`) and LinkedIn URL. These are required for outreach.

5. **Filter out irrelevant results.** Add a filter to remove contacts with titles that don't match (Clay sometimes returns loose matches). Also filter out people who have been at the company less than 3 months -- they are still ramping and unlikely to buy.

6. **Score and prioritize.** Use Clay's formula columns to score contacts based on title seniority, company fit, and signal strength (see `fundamentals/enrichment/clay-scoring`).
