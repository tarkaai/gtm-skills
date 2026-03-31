---
name: time-to-value-optimization-baseline
description: >
    Time-to-Value Acceleration — Baseline Run. Systematically reduce time from signup to first value
  through instrumentation, analysis, and optimization of activation funnel.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥60% <8min, ≥15pp"
kpis: ["Time to first value", "Activation rate", "Step completion"]
slug: "time-to-value-optimization"
install: "npx gtm-skills add product/onboard/time-to-value-optimization"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Time-to-Value Acceleration — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
Time-to-Value Acceleration — Baseline Run. Systematically reduce time from signup to first value through instrumentation, analysis, and optimization of activation funnel.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥60% <8min, ≥15pp

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `time-to-value-optimization_impression`, `time-to-value-optimization_engaged`, `time-to-value-optimization_converted`, `time-to-value-optimization_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥60% <8min, ≥15pp. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Time to first value
- Activation rate
- Step completion

---

## Pass threshold
**≥60% <8min, ≥15pp**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/time-to-value-optimization`_
