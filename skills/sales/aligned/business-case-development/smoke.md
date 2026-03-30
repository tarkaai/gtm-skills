---
name: business-case-development-smoke
description: >
  Business Case Development — Smoke Test. Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Business cases created for ≥5 opportunities in 1 week"
kpis: ["Business case completion rate", "Executive approval rate", "Time to approval", "Deal progression"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
---
# Business Case Development — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** Business cases created for ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When 5-8 prospects need internal approval, offer to co-create business case: 'Let me help you build the case for your leadership team'.

2. Structure business case with key sections: Executive Summary (one-page overview), Problem Statement (current pain and cost), Proposed Solution (how you solve it), Financial Analysis (ROI and payback), Implementation Plan (timeline and resources), Risk Mitigation (how you de-risk), Strategic Alignment (how it supports company goals).

3. Quantify current state costs: inefficiencies, manual work, lost opportunities, error rates, customer churn; calculate total annual impact.

4. Model future state benefits: time savings, cost reductions, revenue increases, quality improvements; show year 1, 2, 3 projections.

5. Calculate financial metrics: Total Cost of Ownership (TCO), Return on Investment (ROI), Payback Period, Net Present Value (NPV) if applicable.

6. Address executive concerns: include competitive risks of not acting, alignment with strategic initiatives, change management plan, measurement framework.

7. Track PostHog events: business_case_initiated, section_completed, financial_model_created, executive_review_scheduled.

8. Set pass threshold: Co-create business cases for ≥5 opportunities in 1 week with ≥60% securing executive approval.

9. Measure effectiveness: track business case win rates, time to approval, deal size impact.

10. Document which business case elements drive approvals; proceed to Baseline if threshold met.

---

## KPIs to track
- Business case completion rate
- Executive approval rate
- Time to approval
- Deal progression

---

## Pass threshold
**Business cases created for ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/business-case-development`_
