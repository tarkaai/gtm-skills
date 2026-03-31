---
name: retargeting-campaigns-multi-platform-durable
description: >
    Multi-platform Retargeting — Durable Intelligence. Retarget website visitors across LinkedIn,
  Facebook, and display networks to stay top-of-mind and convert product-aware prospects who showed
  intent.
stage: "Marketing > Product Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained retargeting efficiency and ≥60 conversions/month over 12 months via AI-optimized creative rotation"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "retargeting-campaigns-multi-platform"
install: "npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform"
drills:
  - dashboard-builder
---
# Multi-platform Retargeting — Durable Intelligence

> **Stage:** Marketing → Product Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Overview
Multi-platform Retargeting — Durable Intelligence. Retarget website visitors across LinkedIn, Facebook, and display networks to stay top-of-mind and convert product-aware prospects who showed intent.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained retargeting efficiency and ≥60 conversions/month over 12 months via AI-optimized creative rotation

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
Measure against: Sustained retargeting efficiency and ≥60 conversions/month over 12 months via AI-optimized creative rotation. This level runs continuously. If ROAS sustains, the play is durable. If ROAS decays, test new platforms or audiences.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained retargeting efficiency and ≥60 conversions/month over 12 months via AI-optimized creative rotation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform`_
