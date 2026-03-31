---
name: clay-bant-enrichment
description: Enrich prospects with BANT-relevant signals — budget indicators, org chart, tech spend, and timing triggers
tool: Clay
difficulty: Advanced
---

# Enrich Prospects with BANT Signals

Build a Clay table that enriches raw prospect data with signals relevant to each BANT dimension: Budget (funding, revenue, tech spend), Authority (org chart, reporting structure), Need (tech stack gaps, job postings), Timeline (hiring urgency, contract renewals, fiscal year).

## Prerequisites

- Clay account with enrichment credits
- Prospect list imported into Clay (see `clay-table-setup`)
- ICP definition with BANT criteria defined

## Steps

### 1. Budget signal enrichment

Add enrichment columns for budget indicators:

- **Company revenue:** Use Clearbit or Apollo enrichment. Map to `estimated_annual_revenue`.
- **Funding data:** Add a Crunchbase enrichment column. Extract `last_funding_amount`, `last_funding_date`, `total_funding`, `funding_stage`.
- **Tech spend signals:** Use BuiltWith or Wappalyzer enrichment to detect current technology stack. If they use competitor products or adjacent tools, they have budget allocated to this category.
- **Headcount growth:** Use Apollo or LinkedIn enrichment. Companies growing >20% YoY are more likely to have budget for new tools.

Create a formula column `budget_signal_score`:
```
IF(last_funding_date within 12 months, +30, 0) +
IF(estimated_annual_revenue > $5M, +25, IF(estimated_annual_revenue > $1M, +15, 0)) +
IF(uses_competitor_tool, +25, 0) +
IF(headcount_growth > 20%, +20, 0)
```

### 2. Authority signal enrichment

Add enrichment columns for authority indicators:

- **Title seniority:** Use Apollo person enrichment. Map `seniority` field (C-suite, VP, Director, Manager).
- **Department match:** Check if the contact's department aligns with who buys your product.
- **Org chart depth:** Use LinkedIn enrichment to check how many people report to this person. Decision makers typically have 5+ direct reports.
- **LinkedIn activity:** Use Clay's LinkedIn scraper to check if the person posts about relevant topics (industry pain points, tool evaluations). Active posters in your domain are often champions.

Create a formula column `authority_signal_score`:
```
IF(seniority = "C-suite", +40, IF(seniority = "VP", +30, IF(seniority = "Director", +20, +10))) +
IF(department_match, +25, 0) +
IF(direct_reports > 5, +20, IF(direct_reports > 0, +10, 0)) +
IF(linkedin_posts_relevant > 2, +15, 0)
```

### 3. Need signal enrichment

Add enrichment columns for need indicators:

- **Job postings:** Use Clay's job posting scraper. If the company is hiring for roles related to your product's problem space, they have an active need.
- **Tech stack gaps:** Compare their current tech stack (from BuiltWith) against your product's integration partners. Gaps indicate unmet needs.
- **G2/Capterra reviews:** Use Clay's web scraper to check if the company has reviewed competitors. If they left negative reviews, they may be looking for alternatives.
- **News mentions:** Use Clay's news search to find recent articles mentioning the company + relevant problem keywords.

Create a formula column `need_signal_score`:
```
IF(hiring_relevant_roles > 0, +30, 0) +
IF(tech_stack_gap_detected, +25, 0) +
IF(negative_competitor_review, +25, 0) +
IF(news_mentions_problem > 0, +20, 0)
```

### 4. Timeline signal enrichment

Add enrichment columns for timing indicators:

- **Recent funding:** Companies that just raised are in buying mode for the next 3-6 months.
- **Leadership changes:** New CXO hires often trigger new tool evaluations within 90 days. Use Apollo to detect recent job changes at target accounts.
- **Fiscal year end:** If you can determine their fiscal year (often from annual reports or Crunchbase), approaching fiscal year end means "use it or lose it" budget.
- **Contract renewal dates:** If they use a competitor, typical SaaS contracts renew annually. Look for the competitor adoption date via BuiltWith historical data to estimate renewal window.

Create a formula column `timeline_signal_score`:
```
IF(last_funding_date within 6 months, +30, IF(within 12 months, +15, 0)) +
IF(new_cxo_hire within 90 days, +30, 0) +
IF(fiscal_year_end within 3 months, +25, 0) +
IF(competitor_contract_renewal_window, +15, 0)
```

### 5. Compute composite BANT pre-score

Create a composite column:
```
bant_pre_score = (budget_signal_score * 0.25) + (authority_signal_score * 0.25) + (need_signal_score * 0.30) + (timeline_signal_score * 0.20)
```

Set tiers:
- **Hot (75+):** All four BANT dimensions show signals. Prioritize for immediate outreach.
- **Warm (50-74):** 2-3 dimensions show signals. Good candidates but need discovery call to confirm.
- **Cold (<50):** Weak signals. Nurture or deprioritize.

### 6. Export enriched data

Push the enriched and scored table to Attio via Clay's integration. Map each BANT signal column to the corresponding Attio custom attribute (see `attio-custom-attributes`). Include the raw signal data, not just the scores, so reps have context for discovery calls.

## Error Handling

- **Enrichment provider returns no data:** The waterfall pattern handles this. If all providers fail for a column, leave it blank and deduct points in the scoring formula.
- **Credit exhaustion:** Monitor credit usage per batch. Process in batches of 50 and check remaining credits before each batch.
- **Stale data:** Enrichment data decays. Flag any data older than 90 days for re-enrichment. Set up a quarterly re-enrichment workflow.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay | Enrichment waterfalls | Most flexible, multi-provider |
| Apollo | Built-in enrichment | Good coverage, less customizable |
| Clearbit (HubSpot) | Reveal API | Strong firmographics |
| ZoomInfo | Enrichment API | Enterprise-grade, expensive |
| People Data Labs | Person + Company API | Good fallback provider |
