---
name: pr-campaign-launch-smoke
description: >
    PR Campaign Launch — Smoke Test. Coordinated press outreach for product launches or milestones
  to generate media coverage and awareness with problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥3 press mentions and ≥5 qualified leads from first PR push"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - icp-definition
  - blog-seo-pipeline
  - threshold-engine
---
# PR Campaign Launch — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
PR Campaign Launch — Smoke Test. Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥3 press mentions and ≥5 qualified leads from first PR push

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define your PR angle
Run the `icp-definition` drill to define your target media audience: which publications your ICP reads, which journalists cover your space, what story angles would resonate. List 10-20 target publications and journalists.

### 2. Create foundational content
Run the `blog-seo-pipeline` drill to create 2-3 high-quality content pieces that can serve as PR assets: data-driven blog posts, original research, or expert commentary. These give journalists something to reference and link to.

**Human action required:** Pitch journalists and publications directly. Personalize each pitch with why this is relevant to their beat. Offer exclusive data or quotes. Log all outreach in Attio.

### 3. Track media outreach
Log every pitch: publication, journalist, angle, status (pitched, responded, published, linked). Track resulting coverage: mentions, backlinks, referral traffic.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥3 press mentions and ≥5 qualified leads from first PR push. If PASS, proceed to Baseline. If FAIL, refine your angles or target different publications.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥3 press mentions and ≥5 qualified leads from first PR push**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/pr-campaign-launch`_
