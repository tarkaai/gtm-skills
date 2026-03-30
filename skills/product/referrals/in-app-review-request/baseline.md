---
name: in-app-review-request-baseline
description: >
  G2/Capterra Review Requests — Baseline Run. Ask happy users for G2/Capterra reviews at optimal moments to build social proof.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥25 reviews"
kpis: ["Review request CTR", "Review completion", "Review quality"]
slug: "in-app-review-request"
install: "npx gtm-skills add product/referrals/in-app-review-request"
---
# G2/Capterra Review Requests — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Ask happy users for G2/Capterra reviews at optimal moments to build social proof.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥25 reviews

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

4. Set threshold: ≥25 reviews.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- Review request CTR
- Review completion
- Review quality

---

## Pass threshold
**≥25 reviews**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/in-app-review-request`_
