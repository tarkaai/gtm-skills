---
name: self-serve-signup-optimization-smoke
description: >
  Signup Funnel Optimization — Smoke Test. Reduce friction in signup flow through testing and optimization to increase conversion rate.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Website, Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥30% signup CVR"
kpis: ["Signup conversion", "Form completion", "Drop-off points"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
---
# Signup Funnel Optimization — Smoke Test

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Website, Product

## Overview
Reduce friction in signup flow through testing and optimization to increase conversion rate.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** ≥30% signup CVR

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)

---

## Instructions

1. Define success metric and pass threshold (≥30% signup CVR).

2. In PostHog, create events for key actions; ensure app tracks all interactions.

3. Instrument critical path with clear PostHog event names.

4. Build minimum viable version with simple UI.

5. Launch to 10-20 users via PostHog feature flag.

6. Track progression in PostHog; create funnels for drop-off analysis.

7. After 7 days, compute metrics vs. threshold.

8. Review PostHog data for patterns and friction.

9. If passed, document and proceed to Baseline; if not, iterate.

10. Record observations for optimization.

---

## KPIs to track
- Signup conversion
- Form completion
- Drop-off points

---

## Pass threshold
**≥30% signup CVR**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/self-serve-signup-optimization`_
