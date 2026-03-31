---
name: advocacy-program-scalable
description: >
  Formal Advocacy Program — Scalable Automation. Formal program to reward and recognize advocates with perks, early access, and community status.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Events"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥75 advocates at 500+"
kpis: ["Advocate recruitment", "Advocate activity", "Referrals per advocate", "Segment metrics"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
---
# Formal Advocacy Program — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Overview
Formal program to reward and recognize advocates with perks, early access, and community status.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥75 advocates at 500+

---

## Budget

**Play-specific tools & costs**
- **Intercom (in-app messaging + email sequences):** ~$75–300/mo
- **Loom or Descript (video content at scale):** ~$15–30/mo
- **Typeform (in-app surveys + NPS):** ~$25/mo

_Total play-specific: ~$15–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)
- **n8n** (Automation)
- **Loops** (Email)
- **Intercom** (Communication)

---

## Instructions

1. Roll out to 100%; personalize via PostHog cohorts.

2. Build 2-3 persona variants; assign via properties.

3. Target: ≥500 users/2mo; efficiency: ≥75 advocates at 500+.

4. Automate workflows with n8n + PostHog triggers.

5. Use recordings to fix friction continuously.

6. A/B test via PostHog experiments.

7. Track feature discovery in PostHog.

8. Monitor weekly; alert if below threshold.

9. After 2mo, verify at scale; prep Durable.

10. Document playbook for AI handoff.

---

## KPIs to track
- Advocate recruitment
- Advocate activity
- Referrals per advocate
- Segment metrics

---

## Pass threshold
**≥75 advocates at 500+**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/advocacy-program`_
