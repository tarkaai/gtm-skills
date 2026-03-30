---
name: pricing-presentation-framework-durable
description: >
  Pricing Presentation Framework — Durable Intelligence. Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "145 hours over 6 months"
outcome: "Sustained or improving pricing acceptance and deal profitability over 6 months via AI-driven pricing intelligence"
kpis: ["Pricing acceptance rate", "Deal profitability optimization", "Discount intelligence effectiveness", "Revenue per deal", "Win rate improvement"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
---
# Pricing Presentation Framework — Durable Intelligence

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.

**Time commitment:** 145 hours over 6 months
**Pass threshold:** Sustained or improving pricing acceptance and deal profitability over 6 months via AI-driven pricing intelligence

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$100–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)

---

## Instructions

1. Deploy PostHog streams triggering n8n AI agents when: pricing conversation approaches, discount request detected, or pricing negotiation begins.

2. Build n8n AI pricing intelligence agent analyzing won/lost deals: identifies optimal pricing tiers by segment, effective value anchoring techniques, discount patterns that close vs erode margins.

3. Implement AI-powered pricing optimization: AI generates personalized pricing recommendations based on prospect value drivers, competitive situation, and historical deal patterns.

4. Create learning loop: PostHog tracks pricing presentation approaches and correlates with acceptance rates and deal profitability; AI refines recommendations.

5. Build adaptive value anchoring: AI identifies most compelling value metrics for each prospect based on discovered pain points and similar customer outcomes.

6. Deploy intelligent discount guidance: AI recommends optimal discount levels and structures that close deals while protecting margins based on deal characteristics.

7. Implement dynamic pricing intelligence: AI monitors market conditions, competitive pricing, and customer willingness to pay; suggests pricing adjustments.

8. Create predictive pricing analytics: AI predicts acceptance probability and discount sensitivity for each deal; helps reps optimize pricing approach.

9. Set guardrails: if acceptance rate drops >15% or profitability declines, alert team and suggest pricing refinements.

10. Establish monthly review: analyze pricing effectiveness, tier optimization, discount intelligence; refine AI agent based on profitability data.

---

## KPIs to track
- Pricing acceptance rate
- Deal profitability optimization
- Discount intelligence effectiveness
- Revenue per deal
- Win rate improvement

---

## Pass threshold
**Sustained or improving pricing acceptance and deal profitability over 6 months via AI-driven pricing intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/pricing-presentation-framework`_
