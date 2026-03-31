---
name: intent-signal-tracking-smoke
description: >
    Intent Signal Tracking — Smoke Test. Monitor and act on buyer intent signals like website
  behavior, content consumption, and G2 research to reach prospects at peak buying moment, from
  manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers
  personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week"
kpis: ["Intent signals per day", "Reply rate (intent vs non-intent)", "Time from signal to outreach"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# Intent Signal Tracking — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Intent Signal Tracking — Smoke Test. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** >=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your ICP and build a target list
Run the `icp-definition` drill to document your Ideal Customer Profile for intent-signal-tracking. Define company size, industry, job titles, and pain points. Then run the `build-prospect-list` drill to source 20-50 contacts matching this ICP from Clay. Export the list to Attio CRM.

### 2. Prepare outreach materials
Using the ICP output, draft your intent-signal-tracking materials manually. Write 2-3 variants of your core message targeting the specific pain points identified. Keep it scrappy -- this is a Smoke test to validate the channel, not to optimize.

**Human action required:** Execute the outreach manually. Send messages, make calls, or run the micro-campaign by hand. Log every touchpoint in Attio with status and response.

### 3. Track results
For each interaction, log the outcome in Attio (replied, meeting booked, ignored, bounced). Note which message variant and which ICP segment performed best.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to evaluate results against your pass threshold: >=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week. The threshold engine will pull your logged data from Attio and PostHog, compare against the target, and return PASS or FAIL.

If PASS, proceed to the Baseline level. If FAIL, adjust your ICP, messaging, or targeting and re-run this Smoke test.

---

## KPIs to track
- Intent signals per day
- Reply rate (intent vs non-intent)
- Time from signal to outreach

---

## Pass threshold
**>=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
