---
name: bant-qualification-durable
description: >
  BANT Qualification Framework — Durable Intelligence. Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving qualification accuracy (>=35%) over 6 months via continuous agent-driven BANT optimization and market adaptation"
kpis: ["Qualification accuracy", "Agent-driven experiment win rate", "False negative rate", "Time-to-qualification trend"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
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
# BANT Qualification Framework — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically qualify leads using Budget, Authority, Need, and Timeline to ensure you spend time on deals that can close, from manual scoring in spreadsheets to AI-driven continuous qualification that adapts criteria to market feedback.

**Time commitment:** 120 hours over 6 months
**Pass threshold:** Sustained or improving qualification accuracy (>=35%) over 6 months via continuous agent-driven BANT optimization and market adaptation

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
- **Cal.com** (Scheduling)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes won vs lost deals in PostHog to identify which BANT patterns correlate with closed revenue.

2. Configure the agent to run weekly experiments: adjust BANT scoring weights, test new qualification questions, or add/remove enrichment signals based on win/loss patterns.

3. Set up a feedback loop where every won deal triggers the agent to analyze that lead's original BANT scores; strengthen scoring rules for similar profiles.

4. When a lead is disqualified but later closes (false negative), the agent flags the pattern and suggests criteria adjustments; test changes on 10% of new leads before full rollout.

5. Build an agent-driven A/B testing framework in PostHog: split new leads into control (current BANT rules) and variant (agent-optimized rules); compare qualification accuracy and close rates.

6. Deploy an AI co-pilot in n8n that listens to discovery call recordings (via Fireflies or similar), extracts BANT signals automatically, and updates Attio with confidence scores.

7. Create market adaptation logic: if qualification rate drops >20% for 2 consecutive weeks, agent alerts team and suggests re-calibrating BANT thresholds or enrichment sources.

8. Agent continuously refines pre-scoring rules by analyzing which enrichment signals (revenue, tech stack, funding events) best predict successful qualification.

9. Implement automatic tuning: agent adjusts BANT question library based on which questions yield highest correlation with closed deals; archive low-signal questions.

10. Establish monthly review cycles: agent generates reports on BANT optimization experiments, qualification trends, and recommended scoring model updates; team reviews and approves changes or rolls back underperformers.

---

## KPIs to track
- Qualification accuracy
- Agent-driven experiment win rate
- False negative rate
- Time-to-qualification trend

---

## Pass threshold
**Sustained or improving qualification accuracy (>=35%) over 6 months via continuous agent-driven BANT optimization and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/bant-qualification`_
