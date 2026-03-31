---
name: communities-slack-discord-baseline
description: >
    Slack/Discord Community Rhythm — Baseline Run. Join a few groups and post value weekly to test
  repeatable leads and whether to scale or pause low-signal communities.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Communities"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2 meetings over 2 weeks"
kpis: ["Engagement rate", "Inbound inquiries"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - posthog-gtm-events
  - content-repurposing
---
# Slack/Discord Community Rhythm — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Communities

## Overview
Slack/Discord Community Rhythm — Baseline Run. Join a few groups and post value weekly to test repeatable leads and whether to scale or pause low-signal communities.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 2 meetings over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up analytics
Run the `posthog-gtm-events` drill to track community-driven traffic and conversions: `communities-slack-discord_community_post`, `communities-slack-discord_referral_visit`, `communities-slack-discord_signup_from_community`. Use UTM parameters on all shared links to attribute traffic to specific communities.

### 2. Build a content repurposing system
Run the `content-repurposing` drill to adapt your best-performing community content across multiple communities and formats. One detailed answer can become a Reddit post, a Slack thread, a blog post, and a Twitter thread.

### 3. Execute a 2-week community engagement plan
Post 2-3 times per week across your top communities. Track everything in PostHog. Focus on communities that showed traction in Smoke.

### 4. Evaluate against threshold
Measure against: ≥ 2 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, narrow focus to fewer communities or try different content types.

---

## KPIs to track
- Engagement rate
- Inbound inquiries

---

## Pass threshold
**≥ 2 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/communities-slack-discord`_
