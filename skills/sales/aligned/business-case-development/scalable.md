---
name: business-case-development-scalable
description: >
  Business Case Development — Scalable Automation. Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Business cases automated at scale over 2 months with maintained approval rates"
kpis: ["Automation efficiency", "Executive approval rate", "Time to approval", "Enterprise win rate", "Deal size impact"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Business Case Development — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** Business cases automated at scale over 2 months with maintained approval rates

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

---

## Instructions

1. Build n8n workflow that auto-generates business case templates populated with prospect data from Attio and discovery calls.

2. Create intelligent financial modeling: n8n analyzes prospect's current state costs and generates realistic ROI projections based on similar customer outcomes.

3. Implement automated business case assembly: n8n pulls relevant customer case studies, industry benchmarks, and ROI data; compiles into formatted business case document.

4. Set up approval tracking: n8n monitors business case progress through approval chain; alerts when additional support needed.

5. Connect PostHog to n8n: when business case is shared, track which sections executives view, time spent, questions raised.

6. Build business case intelligence dashboard: track completion rates, approval velocity, win rates, common objections by executive level.

7. Create stakeholder-specific versions: auto-generate CFO-focused (financial), CEO-focused (strategic), CTO-focused (technical) versions from master business case.

8. Set guardrails: business case approval rate must stay ≥65% of Baseline; time to executive approval must not exceed 3 weeks.

9. Implement business case optimization: A/B test different structures, financial presentations, risk mitigation approaches.

10. After 2 months, evaluate business case impact on enterprise close rates; if metrics hold, proceed to Durable.

---

## KPIs to track
- Automation efficiency
- Executive approval rate
- Time to approval
- Enterprise win rate
- Deal size impact

---

## Pass threshold
**Business cases automated at scale over 2 months with maintained approval rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/business-case-development`_
