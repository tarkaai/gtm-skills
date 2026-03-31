---
name: podcast-launch-distribution-baseline
description: >
    Branded Podcast Launch — Baseline Run. Launch and distribute a branded podcast to build
  awareness, generate inbound interest, and establish thought leadership with problem-aware and
  solution-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥500 downloads/episode and ≥10 qualified leads from first 10 episodes over 10 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Branded Podcast Launch — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Overview
Branded Podcast Launch — Baseline Run. Launch and distribute a branded podcast to build awareness, generate inbound interest, and establish thought leadership with problem-aware and solution-aware audiences.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥500 downloads/episode and ≥10 qualified leads from first 10 episodes over 10 weeks

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
Run the `posthog-gtm-events` drill to track content performance events: `podcast-launch-distribution_post_published`, `podcast-launch-distribution_engagement_received`, `podcast-launch-distribution_profile_visit`, `podcast-launch-distribution_dm_received`, `podcast-launch-distribution_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥500 downloads/episode and ≥10 qualified leads from first 10 episodes over 10 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥500 downloads/episode and ≥10 qualified leads from first 10 episodes over 10 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/podcast-launch-distribution`_
