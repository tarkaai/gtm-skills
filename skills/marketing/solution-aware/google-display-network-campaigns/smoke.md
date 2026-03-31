---
name: google-display-network-campaigns-smoke
description: >
  Google Display Network — Smoke Test. Run GDN campaigns targeting in-market audiences and affinity segments to build awareness and generate leads from solution-aware searchers.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥30,000 impressions and ≥5 qualified leads from $300 GDN test"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
drills:
  - ad-campaign-setup
  - threshold-engine
---
# Google Display Network — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Run GDN campaigns targeting in-market audiences and affinity segments to build awareness and generate leads from solution-aware searchers.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥30,000 impressions and ≥5 qualified leads from $300 GDN test

---

## Budget

**Play-specific tools & costs**
- **Ad spend (LinkedIn, Google, or Meta):** $300–1,000 test budget

_Total play-specific: $300–1,000 ad spend_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Define your ICP and target audience for this google display network play; document hypothesis and success criteria.

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
**≥30,000 impressions and ≥5 qualified leads from $300 GDN test**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/google-display-network-campaigns`_
