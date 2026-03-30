---
name: business-case-development-baseline
description: >
  Business Case Development — Baseline Run. Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Business cases developed on ≥80% of enterprise deals over 2 weeks"
kpis: ["Business case completion rate", "Executive approval rate", "Deal size impact", "Win rate with business case"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
---
# Business Case Development — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** Business cases developed on ≥80% of enterprise deals over 2 weeks

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

---

## Instructions

1. Expand business case development to 15-25 opportunities over 2 weeks.

2. Build business case template library: executive summary templates, financial model spreadsheets, implementation timelines, risk matrices by industry and company size.

3. Create ROI calculator integrated into business case: prospect inputs their numbers; auto-generates TCO, ROI, payback period charts.

4. Set up PostHog tracking: business_case_stage, approval_level_reached, objection_encountered, final_outcome.

5. Develop strategic alignment framework: map solution benefits to common corporate initiatives (digital transformation, efficiency, growth, customer experience).

6. Track business case outcomes: measure approval rates, time to executive buy-in, deal size correlation, win rates with vs without business case.

7. Build executive objection library: common CFO/CEO concerns and responses with supporting data.

8. Set pass threshold: Business cases developed on ≥80% of enterprise opportunities over 2 weeks with ≥70% securing approval.

9. Analyze success patterns: which financial metrics executives prioritize, which risk mitigations build confidence, which strategic alignments resonate.

10. If threshold met, document business case playbook and proceed to Scalable; if not, refine template or financial modeling.

---

## KPIs to track
- Business case completion rate
- Executive approval rate
- Deal size impact
- Win rate with business case

---

## Pass threshold
**Business cases developed on ≥80% of enterprise deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/business-case-development`_
