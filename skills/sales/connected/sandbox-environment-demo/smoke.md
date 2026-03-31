---
name: sandbox-environment-demo-smoke
description: >
  Sandbox Environment Demo — Smoke Test. Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.
stage: "Sales > Connected"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Sandboxes provided to ≥5 opportunities in 1 week"
kpis: ["Sandbox provisioning rate", "Active usage rate", "Feature exploration depth", "Demo-to-proposal conversion"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - onboarding-flow
  - threshold-engine
---
# Sandbox Environment Demo — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** Sandboxes provided to ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Set up 5-8 sandbox environments for qualified prospects after discovery; provision with sample data relevant to their industry and use case.

2. Create sandbox kickoff guide: step-by-step instructions for getting started, key workflows to test, sample data available, how to add their own data if applicable.

3. Send sandbox access with personalized onboarding: 'Here's your hands-on environment to test [specific use cases discussed]. I've pre-loaded [relevant sample data]. Start with [suggested workflow]'.

4. Schedule 30-minute sandbox walkthrough call: demonstrate key features, show how to accomplish their specific use cases, answer questions, encourage experimentation.

5. Track sandbox usage in PostHog: logins, features accessed, time spent, workflows completed, data uploaded, errors encountered.

6. Implement proactive check-ins: reach out when sandbox shows low usage, offer help when errors occur, celebrate when key milestones are achieved.

7. Create sandbox success checklist: 3-5 key workflows or outcomes for prospect to validate; track completion in PostHog.

8. Set pass threshold: Provision sandboxes for ≥5 opportunities in 1 week with ≥60% showing active usage (3+ sessions, 30+ minutes total).

9. Measure sandbox effectiveness: track correlation between sandbox usage and demo-to-proposal conversion, deal velocity, close rate.

10. Document which sandbox approaches and check-in strategies drive highest engagement; proceed to Baseline if threshold met.

---

## KPIs to track
- Sandbox provisioning rate
- Active usage rate
- Feature exploration depth
- Demo-to-proposal conversion

---

## Pass threshold
**Sandboxes provided to ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/sandbox-environment-demo`_
