---
name: founder-guest-podcasts-smoke
description: >
    Founder Guest Podcast — Smoke Test. Pitch a handful of micro podcasts for one guest spot to test
  whether podcast exposure drives at least one inbound lead.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 inbound lead in 1 week"
kpis: ["Podcast listens", "Referral traffic"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - icp-definition
  - blog-seo-pipeline
  - threshold-engine
---
# Founder Guest Podcast — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Overview
Founder Guest Podcast — Smoke Test. Pitch a handful of micro podcasts for one guest spot to test whether podcast exposure drives at least one inbound lead.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 1 inbound lead in 1 week

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
Run the `threshold-engine` drill to measure against: ≥ 1 inbound lead in 1 week. If PASS, proceed to Baseline. If FAIL, refine your angles or target different publications.

---

## KPIs to track
- Podcast listens
- Referral traffic

---

## Pass threshold
**≥ 1 inbound lead in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/founder-guest-podcasts`_
