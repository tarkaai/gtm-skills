---
name: roi-skepticism-objection-baseline
description: >
  ROI Skepticism Handling — Baseline Run. Prove ROI when prospects question value by using customer data, conservative modeling, and co-creating financial analysis with prospect's own inputs to build conviction.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "ROI skepticism handled on ≥80% of instances over 2 weeks"
kpis: ["Objection resolution rate", "Collaborative model adoption", "Customer reference effectiveness", "ROI claim accuracy post-sale"]
slug: "roi-skepticism-objection"
install: "npx gtm-skills add sales/aligned/roi-skepticism-objection"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# ROI Skepticism Handling — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Prove ROI when prospects question value by using customer data, conservative modeling, and co-creating financial analysis with prospect's own inputs to build conviction.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ROI skepticism handled on ≥80% of instances over 2 weeks

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

1. Expand ROI skepticism handling to 20-30 instances over 2 weeks.

2. Build ROI proof framework: customer results database, collaborative calculator template, conservative modeling guidelines, measurement framework templates.

3. Create customer proof library: document 10-15 customer success stories with specific ROI metrics (time saved, cost reduced, revenue increased), organized by industry and use case.

4. Set up PostHog event tracking: skepticism_type, proof_method_used, collaborative_modeling_completed, conservative_vs_aggressive_assumptions, agreement_reached.

5. Develop collaborative ROI calculator: spreadsheet or tool that prospect can input their numbers, adjust assumptions, see impact; increases ownership of results.

6. Track ROI proof outcomes: measure resolution rates by proof method, deals progressed with ROI agreement, post-sale validation of ROI claims.

7. Build measurement framework templates: define KPIs to track, baseline metrics to establish, timeframes for evaluation, reporting cadence.

8. Set pass threshold: ROI skepticism addressed on ≥80% of instances over 2 weeks with ≥65% achieving ROI agreement and progressing to proposal.

9. Analyze ROI proof patterns: which proof methods work best, which customer examples resonate most, which assumptions prospects challenge, which measurement frameworks build confidence.

10. If threshold met, document ROI proof playbook and proceed to Scalable; if not, refine customer proof or calculator methodology.

---

## KPIs to track
- Objection resolution rate
- Collaborative model adoption
- Customer reference effectiveness
- ROI claim accuracy post-sale

---

## Pass threshold
**ROI skepticism handled on ≥80% of instances over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/roi-skepticism-objection`_
