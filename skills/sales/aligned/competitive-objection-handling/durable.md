---
name: competitive-objection-handling-durable
description: >
  Competitive Objection Handling — Durable Intelligence. Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving competitive win rate (>=45%) over 6 months via continuous agent-driven battlecard updates, positioning optimization, and market intelligence"
kpis: ["Competitive win rate trend", "Agent experiment win rate", "Battlecard currency score", "Positioning personalization impact"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
---
# Competitive Objection Handling — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.

**Time commitment:** 135 hours over 6 months
**Pass threshold:** Sustained or improving competitive win rate (>=45%) over 6 months via continuous agent-driven battlecard updates, positioning optimization, and market intelligence

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

1. Deploy an AI agent in n8n that continuously monitors competitive landscape (product launches, pricing changes, customer wins/losses) and auto-updates battlecards in Attio with latest intelligence.

2. Set up the agent to analyze every competitive win and loss: identify which differentiators mattered, which decision criteria drove choice, which positioning worked; strengthen winning patterns in battlecards.

3. Build a feedback loop where competitive losses trigger deep-dive analysis: agent reviews call recordings, identifies where positioning failed, suggests messaging improvements or product roadmap priorities.

4. Deploy AI-driven competitive positioning personalization: agent analyzes prospect's industry, role, and decision criteria to auto-generate custom competitive positioning specific to their priorities.

5. Implement real-time competitive coaching: agent listens to calls and detects competitive mentions; suggests specific differentiators to emphasize based on what has won vs that competitor in similar deals.

6. Build predictive competitive detection: agent analyzes deal characteristics to predict which competitors are likely to appear; prompts reps to position proactively before competitors are mentioned.

7. Create market adaptation logic: if a competitor launches feature that closes your differentiation gap, agent alerts team and suggests new positioning angles or roadmap acceleration.

8. Agent continuously experiments with competitive messaging: tests different framing (feature-based vs outcome-based), different proof points (case studies vs demos), different timing (early vs late stage); promotes winners.

9. Implement dynamic battlecard generation: agent creates deal-specific battlecards combining standard competitive intel with prospect's unique criteria, pains, and stakeholder priorities.

10. Establish monthly review cycles: agent generates competitive intelligence reports showing win rates, emerging threats, positioning effectiveness, and recommended battlecard updates; team reviews and approves changes or adjusts strategy.

---

## KPIs to track
- Competitive win rate trend
- Agent experiment win rate
- Battlecard currency score
- Positioning personalization impact

---

## Pass threshold
**Sustained or improving competitive win rate (>=45%) over 6 months via continuous agent-driven battlecard updates, positioning optimization, and market intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/competitive-objection-handling`_
