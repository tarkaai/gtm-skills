---
name: timing-objection-handling-durable
description: >
  Timing Objection Handling — Durable Intelligence. Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving timing objection resolution and deal acceleration over 6 months via continuous AI-driven timing intelligence"
kpis: ["Timeline acceleration rate", "Objection resolution effectiveness", "True objection detection accuracy", "Deal velocity improvement", "Eventually close rate"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
---
# Timing Objection Handling — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.

**Time commitment:** 140 hours over 6 months
**Pass threshold:** Sustained or improving timing objection resolution and deal acceleration over 6 months via continuous AI-driven timing intelligence

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

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: timing objection is raised, deal timeline slips, or reengagement date approaches.

2. Build n8n AI timing intelligence agent analyzing historical timing objections and outcomes: identifies which are real constraints vs. avoidance, which resolution tactics work best by segment.

3. Implement AI-powered objection diagnosis: AI agent analyzes language patterns in objection to determine true underlying concern (budget, authority, technical fit, competing priority, risk aversion).

4. Create learning loop: PostHog tracks which timing objection responses lead to timeline acceleration and eventual closes; AI agent recommends optimal approaches by prospect type.

5. Build adaptive cost of inaction modeling: AI agent generates personalized, data-driven cost analyses based on prospect's specific situation and historical similar customer outcomes.

6. Deploy proactive timing risk management: AI agent monitors deal progression and predicts timing objections before they're raised; suggests preemptive urgency creation.

7. Implement intelligent reengagement: AI agent tracks reengagement timing and generates personalized outreach when stated 'right time' approaches or market conditions create urgency.

8. Create dynamic urgency generation: AI agent identifies prospect-specific urgency drivers (budget cycles, competitive pressures, seasonal needs, regulatory changes) and suggests timing tactics.

9. Set guardrails: if timeline acceleration rate drops >15% or resolution effectiveness falls below Scalable benchmark for 2+ weeks, alert team and suggest refinements.

10. Establish monthly review cycle: analyze timing objection patterns, resolution effectiveness, urgency tactics performance; refine AI agent intelligence based on deal outcomes.

---

## KPIs to track
- Timeline acceleration rate
- Objection resolution effectiveness
- True objection detection accuracy
- Deal velocity improvement
- Eventually close rate

---

## Pass threshold
**Sustained or improving timing objection resolution and deal acceleration over 6 months via continuous AI-driven timing intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/timing-objection-handling`_
