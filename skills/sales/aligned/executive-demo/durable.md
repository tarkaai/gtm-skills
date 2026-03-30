---
name: executive-demo-durable
description: >
  Executive-Focused Demo — Durable Intelligence. Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving exec demo effectiveness (>=75% conversion, >=35% velocity lift) over 6 months via continuous agent-driven personalization, content optimization, and coaching"
kpis: ["Exec demo conversion trend", "Agent experiment win rate", "Personalization impact", "Deal velocity by exec engagement"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
---
# Executive-Focused Demo — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving exec demo effectiveness (>=75% conversion, >=35% velocity lift) over 6 months via continuous agent-driven personalization, content optimization, and coaching

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (AI-assisted calling):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which exec demo narratives and proof points best predict deal closure by persona, industry, and company size; auto-optimizes demo content based on win patterns.

2. Set up the agent to run experiments on exec messaging: test different value framings (growth vs efficiency vs risk), different proof types (case studies vs data vs analyst quotes); promote highest-conversion approaches.

3. Build a feedback loop where every closed-won deal with exec engagement triggers the agent to analyze which demo elements drove executive endorsement; strengthen successful patterns.

4. Deploy AI-driven exec demo personalization: agent analyzes exec's LinkedIn, company financials, recent news, and industry trends to generate custom demo narrative and slide deck tailored to that executive's priorities.

5. Implement real-time exec demo coaching: agent listens to live exec demos and suggests next topics based on exec engagement cues ("Exec asked about ROI—emphasize payback period next").

6. Build predictive exec engagement: agent analyzes deal characteristics to predict which execs need to be engaged and when; prompts reps to orchestrate exec involvement at optimal moments.

7. Create market adaptation logic: if exec priorities shift (e.g., from growth to cost-cutting during recession), agent automatically adjusts demo messaging and proof points to emphasize relevant themes.

8. Agent continuously refines exec proof library: learns which case studies, benchmarks, and testimonials resonate with which exec personas; surfaces optimal proof for each demo automatically.

9. Implement dynamic ROI personalization: agent generates exec-specific ROI narratives based on company financials, industry benchmarks, and exec's stated priorities; calculates most compelling ROI framing.

10. Establish monthly review cycles: agent generates exec demo intelligence reports showing conversion trends, persona effectiveness, proof point impact, and recommended content updates; team reviews and approves changes.

---

## KPIs to track
- Exec demo conversion trend
- Agent experiment win rate
- Personalization impact
- Deal velocity by exec engagement

---

## Pass threshold
**Sustained or improving exec demo effectiveness (>=75% conversion, >=35% velocity lift) over 6 months via continuous agent-driven personalization, content optimization, and coaching**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/executive-demo`_
