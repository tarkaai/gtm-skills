---
name: usage-limit-sales-upsell-durable
description: >
  Usage-Based Upsell — Durable Intelligence. Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving expansion metrics (>=35% conversion, >=15% expansion ARR) over 6 months via continuous agent-driven signal optimization, personalization, and market adaptation"
kpis: ["Expansion conversion trend", "Agent experiment win rate", "Expansion ARR growth rate", "Predictive accuracy"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add sales/won/usage-limit-sales-upsell"
---
# Usage-Based Upsell — Durable Intelligence

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Direct

## Overview
Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving expansion metrics (>=35% conversion, >=15% expansion ARR) over 6 months via continuous agent-driven signal optimization, personalization, and market adaptation

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
- **PostHog** (CDP)
- **Attio** (CRM)
- **n8n** (Automation)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which usage patterns best predict successful upsells; auto-tunes expansion scoring model and signal definitions based on closed expansion deals.

2. Set up the agent to run experiments on upsell timing: test immediate outreach when threshold hit vs 24-hour delay vs wait for customer to contact support; promote optimal timing per segment.

3. Build a feedback loop where every closed upsell triggers the agent to analyze usage history and identify early signals that predicted expansion need; strengthen detection of those patterns.

4. Deploy AI-driven expansion personalization: agent analyzes each customer's usage pattern, business context, and engagement to generate custom expansion proposals emphasizing most relevant benefits.

5. Implement predictive expansion forecasting: agent predicts which customers will need expansion in next 30/60/90 days based on growth velocity; enables proactive outreach before limits are hit.

6. Build market adaptation logic: if expansion conversion rates drop (economic downturn, budget freezes), agent suggests alternative offers (month-to-month vs annual, smaller increments, pay-as-you-grow pricing).

7. Create automatic upsell optimization: agent tests different prompt copy, offer structures, discount levels, and payment terms; promotes combinations with highest conversion rates and lowest churn.

8. Agent continuously refines expansion segmentation: learns which customer types prefer self-service vs assisted upsells; routes opportunities to optimal motion.

9. Implement dynamic pricing intelligence: agent monitors competitor pricing, customer willingness-to-pay signals, and deal velocity to recommend optimal upsell pricing per account.

10. Establish monthly review cycles: agent generates expansion intelligence reports showing conversion trends, signal quality, pricing effectiveness, and recommended strategy updates; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Expansion conversion trend
- Agent experiment win rate
- Expansion ARR growth rate
- Predictive accuracy

---

## Pass threshold
**Sustained or improving expansion metrics (>=35% conversion, >=15% expansion ARR) over 6 months via continuous agent-driven signal optimization, personalization, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/usage-limit-sales-upsell`_
