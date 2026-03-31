---
name: technical-seo-audit-optimization-baseline
description: >
    Technical SEO Audit & Fix — Baseline Run. Systematically audit and fix technical SEO issues to
  improve search rankings, organic traffic, and lead generation from solution-aware searchers.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Increase organic traffic by 20% and improve average position by 5 ranks in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "technical-seo-audit-optimization"
install: "npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Technical SEO Audit & Fix — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Technical SEO Audit & Fix — Baseline Run. Systematically audit and fix technical SEO issues to improve search rankings, organic traffic, and lead generation from solution-aware searchers.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** Increase organic traffic by 20% and improve average position by 5 ranks in 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `technical-seo-audit-optimization_impression`, `technical-seo-audit-optimization_engaged`, `technical-seo-audit-optimization_converted`, `technical-seo-audit-optimization_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: Increase organic traffic by 20% and improve average position by 5 ranks in 8 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**Increase organic traffic by 20% and improve average position by 5 ranks in 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/technical-seo-audit-optimization`_
