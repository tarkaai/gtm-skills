---
name: technical-requirements-discovery-durable
description: >
  Technical Requirements Discovery — Durable Intelligence. Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving technical fit accuracy and implementation success over 6 months via continuous AI-driven technical intelligence"
kpis: ["Technical fit prediction accuracy", "Technical blocker early detection", "Implementation success rate", "Solutions engineer efficiency", "Technical win rate"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
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
# Technical Requirements Discovery — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.

**Time commitment:** 140 hours over 6 months
**Pass threshold:** Sustained or improving technical fit accuracy and implementation success over 6 months via continuous AI-driven technical intelligence

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

1. Deploy PostHog event streams triggering n8n AI agents when: new opportunity lacks technical assessment after 48 hours, complex technical requirement emerges, or technical blocker is identified.

2. Build n8n AI technical intelligence agent analyzing won/lost deal data: identifies which technical requirements predict wins, which integrations are deal-breakers, which security needs are negotiable.

3. Implement AI-powered technical discovery: AI agent analyzes sales call transcripts and emails to automatically extract technical requirements; auto-populates technical assessment in Attio.

4. Create learning loop: PostHog tracks which technical discovery approaches uncover critical requirements early; AI agent recommends optimal technical qualification sequences by industry and prospect tech maturity.

5. Build adaptive technical fit scoring: AI agent learns from closed deals which technical factors most strongly predict success; continuously refines scoring model.

6. Deploy proactive technical risk management: AI agent monitors technical discussions for emerging blockers; suggests mitigation strategies (roadmap commitments, partner integrations, workarounds).

7. Implement automatic technical content matching: AI agent analyzes prospect's specific technical needs and automatically surfaces most relevant technical collateral and case studies.

8. Create technical competitive intelligence: AI agent tracks competitor technical capabilities from win/loss data; identifies technical differentiation opportunities and gaps.

9. Set guardrails: if technical discovery completion drops >15% or prediction accuracy falls below Scalable benchmark for 2+ weeks, alert technical sales team and suggest refinements.

10. Establish monthly review cycle: analyze technical requirement evolution, discovery question effectiveness, technical win/loss patterns; refine AI agent intelligence based on implementation outcomes.

---

## KPIs to track
- Technical fit prediction accuracy
- Technical blocker early detection
- Implementation success rate
- Solutions engineer efficiency
- Technical win rate

---

## Pass threshold
**Sustained or improving technical fit accuracy and implementation success over 6 months via continuous AI-driven technical intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/technical-requirements-discovery`_
