---
name: feature-deprecation-management-scalable
description: >
    Feature Sunset Communication — Scalable Automation. Sunset old features without losing users
  through clear communication and migration paths.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥85% at 500+"
kpis: ["Migration rate", "Churn from sunset", "Communication engagement", "Segment metrics"]
slug: "feature-deprecation-management"
install: "npx gtm-skills add product/retain/feature-deprecation-management"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---
# Feature Sunset Communication — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Feature Sunset Communication — Scalable Automation. Sunset old features without losing users through clear communication and migration paths.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥85% at 500+

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Launch systematic testing
Run the `ab-test-orchestrator` drill to test variations of your product experience: messaging copy, timing of prompts, CTA placement, and user segments. Use PostHog feature flags to run experiments. Run each test for statistical significance.

### 2. Build churn prevention
Run the `churn-prevention` drill to configure automated interventions: detect at-risk users via PostHog cohorts (declining usage, missed milestones), trigger Intercom messages or Loops emails to re-engage them.

### 3. Set up expansion prompts
Run the `upgrade-prompt` drill to configure upgrade and expansion triggers: usage threshold notifications, feature gate messages, and team invitation prompts. Time these based on user engagement data from PostHog.

### 4. Evaluate against threshold
Measure against: ≥85% at 500+. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate.

---

## KPIs to track
- Migration rate
- Churn from sunset
- Communication engagement
- Segment metrics

---

## Pass threshold
**≥85% at 500+**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/retain/feature-deprecation-management`_
