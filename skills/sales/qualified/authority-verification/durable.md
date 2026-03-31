---
name: authority-verification-durable
description: >
  Authority Verification Process — Durable Intelligence. Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving deal velocity and close rate over 6 months via continuous AI-driven authority intelligence and adaptive navigation strategies"
kpis: ["Authority verification rate", "Deal velocity improvement", "Close rate with verified authority", "Multi-threading success rate", "Authority intelligence accuracy"]
slug: "authority-verification"
install: "npx gtm-skills add sales/qualified/authority-verification"
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
# Authority Verification Process — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Confirm you're speaking with actual decision-makers to prevent wasted cycles on non-buyers and accelerate deals through the right stakeholders.

**Time commitment:** 120 hours over 6 months
**Pass threshold:** Sustained or improving deal velocity and close rate over 6 months via continuous AI-driven authority intelligence and adaptive navigation strategies

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
- **LinkedIn Sales Navigator** (Channel)
- **Apollo** (Enrichment)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: new opportunity created without authority verification after 48 hours, deal stalls with non-decision-maker, or buying committee structure changes.

2. Build n8n AI authority intelligence agent that analyzes won/lost deals in Attio: identifies patterns in org structures that predict deal success; learns which authority levels and multi-threading strategies correlate with wins.

3. Implement continuous org chart learning: AI agent monitors job changes, promotions, and org restructures on LinkedIn; proactively updates Attio and alerts sales reps when authority structures shift.

4. Create AI-powered authority navigation: when rep logs call with influencer, AI agent suggests specific next steps: recommended questions, introduction requests, alternative paths to economic buyer based on similar successful deals.

5. Build learning loop: PostHog tracks authority verification tactics (questions, timing, approach) and correlates with meeting acceptance, deal progression, and close rate; AI agent surfaces winning patterns and shares with team.

6. Deploy adaptive authority scoring: AI agent continuously refines authority likelihood scoring based on historical data; learns industry-specific, company-size-specific, and role-specific authority patterns.

7. Implement automatic buying committee intelligence: AI agent analyzes email threads and call transcripts to identify all stakeholders; builds comprehensive RACI map; suggests who to engage next.

8. Create proactive authority risk alerts: when deals progress without verified economic buyer involvement, AI agent flags risk and recommends intervention strategies based on similar deal recovery patterns.

9. Set guardrails: if authority verification rate drops >15% or deal velocity improvement falls below Scalable benchmark for 2+ weeks, n8n alerts sales leadership and agent suggests process refinements.

10. Establish monthly review cycle: analyze authority verification effectiveness, org structure insights, multi-threading success patterns; refine AI agent intelligence and authority navigation strategies based on closed-won data.

---

## KPIs to track
- Authority verification rate
- Deal velocity improvement
- Close rate with verified authority
- Multi-threading success rate
- Authority intelligence accuracy

---

## Pass threshold
**Sustained or improving deal velocity and close rate over 6 months via continuous AI-driven authority intelligence and adaptive navigation strategies**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/authority-verification`_
