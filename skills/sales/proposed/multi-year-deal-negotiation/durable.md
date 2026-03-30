---
name: multi-year-deal-negotiation-durable
description: >
  Multi-Year Deal Structuring — Durable Intelligence. Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving multi-year deal performance (>=35% close rate, >=2.5x LTV) over 6 months via continuous agent-driven contract optimization, pricing intelligence, and renewal management"
kpis: ["Multi-year close rate trend", "LTV optimization", "Agent experiment win rate", "Churn rate (multi-year vs annual)"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
---
# Multi-Year Deal Structuring — Durable Intelligence

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Structure and price multi-year commitments to increase deal value and customer lifetime value, from manual contract terms to AI-driven contract optimization that maximizes ACVand retention while maintaining competitive pricing.

**Time commitment:** 135 hours over 6 months
**Pass threshold:** Sustained or improving multi-year deal performance (>=35% close rate, >=2.5x LTV) over 6 months via continuous agent-driven contract optimization, pricing intelligence, and renewal management

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
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which contract terms (length, discount, payment structure) best predict high LTV and low churn; auto-optimizes multi-year deal structures based on customer patterns.

2. Set up the agent to run pricing experiments: test different discount levels, payment terms, and contract lengths by segment; measure impact on close rate, TCV, and customer retention.

3. Build a feedback loop where every multi-year renewal (or churn) triggers the agent to analyze original contract terms and identify what worked or what caused issues; strengthens successful patterns.

4. Deploy AI-driven contract personalization: agent analyzes customer profile (industry, size, growth stage, cash position) to recommend optimal contract length and payment terms (e.g., high-growth startup → annual payments, established enterprise → 3-year prepay).

5. Implement predictive contract modeling: agent forecasts customer LTV, expansion probability, and churn risk based on contract terms; recommends structures that maximize LTV while minimizing churn.

6. Build market adaptation logic: during economic downturns, agent suggests shorter contracts or flexible payment terms; during growth periods, emphasizes longer commitments with strategic benefits.

7. Create automatic discount optimization: agent learns which discount levels close deals without leaving money on table; recommends minimum effective discount for each opportunity based on competitive situation and customer urgency.

8. Agent continuously refines multi-year positioning: experiments with different value propositions (cost savings vs strategic partnership vs priority access) and measures which resonate best by persona and industry.

9. Implement dynamic renewal orchestration: agent predicts renewal likelihood 90 days out; for at-risk renewals, suggests shorter terms or flexible options; for strong renewals, suggests longer commitments with expansion.

10. Establish monthly review cycles: agent generates multi-year deal intelligence reports showing contract performance, pricing optimization, LTV trends, and recommended term updates; team reviews and approves changes.

---

## KPIs to track
- Multi-year close rate trend
- LTV optimization
- Agent experiment win rate
- Churn rate (multi-year vs annual)

---

## Pass threshold
**Sustained or improving multi-year deal performance (>=35% close rate, >=2.5x LTV) over 6 months via continuous agent-driven contract optimization, pricing intelligence, and renewal management**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/multi-year-deal-negotiation`_
