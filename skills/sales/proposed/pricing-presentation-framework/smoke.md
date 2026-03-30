---
name: pricing-presentation-framework-smoke
description: >
  Pricing Presentation Framework — Smoke Test. Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Pricing presented to ≥5 opportunities in 1 week with ≥60% acceptance"
kpis: ["Pricing acceptance rate", "Discount request frequency", "Value anchoring effectiveness", "Close rate"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
---
# Pricing Presentation Framework — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Pricing presented to ≥5 opportunities in 1 week with ≥60% acceptance

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 5-8 pricing conversations, lead with value before price: recap pain points discovered, solution value delivered, expected outcomes agreed upon.

2. Present pricing in context: 'Based on [specific value you'll deliver], our investment is [price]' rather than leading with raw numbers.

3. Offer 3 options: Good (meets core needs), Better (recommended, includes value-adds), Best (premium features); anchor on Better as recommended choice.

4. Frame monthly vs annual: show annual pricing with monthly equivalent; highlight annual savings percentage to incentivize upfront commitment.

5. Link price to value metrics: 'For [your expected ROI/time savings/revenue impact], the investment is [price per month/user/transaction]'.

6. Pause after presenting: don't immediately defend or discount; let prospect process; wait for their response before addressing concerns.

7. Track PostHog events: pricing_presented, option_selected, discount_requested, objection_type, deal_progressed.

8. Set pass threshold: Present pricing to ≥5 opportunities in 1 week with ≥60% accepting proposal or requesting only modest adjustments.

9. Measure effectiveness: track acceptance rate, discount request frequency, average discount given, close rate by pricing approach.

10. Document which pricing presentation techniques work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Pricing acceptance rate
- Discount request frequency
- Value anchoring effectiveness
- Close rate

---

## Pass threshold
**Pricing presented to ≥5 opportunities in 1 week with ≥60% acceptance**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/pricing-presentation-framework`_
