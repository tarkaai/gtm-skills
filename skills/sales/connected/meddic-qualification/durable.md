---
name: meddic-qualification-durable
description: >
  MEDDIC Qualification System — Durable Intelligence. Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving MEDDIC-driven close rates (>=15% lift) over 6 months via continuous agent-driven element optimization, call coaching, and market adaptation"
kpis: ["Close rate by MEDDIC score", "Agent experiment win rate", "Element quality trend", "Predictive accuracy"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
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
# MEDDIC Qualification System — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Apply MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) to complex enterprise deals, from manual tracking to AI-driven continuous qualification that surfaces deal risks and accelerates cycles.

**Time commitment:** 140 hours over 6 months
**Pass threshold:** Sustained or improving MEDDIC-driven close rates (>=15% lift) over 6 months via continuous agent-driven element optimization, call coaching, and market adaptation

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
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes closed-won vs closed-lost deals to identify which MEDDIC patterns predict wins; adjust scoring weights dynamically.

2. Set up the agent to run A/B tests on MEDDIC element prioritization: test whether focusing on Champion first vs Economic Buyer first yields faster progression.

3. Build a feedback loop where every closed deal triggers the agent to analyze MEDDIC completeness at each stage; strengthen discovery questions for elements that were weak in losses.

4. When a deal with high MEDDIC score is lost, the agent investigates: were MEDDIC elements accurate or aspirational? Update scoring to penalize low-confidence data.

5. Deploy an AI co-pilot that listens to discovery calls, extracts MEDDIC elements in real-time, and suggests follow-up questions mid-call to uncover missing elements.

6. Create market adaptation logic: if Decision Process timelines lengthen across multiple deals, agent alerts team to macro trend (e.g., budget freezes) and adjusts forecasts.

7. Agent continuously experiments with MEDDIC question variations; track which phrasing yields highest response quality and auto-updates rep guidance in Attio.

8. Implement predictive deal scoring: agent combines MEDDIC completeness, quality, and historical win patterns to generate close probability; auto-prioritizes high-probability deals for rep focus.

9. Build automatic coaching triggers: when a rep's deals consistently miss Champion or Economic Buyer, agent schedules targeted training and provides call examples where those elements were uncovered effectively.

10. Establish monthly review cycles: agent generates MEDDIC health reports showing trends in completeness, element quality, and correlation with revenue; team reviews and approves scoring model updates or rolls back experiments that reduced win rates.

---

## KPIs to track
- Close rate by MEDDIC score
- Agent experiment win rate
- Element quality trend
- Predictive accuracy

---

## Pass threshold
**Sustained or improving MEDDIC-driven close rates (>=15% lift) over 6 months via continuous agent-driven element optimization, call coaching, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/meddic-qualification`_
