---
name: comparison-alternative-pages-scalable
description: >
  Comparison and Alternative Pages — Scalable Automation. Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥5,000 page views/month and conversion rate ≥1.0%"
kpis: ["Organic traffic to comparison pages", "Conversion rate", "Keyword ranking distribution", "CTA click rate", "Competitor keyword coverage"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
---
# Comparison and Alternative Pages — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥5,000 page views/month and conversion rate ≥1.0%

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
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)
- **Google Search Console** (Analytics)

---

## Instructions

1. Scale to 50-80 comparison pages covering all significant competitors, adjacent categories, and long-tail variations (e.g., "Best X for [vertical/use case]").

2. Build automated competitor intelligence pipeline in n8n: fetch competitor data from G2 API, Crunchbase, and web scraping; maintain up-to-date competitive database.

3. Create n8n workflow to generate comparison pages: fetch competitor data, use AI to generate page content (feature tables, pros/cons, recommendations), format for CMS, and publish to staging.

4. Implement automatic feature comparison updates: n8n monitors competitor product pages and changelogs; when features change, AI agent updates comparison tables and notifies team.

5. Build SEO optimization automation: n8n extracts target keywords from Ahrefs, ensures keyword placement in titles/descriptions, and suggests internal link opportunities.

6. Connect PostHog to n8n: when a comparison page reaches ≥300 views, trigger workflow to create supporting content (LinkedIn posts, email sequences) to amplify traffic.

7. Set guardrails: conversion rate must stay within 20% of Baseline rate; if organic traffic to comparison pages drops >15% week-over-week for 2+ weeks, alert team.

8. Use PostHog to track user journeys from comparison pages to signup; identify which competitor pages and CTAs drive highest conversion rates.

9. After 2 months, evaluate total organic traffic to comparison pages, keyword rankings, and conversion volume; calculate ROI vs. paid competitor campaigns.

10. If metrics hold, document the automated pipeline and prepare for Durable agent-driven competitive intelligence; if metrics decline, refine content quality or update competitive data more frequently.

---

## KPIs to track
- Organic traffic to comparison pages
- Conversion rate
- Keyword ranking distribution
- CTA click rate
- Competitor keyword coverage

---

## Pass threshold
**≥5,000 page views/month and conversion rate ≥1.0%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/comparison-alternative-pages`_
