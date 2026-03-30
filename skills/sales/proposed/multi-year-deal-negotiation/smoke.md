---
name: multi-year-deal-negotiation-smoke
description: >
  Multi-Year Deal Structuring — Smoke Test. Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: ">=1 multi-year deal closed (2+ years) within 2 weeks"
kpis: ["Multi-year deal rate", "Average contract length", "Total contract value", "Discount accepted"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
---
# Multi-Year Deal Structuring — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.

**Time commitment:** 8 hours over 2 weeks
**Pass threshold:** >=1 multi-year deal closed (2+ years) within 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Define multi-year deal parameters in a spreadsheet: discount structure (e.g., 1-year full price, 2-year 10% discount, 3-year 20% discount), payment terms (annual prepay vs quarterly), expansion clauses (pricing for additional seats/usage), renewal terms.

2. Identify 3-5 opportunities in proposal stage where multi-year deals make sense (strong fit, large company, strategic importance, high expansion potential); prepare multi-year proposals.

3. Set pass threshold: propose multi-year terms to >=3 prospects and close >=1 multi-year deal (2+ years) within 2 weeks.

4. Position multi-year benefits to prospects: "Locking in pricing now protects you from future increases" (hedge against inflation), "Multi-year commitment unlocks priority support and early access to features" (added value), "Predictable annual spend simplifies budgeting" (CFO benefit).

5. Create pricing scenarios for prospects: Option A (1-year at $100K), Option B (2-year at $180K total = 10% savings), Option C (3-year at $240K total = 20% savings); show total savings and annual cost clearly.

6. Address objections: "What if our needs change?" → Include expansion clauses allowing seat/usage increases mid-contract. "What if we want to cancel?" → Offer annual payment terms (less risk than full prepay) or exit clauses after year 1.

7. Log multi-year proposals in Attio with fields for contract_length, total_contract_value, annual_discount, payment_terms, and outcome; track which terms close most often.

8. In PostHog, create events for multiyear_proposed and multiyear_closed with properties for deal length, discount, and TCV.

9. After 2 weeks, analyze: did >=1 multi-year deal close? What objections arose? What terms were most attractive? If multi-year deals close and TCV is >=1.8x annual deal, multi-year motion is working.

10. If threshold met, document multi-year positioning and pricing structure, then proceed to Baseline; otherwise refine discount levels, payment terms, or value positioning.

---

## KPIs to track
- Multi-year deal rate
- Average contract length
- Total contract value
- Discount accepted

---

## Pass threshold
**>=1 multi-year deal closed (2+ years) within 2 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/multi-year-deal-negotiation`_
