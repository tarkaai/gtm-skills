---
name: founder-social-content-smoke
description: >
    Founder Social & Content — Smoke Test. Publish a few posts per week with a clear CTA to see if
  founder-led content drives inbound leads or DMs before scaling.
stage: "Marketing > Unaware"
motion: "Founder Social Content"
channels: "Social"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 leads or ≥ 2 meetings in 1 week"
kpis: ["Impressions", "Engagement rate", "Profile visits"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - icp-definition
  - social-content-pipeline
  - threshold-engine
---
# Founder Social & Content — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Founder Social & Content — Smoke Test. Publish a few posts per week with a clear CTA to see if founder-led content drives inbound leads or DMs before scaling.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 3 leads or ≥ 2 meetings in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your content ICP
Run the `icp-definition` drill to define who you are creating content for. Document: target audience job titles, pain points they search for, platforms they use, content formats they engage with.

### 2. Create a content batch
Run the `social-content-pipeline` drill to create 5-10 pieces of social content. Use the LinkedIn hook frameworks and content templates. Write posts targeting the pain points from your ICP definition. Prepare content for manual posting.

**Human action required:** Post the content manually on LinkedIn/Twitter over 1-2 weeks. Engage with comments and replies personally.

### 3. Track engagement
Log each post's performance: impressions, likes, comments, profile views, DMs received, link clicks. Note which topics and formats got the most engagement.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure results against: ≥ 3 leads or ≥ 2 meetings in 1 week. If PASS, proceed to Baseline. If FAIL, adjust your content topics, hooks, or posting frequency and re-run.

---

## KPIs to track
- Impressions
- Engagement rate
- Profile visits

---

## Pass threshold
**≥ 3 leads or ≥ 2 meetings in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/founder-social-content`_
