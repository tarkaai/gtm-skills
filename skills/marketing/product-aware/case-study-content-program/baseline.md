---
name: case-study-content-program-baseline
description: >
    Case Study Content Program — Baseline Run. Create in-depth customer success stories with metrics
  and storytelling to build credibility and drive conversions, from manual interviews to systematic
  production and AI-driven story optimization.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "35 hours over 8 weeks"
outcome: "≥2,000 page views and ≥30 conversions over 8 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Sales usage rate", "Customer participation rate"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Case Study Content Program — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Case Study Content Program — Baseline Run. Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.

**Time commitment:** 35 hours over 8 weeks
**Pass threshold:** ≥2,000 page views and ≥30 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `case-study-content-program_impression`, `case-study-content-program_engaged`, `case-study-content-program_converted`, `case-study-content-program_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥2,000 page views and ≥30 conversions over 8 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Page views
- Time on page
- Conversion rate
- Sales usage rate
- Customer participation rate

---

## Pass threshold
**≥2,000 page views and ≥30 conversions over 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/case-study-content-program`_
