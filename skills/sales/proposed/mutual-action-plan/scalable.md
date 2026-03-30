---
name: mutual-action-plan-scalable
description: >
  Mutual Action Plan (MAP) — Scalable Automation. Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=70% MAP adoption and >=35% faster close time with >=25% higher win rate for MAP deals over 2 months"
kpis: ["MAP adoption rate", "Milestone completion rate", "Deal velocity improvement", "Forecast accuracy by MAP adherence"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
---
# Mutual Action Plan (MAP) — Scalable Automation

> **Stage:** Sales → Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create timeline and milestones with prospect to align on deal progression and prevent stalls, from manual shared timelines to AI-driven MAP orchestration that monitors progress and auto-escalates risks.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=70% MAP adoption and >=35% faster close time with >=25% higher win rate for MAP deals over 2 months

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

1. Scale MAPs to 50+ deals per quarter; build n8n workflows that auto-generate draft MAPs when opportunities reach proposal stage: pull deal data from Attio, populate milestone template based on deal size and complexity, send draft to rep for review.

2. Integrate MAPs with Attio as custom objects: create MAP records linked to opportunities with milestone fields (name, owner, due date, status, dependencies); track completion automatically.

3. Set up PostHog to monitor MAP health in real-time: alert when milestones are overdue, when completion rate drops below 60%, or when multiple stakeholder-owned milestones are delayed (risk of stall).

4. Build automated MAP update workflows in n8n: weekly emails to prospects showing completed milestones, upcoming milestones, and overall progress; auto-generated with Attio data.

5. Create MAP templates by industry and deal complexity: SaaS SMB (10 milestones, 3-week timeline), Enterprise Security (20 milestones, 12-week timeline, includes POC and compliance review).

6. Implement MAP-based forecasting: use milestone completion rates and historical data to predict close probability and expected close date; deals with high MAP adherence forecast more accurately.

7. Build a MAP performance dashboard in PostHog showing adoption rate, completion rates by milestone type, average delay time, and impact on deal velocity and win rate.

8. Each week, identify deals with at-risk MAPs (low completion rate, multiple overdue milestones); prioritize those for sales leadership intervention or champion re-engagement.

9. Test different MAP formats: detailed (20+ milestones) vs streamlined (5-7 key milestones); measure which prospects prefer and which yields better completion rates.

10. After 2 months, if MAP adoption >=70% and MAP deals close >=35% faster with >=25% higher win rate, move to Durable; otherwise refine templates or improve stakeholder engagement.

---

## KPIs to track
- MAP adoption rate
- Milestone completion rate
- Deal velocity improvement
- Forecast accuracy by MAP adherence

---

## Pass threshold
**>=70% MAP adoption and >=35% faster close time with >=25% higher win rate for MAP deals over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/proposed/mutual-action-plan`_
