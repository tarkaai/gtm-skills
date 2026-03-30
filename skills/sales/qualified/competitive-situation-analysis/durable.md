---
name: competitive-situation-analysis-durable
description: >
  Competitive Situation Assessment — Durable Intelligence. Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "135 hours over 6 months"
outcome: "Sustained or improving win rates against competitors over 6 months via continuous AI-driven competitive intelligence and adaptive positioning"
kpis: ["Win rate by competitor", "Competitive intelligence freshness", "Positioning effectiveness", "Competitive discovery accuracy", "AI-driven win rate improvement"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
---
# Competitive Situation Assessment — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.

**Time commitment:** 135 hours over 6 months
**Pass threshold:** Sustained or improving win rates against competitors over 6 months via continuous AI-driven competitive intelligence and adaptive positioning

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

1. Deploy PostHog event streams triggering n8n AI agents when: competitor is mentioned in deal, competitive situation shifts, or win/loss data is logged.

2. Build n8n AI competitive intelligence agent analyzing historical win/loss data: identifies which competitive situations you win, which positioning strategies work best, which competitors are most defeatable.

3. Implement AI-powered competitive discovery: AI agent scans call transcripts and emails to automatically identify competitors being evaluated; extracts prospect sentiment and specific evaluation criteria.

4. Create learning loop: PostHog tracks which competitive questions and positioning approaches correlate with wins against specific competitors; AI agent recommends optimal competitive strategies by deal characteristics.

5. Build adaptive competitive positioning: AI agent analyzes latest competitor product updates, pricing changes, messaging shifts; automatically updates battlecards and suggests positioning adjustments.

6. Deploy real-time competitive intelligence: AI agent monitors competitor websites, review sites, social channels, press releases; alerts sales team to competitive threats and opportunities immediately.

7. Implement automatic competitive content generation: when new competitor emerges or existing competitor changes strategy, AI agent generates updated battlecard, comparison docs, and objection handlers.

8. Create predictive competitive analytics: AI agent identifies deal patterns that predict competitive losses early; suggests intervention strategies to improve win probability.

9. Set guardrails: if win rate against any major competitor drops >10% or competitive discovery rate falls below Scalable benchmark for 2+ weeks, alert team and recommend strategy refinements.

10. Establish monthly review cycle: analyze competitive win/loss trends, positioning effectiveness, competitor strategy evolution; refine AI agent intelligence and competitive playbooks based on outcomes.

---

## KPIs to track
- Win rate by competitor
- Competitive intelligence freshness
- Positioning effectiveness
- Competitive discovery accuracy
- AI-driven win rate improvement

---

## Pass threshold
**Sustained or improving win rates against competitors over 6 months via continuous AI-driven competitive intelligence and adaptive positioning**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/competitive-situation-analysis`_
