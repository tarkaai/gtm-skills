---
name: developer-newsletter-program-baseline
description: >
    Developer Newsletter — Baseline Run. Launch a technical newsletter with code examples,
  tutorials, and industry insights to build audience and generate developer leads.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Email, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥500 subscribers and ≥12 qualified leads from first 8 issues over 8 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "developer-newsletter-program"
install: "npx gtm-skills add marketing/problem-aware/developer-newsletter-program"
drills:
  - content-repurposing
  - posthog-gtm-events
---
# Developer Newsletter — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Email, Content

## Overview
Developer Newsletter — Baseline Run. Launch a technical newsletter with code examples, tutorials, and industry insights to build audience and generate developer leads.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥500 subscribers and ≥12 qualified leads from first 8 issues over 8 weeks

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
Run the `posthog-gtm-events` drill to track content performance events: `developer-newsletter-program_post_published`, `developer-newsletter-program_engagement_received`, `developer-newsletter-program_profile_visit`, `developer-newsletter-program_dm_received`, `developer-newsletter-program_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: ≥500 subscribers and ≥12 qualified leads from first 8 issues over 8 weeks. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥500 subscribers and ≥12 qualified leads from first 8 issues over 8 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/developer-newsletter-program`_
