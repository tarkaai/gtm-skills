---
name: multi-stakeholder-discovery-scalable
description: >
  Multi-Stakeholder Discovery Process — Scalable Automation. Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "62 hours over 2 months"
outcome: "Multi-stakeholder discovery on ≥75% of complex deals at scale over 2 months with improved consensus building"
kpis: ["Stakeholder coverage rate", "Consensus building success", "Multi-threading efficiency", "Close rate improvement", "Deal velocity"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
---
# Multi-Stakeholder Discovery Process — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Conduct discovery across all key stakeholders to understand diverse needs, priorities, and concerns before proposing solution.

**Time commitment:** 62 hours over 2 months
**Pass threshold:** Multi-stakeholder discovery on ≥75% of complex deals at scale over 2 months with improved consensus building

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
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Build n8n workflow that prompts stakeholder mapping after first discovery call; provides templates for tracking stakeholder matrix.

2. Create stakeholder intelligence: n8n analyzes LinkedIn and organizational data to predict stakeholder structure before first call; suggests who to engage.

3. Implement automated stakeholder outreach: n8n generates personalized meeting requests for each stakeholder group with tailored messaging by role.

4. Set up stakeholder engagement tracking: n8n monitors which stakeholders have been engaged, which need follow-up, which are blocking progress.

5. Connect PostHog to n8n: when key stakeholder group hasn't been engaged after 7 days, trigger reminder with suggested outreach approach.

6. Build stakeholder intelligence dashboard: track engagement coverage, consensus levels, multi-threading success rates, stakeholder-specific close rates.

7. Create stakeholder content library: maintain role-specific materials (executive one-pagers, technical architecture docs, user guides, ROI calculators) for targeted engagement.

8. Set guardrails: stakeholder discovery completeness must stay ≥75% of Baseline level; deals must engage ≥3 stakeholder types before proposal.

9. Implement stakeholder gap alerting: flag deals advancing without key stakeholder engagement as high risk for late-stage blockers.

10. After 2 months, evaluate multi-stakeholder discovery impact on close rates and deal predictability; if metrics hold, proceed to Durable AI-driven stakeholder intelligence.

---

## KPIs to track
- Stakeholder coverage rate
- Consensus building success
- Multi-threading efficiency
- Close rate improvement
- Deal velocity

---

## Pass threshold
**Multi-stakeholder discovery on ≥75% of complex deals at scale over 2 months with improved consensus building**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/multi-stakeholder-discovery`_
