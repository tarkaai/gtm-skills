---
name: reddit-ama-series-smoke
description: >
    Reddit AMA Series — Smoke Test. Host Ask Me Anything sessions on relevant subreddits to build
  brand awareness, engage community, and generate inbound interest from problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Communities, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥200 upvotes and ≥5 qualified leads from first AMA"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - icp-definition
  - social-content-pipeline
  - threshold-engine
---
# Reddit AMA Series — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Communities, Social

## Overview
Reddit AMA Series — Smoke Test. Host Ask Me Anything sessions on relevant subreddits to build brand awareness, engage community, and generate inbound interest from problem-aware audiences.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥200 upvotes and ≥5 qualified leads from first AMA

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
Run the `threshold-engine` drill to measure against: ≥200 upvotes and ≥5 qualified leads from first AMA. If PASS, proceed to Baseline. If FAIL, try different communities or adjust your content approach.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥200 upvotes and ≥5 qualified leads from first AMA**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/reddit-ama-series`_
