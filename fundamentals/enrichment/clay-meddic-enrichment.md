---
name: clay-meddic-enrichment
description: Enrich prospects with MEDDIC-relevant signals — org chart for economic buyer, decision process indicators, pain signals, and champion identification
tool: Clay
difficulty: Advanced
---

# Enrich Prospects with MEDDIC Signals

Build a Clay table that enriches raw prospect data with signals relevant to each MEDDIC element: Metrics (quantified business outcomes they care about), Economic Buyer (who holds the budget), Decision Criteria (how they evaluate), Decision Process (procurement steps), Identify Pain (current frustrations), Champion (internal advocate potential).

## Prerequisites

- Clay account with enrichment credits
- Prospect list imported into Clay (see `clay-table-setup`)
- ICP definition with MEDDIC criteria defined

## Steps

### 1. Metrics signal enrichment

Add enrichment columns for quantifiable business outcome indicators:

- **Company KPIs:** Use Clearbit or Apollo enrichment to get company size, revenue, growth rate. Map to `estimated_annual_revenue`, `employee_count`, `yoy_growth`.
- **Industry benchmarks:** Use Clay's web scraper to pull industry-specific KPIs from public sources (e.g., for SaaS: ARR growth, churn rate, NRR). These inform what metrics the prospect likely cares about.
- **Public financial data:** For public companies, use SEC API or financial data providers. For private companies, estimate from funding data via Crunchbase enrichment.
- **Competitor usage patterns:** Use BuiltWith to detect competitor tools. If they use a competitor, they already measure outcomes in that category — gives you a basis for quantified comparison.

Create a formula column `metrics_signal_score`:
```
IF(estimated_annual_revenue > $10M, +20, IF(> $1M, +10, 0)) +
IF(yoy_growth > 30%, +25, IF(> 10%, +15, 0)) +
IF(uses_competitor_tool, +30, 0) +
IF(public_company OR has_recent_funding, +25, 0)
```

### 2. Economic Buyer signal enrichment

Add enrichment columns for identifying who controls the budget:

- **Org chart mapping:** Use Apollo or LinkedIn enrichment to identify the reporting chain. For your contact, find: their manager, their manager's title, and the department head.
- **C-suite identification:** Use Apollo company enrichment to list all C-suite and VP-level contacts. Cross-reference with the department that typically buys your product.
- **Budget authority signals:** Use LinkedIn enrichment to check if the contact's title includes budget-related keywords (Head of, VP of, Director of, Chief). Map to `likely_budget_authority` boolean.
- **Previous purchase behavior:** Use Clay's Claygent to research whether this person has publicly discussed purchasing decisions (LinkedIn posts about tool evaluations, conference talks about stack decisions).

Create a formula column `economic_buyer_signal_score`:
```
IF(contact_is_c_suite OR contact_is_vp, +40, IF(contact_is_director, +25, +10)) +
IF(department_matches_buying_center, +25, 0) +
IF(org_chart_mapped AND budget_owner_identified, +20, 0) +
IF(previous_purchase_signals > 0, +15, 0)
```

### 3. Decision Criteria signal enrichment

Add enrichment columns for evaluation criteria indicators:

- **Tech stack analysis:** Use BuiltWith or Wappalyzer enrichment to map their current technology stack. This reveals what integrations matter, what standards they follow, and what their technical preferences are.
- **Security/compliance requirements:** Use Clay's web scraper to check if the company mentions SOC2, HIPAA, GDPR, FedRAMP on their website or job postings. These become decision criteria.
- **Job posting analysis:** Use Clay's job posting scraper to find roles related to your product area. Job requirements reveal the criteria they value (e.g., "experience with enterprise-grade tools" = they care about scale).
- **G2/Capterra review analysis:** Use Clay's web scraper to check what criteria the company (or similar companies) use in reviews. Extract themes: price sensitivity, ease of use, integration quality, support responsiveness.

Create a formula column `decision_criteria_signal_score`:
```
IF(tech_stack_complexity > 5 tools, +20, +10) +
IF(compliance_requirements_detected, +25, 0) +
IF(relevant_job_postings > 0, +20, 0) +
IF(review_criteria_extracted, +20, 0) +
IF(rfp_or_evaluation_signals, +15, 0)
```

### 4. Decision Process signal enrichment

Add enrichment columns for procurement and buying process:

- **Company size and structure:** Use Apollo enrichment. Larger companies (500+ employees) typically have formal procurement. Startups (< 50) often have founder-decides processes.
- **Procurement team detection:** Use Apollo to check for procurement, vendor management, or IT purchasing roles at the company. Presence indicates a formal buying process.
- **Legal/security team size:** Use LinkedIn enrichment to estimate legal and infosec team size. Larger teams = more review steps.
- **Industry regulatory context:** Use Clay's Claygent to research industry-specific procurement requirements (e.g., healthcare = HIPAA BAA required, finance = vendor risk assessment).

Create a formula column `decision_process_signal_score`:
```
IF(employee_count < 50, +30, IF(< 200, +20, +10)) +
IF(no_procurement_team_detected, +25, 0) +
IF(legal_team_size < 3, +20, IF(< 10, +10, 0)) +
IF(industry_low_regulation, +15, 0) +
IF(recent_tool_purchase_detected, +10, 0)
```

Note: Higher scores mean EASIER/FASTER decision process. This is inverted because a simpler process is better for deal velocity.

### 5. Identify Pain signal enrichment

Add enrichment columns for pain and urgency indicators:

- **Job postings for your problem area:** Use Clay's job posting scraper. Hiring for roles your product replaces or augments indicates active pain.
- **Negative competitor reviews:** Use Clay's web scraper to check G2/Capterra for the company's reviews of competing products. Negative reviews = active pain with current solution.
- **News/press mentions:** Use Clay's news search for recent articles mentioning the company + problem-related keywords (e.g., "data breach" for security tools, "churn" for retention tools).
- **Social signals:** Use Clay's LinkedIn scraper to check if contacts at the company post about the problem your product solves. Public complaints indicate felt pain.
- **Headcount changes:** Rapid hiring or layoffs in relevant departments signal organizational stress and potential pain.

Create a formula column `identify_pain_signal_score`:
```
IF(hiring_for_problem_roles > 2, +30, IF(> 0, +20, 0)) +
IF(negative_competitor_reviews > 0, +25, 0) +
IF(news_mentions_problem > 0, +20, 0) +
IF(social_pain_signals > 0, +15, 0) +
IF(headcount_change_in_dept > 20%, +10, 0)
```

### 6. Champion signal enrichment

Add enrichment columns for internal advocate identification:

- **LinkedIn engagement:** Use Clay's LinkedIn scraper to check if the contact engages with content about your product category (likes, comments, shares). Active engagers are potential champions.
- **Conference/event attendance:** Use Clay's web scraper to find if the contact has attended or spoken at events related to your product area.
- **Content creation:** Check if the contact publishes articles, blog posts, or videos about the problem you solve. Thought leaders in the space make strong champions.
- **Internal influence:** Use Apollo enrichment to assess team size, tenure, and cross-functional connections. Long-tenured leaders with large teams have more influence.
- **Previous vendor advocacy:** Use Clay's Claygent to research if this person has publicly endorsed or recommended tools similar to yours.

Create a formula column `champion_signal_score`:
```
IF(linkedin_engagement_with_category > 3, +25, IF(> 0, +15, 0)) +
IF(event_attendance_or_speaking, +20, 0) +
IF(publishes_relevant_content, +20, 0) +
IF(team_size > 10 AND tenure > 2_years, +20, IF(team_size > 5, +10, 0)) +
IF(previous_vendor_advocacy, +15, 0)
```

### 7. Compute composite MEDDIC pre-score

Create a composite column:
```
meddic_pre_score = (metrics_signal_score * 0.15) + (economic_buyer_signal_score * 0.20) + (decision_criteria_signal_score * 0.15) + (decision_process_signal_score * 0.15) + (identify_pain_signal_score * 0.20) + (champion_signal_score * 0.15)
```

Set tiers:
- **Hot (75+):** Strong signals across most MEDDIC elements. Prioritize for immediate outreach.
- **Warm (50-74):** 3-4 elements show signals. Good candidates but need discovery call to confirm.
- **Cold (<50):** Weak signals. Nurture or deprioritize.

### 8. Export enriched data

Push the enriched and scored table to Attio via Clay's integration. Map each MEDDIC signal column to the corresponding Attio custom attribute (see `attio-custom-attributes`). Include the raw signal data, not just the scores, so the founder has context for discovery calls.

## Error Handling

- **Enrichment provider returns no data:** The waterfall pattern handles this. If all providers fail for a column, leave it blank and deduct points in the scoring formula.
- **Credit exhaustion:** Monitor credit usage per batch. Process in batches of 50 and check remaining credits before each batch.
- **Stale data:** Enrichment data decays. Flag any data older than 90 days for re-enrichment. Set up a quarterly re-enrichment workflow.
- **Org chart gaps:** If Apollo/LinkedIn cannot map the org chart, flag the prospect for manual research. Economic Buyer identification is critical for MEDDIC — do not skip it.

## Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Clay | Enrichment waterfalls | Most flexible, multi-provider |
| Apollo | Built-in enrichment + org chart | Good for Economic Buyer identification |
| Clearbit (HubSpot) | Reveal API | Strong firmographics, weaker on org chart |
| ZoomInfo | Enrichment API + Org Charts | Best org chart data, enterprise pricing |
| People Data Labs | Person + Company API | Good fallback provider |
| 6sense | Intent data API | Strong for identifying active buyers |
