---
name: need-assessment-framework-baseline
description: >
  Need Assessment Framework — Baseline Run. Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Need assessment completed on ≥80% of opportunities over 2 weeks"
kpis: ["Need assessment completion rate", "Need score correlation with close rate", "Disqualification rate", "Deal velocity by need tier"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Need Assessment Framework — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Need assessment completed on ≥80% of opportunities over 2 weeks

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

1. Expand need assessment to 50-100 opportunities over 2 weeks; refine scoring criteria based on Smoke test learnings.

2. Build need-to-product mapping: document exactly how each critical need maps to specific product capabilities and customer outcomes.

3. Create tiered qualification criteria: A-tier (≥18 need score), B-tier (12-17), C-tier (<12); define different engagement strategies for each tier.

4. Develop need-specific discovery question banks: 3-5 probing questions per need area to uncover depth, urgency, budget impact, and stakeholder buy-in.

5. Set up PostHog event tracking: need_category_identified, high_need_opportunity, multi_need_prospect, need_to_product_mapped.

6. Track conversion funnel: measure how need scores correlate with demo acceptance, proposal delivery, and close rate across different deal sizes.

7. Analyze need patterns by segment: which ICPs have which need profiles, what need combinations predict highest win rates.

8. Set pass threshold: Need assessment completed on ≥80% of opportunities over 2 weeks, with need score predicting close rate within 15% accuracy.

9. Build need assessment playbook: standardized questions, scoring rubric, qualification thresholds, and handoff criteria to next stage.

10. If threshold met, document need patterns and proceed to Scalable; if not, refine need definitions or assessment methodology.

---

## KPIs to track
- Need assessment completion rate
- Need score correlation with close rate
- Disqualification rate
- Deal velocity by need tier

---

## Pass threshold
**Need assessment completed on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/need-assessment-framework`_
