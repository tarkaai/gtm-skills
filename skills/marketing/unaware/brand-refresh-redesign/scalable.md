---
name: brand-refresh-redesign-scalable
description: >
    Brand Refresh & Redesign — Scalable Automation. Update brand identity, messaging, and website to
  better position for target market and improve conversion across all awareness stages.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥30% improvement in brand recognition and ≥25% lift in conversion rates over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---
# Brand Refresh & Redesign — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Brand Refresh & Redesign — Scalable Automation. Update brand identity, messaging, and website to better position for target market and improve conversion across all awareness stages.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥30% improvement in brand recognition and ≥25% lift in conversion rates over 6 months

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
Measure against: ≥30% improvement in brand recognition and ≥25% lift in conversion rates over 6 months. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥30% improvement in brand recognition and ≥25% lift in conversion rates over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/brand-refresh-redesign`_
