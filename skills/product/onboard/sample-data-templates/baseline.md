---
name: sample-data-templates-baseline
description: >
    Sample Data Acceleration — Baseline Run. Pre-populate accounts with sample data and templates so
  users can explore functionality before adding real data.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥80%, ≥15pp"
kpis: ["Sample engagement", "Time to first action", "Activation rate"]
slug: "sample-data-templates"
install: "npx gtm-skills add product/onboard/sample-data-templates"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Sample Data Acceleration — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
Sample Data Acceleration — Baseline Run. Pre-populate accounts with sample data and templates so users can explore functionality before adding real data.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥80%, ≥15pp

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `sample-data-templates_impression`, `sample-data-templates_engaged`, `sample-data-templates_converted`, `sample-data-templates_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥80%, ≥15pp. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Sample engagement
- Time to first action
- Activation rate

---

## Pass threshold
**≥80%, ≥15pp**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/sample-data-templates`_
