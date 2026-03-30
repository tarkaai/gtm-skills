---
name: mutual-action-plan-durable
description: >
  Mutual Action Plan (MAP) — Durable Intelligence. Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving MAP impact (>=35% velocity lift, >=25% win rate lift) over 6 months via continuous agent-driven milestone optimization, risk detection, and timeline personalization"
kpis: ["MAP impact on velocity/win rate", "Agent experiment win rate", "Risk prediction accuracy", "Milestone optimization effectiveness"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
---
# Mutual Action Plan (MAP) — Durable Intelligence

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving MAP impact (>=35% velocity lift, >=25% win rate lift) over 6 months via continuous agent-driven milestone optimization, risk detection, and timeline personalization

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

1. Deploy an AI agent in n8n that continuously analyzes which MAP milestones and timelines best predict successful closes; auto-optimizes milestone templates based on win patterns.

2. Set up the agent to monitor MAP progress in real-time and predict deal risk: if milestone completion rate drops below historical patterns, alert team and suggest intervention tactics.

3. Build a feedback loop where every closed deal with MAP triggers the agent to analyze milestone adherence and identify which milestones were most predictive of outcome; strengthen those in future MAPs.

4. Deploy AI-driven MAP personalization: agent analyzes deal characteristics (size, complexity, industry, buyer type) to generate custom milestone timelines that reflect realistic completion times for that profile.

5. Implement automatic milestone risk detection: agent identifies when prospects miss milestones, analyzes historical data for similar delays, and recommends specific actions (escalate to executive, offer implementation support, simplify milestone).

6. Build market adaptation logic: if economic conditions slow buying cycles, agent adjusts MAP timelines to reflect longer decision processes; prevents unrealistic expectations.

7. Create predictive close date estimation: agent uses MAP completion velocity and historical patterns to forecast close date; updates automatically as milestones are completed or delayed.

8. Agent continuously experiments with MAP structures: tests different milestone sequences, ownership assignments, and granularity levels; promotes structures with highest completion and win rates.

9. Implement dynamic milestone recommendations: when prospects complete milestones faster than expected, agent suggests accelerating subsequent milestones to maintain momentum.

10. Establish monthly review cycles: agent generates MAP intelligence reports showing completion trends, risk predictions, optimal timeline templates, and recommended process updates; team reviews and approves changes.

---

## KPIs to track
- MAP impact on velocity/win rate
- Agent experiment win rate
- Risk prediction accuracy
- Milestone optimization effectiveness

---

## Pass threshold
**Sustained or improving MAP impact (>=35% velocity lift, >=25% win rate lift) over 6 months via continuous agent-driven milestone optimization, risk detection, and timeline personalization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/mutual-action-plan`_
