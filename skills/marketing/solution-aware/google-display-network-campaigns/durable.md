---
name: google-display-network-campaigns-durable
description: >
  Google Display Network — Durable Intelligence. Run GDN campaigns targeting in-market audiences and affinity segments to build awareness and generate leads from solution-aware searchers.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained GDN performance and ≥60 qualified leads/month over 12 months via AI-optimized audience targeting"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
---
# Google Display Network — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Run GDN campaigns targeting in-market audiences and affinity segments to build awareness and generate leads from solution-aware searchers.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained GDN performance and ≥60 qualified leads/month over 12 months via AI-optimized audience targeting

---

## Budget

**Play-specific tools & costs**
- **Ad spend (agent-optimized across channels):** $5,000–20,000/mo

_Total play-specific: $5,000–20,000/mo_

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

1. Deploy AI-powered intelligence system in n8n: analyze PostHog data to identify patterns predicting success and failure in google display network campaigns.

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
**Sustained GDN performance and ≥60 qualified leads/month over 12 months via AI-optimized audience targeting**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/google-display-network-campaigns`_
