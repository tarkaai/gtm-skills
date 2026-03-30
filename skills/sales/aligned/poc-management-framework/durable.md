---
name: poc-management-framework-durable
description: >
  POC Management Framework — Durable Intelligence. Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: "Sustained or improving POC conversion rates over 6 months via continuous AI-driven POC intelligence and adaptive support"
kpis: ["POC-to-close conversion rate", "POC success prediction accuracy", "Intervention effectiveness", "Time to POC completion", "Customer satisfaction with POC"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
---
# POC Management Framework — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Overview
Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.

**Time commitment:** 160 hours over 6 months
**Pass threshold:** Sustained or improving POC conversion rates over 6 months via continuous AI-driven POC intelligence and adaptive support

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

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: POC is initiated, usage patterns indicate risk, milestones are missed, or success criteria aren't being met.

2. Build n8n AI POC intelligence agent analyzing historical POC data: identifies which success criteria predict closes, which usage patterns indicate strong intent, which interventions improve outcomes.

3. Implement AI-powered POC scoping: AI agent analyzes prospect requirements and historical similar POCs; recommends optimal success criteria, timeline, and test scenarios.

4. Create learning loop: PostHog tracks POC usage patterns, milestone achievement, and outcomes; AI agent learns which POC structures drive highest conversion by segment.

5. Build adaptive POC support: AI agent monitors POC engagement in real-time; predicts when prospect needs help; automatically suggests resources or triggers human intervention.

6. Deploy proactive POC risk management: AI agent identifies POC risk signals (declining usage, missed milestones, unanswered questions); recommends specific intervention strategies.

7. Implement automatic POC optimization: AI agent analyzes POC results and suggests improvements to success criteria, timeline, or support model for future POCs.

8. Create predictive POC outcomes: AI agent predicts POC success probability based on early usage patterns and engagement signals; prioritizes high-risk POCs for attention.

9. Set guardrails: if POC conversion rate drops >10% or completion rate falls below Scalable benchmark for 2+ weeks, alert team and suggest POC refinements.

10. Establish monthly review cycle: analyze POC success patterns, intervention effectiveness, prediction accuracy; refine AI agent intelligence based on POC outcomes and close rates.

---

## KPIs to track
- POC-to-close conversion rate
- POC success prediction accuracy
- Intervention effectiveness
- Time to POC completion
- Customer satisfaction with POC

---

## Pass threshold
**Sustained or improving POC conversion rates over 6 months via continuous AI-driven POC intelligence and adaptive support**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/poc-management-framework`_
