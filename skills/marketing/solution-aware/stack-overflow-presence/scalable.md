---
name: stack-overflow-presence-scalable
description: >
    Stack Overflow Presence — Scalable Automation. Answer questions on Stack Overflow to build
  authority, drive organic traffic, and generate awareness with solution-aware developers searching
  for solutions.
stage: "Marketing > Solution Aware"
motion: "Communities & Forums"
channels: "Communities"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥100 answers, ≥10,000 views, and ≥20 qualified leads over 4 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "stack-overflow-presence"
install: "npx gtm-skills add marketing/solution-aware/stack-overflow-presence"
drills:
  - tool-sync-workflow
  - ab-test-orchestrator
---
# Stack Overflow Presence — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Communities & Forums | **Channels:** Communities

## Overview
Stack Overflow Presence — Scalable Automation. Answer questions on Stack Overflow to build authority, drive organic traffic, and generate awareness with solution-aware developers searching for solutions.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥100 answers, ≥10,000 views, and ≥20 qualified leads over 4 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate community monitoring
Run the `tool-sync-workflow` drill to build n8n workflows that monitor target communities for relevant discussions, new questions matching your expertise, and mentions of competitors. Send alerts to Slack when high-opportunity threads appear.

### 2. Test engagement approaches
Run the `ab-test-orchestrator` drill to test: response formats (short vs detailed), content types (how-to vs opinion vs data), timing of engagement, and CTA approaches (soft mention vs case study link).

### 3. Scale to daily community presence
Respond to community threads daily using the monitoring alerts. Establish authority in 3-5 key communities. Track which communities drive the most qualified traffic and focus effort there.

### 4. Evaluate against threshold
Measure against: ≥100 answers, ≥10,000 views, and ≥20 qualified leads over 4 months. If PASS, proceed to Durable. If FAIL, reassess community selection or pivot to creating your own community.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥100 answers, ≥10,000 views, and ≥20 qualified leads over 4 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/stack-overflow-presence`_
