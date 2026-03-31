---
name: roi-calculator-durable
description: >
  ROI Calculator & Business Case — Durable Intelligence. Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving ROI effectiveness (>=70% strong ROI, >=60% completion) over 6 months via continuous agent-driven calculator optimization, personalization, and accuracy improvement"
kpis: ["ROI projection accuracy", "Agent experiment win rate", "Business case conversion rate", "Realized vs projected ROI"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
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
# ROI Calculator & Business Case — Durable Intelligence

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Overview
Quantify and demonstrate ROI to justify purchase decisions and overcome budget objections, from manual ROI spreadsheets to AI-driven dynamic business case generation that personalizes value narratives and auto-updates based on prospect data and market benchmarks.

**Time commitment:** 140 hours over 6 months
**Pass threshold:** Sustained or improving ROI effectiveness (>=70% strong ROI, >=60% completion) over 6 months via continuous agent-driven calculator optimization, personalization, and accuracy improvement

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

1. Deploy an AI agent in n8n that continuously analyzes which ROI assumptions and value drivers best predict closed-won deals and actual customer outcomes; auto-tunes calculator logic based on win patterns and realized ROI data.

2. Set up the agent to run experiments on ROI framing: test conservative vs aggressive assumptions, different time horizons (1-year vs 3-year), different value drivers emphasized; promote highest-conversion approaches.

3. Build a feedback loop where every closed-won customer triggers the agent to compare projected ROI vs actual realized ROI; strengthen calculator accuracy by learning from real outcomes.

4. Deploy AI-driven ROI personalization: agent analyzes prospect's industry, size, role, and pain points to generate custom ROI narratives emphasizing most relevant value drivers for that profile.

5. Implement real-time ROI coaching: during discovery calls, agent listens for ROI input mentions and prompts reps to dig deeper ("Prospect mentioned 10 hours/week—ask about team size and loaded cost").

6. Build market adaptation logic: if economic conditions change (recession, inflation), agent adjusts ROI messaging to emphasize cost savings over growth; if market is hot, emphasize competitive advantage and revenue impact.

7. Create automatic business case generation: agent listens to discovery calls, extracts ROI inputs, generates full business case with industry benchmarks and case studies, and sends draft to rep for review within 1 hour of call.

8. Agent continuously refines industry benchmarks: learns from every new deal to improve "typical savings" estimates; increases credibility and accuracy of ROI projections for prospects without measured data.

9. Implement predictive ROI scoring: agent predicts which prospects will achieve strong ROI based on early discovery signals; prioritizes those prospects for sales focus.

10. Establish monthly review cycles: agent generates ROI intelligence reports showing projection accuracy, value driver trends, conversion impact, and recommended calculator updates; team reviews and approves changes or adjusts assumptions.

---

## KPIs to track
- ROI projection accuracy
- Agent experiment win rate
- Business case conversion rate
- Realized vs projected ROI

---

## Pass threshold
**Sustained or improving ROI effectiveness (>=70% strong ROI, >=60% completion) over 6 months via continuous agent-driven calculator optimization, personalization, and accuracy improvement**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/roi-calculator`_
