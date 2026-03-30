---
name: paid-social-ads-baseline
description: >
  Paid Social Ads — Baseline Run. Run a capped spend across a couple of ad groups and one LP to see if you get first conversions or a meeting within budget.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 8 leads or ≥ 4 meetings over 2 weeks"
kpis: ["Click-through rate", "Landing page visits"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
---
# Paid Social Ads — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Run a capped spend across a couple of ad groups and one LP to see if you get first conversions or a meeting within budget.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 8 leads or ≥ 4 meetings over 2 weeks

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

---

## Instructions

1. Define your 2-week experiment scope: list size, channels, and success criteria aligned with your pass threshold (e.g. ≥ 8 leads or ≥ 4 meetings over 2 weeks).

2. Choose where you will log every outcome: PostHog and optionally your CRM; create or use events for each key action.

3. Build your list and run enrichment (e.g. Clay, Apollo) so you have enough qualified contacts for the 2-week window.

4. Execute the campaign: send sequences, make calls, or run touchpoints according to your plan; cap time and budget as defined for Baseline.

5. Log every outcome in PostHog: track Click-through rate, Landing page visits so you can compute rates and compare to threshold.

6. At the end of week 1, review mid-point metrics; adjust cadence or targeting for week 2 if needed.

7. At the end of 2 weeks, compute final metrics (e.g. meeting rate, reply rate, signups) and compare to your pass threshold.

8. Document what worked (list source, message, channel mix) so you can repeat or scale.

9. If metrics hold, proceed to Scalable; if not, iterate on list, offer, or channel and re-run Baseline.

10. Record qualitative notes (who responded, objections) in PostHog or CRM for future optimization.

---

## KPIs to track
- Click-through rate
- Landing page visits

---

## Pass threshold
**≥ 8 leads or ≥ 4 meetings over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/paid-social-ads`_
