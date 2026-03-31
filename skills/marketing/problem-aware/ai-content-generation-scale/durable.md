---
name: ai-content-generation-scale-durable
description: >
  AI Content Generation — Durable Intelligence. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content"
level: "Durable Intelligence"
time: "100 hours over 6 months"
outcome: "Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content strategy optimization and real-time adaptation to market trends"
kpis: ["Organic traffic trend", "Conversion rate", "Content production velocity", "Time on page", "Content refresh rate", "Topic relevance score"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - content-repurposing
  - newsletter-pipeline
  - video-content-pipeline
  - dashboard-builder
  - ab-test-orchestrator
---
# AI Content Generation — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 100 hours over 6 months
**Pass threshold:** Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content strategy optimization and real-time adaptation to market trends

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
- **Anthropic** (AI/LLM)
- **Ghost** (Content)
- **Ahrefs** (Analytics)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: organic traffic patterns shift, competitor content is published, or new high-value keywords emerge.

2. Build n8n AI content strategist agent that analyzes PostHog data weekly: identifies content gaps, trending topics in your ICP, and underperforming posts that need refresh.

3. Implement continuous content experimentation: n8n AI agent tests different content formats, CTAs, and structures; automatically promotes winning formats and retires low-performers.

4. Create market adaptation system: AI agent monitors industry news, competitor blogs, and social conversations; automatically adjusts content calendar to capitalize on trending topics within 24 hours.

5. Build learning loop: PostHog tracks reader journey from first content interaction to conversion; n8n AI analyzes patterns monthly and adjusts content strategy (topics, formats, CTAs) to optimize conversion paths.

6. Deploy AI content refresh agent: identifies posts with declining traffic or outdated information; generates updated content with fresh examples, data, and perspectives; publishes refreshed posts quarterly.

7. Implement automatic content distribution optimization: AI agent analyzes which distribution channels drive best engagement per content type; adjusts cross-posting strategy in real-time.

8. Create competitor intelligence system: n8n monitors top competitor blogs daily via RSS feeds; AI agent identifies content gaps and opportunities; generates briefs for differentiated counter-content within 48 hours.

9. Set guardrails: if organic traffic drops >20% for 2+ weeks or conversion rate falls below Scalable threshold, n8n alerts team and pauses automatic content generation pending review.

10. Establish monthly review cycle: analyze which content experiments succeeded, which topics to retire, which new formats to test; refine AI agent prompts and content strategy based on performance data.

---

## KPIs to track
- Organic traffic trend
- Conversion rate
- Content production velocity
- Time on page
- Content refresh rate
- Topic relevance score

---

## Pass threshold
**Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content strategy optimization and real-time adaptation to market trends**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/ai-content-generation-scale`_
