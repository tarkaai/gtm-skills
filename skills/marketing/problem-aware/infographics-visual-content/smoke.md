---
name: infographics-visual-content-smoke
description: >
    Infographics & Visual Content — Smoke Test. Create shareable data visualizations and
  infographics to drive social engagement, backlinks, and brand awareness with problem-aware
  audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥100 impressions and ≥10 shares in 3 days"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "infographics-visual-content"
install: "npx gtm-skills add marketing/problem-aware/infographics-visual-content"
drills:
  - icp-definition
  - social-content-pipeline
  - threshold-engine
---
# Infographics & Visual Content — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content

## Overview
Infographics & Visual Content — Smoke Test. Create shareable data visualizations and infographics to drive social engagement, backlinks, and brand awareness with problem-aware audiences.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥100 impressions and ≥10 shares in 3 days

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
Run the `threshold-engine` drill to measure results against: ≥100 impressions and ≥10 shares in 3 days. If PASS, proceed to Baseline. If FAIL, adjust your content topics, hooks, or posting frequency and re-run.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥100 impressions and ≥10 shares in 3 days**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/infographics-visual-content`_
