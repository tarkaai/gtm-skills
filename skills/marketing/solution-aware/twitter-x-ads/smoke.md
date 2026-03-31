---
name: twitter-x-ads-smoke
description: >
    Twitter/X Ads — Smoke Test. Run promoted tweets and accounts targeting specific audiences,
  keywords, and interests to build awareness and drive traffic from solution-aware users.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥15,000 impressions and ≥5 qualified leads from $200 Twitter test"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---
# Twitter/X Ads — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Twitter/X Ads — Smoke Test. Run promoted tweets and accounts targeting specific audiences, keywords, and interests to build awareness and drive traffic from solution-aware users.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥15,000 impressions and ≥5 qualified leads from $200 Twitter test

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up ad campaign
Run the `ad-campaign-setup` drill to configure your ad platform (Google Ads, LinkedIn Ads, or Meta Ads depending on the play). Set up conversion tracking pixels. Define your target audience using the ICP from your Smoke hypothesis.

### 2. Build a landing page
Run the `landing-page-pipeline` drill to create a dedicated landing page in Webflow for this campaign. Include: clear headline matching the ad copy, social proof, single CTA, and PostHog tracking. Keep the page simple -- one message, one action.

**Human action required:** Set a small test budget ($200-500). Launch the campaign and monitor for 1 week. Do not optimize mid-flight -- let the data accumulate.

### 3. Track results
Monitor: impressions, clicks, CTR, landing page conversion rate, cost per lead, lead quality (are they ICP matches?).

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥15,000 impressions and ≥5 qualified leads from $200 Twitter test. If PASS, proceed to Baseline. If FAIL, diagnose whether the issue is targeting (wrong audience), creative (low CTR), or landing page (low conversion).

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥15,000 impressions and ≥5 qualified leads from $200 Twitter test**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/twitter-x-ads`_
