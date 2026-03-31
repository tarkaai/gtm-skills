---
name: clay-enrichment-waterfall
description: Configure multi-provider enrichment waterfalls to maximize data coverage
tool: Clay
product: Clay
difficulty: Intermediate
---

# Configure Clay Enrichment Waterfalls

## Prerequisites
- Clay table with seed data (see `fundamentals/enrichment/clay-table-setup`)
- Clay credits available (waterfall uses credits per provider attempt)

## Steps

1. **Understand the waterfall pattern.** A waterfall runs multiple enrichment providers in sequence. If Provider A returns no result, Provider B is tried, then Provider C. This maximizes hit rates while controlling cost since you only pay for the provider that returns data.

2. **Set up email waterfall.** Add an "Enrich Email" column and configure the waterfall with providers in this order: Apollo (highest hit rate for tech), Hunter.io (good for SMB), Dropcontact (GDPR-compliant fallback). Clay will try each until one returns a verified email.

3. **Set up company enrichment waterfall.** Add "Enrich Company" with providers: Clearbit (best firmographics), Apollo (good coverage), LinkedIn (fallback). This populates employee count, revenue, funding, and industry.

4. **Set up person enrichment waterfall.** Add "Enrich Person" with: Apollo, LinkedIn, Clearbit. This fills job title, seniority, department, and social profiles.

5. **Add conditional logic.** Use Clay's "Run if" conditions so expensive providers only fire when cheaper ones fail. Example: only run Clearbit if Apollo returned no company data.

6. **Monitor hit rates.** After running 50 rows, check the enrichment status column. Target 80%+ email hit rate and 90%+ company data hit rate. If below, adjust provider order or add providers.
