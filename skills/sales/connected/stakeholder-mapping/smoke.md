---
name: stakeholder-mapping-smoke
description: >
  Stakeholder Mapping Framework — Smoke Test. Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Social, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=3 stakeholders mapped per deal for >=3 deals in 1 week"
kpis: ["Stakeholders per deal", "Economic Buyer identification rate", "Champion identification rate", "Deal velocity by stakeholder count"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
---
# Stakeholder Mapping Framework — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social, Email

## Overview
Identify and map all stakeholders in the buying process—champions, influencers, blockers, economic buyers—to ensure multi-threaded engagement and prevent single-point-of-failure deals, from manual org charts to AI-driven dynamic stakeholder intelligence.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=3 stakeholders mapped per deal for >=3 deals in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create a stakeholder mapping template in a spreadsheet with columns for Name, Title, Role in Deal (Champion, Influencer, Blocker, Economic Buyer, End User), Sentiment (Supporter/Neutral/Opposed), and Engagement Level (High/Medium/Low).

2. Select 3-5 active deals from your pipeline; for each deal, list all known stakeholders based on discovery calls and email threads.

3. For each stakeholder, assign their role in the buying process: Champion (internal advocate), Economic Buyer (budget authority), Influencer (shapes opinion), Blocker (resists change), End User (will use product).

4. Set pass threshold: map >=3 stakeholders per deal (including at least one Economic Buyer or Champion) for >=3 deals within 1 week.

5. During follow-up calls, ask stakeholder discovery questions: "Who else is involved in evaluating this?" "Who controls budget?" "Who will be using this day-to-day?" "Who might have concerns?"

6. After each call, update stakeholder map in spreadsheet and log in Attio; create custom fields for stakeholder_count, champion_identified, economic_buyer_identified.

7. In PostHog, create events for stakeholder_added with properties for role type, sentiment, and deal stage.

8. Identify gaps: deals missing Economic Buyer or Champion are high-risk; prioritize uncovering those roles in next calls.

9. After 1 week, analyze deals by stakeholder completeness: do deals with >=3 stakeholders mapped progress faster than those with 1-2?

10. If >=3 deals have >=3 stakeholders mapped and multi-stakeholder deals progress faster, document mapping process and proceed to Baseline; otherwise refine discovery questions.

---

## KPIs to track
- Stakeholders per deal
- Economic Buyer identification rate
- Champion identification rate
- Deal velocity by stakeholder count

---

## Pass threshold
**>=3 stakeholders mapped per deal for >=3 deals in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/stakeholder-mapping`_
