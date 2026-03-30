---
name: budget-objection-handling-smoke
description: >
  Budget Objection Navigation — Smoke Test. Navigate 'no budget' situations by helping prospects find budget, build compelling business case, or structure creative payment terms that enable purchase within constraints.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Budget objections handled on ≥5 opportunities in 1 week"
kpis: ["Budget objection resolution rate", "Budget found rate", "Payment flexibility acceptance", "Deal progression rate"]
slug: "budget-objection-handling"
install: "npx gtm-skills add sales/proposed/budget-objection-handling"
---
# Budget Objection Navigation — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Navigate 'no budget' situations by helping prospects find budget, build compelling business case, or structure creative payment terms that enable purchase within constraints.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Budget objections handled on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When 5-8 prospects raise budget concerns, diagnose true situation: no budget allocated, budget exhausted, competing priorities, price higher than expected, need CFO approval.

2. Explore budget discovery questions: 'Is budget the only concern?', 'If budget were available, would you move forward?', 'Where does budget typically come from for initiatives like this?'.

3. Help find budget: identify budget sources (department budget, project budget, efficiency savings, IT budget, innovation fund), show cost centers being impacted by current problem.

4. Build business case: calculate ROI showing payback period, demonstrate cost savings that exceed investment, quantify revenue impact, show competitive risk of not acting.

5. Offer payment flexibility: monthly vs annual, phased implementation, pilot program, deferred payment, pay-as-you-grow pricing, creative contract structures.

6. Position as investment not expense: show how solution generates value that exceeds cost, tie to strategic initiatives with executive support, frame as enabler of revenue growth.

7. Track PostHog events: budget_objection_raised, objection_type, budget_source_identified, business_case_delivered, payment_flexibility_offered.

8. Set pass threshold: Handle budget objections on ≥5 opportunities in 1 week with ≥60% finding budget solution or payment structure that enables deal.

9. Measure effectiveness: track budget objection resolution rate, deals saved by creative payment terms, business case conversion rate.

10. Document which budget navigation approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Budget objection resolution rate
- Budget found rate
- Payment flexibility acceptance
- Deal progression rate

---

## Pass threshold
**Budget objections handled on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/budget-objection-handling`_
