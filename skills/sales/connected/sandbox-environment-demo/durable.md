---
name: sandbox-environment-demo-durable
description: >
  Sandbox Environment Demo — Durable Intelligence. Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.
stage: "Sales > Connected"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "152 hours over 6 months"
outcome: "Sustained or improving sandbox-to-close conversion over 6 months via continuous AI-driven usage intelligence and personalization"
kpis: ["Sandbox-to-close conversion", "Usage prediction accuracy", "Personalization effectiveness", "Active usage rate", "Deal velocity improvement"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
---
# Sandbox Environment Demo — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Overview
Provide hands-on sandbox environment during sales process so prospects can test product with their own data and use cases to validate fit and build confidence.

**Time commitment:** 152 hours over 6 months
**Pass threshold:** Sustained or improving sandbox-to-close conversion over 6 months via continuous AI-driven usage intelligence and personalization

---

## Budget

**Play-specific tools & costs**
- **Intercom (agent-triggered messaging, health-based):** ~$150–500/mo
- **Typeform (automated NPS + CSAT loops):** ~$25/mo
- **Descript (AI-powered video repurposing):** ~$30/mo

_Total play-specific: ~$25–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: sandbox is provisioned, usage patterns indicate risk or high intent, or milestones are achieved.

2. Build n8n AI sandbox intelligence agent analyzing historical usage data: identifies which usage patterns predict closes, which features drive conviction, which workflows validate fit.

3. Implement AI-powered sandbox personalization: AI agent analyzes prospect's needs and automatically generates customized sandbox with most relevant data, features, and suggested workflows.

4. Create learning loop: PostHog tracks sandbox usage patterns and correlates with deal outcomes; AI agent learns which engagement signals predict success and recommends optimal intervention timing.

5. Build adaptive sandbox guidance: AI agent monitors usage in real-time; provides contextual help, suggests next workflows, celebrates achievements based on individual exploration patterns.

6. Deploy predictive sandbox scoring: AI agent predicts close probability based on early usage signals; helps sales team prioritize high-intent prospects.

7. Implement automatic success path optimization: AI agent identifies most effective workflow sequences that lead to proposal acceptance; guides prospects along optimal evaluation path.

8. Create intelligent re-engagement: when sandbox usage drops, AI agent generates personalized re-engagement content addressing specific features or use cases prospect showed interest in.

9. Set guardrails: if sandbox-to-close conversion drops >10% or active usage rate falls below Scalable benchmark for 2+ weeks, alert team and suggest experience refinements.

10. Establish monthly review cycle: analyze usage patterns, conversion predictors, intervention effectiveness; refine AI agent intelligence based on sandbox outcomes and close rates.

---

## KPIs to track
- Sandbox-to-close conversion
- Usage prediction accuracy
- Personalization effectiveness
- Active usage rate
- Deal velocity improvement

---

## Pass threshold
**Sustained or improving sandbox-to-close conversion over 6 months via continuous AI-driven usage intelligence and personalization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/sandbox-environment-demo`_
