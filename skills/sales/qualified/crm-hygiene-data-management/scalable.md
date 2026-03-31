---
name: crm-hygiene-data-management-scalable
description: >
  CRM Hygiene & Data Quality — Scalable Automation. Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=90% data quality score and >=70% reduction in manual cleanup time over 2 months"
kpis: ["Data quality score", "Automation coverage", "Manual cleanup time reduction", "Enrichment success rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# CRM Hygiene & Data Quality — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product

## Overview
Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** >=90% data quality score and >=70% reduction in manual cleanup time over 2 months

---

## Budget

**Play-specific tools & costs**
- **Intercom or Loops (automated sequences):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)

---

## Instructions

1. Scale data quality to 500+ active records; build n8n workflows that automatically detect and fix common data quality issues: missing fields (auto-enrich via Clay), duplicates (auto-merge based on rules), stale data (auto-alert owner).

2. Implement real-time data validation in Attio: when rep enters/updates record, validate against quality rules; block save if critical fields are missing or invalid; prompt for correction immediately.

3. Set up PostHog to track data quality metrics in real-time: monitor quality score, error rates, enrichment success rate, duplicate detection rate; alert when metrics degrade.

4. Build automated duplicate prevention: when new record is created, n8n workflow searches Attio for matches; if potential duplicate found, sends alert to rep with merge recommendation before allowing creation.

5. Create auto-enrichment workflows in n8n: when new contact/company is added, trigger Clay enrichment to fill missing fields (revenue, employee count, tech stack, funding); update Attio automatically.

6. Implement stale data management: n8n workflow identifies records with no activity >30 days; sends re-engagement prompts to owners or auto-archives if no response after 60 days.

7. Build data quality scoring engine: assign scores to each record based on completeness (40%), recency (30%), accuracy (20%), and activity (10%); surface low-scoring records for cleanup.

8. Create automated data quality reports: weekly summary showing quality trends, top issues, rep compliance, records needing attention; auto-distribute to sales leadership.

9. Each week, measure data quality impact on sales metrics: do deals with higher data quality close faster? forecast more accurately? Use findings to justify continued investment in data hygiene.

10. After 2 months, if data quality score >=90%, duplicate rate <2%, and automation reduces manual cleanup time by >=70%, move to Durable; otherwise refine workflows or validation rules.

---

## KPIs to track
- Data quality score
- Automation coverage
- Manual cleanup time reduction
- Enrichment success rate

---

## Pass threshold
**>=90% data quality score and >=70% reduction in manual cleanup time over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/crm-hygiene-data-management`_
