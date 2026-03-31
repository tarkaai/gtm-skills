---
name: usage-based-upsell-baseline
description: >
    Automatic Usage Upsell — Baseline Run. Automatically upgrade users as usage grows based on
  consumption thresholds.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥60% accept"
kpis: ["Auto-upgrade acceptance", "Usage growth", "ARPU lift"]
slug: "usage-based-upsell"
install: "npx gtm-skills add product/upsell/usage-based-upsell"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Automatic Usage Upsell — Baseline Run

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
Automatic Usage Upsell — Baseline Run. Automatically upgrade users as usage grows based on consumption thresholds.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥60% accept

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `usage-based-upsell_impression`, `usage-based-upsell_engaged`, `usage-based-upsell_converted`, `usage-based-upsell_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥60% accept. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Auto-upgrade acceptance
- Usage growth
- ARPU lift

---

## Pass threshold
**≥60% accept**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/upsell/usage-based-upsell`_
