---
name: champion-identification-durable
description: >
  Champion Identification & Development — Durable Intelligence. Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "125 hours over 6 months"
outcome: "Sustained or improving champion impact (>=40% win rate lift) over 6 months via continuous agent-driven recruitment optimization, enablement personalization, and risk monitoring"
kpis: ["Champion win rate lift", "Champion engagement trend", "Agent experiment win rate", "Champion prediction accuracy"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
---
# Champion Identification & Development — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.

**Time commitment:** 125 hours over 6 months
**Pass threshold:** Sustained or improving champion impact (>=40% win rate lift) over 6 months via continuous agent-driven recruitment optimization, enablement personalization, and risk monitoring

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
- **Loom** (Video)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which contact behaviors best predict strong championship; auto-adjusts champion scoring model weekly based on win/loss data.

2. Set up the agent to run experiments on champion recruitment messaging: test different value propositions, enablement offers, and timing; promote high-conversion approaches.

3. Build a feedback loop where every closed-won deal triggers the agent to analyze the champion's engagement history; identify early signals that predicted strong advocacy and boost those signals.

4. Deploy AI-driven champion enablement personalization: agent analyzes each champion's role, seniority, and company to recommend tailored materials (CFO gets ROI focus, VP Ops gets efficiency focus).

5. Implement champion risk monitoring: agent tracks champion engagement trends and alerts when champions disengage (no activity for 10 days, declining meeting attendance); suggests re-engagement tactics.

6. Build automatic champion coaching: agent generates pre-call briefings for champions based on upcoming internal meetings (e.g., "Your CFO cares about payback period—emphasize 6-month ROI").

7. Create market adaptation logic: if champion patterns change (e.g., more deals require IT champion during security-focused buying cycles), agent updates recruitment targets and enablement kits.

8. Agent continuously experiments with champion development cadence: test different touchpoint frequencies, content types, and engagement tactics; optimize for highest champion scores and win rates.

9. Implement predictive champion identification: agent uses machine learning on historical engagement data to predict which contacts will become strong champions before they fully emerge.

10. Establish monthly review cycles: agent generates champion program reports showing recruitment rates, engagement trends, win rate impact, and recommended enablement updates; team reviews and approves changes or rolls back underperforming experiments.

---

## KPIs to track
- Champion win rate lift
- Champion engagement trend
- Agent experiment win rate
- Champion prediction accuracy

---

## Pass threshold
**Sustained or improving champion impact (>=40% win rate lift) over 6 months via continuous agent-driven recruitment optimization, enablement personalization, and risk monitoring**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/champion-identification`_
