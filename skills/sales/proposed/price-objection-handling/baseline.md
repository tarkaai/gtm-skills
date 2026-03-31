---
name: price-objection-handling-baseline
description: >
  Price Objection Handling — Baseline Run. Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=60% of price objections overcome with <=14 days to close after resolution over 2 weeks"
kpis: ["Objection overcome rate", "Time to objection resolution", "Close rate (objection vs non-objection deals)", "Asset effectiveness"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Price Objection Handling — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** >=60% of price objections overcome with <=14 days to close after resolution over 2 weeks

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
- **Loom** (Video)

---

## Instructions

1. Expand to 15-20 price objections over 2 weeks; build an objection handling playbook in Attio with 5-7 response frameworks and when to use each based on objection root cause.

2. Create objection diagnostic questions: "Budget: Do you have budget allocated?" "Value: Do you see ROI?" "Alternatives: Are you comparing to other solutions?" "Authority: Is price your only concern or is there something else?"

3. Set pass threshold: overcome >=60% of price objections (prospects move to next stage), and objection-to-close time is <=14 days for overcome objections.

4. Develop objection-specific assets: ROI calculator showing payback period, case studies with quantified value, pricing comparison sheet showing TCO vs competitors, flexible payment term options.

5. When objection arises, send follow-up email within 24 hours with relevant asset: "To address your pricing question, here's a case study showing how [similar company] achieved 5x ROI in 6 months" + ROI calculator pre-filled with their numbers.

6. Sync objection data from Attio to PostHog; create a funnel showing price_objection_received → diagnostic_questions_asked → response_framework_applied → objection_overcome → deal_progressed.

7. Track which objection root causes are most common: if most objections are "no budget allocated," that's a qualification issue (solve in discovery); if "don't see ROI," that's a value communication issue (solve in demo/pain discovery).

8. For objections that don't move forward after initial response, schedule second conversation with economic buyer or champion to address concerns at higher level.

9. After 2 weeks, measure: objection overcome rate, time from objection to resolution, and close rate for deals that had price objections vs deals that didn't.

10. If >=60% of objections overcome and objection deals close within 14 days of resolution, move to Scalable; otherwise refine diagnostic process or response assets.

---

## KPIs to track
- Objection overcome rate
- Time to objection resolution
- Close rate (objection vs non-objection deals)
- Asset effectiveness

---

## Pass threshold
**>=60% of price objections overcome with <=14 days to close after resolution over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/price-objection-handling`_
