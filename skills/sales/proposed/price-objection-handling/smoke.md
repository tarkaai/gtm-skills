---
name: price-objection-handling-smoke
description: >
  Price Objection Handling — Smoke Test. Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Overcome >=3 out of 5 price objections within 1 week"
kpis: ["Objection overcome rate", "Response framework effectiveness", "Time to overcome objection"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - icp-definition
  - threshold-engine
---
# Price Objection Handling — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Overcome >=3 out of 5 price objections within 1 week

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

1. Document 5 recent price objections in a spreadsheet with columns: Objection Statement, Prospect Context (budget, company size), Your Response, Outcome; identify patterns in why prospects push back on price.

2. Create 3-5 price objection response frameworks: Value Reframe ("$20K seems high, but you're losing $100K/year—this pays for itself in 10 weeks"), ROI Proof (share case study with similar savings), Payment Flexibility (offer quarterly vs annual), Discount Logic (volume discount, multi-year discount).

3. Set pass threshold: successfully overcome >=3 out of 5 price objections (prospects move forward after objection) within 1 week.

4. When prospects say "too expensive," diagnose root cause with questions: "Compared to what?" "What budget did you have in mind?" "What's the cost of not solving this problem?" "How are you measuring value?"

5. Use pain quantification from discovery to reframe price: "You're spending $100K/year on this problem. Our $20K solution saves you $80K annually—would you spend 20 cents to save a dollar?"

6. Log objection handling attempts in Attio with fields for objection_type, response_framework, and outcome (moved forward, still negotiating, lost); track success rate per framework.

7. In PostHog, create events for price_objection_received and price_objection_handled with properties for response type and outcome.

8. For objections you can't overcome, identify why: insufficient pain quantification? champion not strong? no budget allocated? missing economic buyer? Document root causes.

9. After 1 week, analyze which response frameworks work best; if >=3 out of 5 objections are overcome, you have a repeatable process.

10. If threshold met, document winning objection responses and proceed to Baseline; if not, refine value messaging or improve discovery quality to prevent weak objections.

---

## KPIs to track
- Objection overcome rate
- Response framework effectiveness
- Time to overcome objection

---

## Pass threshold
**Overcome >=3 out of 5 price objections within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/price-objection-handling`_
