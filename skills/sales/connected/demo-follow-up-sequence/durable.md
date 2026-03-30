---
name: demo-follow-up-sequence-durable
description: >
  Demo Follow-Up Sequence — Durable Intelligence. Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "148 hours over 6 months"
outcome: "Sustained or improving demo-to-proposal conversion over 6 months via continuous AI-driven follow-up optimization and personalization"
kpis: ["Next step conversion rate", "Response rate", "Personalization effectiveness", "Demo-to-close rate", "Follow-up efficiency"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
---
# Demo Follow-Up Sequence — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.

**Time commitment:** 148 hours over 6 months
**Pass threshold:** Sustained or improving demo-to-proposal conversion over 6 months via continuous AI-driven follow-up optimization and personalization

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

1. Deploy PostHog event streams triggering n8n AI agents when: demo is completed, follow-up receives no response, or prospect shows buying signals.

2. Build n8n AI follow-up intelligence agent analyzing historical demo and follow-up data: identifies which follow-up approaches drive highest next step conversion by segment.

3. Implement AI-powered personalization: AI agent analyzes demo transcript and generates highly personalized follow-up content addressing specific points discussed, questions raised, and concerns mentioned.

4. Create learning loop: PostHog tracks which follow-up touches, timing, and content types correlate with highest response and conversion rates; AI agent continuously optimizes sequence.

5. Build adaptive follow-up timing: AI agent learns optimal follow-up timing by prospect segment and behavior patterns; dynamically adjusts send times to maximize engagement.

6. Deploy intelligent content recommendations: AI agent predicts which resources will be most valuable to each prospect based on demo discussion and similar customer journeys.

7. Implement real-time opportunity identification: AI agent monitors prospect website activity and content engagement; triggers relevant follow-up when buying signals appear.

8. Create predictive follow-up prioritization: AI agent scores demo follow-up opportunities by likelihood to convert; helps reps focus manual efforts on highest-probability deals.

9. Set guardrails: if next step conversion drops >10% or response rate falls below Scalable benchmark for 2+ weeks, alert team and suggest sequence refinements.

10. Establish monthly review cycle: analyze follow-up effectiveness, content performance, timing optimization, conversion patterns; refine AI agent intelligence based on demo outcomes.

---

## KPIs to track
- Next step conversion rate
- Response rate
- Personalization effectiveness
- Demo-to-close rate
- Follow-up efficiency

---

## Pass threshold
**Sustained or improving demo-to-proposal conversion over 6 months via continuous AI-driven follow-up optimization and personalization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-follow-up-sequence`_
