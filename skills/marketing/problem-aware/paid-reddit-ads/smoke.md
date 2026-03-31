---
name: paid-reddit-ads-smoke
description: >
    Paid Reddit Ads — Smoke Test. Run a small Reddit ad budget across a couple of sets and one LP to
  test if paid community placement drives leads or a meeting.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 2 leads or ≥ 1 meeting in 1 week"
kpis: ["Click-through rate", "Landing page visits"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---
# Paid Reddit Ads — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Paid Reddit Ads — Smoke Test. Run a small Reddit ad budget across a couple of sets and one LP to test if paid community placement drives leads or a meeting.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 2 leads or ≥ 1 meeting in 1 week

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
Run the `threshold-engine` drill to measure against: ≥ 2 leads or ≥ 1 meeting in 1 week. If PASS, proceed to Baseline. If FAIL, diagnose whether the issue is targeting (wrong audience), creative (low CTR), or landing page (low conversion).

---

## KPIs to track
- Click-through rate
- Landing page visits

---

## Pass threshold
**≥ 2 leads or ≥ 1 meeting in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/paid-reddit-ads`_
