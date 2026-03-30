---
name: programmatic-seo-pages-scalable
description: >
  Programmatic SEO Pages — Scalable Automation. Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.
stage: "Marketing > Problem Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥5,000 organic visits/month and conversion rate ≥1.2%"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position", "Click-through rate", "Page generation velocity"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
---
# Programmatic SEO Pages — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥5,000 organic visits/month and conversion rate ≥1.2%

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
- **Webflow** (Content)
- **Ahrefs** (Analytics)
- **OpenAI** (AI/LLM)
- **Google Search Console** (Analytics)

---

## Instructions

1. Scale keyword research to 1,000-2,000 keywords using Ahrefs or SEMrush; organize into clusters by topic and search intent.

2. Build automated page generation pipeline: use n8n workflow to fetch keywords from Ahrefs API, generate pages from templates, and publish to CMS automatically on a weekly schedule.

3. Integrate AI content generation (OpenAI or Anthropic API) in n8n to create unique body content for each page; include human review/editing for top-priority keywords.

4. Generate 500-1,000 pages over 2 months; set up staging environment to review pages before publishing; ensure all pages pass Core Web Vitals thresholds.

5. Implement advanced internal linking: n8n workflow automatically adds contextual internal links based on keyword similarity and page relationships.

6. Connect Google Search Console and PostHog to n8n; create automated reporting workflow that sends weekly summaries of new pages indexed, traffic, and conversions.

7. Set guardrails: conversion rate must stay within 20% of Baseline rate (e.g., if Baseline was 1.5%, Scalable must maintain ≥1.2%); if performance drops, pause page generation and diagnose.

8. Use PostHog to track user journeys from programmatic pages to signup; identify which page templates and topics drive highest conversion rates.

9. After 2 months, evaluate: total pages indexed, organic traffic growth, conversion volume; create a prioritization model to focus on high-performing page types.

10. If metrics hold, document the automated pipeline and prepare for Durable agent-driven optimization; if metrics decline, refine content quality or reduce page generation velocity.

---

## KPIs to track
- Organic traffic
- Pages indexed
- Conversion rate
- Average position
- Click-through rate
- Page generation velocity

---

## Pass threshold
**≥5,000 organic visits/month and conversion rate ≥1.2%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/programmatic-seo-pages`_
