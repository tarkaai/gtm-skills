---
name: youtube-channel-seo-durable
description: >
  YouTube Channel and SEO — Durable Intelligence. Create video content optimized for YouTube search and discovery to reach visual learners and build brand authority, from manual uploads to automated production and AI-driven optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Durable Intelligence"
time: "100 hours over 6 months"
outcome: "Sustained or improving video views and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to platform trends"
kpis: ["Video views trend", "Watch time trend", "CTR on thumbnails", "Conversion rate", "Subscriber growth rate", "Content relevance score"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
---
# YouTube Channel and SEO — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Overview
Create video content optimized for YouTube search and discovery to reach visual learners and build brand authority, from manual uploads to automated production and AI-driven optimization.

**Time commitment:** 100 hours over 6 months
**Pass threshold:** Sustained or improving video views and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to platform trends

---

## Budget

**Play-specific tools & costs**
- **Taplio (analytics + AI content engine):** ~$50/mo
- **Buffer or Typefully:** ~$10–20/mo
- **Descript or Loom (repurposing content to video):** ~$15–30/mo

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

1. Deploy PostHog event streams that trigger n8n AI agents when: video performance deviates from benchmarks, new trending topics emerge, or viewer drop-off patterns change.

2. Build n8n AI content strategist for YouTube that analyzes video performance weekly: identifies underperforming videos, trending topics in your niche, and optimal video formats by watch time.

3. Implement continuous video experimentation: AI agent tests different thumbnail styles, title formats, video lengths, and intro hooks; automatically promotes winning patterns to future videos.

4. Create market adaptation system: AI agent monitors YouTube trends, competitor channels, and search demand shifts; adjusts content calendar to capitalize on emerging topics within 48 hours.

5. Build learning loop: PostHog tracks complete viewer journey from video view to conversion; AI agent analyzes which video topics, CTAs, and link placements drive highest conversion rates; optimizes accordingly.

6. Deploy AI video refresh agent: identifies videos with declining views or outdated content; generates updated scripts with fresh examples and data; schedules re-recordings or annotation updates.

7. Implement automatic A/B testing for thumbnails and titles: AI agent generates variants for new uploads; YouTube's built-in A/B test tool tests them; agent analyzes results and applies winning principles to future videos.

8. Create competitor intelligence system: n8n monitors top competitor channels via YouTube API; AI agent identifies content gaps and high-performing video types; generates video briefs for differentiated counter-content.

9. Set guardrails: if video views drop >20% for 2+ weeks or conversion rate falls below Scalable threshold, n8n alerts team and pauses automatic content changes pending review.

10. Establish monthly review cycle: analyze which video experiments succeeded, which topics to expand, which formats to retire; refine AI agent prompts and content strategy based on performance data.

---

## KPIs to track
- Video views trend
- Watch time trend
- CTR on thumbnails
- Conversion rate
- Subscriber growth rate
- Content relevance score

---

## Pass threshold
**Sustained or improving video views and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to platform trends**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/youtube-channel-seo`_
