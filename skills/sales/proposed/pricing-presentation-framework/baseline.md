---
name: pricing-presentation-framework-baseline
description: >
  Pricing Presentation Framework — Baseline Run. Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Pricing presented on ≥80% of opportunities over 2 weeks with ≥65% acceptance"
kpis: ["Pricing acceptance rate", "Average discount percentage", "Tier mix optimization", "Deal size preservation"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
---
# Pricing Presentation Framework — Baseline Run

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Present pricing confidently with value anchoring, multiple options, and clear ROI context to maximize acceptance and minimize discount requests.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Pricing presented on ≥80% of opportunities over 2 weeks with ≥65% acceptance

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

1. Expand pricing presentations to 20-30 opportunities over 2 weeks.

2. Build pricing presentation playbook: value recap script, pricing reveal frameworks, three-option structures, objection responses, discount guidelines.

3. Create pricing tiers strategy: define Good/Better/Best packages with clear feature differentiation; position Better as optimal value.

4. Set up PostHog tracking: pricing_tier_presented, initial_reaction, discount_requested, final_tier_selected, contract_value.

5. Develop value anchoring techniques: always tie price to specific ROI, time savings, or revenue impact discovered in qualification.

6. Track pricing outcomes: measure acceptance rates by tier, discount frequency and size, time from pricing to signature, deal size preservation.

7. Build discount authority matrix: define when reps can discount without approval, escalation thresholds, maximum discounts by deal size.

8. Set pass threshold: Pricing presented on ≥80% of qualified opportunities over 2 weeks with ≥65% accepting without significant discounting.

9. Analyze pricing patterns: which tiers sell best, which objections arise most, which value anchors work, what discount requests indicate.

10. If threshold met, document pricing framework and proceed to Scalable; if not, refine presentation or tier structure.

---

## KPIs to track
- Pricing acceptance rate
- Average discount percentage
- Tier mix optimization
- Deal size preservation

---

## Pass threshold
**Pricing presented on ≥80% of opportunities over 2 weeks with ≥65% acceptance**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/pricing-presentation-framework`_
