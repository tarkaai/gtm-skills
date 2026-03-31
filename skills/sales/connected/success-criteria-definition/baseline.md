---
name: success-criteria-definition-baseline
description: >
  Success Criteria Definition — Baseline Run. Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Success criteria defined on ≥80% of opportunities over 2 weeks"
kpis: ["Success criteria definition rate", "Stakeholder alignment rate", "Close rate with defined criteria", "Post-sale success achievement rate"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Success Criteria Definition — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Success criteria defined on ≥80% of opportunities over 2 weeks

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

1. Expand success criteria definition to 35-50 opportunities over 2 weeks; develop systematic framework for defining and validating success.

2. Create success criteria templates by use case: efficiency gains, revenue impact, cost savings, quality improvements, time-to-value metrics.

3. Build success criteria workshop format: structured 30-minute conversation to collaboratively define measurable outcomes with prospect stakeholders.

4. Set up PostHog event tracking: success_workshop_completed, criteria_by_category, achievability_score, stakeholder_alignment, baseline_metrics_established.

5. Implement baseline measurement: help prospects establish current-state metrics so success can be measured against starting point.

6. Track success criteria to outcome correlation: measure how well-defined success criteria predict close rate, deal velocity, customer satisfaction, and renewal rates.

7. Create mutual success plan document: formalize success criteria in shared document with prospect showing metrics, measurement methods, timeline, responsibilities.

8. Set pass threshold: Success criteria defined on ≥80% of opportunities over 2 weeks with ≥70% achieving mutual stakeholder agreement.

9. Analyze success patterns: which types of success criteria correlate with fastest closes and highest retention; which criteria are most frequently achieved post-sale.

10. If threshold met, document success criteria playbook and proceed to Scalable; if not, refine definition and validation process.

---

## KPIs to track
- Success criteria definition rate
- Stakeholder alignment rate
- Close rate with defined criteria
- Post-sale success achievement rate

---

## Pass threshold
**Success criteria defined on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/success-criteria-definition`_
