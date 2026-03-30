---
name: timing-qualification-scalable
description: >
  Timing Qualification Process — Scalable Automation. Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Scalable Automation"
time: "52 hours over 2 months"
outcome: "Timeline qualified on ≥70% of opportunities at scale over 2 months"
kpis: ["Timeline qualification rate", "Forecast accuracy", "Deal velocity by timeline", "Timeline slippage rate"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
---
# Timing Qualification Process — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.

**Time commitment:** 52 hours over 2 months
**Pass threshold:** Timeline qualified on ≥70% of opportunities at scale over 2 months

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

1. Build n8n workflow that prompts for timeline qualification after discovery calls; auto-assigns timeline category.

2. Create timeline intelligence: n8n analyzes prospect signals to predict urgency before first call.

3. Implement automated timeline-based cadences: urgent deals get next-day follow-up, long-term get nurture.

4. Set up timeline monitoring: n8n tracks whether deals progress according to stated timeline.

5. Connect PostHog to n8n: when deal timeline shifts, trigger automated strategy adjustment.

6. Build timeline accuracy dashboard tracking actual close dates vs predictions.

7. Create timeline-triggered content delivery: near-term prospects receive urgency-focused materials.

8. Set guardrails: timeline qualification rate must stay ≥70% of Baseline level.

9. Implement timeline risk scoring: flag deals with soft timelines as higher slippage risk.

10. After 2 months, evaluate impact on forecast accuracy; if metrics hold, proceed to Durable.

---

## KPIs to track
- Timeline qualification rate
- Forecast accuracy
- Deal velocity by timeline
- Timeline slippage rate

---

## Pass threshold
**Timeline qualified on ≥70% of opportunities at scale over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/timing-qualification`_
