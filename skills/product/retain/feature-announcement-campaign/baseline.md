---
name: feature-announcement-campaign-baseline
description: >
  New Feature Announcements — Baseline Run. Multi-channel campaigns (in-app, email, social) announcing new features to drive awareness and trial among existing users.
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
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - threshold-engine
---
# New Feature Announcements — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Overview
Multi-channel campaigns (in-app, email, social) announcing new features to drive awareness and trial among existing users.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥35% trial, ≥15% sustained

---

## Budget

**Play-specific tools & costs**
- **Tally or Typeform (surveys + forms):** Free–$25/mo
- **Loom (async video for onboarding/CSM):** Free–$15/mo

_Total play-specific: ~$15–25/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)
- **n8n** (Automation)
- **Loops** (Email)

---

## Instructions

1. Build production version with polished UX.

2. Create PostHog funnels, cohorts, dashboards.

3. Launch to 50% via feature flag; 50% control.

4. Set threshold: ≥35% trial, ≥15% sustained.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- Feature trial
- Sustained adoption
- Announcement engagement

---

## Pass threshold
**≥35% trial, ≥15% sustained**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/retain/feature-announcement-campaign`_
