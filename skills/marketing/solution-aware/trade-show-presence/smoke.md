---
name: trade-show-presence-smoke
description: >
  Trade Show Presence — Smoke Test. Attend industry trade shows with booth and demos to generate leads, demonstrate product, and engage solution-aware prospects in high-intent buying environment.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥80 booth visitors and ≥15 qualified leads from first trade show"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "trade-show-presence"
install: "npx gtm-skills add marketing/solution-aware/trade-show-presence"
---
# Trade Show Presence — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Attend industry trade shows with booth and demos to generate leads, demonstrate product, and engage solution-aware prospects in high-intent buying environment.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥80 booth visitors and ≥15 qualified leads from first trade show

---

## Budget

**Play-specific tools & costs**
- **Webinar platform — Zoom free tier or Google Meet:** Free
- **Cal.com (scheduling, optional):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Define your ICP and target audience for this trade show presence play; document hypothesis and success criteria.

2. Create minimal viable version manually with small test size (10-50 contacts, pieces, or interactions).

3. Set pass threshold upfront (e.g., ≥2 qualified responses, ≥3% engagement, ≥50 interactions) and choose where to log results.

4. Execute play within time cap (hours to 1 week) using free or existing tools; keep it scrappy and manual.

5. Track all activities and outcomes in spreadsheet or basic CRM (Attio); log dates, responses, and key metrics.

6. Monitor engagement and response quality; note any unexpected positive or negative signals.

7. Measure final results against your pass threshold after test period ends.

8. Document key learnings: what messaging resonated, what channels worked, what timing was optimal.

9. Calculate rough ROI: time invested vs. qualified responses or meetings generated.

10. Decide next step: proceed to Baseline if passed threshold, iterate if close but needs refinement, or pivot to different play if fundamentally not working.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥80 booth visitors and ≥15 qualified leads from first trade show**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/trade-show-presence`_
