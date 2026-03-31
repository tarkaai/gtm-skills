---
name: integration-partner-discovery
description: Find, score, and qualify complementary products as integration partner candidates based on audience overlap and technical feasibility
category: Partnerships
tools:
  - Clay
  - Attio
  - Crossbeam
fundamentals:
  - clay-company-search
  - clay-enrichment-waterfall
  - clay-claygent
  - crossbeam-account-mapping
  - integration-compatibility-assessment
  - attio-lists
---

# Integration Partner Discovery

This drill identifies complementary products whose user base overlaps your ICP, assesses whether a product integration is technically feasible, and produces a ranked list of integration partner candidates ready for outreach.

## Input

- Your ICP definition (firmographics, buyer persona, pain points, tech stack)
- Your product's integration capabilities (APIs, webhooks, supported platforms)
- Target number of qualified integration partners (default: 15)

## Steps

### 1. Source integration partner candidates from Clay

Use the `clay-company-search` fundamental to find companies that build products your ICP already uses. Search for:

- **Adjacent category products**: Tools that solve a different problem for the same buyer (e.g., if you sell a CRM, look for email tools, scheduling tools, enrichment tools)
- **Workflow neighbors**: Products that come before or after yours in the user's workflow (data flows into your product from X, output flows to Y)
- **Stack companions**: Tools commonly found alongside yours in customer tech stacks (check BuiltWith, G2 Stack, or customer surveys)

Set Clay filters: SaaS companies, employee count 10-1000, not direct competitors, has a public API or integration marketplace. Pull 100-150 candidates.

### 2. Enrich partner candidates

Use the `clay-enrichment-waterfall` fundamental to add:

- Company domain, LinkedIn URL, and product category
- Employee count, funding stage, estimated ARR
- Contact info for the partnerships/BD lead, developer relations lead, or CTO
- Whether they have a public API (check `{domain}/docs` or `{domain}/developers`)
- Number of existing integrations listed on their website or marketplace

### 3. Assess technical compatibility

For the top 40 candidates (sorted by ICP overlap and company stage), run the `integration-compatibility-assessment` fundamental. For each partner, determine:

- API maturity score (1-5)
- Integration type (Light / Medium / Heavy / Native Marketplace)
- Estimated development effort in days
- Whether an existing n8n/Zapier connector covers the use case
- Any technical blockers

Disqualify partners with API maturity score < 2 or estimated effort > 30 days (for Smoke/Baseline levels). Keep these on a "Future" list for Scalable level.

### 4. Check audience overlap with Crossbeam

If Crossbeam is configured, use the `crossbeam-account-mapping` fundamental to check which partner candidates share the most overlapping accounts with your CRM. Partners with high account overlap are the highest-value integration targets because their users are literally your prospects.

For partners not on Crossbeam, use Clay's Claygent to estimate overlap:

```
Clay Claygent prompt:
"Research {partner_domain}. Identify their target customer profile: company size,
industry, buyer persona. Compare to this ICP: {your_icp_description}. Score audience
overlap 1-10 (10 = identical audience, 1 = no overlap). Return: partner_icp_summary,
overlap_score, overlap_reasoning."
```

### 5. Score and rank candidates

Score each partner on three dimensions (each 1-10, max 30):

**Audience Overlap (1-10):** How well does their user base match your ICP?
- 10: Same buyer persona, same company size, same industries
- 7: Same buyer persona, different company sizes
- 4: Adjacent persona (different title, same department)
- 1: No meaningful overlap

**Technical Feasibility (1-10):** How easy is the integration to build?
- 10: API maturity 5, Light integration, existing connector available
- 7: API maturity 4, Medium integration, good docs
- 4: API maturity 3, Medium integration, limited docs
- 1: No API, Heavy integration, significant blockers

**Co-Marketing Potential (1-10):** How likely is the partner to actively co-market?
- 10: Active integration marketplace + partner program + co-marketing history
- 7: Integration marketplace but no formal partner program
- 4: Blog mentions of integrations but no marketplace
- 1: No visible integration marketing activity

Keep candidates scoring 18+ out of 30.

### 6. Build the ranked partner list in Attio

Use the `attio-lists` fundamental to create a list called "Integration Partners — {date}". Add qualified partners with fields:

- Company name and domain
- Product name and category
- Integration score (out of 30)
- Audience overlap score (1-10)
- Technical feasibility score (1-10)
- Co-marketing potential score (1-10)
- API maturity (1-5)
- Integration type (Light / Medium / Heavy)
- Estimated dev days
- Existing connector (Yes/No and platform)
- Contact name, email, and LinkedIn URL for partnerships/BD lead
- Crossbeam overlap count (if available)
- Status: "Prospect" (initial state)

Sort by integration score descending. The top 10-15 are your outreach targets.

## Output

- Ranked list of 10-15 qualified integration partner candidates in Attio
- Each partner scored on audience overlap, technical feasibility, and co-marketing potential
- Technical compatibility assessment for each (API maturity, effort estimate, blockers)
- Contact info for the right person at each partner company
- Ready for outreach via `warm-intro-request` drill or direct email

## Triggers

Run this drill once at Smoke level to identify the first 3-5 partners. Run quarterly at Baseline+ to refresh the integration partner pipeline and identify new opportunities as the partner ecosystem evolves.
