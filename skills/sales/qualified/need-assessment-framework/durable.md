---
name: need-assessment-framework-durable
description: >
  Need Assessment Framework — Durable Intelligence. Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving close rate prediction and qualification accuracy over 6 months via continuous AI-driven need intelligence and adaptive assessment"
kpis: ["Need assessment accuracy", "Close rate prediction accuracy", "Sales cycle length", "Win rate by need profile", "Need intelligence refinement rate"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
---
# Need Assessment Framework — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Systematically evaluate whether prospects have genuine business needs your product solves to avoid wasting time on poor-fit opportunities.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving close rate prediction and qualification accuracy over 6 months via continuous AI-driven need intelligence and adaptive assessment

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

1. Deploy PostHog event streams that trigger n8n AI agents when: new opportunity lacks need assessment after 72 hours, need profile appears misaligned with ICP, or prospect's needs shift during sales cycle.

2. Build n8n AI need intelligence agent that analyzes won/lost deal data: identifies which need combinations and severity levels predict wins; continuously refines need scoring model based on outcomes.

3. Implement AI-powered need discovery: during discovery calls, AI agent (via call transcription) listens for need signals in real-time; suggests follow-up questions to probe deeper; auto-populates need assessment in Attio.

4. Create learning loop: PostHog tracks which discovery questions uncover the most critical needs and correlate with deal progression; AI agent recommends optimal question sequences by prospect segment.

5. Build adaptive need scoring: AI agent learns from closed deals which needs are strongest predictors of success for different ICPs, deal sizes, and industries; automatically adjusts scoring weights.

6. Deploy proactive need shift detection: AI agent monitors email threads and call notes for language indicating changing needs or priorities; alerts rep and suggests adjustment strategies.

7. Implement automatic need-to-solution mapping: AI agent generates personalized need-solution narratives for each prospect showing exactly how product addresses their specific need profile.

8. Create competitive need intelligence: AI agent analyzes competitor positioning and win/loss reasons; identifies need areas where you have strongest differentiation and focuses discovery there.

9. Set guardrails: if need assessment completion rate drops >15% or predictive accuracy falls below Scalable benchmark for 2+ weeks, n8n alerts team and agent suggests refinements.

10. Establish monthly review cycle: analyze need pattern evolution, discovery question effectiveness, predictive model accuracy; refine AI agent intelligence and need assessment methodology based on deal outcomes.

---

## KPIs to track
- Need assessment accuracy
- Close rate prediction accuracy
- Sales cycle length
- Win rate by need profile
- Need intelligence refinement rate

---

## Pass threshold
**Sustained or improving close rate prediction and qualification accuracy over 6 months via continuous AI-driven need intelligence and adaptive assessment**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/need-assessment-framework`_
