---
name: case-study-content-program-scalable
description: >
  Case Study Content Program — Scalable Automation. Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥4,000 page views/month and deal close rate +15% when case studies used"
kpis: ["Page views", "Conversion rate", "Sales usage rate", "Deal close rate impact", "Production velocity", "Multi-format engagement"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
---
# Case Study Content Program — Scalable Automation

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥4,000 page views/month and deal close rate +15% when case studies used

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
- **Anthropic** (AI/LLM)
- **Attio** (CRM)
- **Riverside** (Video)
- **Cal.com** (Scheduling)

---

## Instructions

1. Scale to 30-40 case studies covering comprehensive ICP and use case matrix; build systematic production pipeline with monthly cadence (3-4 new case studies per month).

2. Create n8n workflow to automate case study production: PostHog identifies high-NPS customers, n8n triggers outreach email, schedules interview via Cal.com, transcribes with AI, generates first draft.

3. Implement multi-format content production: for each case study, create written version, video testimonial, one-pager PDF, LinkedIn post, Twitter thread, and sales deck slide.

4. Build automated case study matching: n8n analyzes prospect data (industry, use case, company size) and recommends most relevant case studies; automatically includes them in sales sequences and demo follow-ups.

5. Connect PostHog to n8n: when a prospect views a case study, trigger personalized follow-up email referencing the specific customer story and offering to connect with that customer.

6. Set guardrails: conversion rate must stay within 20% of Baseline rate; if case study production drops below 3 per month for 2+ months, revisit customer recruitment process.

7. Use PostHog to track case study effectiveness in the sales cycle: correlate case study engagement with deal close rate and velocity.

8. Implement A/B testing for case study formats: test different structures (challenge-first vs. results-first), lengths (short vs. comprehensive), and visual designs; promote winning formats.

9. After 2 months, evaluate total case study traffic, conversion volume, and impact on sales efficiency; calculate ROI including sales productivity gains.

10. If metrics hold, document the automated production pipeline and prepare for Durable AI-driven story optimization; if metrics decline, improve story quality or customer selection criteria.

---

## KPIs to track
- Page views
- Conversion rate
- Sales usage rate
- Deal close rate impact
- Production velocity
- Multi-format engagement

---

## Pass threshold
**≥4,000 page views/month and deal close rate +15% when case studies used**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/case-study-content-program`_
