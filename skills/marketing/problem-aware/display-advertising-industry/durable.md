---
name: display-advertising-industry-durable
description: >
    Display Advertising — Durable Intelligence. Run banner ads on relevant industry sites and
  publications to build awareness and drive traffic from problem-aware and solution-aware target
  audiences.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained display efficiency and ≥50 qualified leads/month over 12 months via AI-optimized placements"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "display-advertising-industry"
install: "npx gtm-skills add marketing/problem-aware/display-advertising-industry"
drills:
  - dashboard-builder
---
# Display Advertising — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Display Advertising — Durable Intelligence. Run banner ads on relevant industry sites and publications to build awareness and drive traffic from problem-aware and solution-aware target audiences.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained display efficiency and ≥50 qualified leads/month over 12 months via AI-optimized placements

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
Measure against: Sustained display efficiency and ≥50 qualified leads/month over 12 months via AI-optimized placements. This level runs continuously. If ROAS sustains, the play is durable. If ROAS decays, test new platforms or audiences.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained display efficiency and ≥50 qualified leads/month over 12 months via AI-optimized placements**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/display-advertising-industry`_
