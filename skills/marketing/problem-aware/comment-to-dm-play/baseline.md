---
name: comment-to-dm-play-baseline
description: >
    Comment-to-DM Play — Baseline Run. Leave thoughtful comments in relevant threads for a few days,
  then soft CTA into DMs to test whether earned engagement turns into conversations and meetings.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 15 DMs and ≥ 2 meetings over 2 weeks"
kpis: ["Comment engagement", "Profile visits"]
slug: "comment-to-dm-play"
install: "npx gtm-skills add marketing/problem-aware/comment-to-dm-play"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Comment-to-DM Play — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Comment-to-DM Play — Baseline Run. Leave thoughtful comments in relevant threads for a few days, then soft CTA into DMs to test whether earned engagement turns into conversations and meetings.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 15 DMs and ≥ 2 meetings over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up content repurposing
Run the `content-repurposing` drill to build a system that takes each piece of content and adapts it across formats: LinkedIn post to Twitter thread, blog post to newsletter, video clip to social post. This multiplies your content output without multiplying effort.

### 2. Configure analytics tracking
Run the `posthog-gtm-events` drill to track content performance events: `comment-to-dm-play_post_published`, `comment-to-dm-play_engagement_received`, `comment-to-dm-play_profile_visit`, `comment-to-dm-play_dm_received`, `comment-to-dm-play_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥ 15 DMs and ≥ 2 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Comment engagement
- Profile visits

---

## Pass threshold
**≥ 15 DMs and ≥ 2 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/comment-to-dm-play`_
