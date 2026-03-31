---
name: sandbox-environment-demo-smoke
description: >
    Sandbox Environment Demo — Smoke Test. Provide hands-on sandbox environment during sales process
  so prospects can test product with their own data and use cases to validate fit and build
  confidence.
stage: "Sales > Connected"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Sandboxes provided to ≥5 opportunities in 1 week"
kpis: ["Sandbox provisioning rate", "Active usage rate", "Feature exploration depth", "Demo-to-proposal conversion"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - icp-definition
  - onboarding-flow
  - threshold-engine
---
# Sandbox Environment Demo — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Sandbox Environment Demo — Smoke Test. Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** Sandboxes provided to ≥5 opportunities in 1 week

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
Run the `threshold-engine` drill to measure against: Sandboxes provided to ≥5 opportunities in 1 week. If PASS, proceed to Baseline. If FAIL, simplify the experience or target a different user action.

---

## KPIs to track
- Sandbox provisioning rate
- Active usage rate
- Feature exploration depth
- Demo-to-proposal conversion

---

## Pass threshold
**Sandboxes provided to ≥5 opportunities in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/sandbox-environment-demo`_
