---
name: youtube-channel-seo-baseline
description: >
    YouTube Channel and SEO — Baseline Run. Create video content optimized for YouTube search and
  discovery to reach visual learners and build brand authority, from manual uploads to automated
  production and AI-driven optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Baseline Run"
time: "35 hours over 8 weeks"
outcome: "≥3,000 views and ≥25 conversions over 8 weeks"
kpis: ["Video views", "Watch time", "CTR on thumbnails", "Referral traffic", "Conversion rate", "Subscriber growth"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# YouTube Channel and SEO — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Overview
YouTube Channel and SEO — Baseline Run. Create video content optimized for YouTube search and discovery to reach visual learners and build brand authority, from manual uploads to automated production and AI-driven optimization.

**Time commitment:** 35 hours over 8 weeks
**Pass threshold:** ≥3,000 views and ≥25 conversions over 8 weeks

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
Run the `posthog-gtm-events` drill to track content performance events: `youtube-channel-seo_post_published`, `youtube-channel-seo_engagement_received`, `youtube-channel-seo_profile_visit`, `youtube-channel-seo_dm_received`, `youtube-channel-seo_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥3,000 views and ≥25 conversions over 8 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Video views
- Watch time
- CTR on thumbnails
- Referral traffic
- Conversion rate
- Subscriber growth

---

## Pass threshold
**≥3,000 views and ≥25 conversions over 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/youtube-channel-seo`_
