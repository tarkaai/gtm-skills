---
name: linkedin-founder-threads-baseline
description: >
    Founder LinkedIn content — Baseline Run. Founder-led LinkedIn posts and short video with clear
  CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and
  agent-driven optimization that sustains or improves lead volume over time.
stage: "Marketing > Unaware"
motion: "Founder Social Content"
channels: "Social"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 5 inbound leads over 2 weeks"
kpis: ["Impressions", "Engagement rate", "Profile visits", "CTA clicks"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Founder LinkedIn content — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Founder LinkedIn content — Baseline Run. Founder-led LinkedIn posts and short video with clear CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and agent-driven optimization that sustains or improves lead volume over time.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 5 inbound leads over 2 weeks

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
Run the `posthog-gtm-events` drill to track content performance events: `linkedin-founder-threads_post_published`, `linkedin-founder-threads_engagement_received`, `linkedin-founder-threads_profile_visit`, `linkedin-founder-threads_dm_received`, `linkedin-founder-threads_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥ 5 inbound leads over 2 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Impressions
- Engagement rate
- Profile visits
- CTA clicks

---

## Pass threshold
**≥ 5 inbound leads over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/linkedin-founder-threads`_
