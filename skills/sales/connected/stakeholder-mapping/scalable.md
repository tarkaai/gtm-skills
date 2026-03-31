---
name: stakeholder-mapping-scalable
description: >
  Stakeholder Mapping Framework — Scalable Automation. Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Social, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=60% of deals with >=4 stakeholders and >=30% faster close time for multi-threaded deals over 2 months"
kpis: ["Stakeholders per deal", "Multi-threading rate", "Stakeholder engagement score", "Single-threaded risk rate"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Stakeholder Mapping Framework — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social, Email

## Overview
Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=60% of deals with >=4 stakeholders and >=30% faster close time for multi-threaded deals over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo
- **LinkedIn Sales Navigator:** ~$100/mo
- **Dripify or Expandi (LinkedIn sequences):** ~$60–100/mo

_Total play-specific: ~$60–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Scale stakeholder mapping to 50+ deals per quarter; integrate Clay with Attio to auto-populate org charts and identify likely stakeholders based on titles and reporting structures.

2. Build an n8n workflow triggered when a new opportunity is created: pull org chart from LinkedIn/Clay, identify roles (VP Sales, Head of Ops, etc.), predict stakeholder roles (Economic Buyer, Influencer), create contacts in Attio.

3. Create stakeholder engagement scorecards in Attio: track touchpoint frequency, last contact date, sentiment, and engagement level for each stakeholder; flag stakeholders with no contact in 14 days.

4. Set up PostHog to track multi-threading metrics: average stakeholders per deal, percentage of deals with Economic Buyer engaged, percentage with >=3 stakeholders engaged.

5. In n8n, build automated multi-threading reminders: if a deal has <3 engaged stakeholders after 14 days, send alert to rep with suggested stakeholders to contact based on org chart.

6. Integrate email and calendar tools with Attio to auto-log stakeholder touchpoints; track who's been contacted, meeting attendance, and email engagement per stakeholder.

7. Build a stakeholder health dashboard in PostHog showing deals by multi-threading level, average engagement score per stakeholder role, and correlation between stakeholder count and close rate.

8. Implement stakeholder role prediction: use Clay enrichment + title patterns to auto-suggest Economic Buyer, Champion, or Blocker; reps validate and adjust during discovery.

9. Each week, identify deals with single-threaded risk (only 1-2 engaged stakeholders); prioritize multi-threading those deals before champion churn or organizational change derails them.

10. After 2 months, if >=60% of deals have >=4 stakeholders mapped and multi-threaded deals close >=30% faster, move to Durable; otherwise refine org chart sourcing or engagement playbooks.

---

## KPIs to track
- Stakeholders per deal
- Multi-threading rate
- Stakeholder engagement score
- Single-threaded risk rate

---

## Pass threshold
**>=60% of deals with >=4 stakeholders and >=30% faster close time for multi-threaded deals over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/stakeholder-mapping`_
