---
name: ai-content-generation-scale-scalable
description: >
    AI Content Generation — Scalable Automation. Use AI to create high-quality blog posts, guides,
  and educational content at scale, from manual prompt refinement through structured content
  pipelines to agent-driven continuous content strategy optimization.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥8,000 page views/month and conversion rate ≥1.0%"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity", "Organic traffic growth", "Cost per post"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---
# AI Content Generation — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content

## Overview
AI Content Generation — Scalable Automation. Use AI to create high-quality blog posts, guides, and educational content at scale, from manual prompt refinement through structured content pipelines to agent-driven continuous content strategy optimization.

**Time commitment:** 50 hours over 2 months
**Pass threshold:** ≥8,000 page views/month and conversion rate ≥1.0%

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate content distribution
Run the `follow-up-automation` drill to build n8n workflows that: schedule posts across platforms, auto-DM new followers who match ICP criteria, and notify you when high-engagement posts deserve a follow-up or repurpose.

### 2. Launch content A/B testing
Run the `ab-test-orchestrator` drill to systematically test: hook styles (question vs statistic vs story), content length (short vs long-form), posting times, CTAs (comment vs DM vs link). Run each test over 10+ posts before declaring winners.

### 3. Scale to daily publishing
Increase to daily posting with automated scheduling. Use the repurposing pipeline to generate 5+ pieces from each original piece of content. Monitor engagement rates to ensure quality doesn't drop with volume.

### 4. Evaluate against threshold
Measure against: ≥8,000 page views/month and conversion rate ≥1.0%. If PASS, proceed to Durable. If FAIL, focus on the content pillars and formats that showed the best results and cut the rest.

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

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/ai-content-generation-scale`_
