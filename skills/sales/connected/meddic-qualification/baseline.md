---
name: meddic-qualification-baseline
description: >
  MEDDIC Qualification System — Baseline Run. Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=60% of deals with >=80% MEDDIC completeness and >=20% faster deal velocity over 2 weeks"
kpis: ["MEDDIC completeness rate", "Deal velocity", "Close rate by MEDDIC score", "Element quality score"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
---
# MEDDIC Qualification System — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.

**Time commitment:** 22 hours over 2 weeks
**Pass threshold:** >=60% of deals with >=80% MEDDIC completeness and >=20% faster deal velocity over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Clay** (Enrichment)
- **Cal.com** (Scheduling)

---

## Instructions

1. Build a MEDDIC framework in Attio with custom fields for each element; create a deal health score (0-100) based on MEDDIC completeness and quality.

2. Develop a discovery call guide for each MEDDIC element with 3-5 questions and red/yellow/green flag criteria (e.g., Pain: red=no quantifiable impact, green=board-level priority).

3. Apply MEDDIC to 10-15 new opportunities over 2 weeks; aim to complete >=80% of elements within the first 2 discovery calls.

4. Set pass threshold: >=60% of deals reach >=80% MEDDIC completeness within 2 weeks, and deal velocity (days from discovery to proposal) is >=20% faster than non-MEDDIC deals.

5. After each discovery call, update all MEDDIC fields in Attio within 24 hours; score each element's quality (1-5) based on specificity and confidence.

6. Sync Attio to PostHog so every MEDDIC update triggers an event; build a funnel showing progression from 0% → 50% → 80% → 100% MEDDIC completion.

7. For deals missing Champion or Economic Buyer, use LinkedIn and Clay to identify potential champions and decision-makers; reach out directly via email or warm intro.

8. Track which MEDDIC elements correlate with deal progression; if Metrics and Champion are strong, deals move faster; if Economic Buyer is unknown, deals stall.

9. After 2 weeks, compare MEDDIC-qualified deals vs non-MEDDIC deals: measure close rate, cycle time, and average deal size.

10. If >=60% of deals reach 80% MEDDIC completeness and deal velocity improves >=20%, document the process and move to Scalable; otherwise refine discovery questions or calling strategy.

---

## KPIs to track
- MEDDIC completeness rate
- Deal velocity
- Close rate by MEDDIC score
- Element quality score

---

## Pass threshold
**>=60% of deals with >=80% MEDDIC completeness and >=20% faster deal velocity over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/meddic-qualification`_
