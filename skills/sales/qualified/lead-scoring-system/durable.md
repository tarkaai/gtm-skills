---
name: lead-scoring-system-durable
description: >
  Lead Scoring System — Durable Intelligence. Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving lead score accuracy (>=4x Hot vs Cold conversion) over 6 months via continuous agent-driven scoring optimization and market adaptation"
kpis: ["Conversion rate by tier", "Scoring model accuracy", "Agent experiment win rate", "Predictive score vs actual close rate"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
---
# Lead Scoring System — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving lead score accuracy (>=4x Hot vs Cold conversion) over 6 months via continuous agent-driven scoring optimization and market adaptation

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$100–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes closed-won deals to identify which fit+intent combinations best predict revenue; adjust scoring weights monthly based on wins.

2. Set up the agent to run weekly experiments: test new fit attributes (e.g., hiring velocity, recent funding) and intent signals (e.g., feature page visits, API docs); promote high-signal factors.

3. Build a feedback loop where every closed-won deal triggers the agent to boost scores for similar profiles; every closed-lost deal reduces scores for that pattern.

4. Deploy lookalike modeling: agent identifies characteristics of top 10% of closed deals and auto-scores new leads based on similarity; test against rule-based scoring.

5. Implement market adaptation: if score-to-conversion correlation drops for 2+ weeks, agent alerts team and suggests recalibrating model (e.g., new competitors changing buying behavior).

6. Build an AI-driven lead prioritization engine: agent combines lead score, deal velocity prediction, and rep availability to recommend next-best lead to contact in real-time.

7. Create automatic A/B tests: split leads into control (current scoring) and variant (agent-optimized scoring); measure impact on meeting rate, close rate, and cycle time.

8. Agent continuously refines intent signal weighting by analyzing which behaviors most strongly predict near-term purchase intent; deprioritize low-signal behaviors.

9. Implement predictive lead scoring: agent uses machine learning on historical lead data to generate probability-of-close scores; compare to rule-based scores and blend for optimal accuracy.

10. Establish monthly review cycles: agent generates scoring model performance reports showing accuracy trends, signal contributions, and recommended adjustments; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Conversion rate by tier
- Scoring model accuracy
- Agent experiment win rate
- Predictive score vs actual close rate

---

## Pass threshold
**Sustained or improving lead score accuracy (>=4x Hot vs Cold conversion) over 6 months via continuous agent-driven scoring optimization and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/lead-scoring-system`_
