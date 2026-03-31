---
name: stakeholder-mapping-durable
description: >
  Stakeholder Mapping Framework — Durable Intelligence. Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Social, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving multi-threading impact (>=30% faster close time) over 6 months via continuous agent-driven stakeholder intelligence, role prediction, and engagement optimization"
kpis: ["Multi-threading rate", "Stakeholder prediction accuracy", "Deal velocity by stakeholder count", "Single-threaded risk prevention"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
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
# Stakeholder Mapping Framework — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social, Email

## Overview
Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving multi-threading impact (>=30% faster close time) over 6 months via continuous agent-driven stakeholder intelligence, role prediction, and engagement optimization

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo
- **LinkedIn Sales Navigator:** ~$100/mo
- **Dripify or Expandi (LinkedIn automation):** ~$60–100/mo

_Total play-specific: ~$60–500/mo_

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

1. Deploy an AI agent in n8n that continuously analyzes closed-won vs closed-lost deals to identify optimal stakeholder patterns (ideal count, role mix, engagement cadence); adjust mapping guidance dynamically.

2. Set up the agent to run experiments on stakeholder engagement sequences: test whether engaging Economic Buyer first vs Champion first vs parallel engagement yields better outcomes.

3. Build a feedback loop where every closed-lost deal triggers the agent to analyze stakeholder map: was a key stakeholder missed? did a Blocker go unaddressed? update discovery questions accordingly.

4. Deploy AI-driven stakeholder role prediction: agent analyzes LinkedIn profiles, job descriptions, and org structures to predict each person's role in buying process with confidence scores.

5. Implement relationship risk monitoring: agent tracks stakeholder turnover (job changes on LinkedIn) and alerts reps when Champions or Economic Buyers leave; suggests replacement stakeholders immediately.

6. Build automatic multi-threading recommendations: agent analyzes deal progress and suggests next stakeholder to engage based on current engagement pattern and historical win data.

7. Create market adaptation logic: if stakeholder patterns change (e.g., more deals require CFO approval during economic downturn), agent adjusts mapping templates and engagement playbooks.

8. Agent continuously experiments with stakeholder engagement cadence: test different touchpoint frequencies for each role type; optimize for highest sentiment and engagement scores.

9. Implement predictive single-threading alerts: agent predicts which deals will become single-threaded based on engagement patterns and proactively suggests multi-threading actions before risk materializes.

10. Establish monthly review cycles: agent generates stakeholder intelligence reports showing optimal patterns, role predictions accuracy, and engagement recommendations; team reviews and approves mapping updates or rolls back underperforming experiments.

---

## KPIs to track
- Multi-threading rate
- Stakeholder prediction accuracy
- Deal velocity by stakeholder count
- Single-threaded risk prevention

---

## Pass threshold
**Sustained or improving multi-threading impact (>=30% faster close time) over 6 months via continuous agent-driven stakeholder intelligence, role prediction, and engagement optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/stakeholder-mapping`_
