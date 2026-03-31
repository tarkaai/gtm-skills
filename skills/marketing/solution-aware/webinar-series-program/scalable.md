---
name: webinar-series-program-scalable
description: >
  Educational Webinar Series — Scalable Automation. Run regular educational webinars to generate leads, nurture prospects, and establish thought leadership with solution-aware and product-aware audiences.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events, Content, Email"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥200 registrations and ≥40 qualified leads per month from webinar series over 4 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "webinar-series-program"
install: "npx gtm-skills add marketing/solution-aware/webinar-series-program"
drills:
  - meetup-pipeline
  - webinar-pipeline
  - workshop-pipeline
  - crm-pipeline-setup
  - follow-up-automation
  - posthog-gtm-events
---
# Educational Webinar Series — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events, Content, Email

## Overview
Run regular educational webinars to generate leads, nurture prospects, and establish thought leadership with solution-aware and product-aware audiences.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥200 registrations and ≥40 qualified leads per month from webinar series over 4 months

---

## Budget

**Play-specific tools & costs**
- **Riverside or Hopin (production-quality events):** ~$25–150/mo
- **Event promotion spend (LinkedIn, email list):** ~$100–500/mo
- **Loom (post-event follow-up clips):** ~$15/mo

_Total play-specific: ~$15–500/mo_

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

2. Implement automation via n8n workflows to reduce manual effort and increase throughput for educational webinar series execution.

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
**≥200 registrations and ≥40 qualified leads per month from webinar series over 4 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/webinar-series-program`_
