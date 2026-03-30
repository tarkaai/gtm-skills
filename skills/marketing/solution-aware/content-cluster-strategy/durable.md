---
name: content-cluster-strategy-durable
description: >
  Content Cluster Strategy — Durable Intelligence. Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "110 hours over 6 months"
outcome: "Sustained or improving organic traffic and topical authority over 6 months via continuous AI-driven cluster optimization and market-responsive content expansion"
kpis: ["Organic traffic trend", "Keyword ranking distribution", "Topical authority score", "Internal link CTR", "Conversion rate", "Cluster refresh velocity"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
---
# Content Cluster Strategy — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.

**Time commitment:** 110 hours over 6 months
**Pass threshold:** Sustained or improving organic traffic and topical authority over 6 months via continuous AI-driven cluster optimization and market-responsive content expansion

---

## Budget

**Play-specific tools & costs**
- **Webflow:** ~$15–40/mo
- **Hotjar or FullStory:** ~$30–100/mo

_Total play-specific: ~$15–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Ghost** (Content)
- **Anthropic** (AI/LLM)
- **Ahrefs** (Analytics)
- **Google Search Console** (Analytics)

---

## Instructions

1. Set up PostHog event streams that trigger n8n AI agents when: new topic opportunities emerge, cluster performance degrades, or competitor clusters are detected.

2. Build n8n AI cluster strategist agent that analyzes Search Console and PostHog data weekly: identifies underperforming clusters, content gaps within clusters, and new cluster opportunities.

3. Implement continuous cluster experimentation: AI agent tests different cluster structures (hub-and-spoke, matrix, hierarchical), automatically promotes winning patterns.

4. Create automatic cluster expansion: when a pillar page ranks in top 10, AI agent identifies related long-tail keywords and generates additional cluster pages to strengthen topical authority.

5. Deploy AI internal linking optimizer: analyzes PostHog navigation data to identify underutilized links, suggests new link placements, and automatically updates pages with high-value links.

6. Build cluster refresh system: AI agent monitors content freshness, identifies stale statistics or examples, and generates updated sections for pillar and cluster pages quarterly.

7. Implement competitor cluster tracking: n8n monitors competitor pillar pages via Ahrefs API; AI agent identifies their cluster structure and suggests counter-clusters or gap-filling content.

8. Create learning loop: PostHog tracks user journey through clusters to conversion; AI agent analyzes successful paths monthly and adjusts cluster linking and CTA placement to optimize conversion funnels.

9. Set guardrails: if organic traffic drops >20% for any cluster for 2+ weeks, n8n alerts team and the agent suggests content refresh or structure optimization.

10. Establish monthly review cycle: analyze which cluster experiments succeeded, which topics to expand, which structures to replicate; refine AI agent prompts and cluster strategy based on ranking and conversion data.

---

## KPIs to track
- Organic traffic trend
- Keyword ranking distribution
- Topical authority score
- Internal link CTR
- Conversion rate
- Cluster refresh velocity

---

## Pass threshold
**Sustained or improving organic traffic and topical authority over 6 months via continuous AI-driven cluster optimization and market-responsive content expansion**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/content-cluster-strategy`_
