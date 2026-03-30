---
name: trial-to-paid-conversion-scalable
description: >
  Trial-to-Paid Conversion — Scalable Automation. Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Email, Product, Direct"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=50% trial-to-paid conversion rate over 2 months"
kpis: ["Trial conversion rate trend", "Activation funnel completion", "Intervention effectiveness", "Trial length optimization"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add sales/won/trial-to-paid-conversion"
---
# Trial-to-Paid Conversion — Scalable Automation

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Email, Product, Direct

## Overview
Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.

**Time commitment:** 75 hours over 2 months
**Pass threshold:** >=50% trial-to-paid conversion rate over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **n8n** (Automation)
- **Instantly** (Email)

---

## Instructions

1. Scale to 200+ trial users per month; build n8n workflows that trigger based on PostHog events: user completes milestone → send congratulations + next step; user stalls → send help resources; day 10 reached → send upgrade offer.

2. Create personalized trial experiences: use PostHog data to tailor onboarding (if user is Sales role, show sales-specific use cases; if Operations, show ops workflows).

3. Integrate trial activity from PostHog with Attio to auto-score trial health and route high-scoring trials to sales reps for proactive outreach; target >=50% trial conversion rate.

4. Set up PostHog to track trial conversion funnel: trial_started → first_login → activation_milestone_1 → milestone_2 → milestone_3 → trial_converted; identify and fix drop-off points.

5. Build automated trial extension logic: if user is highly engaged (>=2 milestones) but needs more time, offer 7-day extension; if low engaged (<1 milestone), let trial expire to focus resources on engaged users.

6. Implement usage-based upgrade prompts: when trial user hits usage limits (API calls, seats, features), show upgrade prompt: "You're getting great value—upgrade to remove limits."

7. Create a trial performance dashboard in PostHog showing conversion rate by source, activation milestone completion rates, average time to conversion, and cohort performance over time.

8. Each week, analyze why trials don't convert: survey non-converters or review PostHog data to identify friction (onboarding too complex? missing feature? budget not allocated?).

9. Test trial length experiments: use PostHog feature flags to offer 7-day vs 14-day vs 30-day trials to different cohorts; measure which yields highest conversion without excessive support burden.

10. After 2 months, if trial conversion rate >=50% and activation-based interventions show clear ROI, move to Durable; otherwise refine onboarding or intervention triggers.

---

## KPIs to track
- Trial conversion rate trend
- Activation funnel completion
- Intervention effectiveness
- Trial length optimization

---

## Pass threshold
**>=50% trial-to-paid conversion rate over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/trial-to-paid-conversion`_
