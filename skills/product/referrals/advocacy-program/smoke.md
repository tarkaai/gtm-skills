---
name: advocacy-program-smoke
description: >
    Formal Advocacy Program — Smoke Test. Formal program to reward and recognize advocates with
  perks, early access, and community status.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Events"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥15 advocates"
kpis: ["Advocate recruitment", "Advocate activity", "Referrals per advocate"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - icp-definition
  - onboarding-flow
  - threshold-engine
---
# Formal Advocacy Program — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Overview
Formal Advocacy Program — Smoke Test. Formal program to reward and recognize advocates with perks, early access, and community status.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** ≥15 advocates

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
Run the `threshold-engine` drill to measure against: ≥15 advocates. If PASS, proceed to Baseline. If FAIL, simplify the experience or target a different user action.

---

## KPIs to track
- Advocate recruitment
- Advocate activity
- Referrals per advocate

---

## Pass threshold
**≥15 advocates**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/advocacy-program`_
