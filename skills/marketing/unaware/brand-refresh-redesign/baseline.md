---
name: brand-refresh-redesign-baseline
description: >
    Brand Refresh & Redesign — Baseline Run. Update brand identity, messaging, and website to better
  position for target market and improve conversion across all awareness stages.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Launch refreshed brand identity with ≥20% improvement in key conversion metrics over 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Brand Refresh & Redesign — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Brand Refresh & Redesign — Baseline Run. Update brand identity, messaging, and website to better position for target market and improve conversion across all awareness stages.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** Launch refreshed brand identity with ≥20% improvement in key conversion metrics over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `brand-refresh-redesign_impression`, `brand-refresh-redesign_engaged`, `brand-refresh-redesign_converted`, `brand-refresh-redesign_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: Launch refreshed brand identity with ≥20% improvement in key conversion metrics over 8 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**Launch refreshed brand identity with ≥20% improvement in key conversion metrics over 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/brand-refresh-redesign`_
