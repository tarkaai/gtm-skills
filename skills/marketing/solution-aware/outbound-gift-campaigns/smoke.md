---
name: outbound-gift-campaigns-smoke
description: >
    Outbound Gift Campaigns — Smoke Test. Send physical gifts (books, swag, gift cards) to
  high-value prospects to break through noise and start conversations with solution-aware target
  accounts.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥20% response rate from 20 gift recipients in 2 weeks"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "outbound-gift-campaigns"
install: "npx gtm-skills add marketing/solution-aware/outbound-gift-campaigns"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# Outbound Gift Campaigns — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Outbound Gift Campaigns — Smoke Test. Send physical gifts (books, swag, gift cards) to high-value prospects to break through noise and start conversations with solution-aware target accounts.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥20% response rate from 20 gift recipients in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your ICP and build a target list
Run the `icp-definition` drill to document your Ideal Customer Profile for outbound-gift-campaigns. Define company size, industry, job titles, and pain points. Then run the `build-prospect-list` drill to source 20-50 contacts matching this ICP from Clay. Export the list to Attio CRM.

### 2. Prepare outreach materials
Using the ICP output, draft your outbound-gift-campaigns materials manually. Write 2-3 variants of your core message targeting the specific pain points identified. Keep it scrappy -- this is a Smoke test to validate the channel, not to optimize.

**Human action required:** Execute the outreach manually. Send messages, make calls, or run the micro-campaign by hand. Log every touchpoint in Attio with status and response.

### 3. Track results
For each interaction, log the outcome in Attio (replied, meeting booked, ignored, bounced). Note which message variant and which ICP segment performed best.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to evaluate results against your pass threshold: ≥20% response rate from 20 gift recipients in 2 weeks. The threshold engine will pull your logged data from Attio and PostHog, compare against the target, and return PASS or FAIL.

If PASS, proceed to the Baseline level. If FAIL, adjust your ICP, messaging, or targeting and re-run this Smoke test.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥20% response rate from 20 gift recipients in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-gift-campaigns`_
