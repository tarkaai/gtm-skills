---
name: quick-start-guide-baseline
description: >
    Quick Start Documentation — Baseline Run. Create concise, scannable quick-start guide accessible
  in-app and via email to reduce onboarding friction.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email, Content"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥50%, ≥8pp"
kpis: ["Guide view rate", "Guide completion", "Post-view activation"]
slug: "quick-start-guide"
install: "npx gtm-skills add product/onboard/quick-start-guide"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Quick Start Documentation — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Content

## Overview
Quick Start Documentation — Baseline Run. Create concise, scannable quick-start guide accessible in-app and via email to reduce onboarding friction.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥50%, ≥8pp

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `quick-start-guide_impression`, `quick-start-guide_engaged`, `quick-start-guide_converted`, `quick-start-guide_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥50%, ≥8pp. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Guide view rate
- Guide completion
- Post-view activation

---

## Pass threshold
**≥50%, ≥8pp**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/quick-start-guide`_
