---
name: stakeholder-mapping-baseline
description: >
  Stakeholder Mapping Framework — Baseline Run. Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Social, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=70% of deals with >=4 stakeholders mapped and >=25% faster close time for multi-threaded deals over 2 weeks"
kpis: ["Stakeholders per deal", "Multi-threading rate", "Deal velocity by stakeholder count", "Single-threaded deal risk"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
---
# Stakeholder Mapping Framework — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social, Email

## Overview
Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** >=70% of deals with >=4 stakeholders mapped and >=25% faster close time for multi-threaded deals over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Clay** (Enrichment)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Expand stakeholder mapping to 10-15 deals over 2 weeks; build a visual stakeholder map in Attio for each deal showing relationships (reports to, influences, collaborates with).

2. Develop a stakeholder discovery playbook with questions for each role: Champion ("Who else should I talk to?"), Economic Buyer ("What's your budget process?"), Blocker ("What concerns do you have?").

3. Set pass threshold: map >=4 stakeholders per deal (including Economic Buyer and Champion) for >=70% of deals, and multi-threaded deals (>=3 stakeholder touchpoints) close >=25% faster.

4. Use LinkedIn and Clay to research org structures; identify reporting lines, team sizes, and recent hires to predict who's involved in buying decision.

5. For each deal, create engagement strategy: schedule calls with Economic Buyer, arm Champion with internal selling materials, address Blocker concerns directly, demo to End Users.

6. Track multi-threading progress in Attio: log every stakeholder touchpoint (call, email, meeting); aim for >=3 active stakeholders engaged per deal.

7. Sync stakeholder data from Attio to PostHog; build a funnel showing stakeholder_mapped → stakeholder_engaged → multiple_stakeholders_engaged → deal_progressed.

8. Identify single-threaded risks: deals with only 1 engaged stakeholder are vulnerable to champion leaving or changing priorities; flag for immediate multi-threading.

9. After 2 weeks, compare deal velocity and close rate between single-threaded (1-2 stakeholders) and multi-threaded (>=3 stakeholders) deals.

10. If >=70% of deals have >=4 stakeholders mapped and multi-threaded deals close >=25% faster, document stakeholder playbook and move to Scalable; otherwise refine discovery or engagement tactics.

---

## KPIs to track
- Stakeholders per deal
- Multi-threading rate
- Deal velocity by stakeholder count
- Single-threaded deal risk

---

## Pass threshold
**>=70% of deals with >=4 stakeholders mapped and >=25% faster close time for multi-threaded deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/stakeholder-mapping`_
