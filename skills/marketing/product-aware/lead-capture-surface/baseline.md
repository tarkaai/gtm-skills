---
name: lead-capture-surface-baseline
description: >
    Single CTA Lead Capture — Baseline Run. Use one clear CTA (e.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 4% conversion rate over 2 weeks"
kpis: ["Click-through rate", "Form starts"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Single CTA Lead Capture — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Direct

## Overview
Single CTA Lead Capture — Baseline Run. Use one clear CTA (e.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 4% conversion rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `lead-capture-surface_impression`, `lead-capture-surface_engaged`, `lead-capture-surface_converted`, `lead-capture-surface_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥ 4% conversion rate over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Click-through rate
- Form starts

---

## Pass threshold
**≥ 4% conversion rate over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/lead-capture-surface`_
