---
name: refer-a-friend-incentive-baseline
description: >
  Referral Rewards Program — Baseline Run. Rewards for successful referrals to drive word-of-mouth growth.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥12% refer, ≥35% convert"
kpis: ["Referral rate", "Conversion rate", "Reward cost"]
slug: "refer-a-friend-incentive"
install: "npx gtm-skills add product/referrals/refer-a-friend-incentive"
---
# Referral Rewards Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Rewards for successful referrals to drive word-of-mouth growth.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥12% refer, ≥35% convert

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

4. Set threshold: ≥12% refer, ≥35% convert.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- Referral rate
- Conversion rate
- Reward cost

---

## Pass threshold
**≥12% refer, ≥35% convert**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/refer-a-friend-incentive`_
