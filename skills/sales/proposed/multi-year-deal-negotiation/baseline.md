---
name: multi-year-deal-negotiation-baseline
description: >
  Multi-Year Deal Structuring — Baseline Run. Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=30% close rate on multi-year proposals and average TCV >=2x annual deal value over 2 weeks"
kpis: ["Multi-year proposal rate", "Multi-year close rate", "Average contract length", "TCV vs annual ACV"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
---
# Multi-Year Deal Structuring — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.

**Time commitment:** 22 hours over 2 weeks
**Pass threshold:** >=30% close rate on multi-year proposals and average TCV >=2x annual deal value over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Expand multi-year proposals to 15-20 opportunities over 2 weeks; build standardized multi-year contract templates with clear terms for pricing, payment, expansion, renewal, and exit clauses.

2. Create buyer-persona-specific multi-year positioning: CFO (budget certainty, cost savings), Procurement (simplified vendor management), CTO (stable roadmap, priority support), CEO (strategic partnership).

3. Set pass threshold: propose multi-year terms to >=60% of qualified opportunities, close >=30% of multi-year proposals, and average TCV is >=2x annual deal value.

4. Introduce multi-year options early in sales cycle (post-demo): "Most customers choose 2-3 year agreements to lock in pricing and get priority support—let's explore what makes sense for you."

5. Build multi-year ROI calculators showing cumulative value over contract term: "Year 1 saves $X, Year 2 saves $Y, Year 3 saves $Z—total 3-year savings of $XYZ vs your current solution."

6. Offer payment flexibility: annual prepay (best discount), quarterly payments (lower risk), or hybrid (50% upfront, remainder over contract); remove payment risk as objection.

7. Sync multi-year deal data from Attio to PostHog; create dashboards showing multi-year proposal rate, close rate by contract length, average discount, and TCV by length.

8. Track multi-year deal outcomes: retention (do multi-year customers renew at higher rates?), expansion (do they expand mid-contract?), satisfaction (are they happier with long-term partnership?).

9. After 2 weeks, measure multi-year performance: proposal rate, close rate, TCV, discount levels; if >=30% of multi-year proposals close and TCV >=2x annual, motion is working.

10. If thresholds met and multi-year deals show strong metrics, move to Scalable; otherwise refine pricing, payment terms, or positioning.

---

## KPIs to track
- Multi-year proposal rate
- Multi-year close rate
- Average contract length
- TCV vs annual ACV

---

## Pass threshold
**>=30% close rate on multi-year proposals and average TCV >=2x annual deal value over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/multi-year-deal-negotiation`_
