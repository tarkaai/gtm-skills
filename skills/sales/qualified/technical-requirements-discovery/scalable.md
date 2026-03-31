---
name: technical-requirements-discovery-scalable
description: >
  Technical Requirements Discovery — Scalable Automation. Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "58 hours over 2 months"
outcome: "Technical discovery completed on ≥70% of opportunities at scale over 2 months with improved technical fit prediction"
kpis: ["Technical discovery completion rate", "Technical fit prediction accuracy", "Solutions engineer efficiency", "Technical-driven close rate", "Implementation success rate"]
slug: "technical-requirements-discovery"
install: "npx gtm-skills add sales/qualified/technical-requirements-discovery"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Technical Requirements Discovery — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically uncover technical needs, integrations, security requirements, and constraints to prevent deal-killing surprises late in the sales cycle.

**Time commitment:** 58 hours over 2 months
**Pass threshold:** Technical discovery completed on ≥70% of opportunities at scale over 2 months with improved technical fit prediction

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)

---

## Instructions

1. Build n8n workflow that triggers technical discovery checklist after qualification; auto-assigns technical complexity score based on prospect data.

2. Create technical intelligence layer: n8n analyzes prospect's tech stack (from website, LinkedIn, job postings) and pre-populates likely technical requirements.

3. Implement automated technical routing: high technical complexity deals automatically schedule solutions engineer involvement; low complexity follow standard sales flow.

4. Set up technical requirement matching: n8n compares prospect's stated technical needs against product capabilities; flags gaps for product or solutions team.

5. Connect PostHog to n8n: when critical technical requirement is identified, trigger automated content delivery (security docs, integration guides, architecture diagrams).

6. Build technical intelligence dashboard: track technical requirement patterns, integration demands, security certification requests, technical win/loss reasons.

7. Create technical enablement library: maintain repository of technical collateral (SOC2 report, API docs, security questionnaires, reference architectures) accessible to sales.

8. Set guardrails: technical discovery completion rate must stay ≥70% of Baseline level; technical fit scoring must predict deal outcomes within 15% accuracy.

9. Implement technical risk alerting: flag deals with unmet technical requirements for product roadmap discussions or partnership solutions.

10. After 2 months, evaluate technical discovery impact on deal success and implementation smoothness; if metrics hold, proceed to Durable AI-driven technical intelligence.

---

## KPIs to track
- Technical discovery completion rate
- Technical fit prediction accuracy
- Solutions engineer efficiency
- Technical-driven close rate
- Implementation success rate

---

## Pass threshold
**Technical discovery completed on ≥70% of opportunities at scale over 2 months with improved technical fit prediction**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/technical-requirements-discovery`_
