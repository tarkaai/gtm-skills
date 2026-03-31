---
name: paid-social-ads-durable
description: >
    Paid Social Ads — Durable Intelligence. Run a capped spend across a couple of ad groups and one
  LP to see if you get first conversions or a meeting within budget.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving leads or meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Click-through rate", "Landing page visits"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
drills:
  - dashboard-builder
---
# Paid Social Ads — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Paid Social Ads — Durable Intelligence. Run a capped spend across a couple of ad groups and one LP to see if you get first conversions or a meeting within budget.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving leads or meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build paid media dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: ROAS by campaign, CPA trend over time, lead quality score by source, budget utilization, creative performance decay curves. Set alerts for CPA increases and ROAS drops.

### 2. Autonomous campaign optimization
Configure the agent to: detect creative fatigue (declining CTR over 5+ days), automatically generate new creative briefs, adjust bids based on conversion data, and reallocate budget from underperforming to overperforming campaigns weekly.

### 3. Run continuous improvement
Monthly: review full-funnel attribution (ad click to closed deal), identify which audiences and creatives drive revenue (not just leads), and adjust strategy accordingly. The agent generates a monthly paid media report.

### 4. Evaluate sustainability
Measure against: Sustained or improving leads or meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If ROAS sustains, the play is durable. If ROAS decays, test new platforms or audiences.

---

## KPIs to track
- Click-through rate
- Landing page visits

---

## Pass threshold
**Sustained or improving leads or meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/paid-social-ads`_
