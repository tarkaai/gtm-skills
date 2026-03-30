---
name: video-tutorial-library-baseline
description: >
  Video Tutorial System — Baseline Run. Create and promote short video tutorials for key workflows, accessible in-app and via email, to accelerate learning.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email, Content"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥40%, ≥8pp"
kpis: ["Video view rate", "Completion rate", "Post-video activation"]
slug: "video-tutorial-library"
install: "npx gtm-skills add product/onboard/video-tutorial-library"
---
# Video Tutorial System — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Content

## Overview
Create and promote short video tutorials for key workflows, accessible in-app and via email, to accelerate learning.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥40%, ≥8pp

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

4. Set threshold: ≥40%, ≥8pp.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- Video view rate
- Completion rate
- Post-video activation

---

## Pass threshold
**≥40%, ≥8pp**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/video-tutorial-library`_
