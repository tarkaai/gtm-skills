---
name: demo-follow-up-sequence-smoke
description: >
    Demo Follow-Up Sequence — Smoke Test. Structured multi-touch follow-up after demos delivering
  recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate
  deals.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: "Demo follow-up completed on ≥8 opportunities in 2 weeks"
kpis: ["Follow-up completion rate", "Response rate", "Next step scheduling rate", "Content engagement"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# Demo Follow-Up Sequence — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Demo Follow-Up Sequence — Smoke Test. Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.

**Time commitment:** 6 hours over 2 weeks
**Pass threshold:** Demo follow-up completed on ≥8 opportunities in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your ICP and build a target list
Run the `icp-definition` drill to document your Ideal Customer Profile for demo-follow-up-sequence. Define company size, industry, job titles, and pain points. Then run the `build-prospect-list` drill to source 20-50 contacts matching this ICP from Clay. Export the list to Attio CRM.

### 2. Prepare outreach materials
Using the ICP output, draft your demo-follow-up-sequence materials manually. Write 2-3 variants of your core message targeting the specific pain points identified. Keep it scrappy -- this is a Smoke test to validate the channel, not to optimize.

**Human action required:** Execute the outreach manually. Send messages, make calls, or run the micro-campaign by hand. Log every touchpoint in Attio with status and response.

### 3. Track results
For each interaction, log the outcome in Attio (replied, meeting booked, ignored, bounced). Note which message variant and which ICP segment performed best.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to evaluate results against your pass threshold: Demo follow-up completed on ≥8 opportunities in 2 weeks. The threshold engine will pull your logged data from Attio and PostHog, compare against the target, and return PASS or FAIL.

If PASS, proceed to the Baseline level. If FAIL, adjust your ICP, messaging, or targeting and re-run this Smoke test.

---

## KPIs to track
- Follow-up completion rate
- Response rate
- Next step scheduling rate
- Content engagement

---

## Pass threshold
**Demo follow-up completed on ≥8 opportunities in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-follow-up-sequence`_
