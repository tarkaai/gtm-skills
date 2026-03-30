---
name: timing-qualification-baseline
description: >
  Timing Qualification Process — Baseline Run. Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Baseline Run"
time: "13 hours over 2 weeks"
outcome: "Timeline qualified on ≥80% of opportunities over 2 weeks"
kpis: ["Timeline qualification rate", "Timeline accuracy", "Deal velocity by timeline", "Forecast accuracy"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
---
# Timing Qualification Process — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.

**Time commitment:** 13 hours over 2 weeks
**Pass threshold:** Timeline qualified on ≥80% of opportunities over 2 weeks

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

1. Expand timing qualification to 50-100 opportunities over 2 weeks.

2. Build timing trigger library documenting common urgency drivers by industry and ICP.

3. Create timeline-specific engagement strategies: Immediate gets daily touchpoints, Near-term gets 2-3x/week.

4. Set up PostHog event tracking: timeline_category_assigned, urgency_trigger_identified, timeline_shift_detected.

5. Implement timeline validation process: for Immediate/Near-term deals, confirm timeline with multiple stakeholders.

6. Track conversion metrics: measure close rate, deal velocity, forecast accuracy by timeline category.

7. Build pipeline segmentation: separate 'active pipeline' (0-3 months) from 'future pipeline' (3+ months).

8. Set pass threshold: Timeline qualified on ≥80% of opportunities over 2 weeks.

9. Analyze timing patterns: which prospects give accurate timelines, what causes slippage.

10. If threshold met, document timing qualification playbook and proceed to Scalable.

---

## KPIs to track
- Timeline qualification rate
- Timeline accuracy
- Deal velocity by timeline
- Forecast accuracy

---

## Pass threshold
**Timeline qualified on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/timing-qualification`_
