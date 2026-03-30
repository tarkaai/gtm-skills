---
name: price-objection-handling-durable
description: >
  Price Objection Handling — Durable Intelligence. Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving objection overcome rate (>=65%) over 6 months via continuous agent-driven response optimization, pricing intelligence, and objection prevention"
kpis: ["Objection overcome rate trend", "Agent experiment win rate", "Discount optimization impact", "Objection prevention rate"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
---
# Price Objection Handling — Durable Intelligence

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "too expensive" objections by reframing value, demonstrating ROI, and offering flexible options, from manual objection responses to AI-driven dynamic pricing conversations that adapt based on prospect signals and maximize deal value.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving objection overcome rate (>=65%) over 6 months via continuous agent-driven response optimization, pricing intelligence, and objection prevention

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
- **Fireflies** (Sales Engagement)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which objection responses best predict deal closure; auto-optimizes response frameworks and asset recommendations based on win patterns.

2. Set up the agent to run experiments on objection handling approaches: test different value framing, timing of discount offers, and payment flexibility options; promote highest-win-rate approaches.

3. Build a feedback loop where every closed-won deal that had a price objection triggers the agent to analyze how objection was overcome; strengthen successful patterns in playbook.

4. Deploy real-time objection coaching: agent listens to sales calls and detects price objections in real-time; suggests next question or response framework to rep via notification during call.

5. Implement predictive objection detection: agent analyzes deal characteristics (weak pain quantification, low engagement, missing economic buyer) to predict price objection likelihood; prompts reps to address preemptively.

6. Build AI-driven pricing optimization: agent analyzes which pricing structures (annual vs quarterly, upfront vs installments) overcome objections fastest by segment; auto-recommends optimal structure for each deal.

7. Create market adaptation logic: if price objections increase during economic downturns, agent suggests emphasizing ROI and cost savings over feature value; adjusts messaging automatically.

8. Agent continuously tests objection prevention tactics: stronger discovery questions, earlier price anchoring, champions armed with ROI materials pre-proposal; measures which reduce objection frequency.

9. Implement dynamic discount optimization: agent learns which discount levels (5%, 10%, 15%) successfully close deals without leaving money on table; recommends minimum effective discount per objection scenario.

10. Establish monthly review cycles: agent generates objection intelligence reports showing overcome rates, response effectiveness, pricing optimization results, and recommended playbook updates; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Objection overcome rate trend
- Agent experiment win rate
- Discount optimization impact
- Objection prevention rate

---

## Pass threshold
**Sustained or improving objection overcome rate (>=65%) over 6 months via continuous agent-driven response optimization, pricing intelligence, and objection prevention**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/price-objection-handling`_
