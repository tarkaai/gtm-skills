---
name: multi-stakeholder-discovery-durable
description: >
  Multi-Stakeholder Discovery Process — Durable Intelligence. Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving consensus building and close rates on complex deals over 6 months via continuous AI-driven stakeholder intelligence"
kpis: ["Stakeholder prediction accuracy", "Consensus achievement rate", "Hidden influencer identification", "Close rate on complex deals", "Multi-threading effectiveness"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
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
# Multi-Stakeholder Discovery Process — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.

**Time commitment:** 150 hours over 6 months
**Pass threshold:** Sustained or improving consensus building and close rates on complex deals over 6 months via continuous AI-driven stakeholder intelligence

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
- **Anthropic** (AI/LLM)
- **Gong** (Sales Engagement)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: key stakeholder group is unengaged, stakeholder structure changes, or consensus appears at risk.

2. Build n8n AI stakeholder intelligence agent analyzing historical deal data: identifies which stakeholder engagement patterns predict wins, which stakeholder gaps cause losses, optimal engagement sequences.

3. Implement AI-powered stakeholder prediction: AI agent analyzes prospect organization to predict complete stakeholder map including hidden influencers and potential blockers.

4. Create learning loop: PostHog tracks which stakeholder discovery approaches build strongest consensus; AI agent recommends optimal multi-threading strategies by deal complexity and organization type.

5. Build adaptive stakeholder prioritization: AI agent learns which stakeholders most strongly influence decisions in different contexts; dynamically prioritizes engagement efforts.

6. Deploy proactive consensus monitoring: AI agent analyzes email threads and call transcripts to detect stakeholder misalignment or emerging conflicts; suggests intervention strategies.

7. Implement automatic stakeholder content matching: AI agent analyzes each stakeholder's role, concerns, and communication style; surfaces most relevant content and talking points for each conversation.

8. Create stakeholder influence modeling: AI agent maps actual influence networks beyond org chart based on communication patterns and decision history; identifies true power brokers.

9. Set guardrails: if stakeholder coverage drops >15% or consensus building success falls below Scalable benchmark for 2+ weeks, alert team and suggest engagement refinements.

10. Establish monthly review cycle: analyze stakeholder engagement patterns, consensus strategies effectiveness, influence prediction accuracy; refine AI agent intelligence based on deal outcomes.

---

## KPIs to track
- Stakeholder prediction accuracy
- Consensus achievement rate
- Hidden influencer identification
- Close rate on complex deals
- Multi-threading effectiveness

---

## Pass threshold
**Sustained or improving consensus building and close rates on complex deals over 6 months via continuous AI-driven stakeholder intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/multi-stakeholder-discovery`_
