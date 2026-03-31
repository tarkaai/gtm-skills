---
name: multi-stakeholder-discovery-baseline
description: >
  Multi-Stakeholder Discovery Process — Baseline Run. Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Multi-stakeholder discovery on ≥80% of complex deals over 2 weeks"
kpis: ["Stakeholder coverage completeness", "Consensus achievement rate", "Multi-threading effectiveness", "Close rate on complex deals"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Multi-Stakeholder Discovery Process — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** Multi-stakeholder discovery on ≥80% of complex deals over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Expand multi-stakeholder discovery to 20-30 complex deals over 2 weeks.

2. Build stakeholder discovery framework: standardized approach to identify, prioritize, and engage all key decision participants.

3. Create stakeholder-specific question banks: tailored discovery questions for executives, technical buyers, end users, procurement, legal, security.

4. Set up PostHog event tracking: stakeholder_identified_by_type, discovery_depth_score, consensus_level, multi_threading_success.

5. Develop stakeholder engagement cadence: coordinate timing of discovery calls to gather input without overwhelming prospect organization.

6. Track stakeholder influence mapping: measure how well you understand power dynamics, who influences whom, where decision authority truly lies.

7. Build consensus-building strategies: when stakeholder needs conflict, develop approaches to find common ground or prioritize most critical needs.

8. Set pass threshold: Multi-stakeholder discovery on ≥80% of complex deals over 2 weeks with ≥75% achieving consensus on key requirements.

9. Analyze stakeholder patterns: which stakeholder combinations predict success, which blockers appear most often, which consensus strategies work best.

10. If threshold met, document multi-stakeholder playbook and proceed to Scalable; if not, refine stakeholder engagement approach.

---

## KPIs to track
- Stakeholder coverage completeness
- Consensus achievement rate
- Multi-threading effectiveness
- Close rate on complex deals

---

## Pass threshold
**Multi-stakeholder discovery on ≥80% of complex deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/multi-stakeholder-discovery`_
