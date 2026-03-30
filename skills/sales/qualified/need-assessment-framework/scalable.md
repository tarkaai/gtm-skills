---
name: need-assessment-framework-scalable
description: >
  Need Assessment Framework — Scalable Automation. Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: "Need assessment completed on ≥70% of opportunities at scale over 2 months with improved close rate prediction"
kpis: ["Need assessment completion rate", "Need score accuracy", "Sales cycle reduction", "Win rate by need tier", "Pipeline quality score"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
---
# Need Assessment Framework — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.

**Time commitment:** 55 hours over 2 months
**Pass threshold:** Need assessment completed on ≥70% of opportunities at scale over 2 months with improved close rate prediction

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

1. Build n8n workflow that prompts sales reps to complete need assessment immediately after first discovery call; auto-calculates need score and assigns tier.

2. Create pre-call need hypothesis: n8n analyzes prospect data (industry, company size, tech stack, job postings, LinkedIn signals) and predicts likely need profile before first call.

3. Implement automated need-based routing: high-need (A-tier) opportunities get priority follow-up within 24 hours; low-need (C-tier) get automated nurture sequence or disqualification.

4. Set up need-triggered content delivery: n8n automatically sends need-specific case studies, ROI calculators, and product materials based on identified need areas.

5. Connect PostHog to n8n: when need assessment is incomplete after 48 hours, trigger reminder with pre-populated need hypothesis and suggested questions.

6. Build need intelligence dashboard: track need distribution across pipeline, need-to-close correlation, need pattern trends over time, rep performance on need assessment.

7. Implement A/B testing on need questions: test different question phrasings and sequences to improve assessment accuracy and prospect engagement.

8. Set guardrails: need assessment completion rate must stay ≥70% of Baseline level; predictive accuracy must remain within 20% of close rate correlation.

9. Create need-based forecasting: use need scores as leading indicator for pipeline quality and revenue prediction.

10. After 2 months, evaluate need assessment impact on qualification accuracy and sales efficiency; if metrics hold, proceed to Durable AI-driven need intelligence.

---

## KPIs to track
- Need assessment completion rate
- Need score accuracy
- Sales cycle reduction
- Win rate by need tier
- Pipeline quality score

---

## Pass threshold
**Need assessment completed on ≥70% of opportunities at scale over 2 months with improved close rate prediction**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/need-assessment-framework`_
