---
name: thought-leadership-program-scalable
description: >
  Thought Leadership Program — Scalable Automation. Systematic approach to building founder or executive as recognized thought leader to attract inbound interest from problem-aware and solution-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content, Events"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - content-repurposing
  - newsletter-pipeline
  - posthog-gtm-events
---
# Thought Leadership Program — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content, Events

## Overview
Systematic approach to building founder or executive as recognized thought leader to attract inbound interest from problem-aware and solution-aware audiences.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months

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
- **Attio** (CRM)
- **Clay** (Enrichment)

---

## Instructions

1. Set volume target to scale 5-10x from Baseline while maintaining quality; confirm your systems and list sources can support this volume.

2. Implement automation via n8n workflows to reduce manual effort and increase throughput for thought leadership program execution.

3. Connect all tools via PostHog CDP and n8n: sync events from email tool, CRM, and other platforms for unified tracking.

4. Set up guardrails: conversion rate must stay within 20% of Baseline benchmark; create alerts in n8n when metrics deviate.

5. Build sustainable pipeline for list building, content creation, or outreach that supports target volume week over week.

6. Create standardized templates, sequences, and processes that team members or automation can execute consistently.

7. Monitor key metrics daily in PostHog dashboards; use n8n workflows to alert team when performance exceeds or falls below thresholds.

8. Optimize based on data: identify high-performing segments, messages, or formats; double down on winners and deprioritize losers.

9. Track ROI at scale over 2-3 months: cost per qualified result, time efficiency gains from automation, pipeline impact, and conversion quality.

10. Decide: proceed to Durable if metrics are stable and repeatable at volume, or refine automation and targeting if quality drops or efficiency plateaus.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/thought-leadership-program`_
