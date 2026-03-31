---
name: feature-gating-baseline
description: >
    Premium Feature Gating — Baseline Run. Gate premium features to drive upgrades while showcasing
  value through previews and trials.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥30% upgrade after trial"
kpis: ["Trial rate", "Upgrade rate", "Feature engagement"]
slug: "feature-gating"
install: "npx gtm-skills add product/upsell/feature-gating"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Premium Feature Gating — Baseline Run

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
Premium Feature Gating — Baseline Run. Gate premium features to drive upgrades while showcasing value through previews and trials.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥30% upgrade after trial

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `feature-gating_impression`, `feature-gating_engaged`, `feature-gating_converted`, `feature-gating_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥30% upgrade after trial. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Trial rate
- Upgrade rate
- Feature engagement

---

## Pass threshold
**≥30% upgrade after trial**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/upsell/feature-gating`_
