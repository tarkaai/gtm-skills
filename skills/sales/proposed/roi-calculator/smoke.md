---
name: roi-calculator-smoke
description: >
    ROI Calculator & Business Case — Smoke Test. Quantify and demonstrate ROI to justify purchase
  decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic
  business case generation that personalizes value narratives and auto-updates based on prospect
  data and market benchmarks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week"
kpis: ["ROI value distribution", "Payback period", "ROI validation rate", "ROI impact on deal velocity"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# ROI Calculator & Business Case — Smoke Test

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Overview
ROI Calculator & Business Case — Smoke Test. Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your ICP and build a target list
Run the `icp-definition` drill to document your Ideal Customer Profile for roi-calculator. Define company size, industry, job titles, and pain points. Then run the `build-prospect-list` drill to source 20-50 contacts matching this ICP from Clay. Export the list to Attio CRM.

### 2. Prepare outreach materials
Using the ICP output, draft your roi-calculator materials manually. Write 2-3 variants of your core message targeting the specific pain points identified. Keep it scrappy -- this is a Smoke test to validate the channel, not to optimize.

**Human action required:** Execute the outreach manually. Send messages, make calls, or run the micro-campaign by hand. Log every touchpoint in Attio with status and response.

### 3. Track results
For each interaction, log the outcome in Attio (replied, meeting booked, ignored, bounced). Note which message variant and which ICP segment performed best.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to evaluate results against your pass threshold: >=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week. The threshold engine will pull your logged data from Attio and PostHog, compare against the target, and return PASS or FAIL.

If PASS, proceed to the Baseline level. If FAIL, adjust your ICP, messaging, or targeting and re-run this Smoke test.

---

## KPIs to track
- ROI value distribution
- Payback period
- ROI validation rate
- ROI impact on deal velocity

---

## Pass threshold
**>=5 prospects with >=5x ROI calculated and >=3 reference ROI in decisions within 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/roi-calculator`_
