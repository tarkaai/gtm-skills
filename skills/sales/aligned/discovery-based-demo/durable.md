---
name: discovery-based-demo-durable
description: >
  Discovery-Based Demo — Durable Intelligence. Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving demo effectiveness (>=70% next-step, >=45% proposal conversion) over 6 months via continuous agent-driven personalization, content optimization, and market adaptation"
kpis: ["Demo conversion trends", "Agent experiment win rate", "Demo engagement score", "Predictive accuracy"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - multi-channel-cadence
  - dashboard-builder
  - ab-test-orchestrator
---
# Discovery-Based Demo — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.

**Time commitment:** 135 hours over 6 months
**Pass threshold:** Sustained or improving demo effectiveness (>=70% next-step, >=45% proposal conversion) over 6 months via continuous agent-driven personalization, content optimization, and market adaptation

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (AI-assisted calling):** ~$100–300/mo
- **Intercom or Loops (agent-driven messaging):** ~$150–400/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Loom** (Video)
- **OpenAI** (AI/LLM)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which demo structures and pain-to-feature mappings best predict closed-won deals; auto-optimizes demo playbooks based on win patterns.

2. Set up the agent to run experiments on demo personalization depth: test light customization (custom agenda) vs deep personalization (custom demo environment + data) to find optimal ROI.

3. Build a feedback loop where every closed-won deal triggers the agent to analyze demo recording; identify which moments generated highest engagement and incorporate those patterns into future demos.

4. Deploy AI-driven demo content generation: agent analyzes prospect's industry, pains, and role to auto-generate custom demo scripts, talking points, and ROI narratives for each demo.

5. Implement real-time demo coaching: agent listens to live demos and suggests next topics to cover based on prospect engagement signals (e.g., prospect asked about reporting—agent suggests showing advanced dashboard features next).

6. Build market adaptation logic: if demo conversion rates drop across segments, agent investigates (are competitors featuring new capabilities? have buyer priorities shifted?) and updates demo messaging.

7. Create automatic demo optimization: agent tests different demo structures (pain-first vs feature-first, live vs pre-recorded elements, short vs deep) and routes prospects to highest-converting format.

8. Agent continuously refines demo follow-up sequences: experiments with different content types (video vs doc), timing (immediate vs 1-day delay), and CTAs; promotes winners.

9. Implement predictive demo outcomes: agent analyzes pre-demo data (discovery quality, stakeholder attendance, intent signals) to predict demo success probability; suggests additional preparation for low-probability demos.

10. Establish monthly review cycles: agent generates demo performance reports showing conversion trends, optimal pain coverage, engagement patterns, and recommended playbook updates; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Demo conversion trends
- Agent experiment win rate
- Demo engagement score
- Predictive accuracy

---

## Pass threshold
**Sustained or improving demo effectiveness (>=70% next-step, >=45% proposal conversion) over 6 months via continuous agent-driven personalization, content optimization, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/discovery-based-demo`_
