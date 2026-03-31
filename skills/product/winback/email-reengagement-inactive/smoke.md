---
name: email-reengagement-inactive-smoke
description: >
  Inactive User Re-engagement — Smoke Test. Automated email sequences to win back users who haven't logged in recently with personalized messaging and incentives.
stage: "Product > Winback"
motion: "Lead Capture Surface"
channels: "Email, Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥15% return in 7d"
kpis: ["Email open rate", "Return rate", "Reactivation rate"]
slug: "email-reengagement-inactive"
install: "npx gtm-skills add product/winback/email-reengagement-inactive"
drills:
  - onboarding-flow
  - threshold-engine
---
# Inactive User Re-engagement — Smoke Test

> **Stage:** Product → Winback | **Motion:** Lead Capture Surface | **Channels:** Email, Product

## Overview
Automated email sequences to win back users who haven't logged in recently with personalized messaging and incentives.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** ≥15% return in 7d

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Product Analytics)

---

## Instructions

### 1. Define inactive users in PostHog
Use the `posthog-cohorts` fundamental to create an "Inactive Users" cohort: users who were active 14+ days ago but have not logged in during the last 7 days. Use HogQL:
```sql
SELECT distinct_id FROM persons WHERE last_seen < now() - interval 7 day AND last_seen > now() - interval 90 day
```

### 2. Set up re-engagement tracking
Use the `posthog-custom-events` fundamental to define events: `reengagement_email_sent`, `user_returned`, `reactivation_completed`. These measure whether the email brought them back and whether they performed a meaningful action.

### 3. Write a 3-email re-engagement sequence
Use the `loops-sequences` fundamental to create the sequence:
- **Email 1 (Day 0):** "We noticed you haven't been in -- here's what's new" + link to the product
- **Email 2 (Day 3):** Value-focused: highlight a feature they used before or a new capability
- **Email 3 (Day 7):** Personal note from founder asking if they need help + offer a call

### 4. Send to a small test group
Export 20 inactive users from the PostHog cohort. Send the sequence via Loops. Use the `onboarding-flow` drill patterns for re-onboarding messaging.

### 5. Measure against threshold
Run the `threshold-engine` drill after 7 days:
- **Pass:** ≥ 15% of the 20 users return and log in within 7 days
- Track open rate, return rate, and reactivation rate (performed meaningful action)

### 6. Iterate or proceed
If pass, document the winning sequence and proceed to Baseline with larger cohort. If fail, test different subject lines, different value hooks, or different timing.

---

## KPIs to track
- Email open rate
- Return rate
- Reactivation rate

---

## Pass threshold
**≥15% return in 7d**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/winback/email-reengagement-inactive`_
