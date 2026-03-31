---
name: ai-content-generation-scale-durable
description: >
    AI Content Generation — Durable Intelligence. Use AI to create high-quality blog posts, guides,
  and educational content at scale, from manual prompt refinement through structured content
  pipelines to agent-driven continuous content strategy optimization.
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
  - dashboard-builder
---
# AI Content Generation — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
AI Content Generation — Durable Intelligence. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 100 hours over 6 months
**Pass threshold:** Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content strategy optimization and real-time adaptation to market trends

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build performance dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard tracking: weekly impressions trend, engagement rate by content pillar, follower growth rate, DMs and leads from content, content-attributed pipeline value. Set alerts for engagement rate drops.

### 2. Autonomous content optimization
Configure the agent to: monitor which content pillars are trending up or down, suggest retirement of underperforming topics, propose new topics based on ICP pain point research, and auto-generate content briefs for the next week based on what performed best.

### 3. Run monthly content reviews
The agent generates a monthly report: top-performing posts, engagement trends, audience growth, content-to-pipeline attribution. Review and approve the next month's content strategy.

### 4. Evaluate sustainability
Measure against: Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content strategy optimization and real-time adaptation to market trends. This level runs continuously. If engagement sustains or grows, the play is durable. If engagement decays, test new content formats or platforms.

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
