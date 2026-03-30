---
name: content-cluster-strategy-scalable
description: >
  Content Cluster Strategy — Scalable Automation. Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: "≥12,000 page views/month and conversion rate ≥1.0%"
kpis: ["Organic traffic to clusters", "Internal link CTR", "Conversion rate", "Average position", "Cluster coverage", "Keyword ranking distribution"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
---
# Content Cluster Strategy — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** ≥12,000 page views/month and conversion rate ≥1.0%

---

## Budget

**Play-specific tools & costs**
- **Webflow (landing page optimization):** ~$15–40/mo
- **Hotjar (session recording + heatmaps):** ~$30/mo

_Total play-specific: ~$15–40/mo_

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

1. Scale to 10-12 content clusters covering your core topic areas; build automated cluster production pipeline in n8n.

2. Create n8n workflow that: fetches keyword clusters from Ahrefs API, generates content briefs using AI, produces drafts via Anthropic API, and publishes to Ghost CMS.

3. Build automatic internal linking system in n8n: analyze semantic similarity between pages, automatically insert contextual internal links, and update existing pages with links to new cluster content.

4. Generate 80-100 total pages (10-12 pillars + 70-90 clusters) over 2 months; ensure consistent quality through AI editing and human review of pillar pages.

5. Implement cluster performance tracking: PostHog dashboard showing traffic, conversions, and internal navigation patterns for each cluster.

6. Connect Google Search Console to n8n: automatically track keyword rankings for all pillar and cluster keywords; alert when rankings drop >5 positions.

7. Set guardrails: conversion rate must stay within 20% of Baseline rate; if internal link CTR drops below 30%, review and enhance link anchor text and placement.

8. Use PostHog to identify highest-performing clusters by conversion rate; allocate more cluster pages to top-performing topics in subsequent iterations.

9. After 2 months, evaluate total organic traffic, ranking improvements, and ROI; create prioritization model for new cluster topics based on search volume and conversion potential.

10. If metrics hold, document automated cluster pipeline and prepare for Durable agent-driven cluster optimization; if metrics decline, refine AI content quality or reduce production velocity.

---

## KPIs to track
- Organic traffic to clusters
- Internal link CTR
- Conversion rate
- Average position
- Cluster coverage
- Keyword ranking distribution

---

## Pass threshold
**≥12,000 page views/month and conversion rate ≥1.0%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/content-cluster-strategy`_
