---
name: price-objection-handling-scalable
description: >
  Price Objection Handling — Scalable Automation. Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=65% of price objections overcome with <=10 days to close after resolution over 2 months"
kpis: ["Objection overcome rate", "Objection resolution time", "Objection prevention rate", "Discount rate by objection type"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Price Objection Handling — Scalable Automation

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=65% of price objections overcome with <=10 days to close after resolution over 2 months

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
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale to 50+ price objections per quarter; integrate call recording tools with Attio to auto-detect price objections in sales calls and trigger objection handling workflows.

2. Build an n8n workflow that triggers when price objection is detected: analyze objection context (deal size, pain quantification, competitor evaluation), recommend response framework, send relevant assets to rep, log in Attio.

3. Create dynamic pricing options in Attio: based on deal characteristics, auto-generate 3 pricing scenarios (annual upfront, quarterly payments, multi-year discount) for reps to present during objection conversations.

4. Set up PostHog to track objection patterns: which deal sizes trigger most objections? which industries? which pain types? Use patterns to improve pricing positioning or adjust qualification.

5. Build an objection asset library in n8n: ROI calculators, case studies, TCO comparisons, payment options; auto-recommend which assets to send based on objection type and prospect profile.

6. Implement objection prevention: if PostHog shows deals with weak pain quantification (<5x pricing) face 3x more price objections, require stronger discovery before progressing to proposal stage.

7. Create objection handling training program: use best rep recordings, successful objection call examples, and response framework documentation; onboard new reps on objection handling.

8. Track objection impact on deal metrics in PostHog: measure deal velocity, close rate, and discount rate for deals with vs without price objections; target <20% impact on close rate.

9. Each week, analyze which response frameworks win most often; update playbook to lead with highest-success approaches; retire low-success frameworks.

10. After 2 months, if >=65% of objections overcome and objection deals close within 10 days of resolution, move to Durable; otherwise refine detection or response automation.

---

## KPIs to track
- Objection overcome rate
- Objection resolution time
- Objection prevention rate
- Discount rate by objection type

---

## Pass threshold
**>=65% of price objections overcome with <=10 days to close after resolution over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/price-objection-handling`_
