---
name: seat-expansion-triggers-smoke
description: >
    Team Growth Upsell — Smoke Test. Prompt to add seats when teams grow or collaboration increases.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥35% add seats"
kpis: ["Seat expansion rate", "Team growth", "Prompt acceptance"]
slug: "seat-expansion-triggers"
install: "npx gtm-skills add product/upsell/seat-expansion-triggers"
drills:
  - icp-definition
  - onboarding-flow
  - threshold-engine
---
# Team Growth Upsell — Smoke Test

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Team Growth Upsell — Smoke Test. Prompt to add seats when teams grow or collaboration increases.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** ≥35% add seats

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your product ICP
Run the `icp-definition` drill to define who this product experience targets: user persona, what they are trying to accomplish, what success looks like, and what would make them convert or expand.

### 2. Set up the experience
Run the `onboarding-flow` drill to configure the in-product experience: Intercom product tours, in-app messages, or Loops email sequences. Focus on the single most important user action that correlates with conversion or retention.

**Human action required:** Review the experience flows before launching. Ensure the copy is clear and the CTAs are specific. Launch to a small test group (10-50 users) and observe behavior.

### 3. Track user behavior
Log all interactions in PostHog: tour started, tour completed, CTA clicked, action taken. Note drop-off points and user feedback.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥35% add seats. If PASS, proceed to Baseline. If FAIL, simplify the experience or target a different user action.

---

## KPIs to track
- Seat expansion rate
- Team growth
- Prompt acceptance

---

## Pass threshold
**≥35% add seats**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/upsell/seat-expansion-triggers`_
