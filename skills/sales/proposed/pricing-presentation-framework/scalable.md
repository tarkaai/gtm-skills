---
name: pricing-presentation-framework-scalable
description: >
  Pricing Presentation Framework — Scalable Automation. Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "58 hours over 2 months"
outcome: "Pricing presented systematically at scale over 2 months with maintained acceptance rates"
kpis: ["Pricing acceptance rate", "Discount optimization", "Tier mix revenue impact", "Deal profitability"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
---
# Pricing Presentation Framework — Scalable Automation

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.

**Time commitment:** 58 hours over 2 months
**Pass threshold:** Pricing presented systematically at scale over 2 months with maintained acceptance rates

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

1. Build n8n workflow generating personalized pricing proposals: pulls discovered value metrics from Attio; creates custom pricing presentation linking price to their specific ROI.

2. Create pricing intelligence: n8n analyzes deal characteristics to recommend optimal tier and pricing structure based on similar won deals.

3. Implement automated proposal generation: n8n creates formatted pricing proposals with value recap, pricing options, ROI summary, next steps.

4. Set up pricing analytics: n8n tracks which pricing approaches drive acceptance, which tiers convert best, which discounts are most effective.

5. Connect PostHog to n8n: when pricing is presented, trigger delivery of supporting materials (ROI calculator, customer case studies, payment options).

6. Build pricing dashboard: track acceptance rates by tier, discount analysis, deal size distribution, conversion velocity after pricing.

7. Create dynamic pricing guidance: n8n recommends pricing tier and structure based on prospect characteristics, competitive situation, deal urgency.

8. Set guardrails: acceptance rate must stay ≥60% of Baseline; average discount must not exceed 12% without strategic justification.

9. Implement pricing experimentation: A/B test different pricing structures, tier positioning, and value anchoring approaches.

10. After 2 months, evaluate pricing framework impact on close rates and deal profitability; if metrics hold, proceed to Durable.

---

## KPIs to track
- Pricing acceptance rate
- Discount optimization
- Tier mix revenue impact
- Deal profitability

---

## Pass threshold
**Pricing presented systematically at scale over 2 months with maintained acceptance rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/pricing-presentation-framework`_
