---
name: roi-skepticism-objection-smoke
description: >
  ROI Skepticism Handling — Smoke Test. Prove ROI when prospects question value by using customer data, conservative modeling, and co-creating financial analysis with prospect's own inputs to build conviction.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "ROI skepticism handled on ≥5 opportunities in 1 week"
kpis: ["ROI objection resolution rate", "Customer proof effectiveness", "Collaborative model acceptance", "Deal progression rate"]
slug: "roi-skepticism-objection"
install: "npx gtm-skills add sales/aligned/roi-skepticism-objection"
drills:
  - icp-definition
  - threshold-engine
---
# ROI Skepticism Handling — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Prove ROI when prospects question value by using customer data, conservative modeling, and co-creating financial analysis with prospect's own inputs to build conviction.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ROI skepticism handled on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When 5-8 prospects express ROI skepticism, diagnose concern: question value proposition, doubt claimed results, need proof for internal approval, burned by past vendor promises.

2. Use customer proof strategy: share specific customer examples with real numbers, show before/after metrics, provide references willing to discuss results.

3. Co-create ROI model: don't present generic calculator; work with prospect to input their specific numbers (current costs, volume, inefficiencies, time spent); calculate ROI using their data.

4. Use conservative assumptions: model worst-case scenario with modest adoption rates and conservative efficiency gains; show ROI even in pessimistic case.

5. Provide payback period focus: shift from multi-year ROI to time-to-payback; show 'How quickly will you recoup your investment?' (aim for <12 months).

6. Offer measurement framework: propose specific metrics to track post-purchase, define success criteria, agree on how ROI will be validated.

7. Track PostHog events: roi_skepticism_raised, customer_proof_shared, collaborative_model_created, conservative_assumptions_used, measurement_framework_agreed.

8. Set pass threshold: Handle ROI skepticism on ≥5 opportunities in 1 week with ≥60% accepting ROI proof and advancing to proposal.

9. Measure effectiveness: track ROI objection resolution rate, collaborative modeling acceptance, deals progressed with ROI agreement.

10. Document which ROI proof approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- ROI objection resolution rate
- Customer proof effectiveness
- Collaborative model acceptance
- Deal progression rate

---

## Pass threshold
**ROI skepticism handled on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/roi-skepticism-objection`_
