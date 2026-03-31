---
name: crm-hygiene-data-management-smoke
description: >
  CRM Hygiene & Data Quality — Smoke Test. Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=80% data quality score and >=50% reduction in critical errors within 1 week"
kpis: ["Data quality score", "Critical error rate", "Duplicate rate", "Stale record rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
drills:
  - icp-definition
  - threshold-engine
---
# CRM Hygiene & Data Quality — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product

## Overview
Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** >=80% data quality score and >=50% reduction in critical errors within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Define 5-7 critical data quality rules in a spreadsheet: required fields (contact name, email, company, stage), valid values (stage must be in defined list), no duplicates, recent activity (last touch <=30 days), complete BANT/MEDDIC for qualified deals.

2. Audit 50 records in Attio manually; for each, check compliance with data quality rules; calculate data quality score (% of rules passed) and identify most common errors (missing fields, stale data, duplicates).

3. Set pass threshold: achieve >=80% data quality score across audited records and reduce critical errors (missing required fields, duplicates) by >=50% within 1 week.

4. Fix identified errors manually: fill missing fields, merge duplicates, update stale records, correct invalid stage values; document time spent on cleanup.

5. Create data entry guidelines for sales team: "Required fields before advancing stage", "Update contact info after every call", "Log all activities in Attio within 24 hours", "Merge duplicates immediately when found".

6. Log data quality issues in a spreadsheet with columns: issue_type, frequency, impact (high/medium/low), owner, resolution; prioritize fixing high-impact issues.

7. In PostHog, create events for data_quality_issue_detected and data_quality_issue_resolved with properties for issue type and resolution time.

8. After cleanup, audit same 50 records again; measure improvement in data quality score; if >=80% score achieved, cleanup was effective.

9. Calculate ROI of data quality: estimate time saved on reporting, reduced duplicate outreach, improved forecasting accuracy; if benefits exceed cleanup time by >=3x, data hygiene is valuable.

10. If >=80% data quality achieved and ROI is positive, document data quality standards and proceed to Baseline; otherwise refine rules or improve enforcement.

---

## KPIs to track
- Data quality score
- Critical error rate
- Duplicate rate
- Stale record rate

---

## Pass threshold
**>=80% data quality score and >=50% reduction in critical errors within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/crm-hygiene-data-management`_
