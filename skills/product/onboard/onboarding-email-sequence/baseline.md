---
name: onboarding-email-sequence-baseline
description: >
    Onboarding email sequence — Baseline Run. Automated email sequence for new signups to activate
  and retain users.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "Early retention ≥ 40% at day 7 over 2 weeks"
kpis: ["Open rate", "Click rate", "Time to first key action"]
slug: "onboarding-email-sequence"
install: "npx gtm-skills add product/onboard/onboarding-email-sequence"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Onboarding email sequence — Baseline Run

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Email

## Overview
Onboarding email sequence — Baseline Run. Automated email sequence for new signups to activate and retain users.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** Early retention ≥ 40% at day 7 over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `onboarding-email-sequence_impression`, `onboarding-email-sequence_engaged`, `onboarding-email-sequence_converted`, `onboarding-email-sequence_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: Early retention ≥ 40% at day 7 over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Open rate
- Click rate
- Time to first key action

---

## Pass threshold
**Early retention ≥ 40% at day 7 over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/onboarding-email-sequence`_
