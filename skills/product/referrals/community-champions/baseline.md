---
name: community-champions-baseline
description: >
  Champion Recognition Program — Baseline Run. Identify and empower community leaders with exclusive access, recognition, and co-marketing opportunities.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥20 champions, ≥5 referrals each"
kpis: ["Champion identification", "Champion activity", "Referrals generated"]
slug: "community-champions"
install: "npx gtm-skills add product/referrals/community-champions"
---
# Champion Recognition Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Overview
Identify and empower community leaders with exclusive access, recognition, and co-marketing opportunities.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥20 champions, ≥5 referrals each

---

## Budget

**Play-specific tools & costs**
- **Tally or Typeform (surveys + forms):** Free–$25/mo
- **Loom (async video for onboarding/CSM):** Free–$15/mo

_Total play-specific: ~$15–25/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)
- **n8n** (Automation)
- **Loops** (Email)

---

## Instructions

1. Build production version with polished UX.

2. Create PostHog funnels, cohorts, dashboards.

3. Launch to 50% via feature flag; 50% control.

4. Set threshold: ≥20 champions, ≥5 referrals each.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- Champion identification
- Champion activity
- Referrals generated

---

## Pass threshold
**≥20 champions, ≥5 referrals each**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/community-champions`_
