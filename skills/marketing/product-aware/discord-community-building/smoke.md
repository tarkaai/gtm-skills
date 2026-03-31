---
name: discord-community-building-smoke
description: >
    Discord Community Management — Smoke Test. Build and nurture a Discord server to engage users,
  provide support, and generate product-aware leads through authentic community interaction.
stage: "Marketing > Product Aware"
motion: "Communities & Forums"
channels: "Communities, Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥50 members and ≥5 daily active users in 2 weeks"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - icp-definition
  - social-content-pipeline
  - threshold-engine
---
# Discord Community Management — Smoke Test

> **Stage:** Marketing → Product Aware | **Motion:** Communities & Forums | **Channels:** Communities, Product

## Overview
Discord Community Management — Smoke Test. Build and nurture a Discord server to engage users, provide support, and generate product-aware leads through authentic community interaction.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥50 members and ≥5 daily active users in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Identify target communities
Run the `icp-definition` drill to map where your ICP spends time: Slack communities, Discord servers, Reddit subreddits, forums, Facebook groups. List 5-10 communities ranked by relevance and activity level.

### 2. Create valuable content for communities
Run the `social-content-pipeline` drill to create 5-10 pieces of community-appropriate content: helpful answers, resource shares, discussion starters, case studies. Avoid promotional content -- focus on being genuinely useful.

**Human action required:** Join the communities and post content manually. Engage authentically in discussions. Build reputation before mentioning your product. Log all activity in Attio.

### 3. Track community engagement
Log each interaction: post/comment, community name, engagement received, DMs or follows generated, any leads captured. Note which communities and content types generate the most interest.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥50 members and ≥5 daily active users in 2 weeks. If PASS, proceed to Baseline. If FAIL, try different communities or adjust your content approach.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥50 members and ≥5 daily active users in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/discord-community-building`_
