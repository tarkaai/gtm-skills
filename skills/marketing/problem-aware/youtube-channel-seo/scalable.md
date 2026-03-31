---
name: youtube-channel-seo-scalable
description: >
  YouTube Channel and SEO — Scalable Automation. Create video content optimized for YouTube search and discovery to reach visual learners and build brand authority, from manual uploads to automated production and AI-driven optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "≥10,000 views/month and conversion rate ≥0.8%"
kpis: ["Video views", "Watch time", "CTR on thumbnails", "Referral traffic", "Conversion rate", "Subscriber growth", "Content production velocity"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - content-repurposing
  - newsletter-pipeline
  - posthog-gtm-events
---
# YouTube Channel and SEO — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Overview
Create video content optimized for YouTube search and discovery to reach visual learners and build brand authority, from manual uploads to automated production and AI-driven optimization.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** ≥10,000 views/month and conversion rate ≥0.8%

---

## Budget

**Play-specific tools & costs**
- **Taplio (LinkedIn scheduling + AI assist):** ~$50/mo
- **Buffer or Typefully (cross-platform scheduling):** ~$10–20/mo
- **Descript or Riverside (video/podcast production):** ~$25–50/mo

_Total play-specific: ~$10–50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Descript** (Video)
- **Riverside** (Video)
- **Anthropic** (AI/LLM)

---

## Instructions

1. Scale to 40-60 videos over 2 months; build video production pipeline with repeatable templates for different content types (tutorials, case studies, product demos).

2. Create n8n workflow to automate video optimization: generate SEO-optimized titles and descriptions using AI based on video transcripts; suggest tags and thumbnail text.

3. Use Descript or similar tool for batch editing: auto-remove filler words, add captions, and create social media clips from longer videos.

4. Implement systematic keyword research: n8n workflow fetches trending keywords from YouTube API and TubeBuddy; AI agent generates video topic ideas aligned with search demand.

5. Build content repurposing automation in n8n: when a video is published, automatically generate LinkedIn posts, Twitter threads, and blog post summaries from the transcript.

6. Set up PostHog to track viewer journey: youtube_view → website_visit → signup; create cohorts for viewers who convert vs. those who don't.

7. Connect YouTube Analytics API to PostHog via n8n; create unified dashboard showing views, watch time, referral traffic, and conversions by video.

8. Set guardrails: conversion rate must stay within 20% of Baseline rate; if average view duration drops below 35%, review content pacing and engagement tactics.

9. Use PostHog to identify which video topics and formats drive highest engagement and conversions; prioritize those topics in future production.

10. After 2 months, evaluate total views, watch time, subscriber growth, and conversion ROI; if metrics hold, document the production pipeline and prepare for Durable AI-driven optimization; if metrics decline, reduce production velocity or improve content quality.

---

## KPIs to track
- Video views
- Watch time
- CTR on thumbnails
- Referral traffic
- Conversion rate
- Subscriber growth
- Content production velocity

---

## Pass threshold
**≥10,000 views/month and conversion rate ≥0.8%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/youtube-channel-seo`_
