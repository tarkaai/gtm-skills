---
name: ai-content-generation-scale-scalable
description: >
  AI Content Generation — Scalable Automation. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥8,000 page views/month and conversion rate ≥1.0%"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity", "Organic traffic growth", "Cost per post"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
---
# AI Content Generation — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 50 hours over 2 months
**Pass threshold:** ≥8,000 page views/month and conversion rate ≥1.0%

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
- **Anthropic** (AI/LLM)
- **Ghost** (Content)
- **Ahrefs** (Analytics)

---

## Instructions

1. Scale to 40-60 posts over 2 months; build content production pipeline in n8n that automates: topic research via Ahrefs API, outline generation, draft creation, and publishing to Ghost CMS.

2. Create n8n workflow that monitors trending topics in your industry (via Reddit API, Twitter API, Google Trends) and automatically generates content briefs for timely articles.

3. Integrate AI content generation into n8n: workflow fetches prompt template, generates draft via Anthropic API, formats for Ghost, and saves to drafts folder for human review.

4. Implement quality control layer: n8n runs generated content through additional AI check for accuracy and brand voice before human review; flag posts that need significant editing.

5. Build automated SEO optimization: n8n extracts target keywords from Ahrefs, ensures keyword placement in title/H1/meta description, and suggests internal link opportunities.

6. Connect PostHog to n8n: when a post reaches ≥500 views, trigger workflow that automatically repurposes content into LinkedIn posts, Twitter threads, and email newsletter snippets.

7. Set guardrails: conversion rate must stay within 20% of Baseline rate; if time on page drops below 1.5 minutes for 3+ consecutive posts, alert team and review AI prompt quality.

8. Use PostHog to track content performance by AI prompt template; identify which templates drive highest engagement and conversions and prioritize those in n8n workflow.

9. After 2 months, analyze content velocity, organic traffic growth, and conversion volume; create ROI model comparing AI content generation cost vs. hiring writers.

10. If metrics hold and ROI is positive, document the n8n pipeline and prepare for Durable agent-driven content strategy; if metrics decline, reduce velocity or enhance human editing.

---

## KPIs to track
- Page views
- Time on page
- Conversion rate
- Content production velocity
- Organic traffic growth
- Cost per post

---

## Pass threshold
**≥8,000 page views/month and conversion rate ≥1.0%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/ai-content-generation-scale`_
