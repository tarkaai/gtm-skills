---
name: programmatic-seo-pages-durable
description: >
  Programmatic SEO Pages — Durable Intelligence. Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.
stage: "Marketing > Problem Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to search algorithm changes"
kpis: ["Organic traffic trend", "Pages indexed", "Conversion rate", "Average position", "Click-through rate", "Content refresh velocity", "Ranking stability"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
  - churn-prevention
  - dashboard-builder
---
# Programmatic SEO Pages — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.

**Time commitment:** 120 hours over 6 months
**Pass threshold:** Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to search algorithm changes

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
- **Webflow** (Content)
- **Ahrefs** (Analytics)
- **OpenAI** (AI/LLM)
- **Anthropic** (AI/LLM)
- **Google Search Console** (Analytics)

---

## Instructions

1. Set up PostHog event streams that trigger n8n AI workflows when new high-opportunity keywords are discovered or when existing pages drop in rankings.

2. Build n8n AI agent that monitors Google Search Console API daily for ranking changes, identifies pages that dropped >5 positions, and automatically generates content refresh suggestions.

3. Create continuous A/B testing framework in PostHog to test page variations: different CTAs, content structures, internal linking patterns; n8n automatically implements winning variants.

4. Deploy AI agent that analyzes top-performing competitor pages for target keywords; generates improved content outlines and suggests page enhancements based on gap analysis.

5. Implement automatic keyword expansion: n8n workflow uses Ahrefs API + AI to discover new long-tail variations weekly, generates pages for high-opportunity keywords automatically.

6. Set up learning loop: PostHog tracks conversion performance by page template and topic; n8n AI analyzes patterns monthly and adjusts content generation strategy to prioritize high-converting templates.

7. Build market adaptation system: when Google algorithm updates are detected (via Search Console volatility), n8n triggers content audits and adjusts page generation parameters to maintain rankings.

8. Create automatic content refresh cycle: n8n AI identifies pages with declining traffic, generates updated content with fresh data/examples, and publishes updates quarterly.

9. Implement guardrails: if organic traffic drops >20% for 2+ weeks or conversion rate falls below Scalable threshold, n8n alerts team and pauses automatic changes pending review.

10. Establish monthly review cycle: analyze what experiments succeeded, which page templates to retire, which new content types to test; refine AI agent prompts and automation logic based on learnings.

---

## KPIs to track
- Organic traffic trend
- Pages indexed
- Conversion rate
- Average position
- Click-through rate
- Content refresh velocity
- Ranking stability

---

## Pass threshold
**Sustained or improving organic traffic and conversion rate over 6 months via continuous AI-driven content optimization and adaptation to search algorithm changes**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/programmatic-seo-pages`_
