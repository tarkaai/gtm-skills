---
name: meddic-qualification-scalable
description: >
  MEDDIC Qualification System — Scalable Automation. Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=50% of deals with >80% MEDDIC completeness and >=15% higher close rate over 2 months"
kpis: ["MEDDIC completeness rate", "Deal health score", "Close rate by MEDDIC quartile", "Velocity by MEDDIC score"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
---
# MEDDIC Qualification System — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=50% of deals with >80% MEDDIC completeness and >=15% higher close rate over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale MEDDIC to 50-100 deals per quarter; integrate Clay with Attio to auto-populate Metrics, Economic Buyer, and Decision Criteria based on company research and job titles.

2. Build an n8n workflow that triggers when a new opportunity is created in Attio: pull org chart from LinkedIn/Clay, identify likely Economic Buyer and Champion candidates, pre-fill MEDDIC fields.

3. Create MEDDIC scorecards in Attio that auto-calculate deal health based on completeness (50%) and quality (50%); flag deals with health <60% for immediate intervention.

4. Set up PostHog to track MEDDIC completeness over time; create alerts when a deal has been open >7 days with <50% MEDDIC completion.

5. In n8n, build a workflow that sends automated reminders to sales reps when MEDDIC elements are missing: "No Champion identified in Deal X—schedule call to find internal advocate."

6. Integrate call recording tools (Fireflies, Gong) with Attio; use AI to extract MEDDIC elements from call transcripts and auto-populate Attio fields with confidence scores.

7. Build a MEDDIC dashboard in PostHog showing distribution of deal health scores, average MEDDIC completeness by stage, and correlation between MEDDIC score and close rate.

8. Each week, analyze which MEDDIC elements are most often missing; if Decision Process is weak across deals, run a team training on how to uncover buying process.

9. Track deal velocity by MEDDIC completeness quartile: deals with >90% MEDDIC should close 30%+ faster than deals with <70% MEDDIC.

10. After 2 months, if >=50% of deals maintain >80% MEDDIC completeness and close rates improve >=15%, move to Durable; otherwise refine automation or rep coaching.

---

## KPIs to track
- MEDDIC completeness rate
- Deal health score
- Close rate by MEDDIC quartile
- Velocity by MEDDIC score

---

## Pass threshold
**>=50% of deals with >80% MEDDIC completeness and >=15% higher close rate over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/meddic-qualification`_
