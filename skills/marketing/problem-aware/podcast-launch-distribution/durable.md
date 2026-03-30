---
name: podcast-launch-distribution-durable
description: >
  Branded Podcast Launch — Durable Intelligence. Launch and distribute a branded podcast to build awareness, generate inbound interest, and establish thought leadership with problem-aware and solution-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained listener growth (≥15% QoQ) and ≥25 qualified leads/quarter over 12 months via AI-driven topic selection and promotion"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
---
# Branded Podcast Launch — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Overview
Launch and distribute a branded podcast to build awareness, generate inbound interest, and establish thought leadership with problem-aware and solution-aware audiences.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained listener growth (≥15% QoQ) and ≥25 qualified leads/quarter over 12 months via AI-driven topic selection and promotion

---

## Budget

**Play-specific tools & costs**
- **Taplio (analytics + AI content engine):** ~$50/mo
- **Buffer or Typefully:** ~$10–20/mo
- **Descript or Loom (repurposing content to video):** ~$15–30/mo

_Total play-specific: ~$10–50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)
- **Attio** (CRM)
- **Clay** (Enrichment)

---

## Instructions

1. Deploy AI-powered intelligence system in n8n: analyze PostHog data to identify patterns predicting success and failure in branded podcast launch campaigns.

2. Build continuous experimentation framework: AI automatically tests variations in messaging, timing, targeting, creative, and channel mix.

3. Implement learning loops: AI monitors experiment results, identifies winners, analyzes root causes, and applies learnings to future campaigns automatically.

4. Set up market adaptation system: AI detects when performance drops due to market saturation, competition, seasonality, or external changes; recommends and tests adjustments.

5. Create smart optimization engine: AI continuously tunes targeting criteria, send times, budget allocation, message variants, and creative based on real-time performance data.

6. Build predictive models in n8n using Anthropic Claude: forecast campaign results, predict lead quality, and recommend proactive optimizations before metrics decline.

7. Deploy competitive intelligence: AI monitors competitor activities, market trends, and emerging best practices; adapts strategy automatically to maintain edge.

8. Establish sophisticated guardrails: if performance drops >20% below Scalable benchmark for 2+ consecutive weeks, AI investigates root causes and suggests specific corrective actions.

9. Implement automated insights and reporting: AI generates weekly summaries of what's working, what's declining, which experiments won, and what to test next.

10. Conduct monthly AI-driven strategy reviews: analyze long-term trends, update success playbooks, identify new opportunities, and maintain or improve results over 6-12 months through continuous intelligent adaptation.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained listener growth (≥15% QoQ) and ≥25 qualified leads/quarter over 12 months via AI-driven topic selection and promotion**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/podcast-launch-distribution`_
