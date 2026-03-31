---
name: feature-announcement-campaign-baseline
description: >
    New Feature Announcements — Baseline Run. Multi-channel campaigns (in-app, email, social)
  announcing new features to drive awareness and trial among existing users.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥35% trial, ≥15% sustained"
kpis: ["Feature trial", "Sustained adoption", "Announcement engagement"]
slug: "feature-announcement-campaign"
install: "npx gtm-skills add product/retain/feature-announcement-campaign"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# New Feature Announcements — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Overview
New Feature Announcements — Baseline Run. Multi-channel campaigns (in-app, email, social) announcing new features to drive awareness and trial among existing users.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥35% trial, ≥15% sustained

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `feature-announcement-campaign_impression`, `feature-announcement-campaign_engaged`, `feature-announcement-campaign_converted`, `feature-announcement-campaign_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥35% trial, ≥15% sustained. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Feature trial
- Sustained adoption
- Announcement engagement

---

## Pass threshold
**≥35% trial, ≥15% sustained**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/retain/feature-announcement-campaign`_
