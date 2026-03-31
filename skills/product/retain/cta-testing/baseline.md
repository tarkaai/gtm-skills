---
name: cta-testing-baseline
description: >
    CTA Optimization — Baseline Run. Test different calls-to-action in product to maximize
  click-through and conversion.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥25% CTR lift"
kpis: ["CTA CTR", "Conversion rate", "Test velocity"]
slug: "cta-testing"
install: "npx gtm-skills add product/retain/cta-testing"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# CTA Optimization — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
CTA Optimization — Baseline Run. Test different calls-to-action in product to maximize click-through and conversion.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥25% CTR lift

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `cta-testing_impression`, `cta-testing_engaged`, `cta-testing_converted`, `cta-testing_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥25% CTR lift. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- CTA CTR
- Conversion rate
- Test velocity

---

## Pass threshold
**≥25% CTR lift**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/retain/cta-testing`_
