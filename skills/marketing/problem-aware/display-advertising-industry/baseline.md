---
name: display-advertising-industry-baseline
description: >
  Display Advertising — Baseline Run. Run banner ads on relevant industry sites and publications to build awareness and drive traffic from problem-aware and solution-aware target audiences.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥200,000 impressions and ≥20 qualified leads from $2,000 budget over 3 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "display-advertising-industry"
install: "npx gtm-skills add marketing/problem-aware/display-advertising-industry"
drills:
  - ad-campaign-setup
  - landing-page-pipeline
  - budget-allocation
  - threshold-engine
---
# Display Advertising — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Run banner ads on relevant industry sites and publications to build awareness and drive traffic from problem-aware and solution-aware target audiences.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥200,000 impressions and ≥20 qualified leads from $2,000 budget over 3 weeks

---

## Budget

**Play-specific tools & costs**
- **Ad spend:** $1,000–3,000/mo
- **Landing page tool (Webflow or Carrd, if needed):** ~$15–40/mo

_Total play-specific: ~$15–3000/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Clay** (Enrichment)

---

## Instructions

1. Expand scope to 100-500 targets for repeatable 2-week display advertising experiment; define detailed ICP criteria.

2. Build structured targeting list or content plan using Clay or Apollo; ensure quality and relevance to ICP.

3. Set up proper tracking in PostHog and Attio CRM to measure all activities, responses, and outcomes consistently.

4. Define pass threshold for Baseline (e.g., ≥2% conversion, ≥10 qualified results) with clear measurement criteria.

5. Create multi-touch or multi-format approach (3-5 touchpoints or content pieces) to test repeatability and engagement.

6. Execute play systematically; log every activity, response, and outcome in PostHog and CRM for complete dataset.

7. Monitor performance weekly; adjust tactics within same play framework (e.g., refine messaging, timing, targeting).

8. Track key metrics: response rate, conversion rate, cycle time from first touch to qualified outcome, and cost per result.

9. After 2 weeks, analyze results against pass threshold; identify what drove success (specific messages, channels, timing).

10. Decide: proceed to Scalable if passed threshold, iterate on targeting or approach if close, or pivot to different play if fundamentally not working.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥200,000 impressions and ≥20 qualified leads from $2,000 budget over 3 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/display-advertising-industry`_
