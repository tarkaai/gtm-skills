---
name: pr-campaign-launch-durable
description: >
  PR Campaign Launch — Durable Intelligence. Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - build-prospect-list
  - cold-email-sequence
  - content-repurposing
  - posthog-gtm-events
  - dashboard-builder
  - newsletter-pipeline
---
# PR Campaign Launch — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting

---

## Budget

**Play-specific tools & costs**
- **Featured.com + Qwoted:** ~$150/mo
- **PR Newswire (occasional press release distribution):** ~$300–1,000 per release

_Total play-specific: ~$150–1000/mo_

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

1. Deploy AI-powered intelligence system in n8n: analyze PostHog data to identify patterns predicting success and failure in pr campaign launch campaigns.

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
**Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/pr-campaign-launch`_
