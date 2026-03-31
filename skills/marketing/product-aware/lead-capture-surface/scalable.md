---
name: lead-capture-surface-scalable
description: >
    Single CTA Lead Capture — Scalable Automation. Use one clear CTA (e.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 4% conversion rate sustained over 2 months"
kpis: ["Click-through rate", "Form starts"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---
# Single CTA Lead Capture — Scalable Automation

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Direct

## Overview
Single CTA Lead Capture — Scalable Automation. Use one clear CTA (e.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 4% conversion rate sustained over 2 months

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
Measure against: ≥ 4% conversion rate sustained over 2 months. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate.

---

## KPIs to track
- Click-through rate
- Form starts

---

## Pass threshold
**≥ 4% conversion rate sustained over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/lead-capture-surface`_
