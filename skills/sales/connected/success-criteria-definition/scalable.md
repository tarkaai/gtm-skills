---
name: success-criteria-definition-scalable
description: >
  Success Criteria Definition — Scalable Automation. Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "56 hours over 2 months"
outcome: "Success criteria defined on ≥75% of opportunities at scale over 2 months with improved close rates"
kpis: ["Success criteria definition rate", "Close rate improvement", "Post-sale achievement rate", "Customer satisfaction correlation", "Deal velocity with defined criteria"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
---
# Success Criteria Definition — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.

**Time commitment:** 56 hours over 2 months
**Pass threshold:** Success criteria defined on ≥75% of opportunities at scale over 2 months with improved close rates

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

1. Build n8n workflow that triggers success criteria definition prompt after discovery phase; provides templates and guidance to sales reps.

2. Create success criteria intelligence: n8n analyzes similar won deals to suggest likely success criteria for each prospect based on industry, use case, and company size.

3. Implement automated mutual success plan generation: n8n creates formatted success plan document from Attio data; auto-sends to prospect for review and agreement.

4. Set up success criteria matching: n8n compares defined success criteria against product capabilities and historical achievement rates; flags unrealistic expectations.

5. Connect PostHog to n8n: when success criteria are defined, trigger delivery of relevant case studies showing similar customers achieving those specific outcomes.

6. Build success criteria dashboard: track definition rates, criteria types, achievability scores, correlation with close rates and customer success outcomes.

7. Create success criteria library: maintain repository of common success criteria by vertical and use case with typical achievement timelines and measurement methods.

8. Set guardrails: success criteria definition rate must stay ≥75% of Baseline level; deals with defined criteria must close at ≥15% higher rate than those without.

9. Implement post-sale success tracking: pass success criteria to customer success team; measure actual achievement rates to validate sales promises.

10. After 2 months, evaluate success criteria impact on close rates and customer outcomes; if metrics hold, proceed to Durable AI-driven success intelligence.

---

## KPIs to track
- Success criteria definition rate
- Close rate improvement
- Post-sale achievement rate
- Customer satisfaction correlation
- Deal velocity with defined criteria

---

## Pass threshold
**Success criteria defined on ≥75% of opportunities at scale over 2 months with improved close rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/success-criteria-definition`_
