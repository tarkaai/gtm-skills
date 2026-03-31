---
name: thought-leadership-program-baseline
description: >
    Thought Leadership Program — Baseline Run. Systematic approach to building founder or executive
  as recognized thought leader to attract inbound interest from problem-aware and solution-aware
  audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content, Events"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥15 thought pieces, ≥2 speaking slots, and ≥20 qualified leads in 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Thought Leadership Program — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content, Events

## Overview
Thought Leadership Program — Baseline Run. Systematic approach to building founder or executive as recognized thought leader to attract inbound interest from problem-aware and solution-aware audiences.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥15 thought pieces, ≥2 speaking slots, and ≥20 qualified leads in 8 weeks

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
Run the `posthog-gtm-events` drill to track content performance events: `thought-leadership-program_post_published`, `thought-leadership-program_engagement_received`, `thought-leadership-program_profile_visit`, `thought-leadership-program_dm_received`, `thought-leadership-program_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥15 thought pieces, ≥2 speaking slots, and ≥20 qualified leads in 8 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥15 thought pieces, ≥2 speaking slots, and ≥20 qualified leads in 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/thought-leadership-program`_
