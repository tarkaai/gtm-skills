---
name: documentation-as-marketing-durable
description: >
    Documentation as Marketing — Durable Intelligence. Build public, SEO-optimized developer
  documentation that attracts organic search traffic and converts technical audiences from
  solution-aware to product-aware.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained organic traffic growth (≥10% QoQ) and ≥2% docs-to-signup conversion over 12 months via AI-driven content optimization"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - dashboard-builder
  - nps-feedback-loop
---
# Documentation as Marketing — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Documentation as Marketing — Durable Intelligence. Build public, SEO-optimized developer documentation that attracts organic search traffic and converts technical audiences from solution-aware to product-aware.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained organic traffic growth (≥10% QoQ) and ≥2% docs-to-signup conversion over 12 months via AI-driven content optimization

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build product dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: activation rate trend, conversion funnel by cohort, churn rate trend, expansion revenue, NPS score trend, feature adoption rates. Set alerts for activation or retention drops.

### 2. Launch feedback loops
Run the `nps-feedback-loop` drill to collect and act on user feedback: deploy NPS surveys at key milestones, route feedback to the product team, trigger follow-ups based on score (promoters get referral asks, detractors get personal outreach).

### 3. Autonomous product optimization
Configure the agent to: monitor all product metrics, detect trends (positive or negative), suggest experiments based on data, and generate weekly product health reports. The agent should flag when any metric deviates from baseline by more than 15%.

### 4. Evaluate sustainability
Measure against: Sustained organic traffic growth (≥10% QoQ) and ≥2% docs-to-signup conversion over 12 months via AI-driven content optimization. This level runs continuously. If product metrics sustain or improve, the play is durable. If metrics decay, the agent diagnoses the cause and recommends interventions.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained organic traffic growth (≥10% QoQ) and ≥2% docs-to-signup conversion over 12 months via AI-driven content optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/documentation-as-marketing`_
