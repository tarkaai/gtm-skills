---
name: documentation-as-marketing-scalable
description: >
    Documentation as Marketing — Scalable Automation. Build public, SEO-optimized developer
  documentation that attracts organic search traffic and converts technical audiences from
  solution-aware to product-aware.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥5,000 organic visits/month and ≥100 signups from docs over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---
# Documentation as Marketing — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Documentation as Marketing — Scalable Automation. Build public, SEO-optimized developer documentation that attracts organic search traffic and converts technical audiences from solution-aware to product-aware.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥5,000 organic visits/month and ≥100 signups from docs over 6 months

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
Measure against: ≥5,000 organic visits/month and ≥100 signups from docs over 6 months. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥5,000 organic visits/month and ≥100 signups from docs over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/documentation-as-marketing`_
