---
name: crm-hygiene-data-management-durable
description: >
  CRM Hygiene & Data Quality — Durable Intelligence. Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product"
level: "Durable Intelligence"
time: "110 hours over 6 months"
outcome: "Sustained or improving data quality (>=90%) over 6 months via continuous agent-driven quality monitoring, error prevention, and automated correction"
kpis: ["Data quality score trend", "Error prevention rate", "Agent correction accuracy", "Manual intervention rate"]
slug: "crm-hygiene-data-management"
install: "npx gtm-skills add sales/qualified/crm-hygiene-data-management"
---
# CRM Hygiene & Data Quality — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product

## Overview
Maintain clean, accurate CRM data to enable reliable forecasting, reporting, and sales execution, from manual data cleanup to AI-driven automated data quality that detects and fixes errors in real-time and prevents data degradation.

**Time commitment:** 110 hours over 6 months
**Pass threshold:** Sustained or improving data quality (>=90%) over 6 months via continuous agent-driven quality monitoring, error prevention, and automated correction

---

## Budget

**Play-specific tools & costs**
- **Intercom or Loops (agent-driven messaging):** ~$150–400/mo

_Total play-specific: ~$150–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously monitors CRM data patterns to detect data quality issues before they become problems; learns from corrections to prevent future errors.

2. Set up the agent to identify anomalies: unusual data patterns (e.g., deals progressing too fast, missing stakeholders in large deals, duplicates with subtle differences); flag for review.

3. Build a feedback loop where every manual data correction triggers the agent to analyze root cause; if enrichment source is providing bad data, switch providers; if validation rule is too loose, tighten it.

4. Deploy AI-driven duplicate detection: agent uses fuzzy matching, semantic analysis, and behavioral patterns to identify duplicates that rule-based systems miss; learns from merge decisions to improve accuracy.

5. Implement predictive data quality: agent predicts which records will become stale or inaccurate based on historical patterns; prompts proactive updates before data degrades.

6. Build automatic data correction: agent detects common errors (typos in company names, outdated job titles, incorrect stages) and auto-corrects based on learned patterns; logs corrections for audit.

7. Create market adaptation logic: if data quality degrades during high-growth periods (more reps, more volume), agent suggests process adjustments or additional automation to maintain quality.

8. Agent continuously refines enrichment strategies: tests different data sources, learns which provide highest accuracy for different record types, automatically routes enrichment to best source.

9. Implement dynamic validation rules: agent experiments with different validation strictness levels and measures impact on data quality vs rep friction; optimizes for balance.

10. Establish monthly review cycles: agent generates data quality intelligence reports showing quality trends, automation effectiveness, error prevention rate, and recommended process updates; team reviews and approves changes.

---

## KPIs to track
- Data quality score trend
- Error prevention rate
- Agent correction accuracy
- Manual intervention rate

---

## Pass threshold
**Sustained or improving data quality (>=90%) over 6 months via continuous agent-driven quality monitoring, error prevention, and automated correction**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/crm-hygiene-data-management`_
