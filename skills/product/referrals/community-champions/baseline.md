---
name: community-champions-baseline
description: >
    Champion Recognition Program — Baseline Run. Identify and empower community leaders with
  exclusive access, recognition, and co-marketing opportunities.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥20 champions, ≥5 referrals each"
kpis: ["Champion identification", "Champion activity", "Referrals generated"]
slug: "community-champions"
install: "npx gtm-skills add product/referrals/community-champions"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---
# Champion Recognition Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Overview
Champion Recognition Program — Baseline Run. Identify and empower community leaders with exclusive access, recognition, and co-marketing opportunities.

**Time commitment:** 16 hours over 2 weeks
**Pass threshold:** ≥20 champions, ≥5 referrals each

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `community-champions_impression`, `community-champions_engaged`, `community-champions_converted`, `community-champions_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: ≥20 champions, ≥5 referrals each. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point.

---

## KPIs to track
- Champion identification
- Champion activity
- Referrals generated

---

## Pass threshold
**≥20 champions, ≥5 referrals each**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/community-champions`_
