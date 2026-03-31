---
name: apollo-enrichment
description: Enrich contact and company records using Apollo's data
tool: Apollo
difficulty: Beginner
---

# Enrich Records with Apollo

## Prerequisites
- Apollo account with API credits
- Contact or company records with at least one identifier (email, domain, or LinkedIn URL)

## Steps

1. **Understand Apollo enrichment.** Apollo maintains a database of 270M+ contacts and 60M+ companies. You can enrich existing records by passing an identifier and getting back firmographic and demographic data.

2. **Enrich contacts via API.** Send a request to Apollo's People Enrichment endpoint with an email address or LinkedIn URL. Apollo returns: full name, current title, company, seniority, department, phone number, and social profiles. Use this to fill gaps in your CRM records.

3. **Enrich companies via API.** Send a domain to Apollo's Company Enrichment endpoint. It returns: company name, industry, employee count, revenue range, funding info, technologies used, and headquarters location.

4. **Bulk enrichment via Clay.** If using Clay, add Apollo as an enrichment provider in your waterfall (see `fundamentals/enrichment/clay-enrichment-waterfall`). Clay handles the API calls and maps Apollo's response fields to your table columns automatically.

5. **Handle missing data.** Apollo's coverage varies by region and industry. For US tech companies, expect 85%+ hit rates. For EU or non-tech, rates drop to 60-70%. Use a waterfall with fallback providers to fill gaps.

6. **Keep data fresh.** Apollo data updates quarterly. If a contact's enrichment is more than 90 days old, re-enrich before outreach. Job changes are the most common source of stale data -- 15-20% of contacts change roles annually.
