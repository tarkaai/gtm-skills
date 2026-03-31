---
name: product-qualified-lead-scoring-baseline
description: >
    PQL Scoring System — Baseline Run. Identify high-intent users for sales outreach based on
  product usage signals.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥70% score accuracy"
kpis: ["PQL identification", "Score accuracy", "Sales conversion"]
slug: "product-qualified-lead-scoring"
install: "npx gtm-skills add product/onboard/product-qualified-lead-scoring"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# PQL Scoring System — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
PQL Scoring System — Baseline Run. Identify high-intent users for sales outreach based on product usage signals.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥70% score accuracy

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `product-qualified-lead-scoring_impression`, `product-qualified-lead-scoring_engaged`, `product-qualified-lead-scoring_converted`, `product-qualified-lead-scoring_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥70% score accuracy. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- PQL identification
- Score accuracy
- Sales conversion

---

## Pass threshold
**≥70% score accuracy**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/product-qualified-lead-scoring`_
