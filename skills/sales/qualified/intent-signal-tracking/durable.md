---
name: intent-signal-tracking-durable
description: >
  Intent Signal Tracking — Durable Intelligence. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving intent-driven conversion (>=3x vs cold) over 6 months via continuous agent-driven signal optimization, orchestration tuning, and market adaptation"
kpis: ["Intent conversion rate", "Agent experiment win rate", "Signal quality score", "Predictive intent accuracy"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
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
# Intent Signal Tracking — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 120 hours over 6 months
**Pass threshold:** Sustained or improving intent-driven conversion (>=3x vs cold) over 6 months via continuous agent-driven signal optimization, orchestration tuning, and market adaptation

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
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes which intent signal patterns best predict closed-won deals; auto-adjusts scoring weights weekly based on revenue attribution.

2. Set up the agent to run experiments on signal definitions: test new signals (e.g., LinkedIn post engagement, competitor review comments), measure predictive power, promote winners to production model.

3. Build a feedback loop where every closed-won deal triggers the agent to analyze that account's intent history; identify early signals that appeared 30-60 days before close and boost those signals.

4. Deploy real-time intent orchestration: agent monitors PostHog stream and auto-generates personalized outreach based on signal type (pricing → ROI case study, API docs → sandbox offer, G2 → competitive battle card).

5. Implement market adaptation: if intent-to-close conversion drops >20% for 2+ weeks, agent investigates (are signals leading to spam traps? new competitor?) and suggests adjustments.

6. Build AI-driven intent clustering: agent groups accounts by intent pattern (researchers, evaluators, buyers) and auto-routes to specialized sales motions (nurture, demo, close).

7. Create predictive intent scoring: agent uses machine learning on historical intent data to predict which accounts will cross high-intent threshold in next 7 days; proactively warm up those accounts.

8. Agent continuously tests outreach timing: for each signal type, experiment with immediate vs 1-hour vs 4-hour delay to find optimal response time; auto-implements winners.

9. Implement multi-channel intent orchestration: when high-intent account identified, agent triggers coordinated sequence (immediate email, LinkedIn connection request in 2 days, direct call in 4 days) and monitors which channel converts.

10. Establish monthly review cycles: agent generates intent performance reports showing signal quality, conversion trends, and recommended model updates; team reviews and approves scoring changes or rolls back underperforming experiments.

---

## KPIs to track
- Intent conversion rate
- Agent experiment win rate
- Signal quality score
- Predictive intent accuracy

---

## Pass threshold
**Sustained or improving intent-driven conversion (>=3x vs cold) over 6 months via continuous agent-driven signal optimization, orchestration tuning, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
