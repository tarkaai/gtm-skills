---
name: crm-hygiene-data-management-baseline
description: >
  CRM Hygiene & Data Quality — Baseline Run. Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=85% data quality score and <3% duplicate rate over 2 weeks"
kpis: ["Data quality score", "Duplicate rate", "Stale record rate", "Compliance rate by rep"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
---
# CRM Hygiene & Data Quality — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product

## Overview
Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** >=85% data quality score and <3% duplicate rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Intercom or Loops (in-app/email triggers):** ~$75–150/mo

_Total play-specific: ~$75–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Clay** (Enrichment)

---

## Instructions

1. Expand data quality program to all active opportunities (100-200 records); create automated data quality reports in Attio showing compliance with quality rules by rep, stage, and record type.

2. Implement data quality checkpoints in sales process: require specific fields before advancing opportunity stages (e.g., can't move to Proposal stage without Economic Buyer identified and BANT complete).

3. Set pass threshold: maintain >=85% data quality score across all records, reduce duplicate rate to <3%, and keep stale record rate (no activity >30 days) <15% over 2 weeks.

4. Build data quality dashboards in Attio showing: quality score trends, top issues by type, compliance by rep, records needing attention; review weekly with sales team.

5. Sync data quality metrics from Attio to PostHog; create alerts when quality drops below thresholds (e.g., quality score <80% for 3 consecutive days triggers alert to manager).

6. Schedule weekly data quality audits: randomly sample 20 records, check compliance, log issues, assign cleanup tasks to record owners; track resolution time.

7. Implement duplicate detection workflow: when new contact/company is created, scan Attio for similar records (matching email, name, domain); flag potential duplicates for review before creation.

8. Create data enrichment process: integrate Clay with Attio to auto-fill missing fields (company size, industry, title) when records are created or updated; reduce manual data entry.

9. After 2 weeks, measure: Is data quality score >=85%? Are duplicates <3%? Are reps entering data consistently? If yes, data hygiene processes are working.

10. If quality thresholds met and compliance is consistent, move to Scalable; otherwise strengthen checkpoints, improve rep training, or add automation.

---

## KPIs to track
- Data quality score
- Duplicate rate
- Stale record rate
- Compliance rate by rep

---

## Pass threshold
**>=85% data quality score and <3% duplicate rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/crm-hygiene-data-management`_
