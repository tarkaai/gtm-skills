---
name: ai-onboarding-coach-baseline
description: >
  AI Onboarding Assistant — Baseline Run. AI agent that guides onboarding with personalized help and proactive suggestions.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥55% use, ≥15pp activation"
kpis: ["AI coach usage", "Activation lift", "User satisfaction"]
slug: "ai-onboarding-coach"
install: "npx gtm-skills add product/onboard/ai-onboarding-coach"
---
# AI Onboarding Assistant — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
AI agent that guides onboarding with personalized help and proactive suggestions.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥55% use, ≥15pp activation

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

4. Set threshold: ≥55% use, ≥15pp activation.

5. Track all interactions and metrics in PostHog.

6. Set up n8n workflows for automation.

7. Weekly PostHog analysis: treatment vs. control.

8. Use session recordings to fix friction.

9. At 2 weeks, verify threshold met.

10. If pass, proceed to Scalable; else iterate.

---

## KPIs to track
- AI coach usage
- Activation lift
- User satisfaction

---

## Pass threshold
**≥55% use, ≥15pp activation**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/ai-onboarding-coach`_
