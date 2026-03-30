---
name: roi-calculator-scalable
description: >
  ROI Calculator & Business Case — Scalable Automation. Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Scalable Automation"
time: "80 hours over 2 months"
outcome: ">=70% of prospects with >=5x ROI and >=60% calculator completion rate over 2 months"
kpis: ["ROI distribution", "Calculator completion rate", "ROI prediction accuracy", "Self-service calculator conversion"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
---
# ROI Calculator & Business Case — Scalable Automation

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Overview
Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.

**Time commitment:** 80 hours over 2 months
**Pass threshold:** >=70% of prospects with >=5x ROI and >=60% calculator completion rate over 2 months

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
- **OpenAI** (AI/LLM)

---

## Instructions

1. Scale ROI calculators to 50+ prospects per quarter; build an interactive web-based ROI calculator that prospects can use self-service; capture inputs in PostHog and sync to Attio.

2. Integrate calculator with Attio and PostHog: when prospect completes calculator, auto-create opportunity with ROI data, trigger sales alert if ROI >=5x, send personalized follow-up email.

3. Build an n8n workflow that pulls discovery data from Attio and auto-generates draft ROI calculator inputs; reps validate/adjust and send calculator to prospect.

4. Set up PostHog to track calculator engagement: completion rate, time spent, inputs adjusted by prospect, ROI tier achieved; use engagement data to score lead intent.

5. Create AI-generated business cases: use Claude or GPT-4 to auto-generate business case documents based on ROI calculator outputs, prospect industry, and pain points from discovery; reps review and personalize.

6. Embed ROI calculator on website and in email sequences; for inbound leads with high ROI (>=7x), fast-track to sales call; for low ROI (<3x), route to nurture or disqualify.

7. Build industry-specific benchmarks: "Companies like yours typically save 30-40% on [cost category]—you're projecting 35%, which aligns with peers"; use benchmarks to validate and strengthen ROI credibility.

8. Track ROI prediction accuracy: for closed customers, compare actual realized ROI (from onboarding/CSM data) vs projected ROI; adjust calculator assumptions if consistently over/under-projecting.

9. Each week, analyze which value drivers contribute most to strong ROI; prioritize uncovering those drivers in discovery (e.g., if time savings dominates, focus discovery questions on current time spent).

10. After 2 months, if >=70% of deals have >=5x ROI and calculator completion rate >=60%, move to Durable; otherwise refine calculator UX or discovery integration.

---

## KPIs to track
- ROI distribution
- Calculator completion rate
- ROI prediction accuracy
- Self-service calculator conversion

---

## Pass threshold
**>=70% of prospects with >=5x ROI and >=60% calculator completion rate over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/roi-calculator`_
