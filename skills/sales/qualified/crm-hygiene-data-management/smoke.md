---
name: crm-hygiene-data-management-smoke
description: >
  CRM Hygiene & Data Quality — Smoke Test. Audit 50 CRM records against data quality rules,
  score completeness and accuracy, fix critical errors manually, and prove that systematic
  data hygiene produces measurable improvement in record quality.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=80% data quality score across 50 audited records and >=50% reduction in critical errors within 1 week"
kpis: ["Data quality score", "Critical error rate", "Duplicate rate", "Stale record rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
drills:
  - threshold-engine
---

# CRM Hygiene & Data Quality — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Product

## Outcomes

Prove that auditing CRM records against explicit quality rules produces a measurable baseline and that manual remediation moves the needle. At this level, the agent runs the audit and scores records — the human fixes issues manually. No automation, no always-on workflows. Just proof that data quality is measurable and improvable.

**Pass threshold:** >=80% data quality score across 50 audited records and >=50% reduction in critical errors within 1 week.

## Leading Indicators

- Data quality rules defined and documented (5-7 rules covering required fields, valid values, freshness, duplicates)
- 50 records scored with per-record quality scores written back to Attio
- At least 3 issue types identified (missing fields, stale records, duplicates, invalid values)
- Remediation of critical errors shows measurable score improvement on re-audit

## Instructions

### 1. Define Data Quality Rules

Before auditing, define what "quality" means. Create custom attributes in Attio using the `attio-custom-attributes` fundamental (called by the the crm data audit workflow (see instructions below) drill):

- `data_quality_score` (number, 0-100) on People, Companies, and Deals objects
- `stale_flag` (checkbox) on Deals
- `last_audit_date` (date) on all objects

Define 5-7 rules in a structured format the agent can evaluate programmatically:

| Rule | Object | Check | Severity |
|------|--------|-------|----------|
| Required contact fields | People | full_name, email, company, job_title, source populated | Critical |
| Required deal fields | Deals | company, contact, deal_value, stage, owner populated | Critical |
| Valid email format | People | email matches `^[^@]+@[^@]+\.[^@]+$` | High |
| Valid stage values | Deals | stage is in defined pipeline stages | High |
| Freshness | Deals | last_contacted within 30 days for open deals | Medium |
| No duplicates | People | no other contact shares same email | Medium |
| Close date validity | Deals | expected_close_date not in past for open deals | Low |

Store these rules as an Attio note on a "Data Quality Standards" record for future reference.

### 2. Run the Initial Audit

Run the the crm data audit workflow (see instructions below) drill with scope = 50 records:

1. Query Attio for 50 active deal records and their associated contacts and companies
2. For each record, evaluate every rule and compute the quality score
3. Write `data_quality_score` back to each record in Attio
4. Flag duplicates and add them to a "Potential Duplicates" list
5. Flag stale records (no activity 30+ days) with `stale_flag = true`
6. Log `data_quality_audit_completed` event to PostHog with aggregate metrics

Record the baseline metrics:
- Average data quality score across 50 records
- Critical error rate (% missing required fields)
- Duplicate rate
- Stale record rate

### 3. Fix Critical Errors

**Human action required:** Review the audit results and manually fix the highest-impact issues:

1. Open the "Records Needing Attention" view in Attio (sorted by quality score ascending)
2. For each record with score < 70:
   - Fill missing required fields (look up company info, verify email, add job title)
   - Correct invalid values (fix stages, update close dates)
   - Update `last_contacted` if activity happened but was not logged
3. For each pair in the "Potential Duplicates" list:
   - Verify whether they are true duplicates
   - Merge confirmed duplicates, keeping the record with more complete data
   - Remove false positives from the list

Log time spent on each fix type. This baseline establishes the manual effort that automation will later replace.

### 4. Re-Audit and Measure Improvement

Run the the crm data audit workflow (see instructions below) drill again on the same 50 records:

1. Recalculate all quality scores
2. Compare against baseline metrics from Step 2
3. Calculate improvement: `(new_score - baseline_score) / baseline_score * 100`

### 5. Evaluate Against Threshold

Run the `threshold-engine` drill:

- Pull the two audit results from PostHog (`data_quality_audit_completed` events)
- Compare: is the current average quality score >= 80%?
- Compare: did critical error rate drop by >= 50% from baseline?
- Verdict: PASS or FAIL

If PASS: Data quality is measurable and improvable. Document the rules, the baseline, and the improvement. Proceed to Baseline.
If FAIL: Diagnose — were the rules too strict? Were there not enough fixable errors? Were the 50 records unrepresentative? Adjust rules or sample and re-run.

### 6. Document the ROI Case

Calculate the value of this cleanup:
- Time spent on manual fixes (from Step 3 logs)
- Estimate: how many of the 50 audited records are associated with active deals?
- Estimate: if clean data prevents 1 duplicate outreach or catches 1 stale deal, what is that worth?
- If estimated value exceeds time investment by >= 3x, the ROI case supports continued investment

## Time Estimate

- 1 hour: Define data quality rules and create custom attributes
- 1.5 hours: Run initial audit (agent executes, human reviews output)
- 2 hours: Manual remediation of critical errors
- 0.5 hours: Re-audit and threshold evaluation
- 1 hour: Documentation and ROI calculation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — record storage, quality scores, lists, views | Free (up to 3 users) or $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — audit event tracking, trend comparison | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost this level:** $0 incremental. Attio and PostHog are default stack tools.

## Drills Referenced

- the crm data audit workflow (see instructions below) — audit CRM records against data quality rules, score completeness and accuracy, produce a prioritized remediation report
- `threshold-engine` — evaluate audit results against the pass threshold using PostHog event comparison
