---
name: budget-objection-handling-baseline
description: >
  Budget Objection Navigation — Baseline Run. Navigate 'no budget' situations by helping prospects find budget, build compelling business case, or structure creative payment terms that enable purchase within constraints.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Budget objections handled on ≥80% of instances over 2 weeks"
kpis: ["Objection resolution rate", "Budget found rate", "Business case win rate", "Payment flexibility effectiveness", "Deal size preservation"]
slug: "budget-objection-handling"
install: "npx gtm-skills add sales/proposed/budget-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Budget Objection Navigation — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Navigate 'no budget' situations by helping prospects find budget, build compelling business case, or structure creative payment terms that enable purchase within constraints.

**Time commitment:** 15 hours over 2 weeks
**Pass threshold:** Budget objections handled on ≥80% of instances over 2 weeks

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

1. Expand budget objection handling to 20-30 instances over 2 weeks.

2. Build budget navigation framework: diagnostic questions, budget source menu, business case templates, payment options catalog, ROI calculators by use case.

3. Create budget source guide: common budget pools by company size and type (departmental, project-based, efficiency, IT, innovation), typical approval processes, timing considerations.

4. Set up PostHog event tracking: budget_objection_type, true_vs_price_objection, budget_source_explored, roi_presented, payment_terms_offered, objection_resolution.

5. Develop ROI template library: industry-specific ROI models, cost savings calculators, revenue impact models, efficiency gain quantifiers, competitive risk assessments.

6. Track budget objection outcomes: measure resolution rates by objection type, deals saved by payment flexibility, business case win rates, average discount given.

7. Build payment flexibility playbook: standard payment terms, creative structures, volume discounts, multi-year incentives, pilot programs, approval required for each.

8. Set pass threshold: Budget objections addressed on ≥80% of instances over 2 weeks with ≥60% finding budget solution or accepting payment terms.

9. Analyze budget patterns: which objections are real vs negotiation tactics, which payment structures work best, which budget sources close fastest.

10. If threshold met, document budget objection playbook and proceed to Scalable; if not, refine business case or payment options.

---

## KPIs to track
- Objection resolution rate
- Budget found rate
- Business case win rate
- Payment flexibility effectiveness
- Deal size preservation

---

## Pass threshold
**Budget objections handled on ≥80% of instances over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/budget-objection-handling`_
