---
name: industry-reports-research-baseline
description: >
    Industry Reports & Research — Baseline Run. Conduct original research and publish data-driven
  industry reports to generate backlinks, press coverage, and inbound leads from problem-aware
  audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥100 downloads and ≥8 qualified leads in 30 days"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "industry-reports-research"
install: "npx gtm-skills add marketing/problem-aware/industry-reports-research"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Industry Reports & Research — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social, Email

## Overview
Industry Reports & Research — Baseline Run. Conduct original research and publish data-driven industry reports to generate backlinks, press coverage, and inbound leads from problem-aware audiences.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥100 downloads and ≥8 qualified leads in 30 days

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up content repurposing
Run the `content-repurposing` drill to build a system that takes each piece of content and adapts it across formats: LinkedIn post to Twitter thread, blog post to newsletter, video clip to social post. This multiplies your content output without multiplying effort.

### 2. Configure analytics tracking
Run the `posthog-gtm-events` drill to track content performance events: `industry-reports-research_post_published`, `industry-reports-research_engagement_received`, `industry-reports-research_profile_visit`, `industry-reports-research_dm_received`, `industry-reports-research_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥100 downloads and ≥8 qualified leads in 30 days. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥100 downloads and ≥8 qualified leads in 30 days**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/industry-reports-research`_
