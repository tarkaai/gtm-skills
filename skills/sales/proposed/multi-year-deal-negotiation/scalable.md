---
name: multi-year-deal-negotiation-scalable
description: >
  Multi-Year Deal Structuring — Scalable Automation. Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=35% close rate on multi-year proposals and LTV for multi-year customers >=2.5x annual customers over 2 months"
kpis: ["Multi-year close rate", "Average contract length", "LTV (multi-year vs annual)", "Discount optimization"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Multi-Year Deal Structuring — Scalable Automation

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.

**Time commitment:** 75 hours over 2 months
**Pass threshold:** >=35% close rate on multi-year proposals and LTV for multi-year customers >=2.5x annual customers over 2 months

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

1. Scale multi-year proposals to 50+ opportunities per quarter; build n8n workflows that auto-generate multi-year pricing scenarios when opportunities reach proposal stage: calculate discount tiers, payment options, and TCV based on deal characteristics.

2. Integrate multi-year contract logic with Attio: when rep marks opportunity as "ready for proposal," n8n calculates optimal contract length and discount based on customer profile (industry, size, strategic value, expansion potential).

3. Set up PostHog to track multi-year deal metrics: proposal rate by segment, close rate by contract length, average discount, TCV, and customer lifetime value (LTV) for multi-year vs annual deals.

4. Create tiered discount structures: Standard (10% for 2-yr, 15% for 3-yr), Strategic (15% for 2-yr, 25% for 3-yr for high-value accounts); auto-recommend tier based on opportunity value and strategic fit.

5. Build automated multi-year renewal workflows: 90 days before contract end, trigger renewal conversation with CSM; offer multi-year renewal with expansion incentives; track renewal rate for multi-year vs annual customers.

6. Implement multi-year forecasting: use contract length and payment terms to model cash flow and revenue recognition; track bookings (TCV) separately from recognized revenue.

7. Create multi-year sales training: equip reps with positioning, objection handling, and negotiation tactics for long-term deals; use role-play and successful deal examples.

8. Each quarter, analyze multi-year deal performance: which segments close most multi-year deals? what discount levels optimize for TCV without leaving money on table? what contract lengths balance revenue and customer commitment?

9. Test multi-year deal incentives: SPIFs for reps who close 3-year deals, accelerated commissions for prepaid multi-year contracts; measure impact on multi-year adoption.

10. After 2 months, if >=40% of opportunities result in multi-year proposals, >=35% of those close, and LTV for multi-year customers is >=2.5x annual customers, move to Durable; otherwise refine pricing or incentives.

---

## KPIs to track
- Multi-year close rate
- Average contract length
- LTV (multi-year vs annual)
- Discount optimization

---

## Pass threshold
**>=35% close rate on multi-year proposals and LTV for multi-year customers >=2.5x annual customers over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/multi-year-deal-negotiation`_
