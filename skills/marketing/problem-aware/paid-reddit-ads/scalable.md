---
name: paid-reddit-ads-scalable
description: >
    Paid Reddit Ads — Scalable Automation. Run a small Reddit ad budget across a couple of sets and
  one LP to test if paid community placement drives leads or a meeting.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 30 leads or ≥ 16 meetings over 2 months"
kpis: ["Click-through rate", "Landing page visits"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---
# Paid Reddit Ads — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Overview
Paid Reddit Ads — Scalable Automation. Run a small Reddit ad budget across a couple of sets and one LP to test if paid community placement drives leads or a meeting.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 30 leads or ≥ 16 meetings over 2 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate campaign management
Run the `ab-test-orchestrator` drill to set up systematic creative testing: test 3-5 ad variants per audience, automatically pause underperformers, promote winners, and launch new variants weekly.

### 2. Build tool sync workflows
Run the `tool-sync-workflow` drill to connect: ad platform conversions to Attio deals, PostHog events to ad platform audiences (for lookalike targeting), and CRM data back to ad platforms for exclusion lists (don't target existing customers).

### 3. Scale budget with guardrails
Increase budget 20-30% monthly as long as CPA stays within target. Set automated alerts for CPA increases above 20%. Build n8n workflows to pause campaigns automatically if daily spend exceeds budget by 10%.

### 4. Evaluate against threshold
Measure against: ≥ 30 leads or ≥ 16 meetings over 2 months. If PASS, proceed to Durable. If FAIL, consolidate to best-performing audiences and creatives before scaling further.

---

## KPIs to track
- Click-through rate
- Landing page visits

---

## Pass threshold
**≥ 30 leads or ≥ 16 meetings over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/paid-reddit-ads`_
