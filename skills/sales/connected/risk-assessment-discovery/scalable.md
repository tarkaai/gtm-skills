---
name: risk-assessment-discovery-scalable
description: >
  Risk & Concern Discovery — Scalable Automation. Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "57 hours over 2 months"
outcome: "Risks discovered and mitigated on ≥75% of opportunities at scale over 2 months with reduced late-stage surprises"
kpis: ["Risk discovery rate", "Early risk identification", "Mitigation success rate", "Close rate improvement", "Deal predictability score"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
---
# Risk & Concern Discovery — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Surface concerns, risks, and objections early in the sales cycle to address them proactively rather than encountering surprises at decision time.

**Time commitment:** 57 hours over 2 months
**Pass threshold:** Risks discovered and mitigated on ≥75% of opportunities at scale over 2 months with reduced late-stage surprises

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

1. Build n8n workflow that triggers risk discovery checklist after every discovery call; prompts rep to assess all five risk categories.

2. Create risk intelligence layer: n8n analyzes similar past deals to predict likely risks for each prospect based on industry, size, and use case.

3. Implement automated risk mitigation content delivery: when specific risk is identified, n8n automatically sends relevant case studies, ROI proof, security docs, or testimonials.

4. Set up risk monitoring: n8n tracks deal notes and emails for risk language; alerts when new concerns emerge or existing risks escalate.

5. Connect PostHog to n8n: when high-severity risk is logged, trigger immediate notification to sales leadership and suggest mitigation resources.

6. Build risk intelligence dashboard: track risk frequency by category, mitigation success rates, correlation with deal outcomes, time-to-resolution.

7. Create risk mitigation library: centralized repository of proof points, case studies, guarantees, and commitments organized by risk type.

8. Set guardrails: risk discovery rate must stay ≥75% of Baseline level; late-stage surprises must be <10% of deals.

9. Implement proactive risk planning: flag common risks for specific ICPs and prepare mitigation materials in advance.

10. After 2 months, evaluate risk discovery impact on close rates and deal predictability; if metrics hold, proceed to Durable AI-driven risk intelligence.

---

## KPIs to track
- Risk discovery rate
- Early risk identification
- Mitigation success rate
- Close rate improvement
- Deal predictability score

---

## Pass threshold
**Risks discovered and mitigated on ≥75% of opportunities at scale over 2 months with reduced late-stage surprises**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/risk-assessment-discovery`_
