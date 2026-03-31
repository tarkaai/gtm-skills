---
name: comparison-alternative-pages-baseline
description: >
    Comparison and Alternative Pages — Baseline Run. Create comparison and alternative pages
  targeting competitor keywords to capture high-intent search traffic, from manual competitor
  research to automated page generation and AI-driven competitive intelligence.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "25 hours over 8 weeks"
outcome: "≥1,500 page views and ≥20 conversions over 8 weeks"
kpis: ["Organic traffic", "Conversion rate", "Average position for competitor keywords", "CTA click rate", "Feature table engagement"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Comparison and Alternative Pages — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Comparison and Alternative Pages — Baseline Run. Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.

**Time commitment:** 25 hours over 8 weeks
**Pass threshold:** ≥1,500 page views and ≥20 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `comparison-alternative-pages_impression`, `comparison-alternative-pages_engaged`, `comparison-alternative-pages_converted`, `comparison-alternative-pages_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥1,500 page views and ≥20 conversions over 8 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Organic traffic
- Conversion rate
- Average position for competitor keywords
- CTA click rate
- Feature table engagement

---

## Pass threshold
**≥1,500 page views and ≥20 conversions over 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/comparison-alternative-pages`_
