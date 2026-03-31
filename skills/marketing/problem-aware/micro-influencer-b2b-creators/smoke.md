---
name: micro-influencer-b2b-creators-smoke
description: >
    Micro-Influencer B2B Post — Smoke Test. Pay for one post or story from a B2B creator to test if
  creator-led shoutouts drive a couple of leads before trying other creators or topics.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 lead in 1 week"
kpis: ["Post reach", "Engagement rate"]
slug: "micro-influencer-b2b-creators"
install: "npx gtm-skills add marketing/problem-aware/micro-influencer-b2b-creators"
drills:
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---
# Micro-Influencer B2B Post — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Micro-Influencer B2B Post — Smoke Test. Pay for one post or story from a B2B creator to test if creator-led shoutouts drive a couple of leads before trying other creators or topics.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 1 lead in 1 week

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
Run the `threshold-engine` drill to measure against: ≥ 1 lead in 1 week. If PASS, proceed to Baseline. If FAIL, diagnose whether the issue is targeting (wrong audience), creative (low CTR), or landing page (low conversion).

---

## KPIs to track
- Post reach
- Engagement rate

---

## Pass threshold
**≥ 1 lead in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/micro-influencer-b2b-creators`_
