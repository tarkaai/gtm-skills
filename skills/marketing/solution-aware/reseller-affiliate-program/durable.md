---
name: reseller-affiliate-program-durable
description: >
    Reseller & Affiliate Program — Durable Intelligence. Recruit partners to sell your product for
  commission, expanding reach and generating leads from solution-aware audiences through partner
  networks.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained partner productivity and ≥20 deals/quarter over 12 months via AI-optimized partner enablement"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - dashboard-builder
---
# Reseller & Affiliate Program — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Reseller & Affiliate Program — Durable Intelligence. Recruit partners to sell your product for commission, expanding reach and generating leads from solution-aware audiences through partner networks.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained partner productivity and ≥20 deals/quarter over 12 months via AI-optimized partner enablement

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build partnership dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: leads per partner, conversion rate by partner, pipeline value by partnership type, partner engagement trends. Set alerts for declining partner referral volume.

### 2. Autonomous partnership management
Configure the agent to: monitor partner referral quality, flag partnerships with declining returns, suggest new partnership opportunities based on ICP overlap, and generate monthly partner reports.

### 3. Sustain and optimize
Monthly: review partner ROI, retire underperforming partnerships, test new collaboration formats. The agent identifies high-potential new partners from your Attio network data.

### 4. Evaluate sustainability
Measure against: Sustained partner productivity and ≥20 deals/quarter over 12 months via AI-optimized partner enablement. This level runs continuously. If partnerships consistently generate pipeline, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained partner productivity and ≥20 deals/quarter over 12 months via AI-optimized partner enablement**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/reseller-affiliate-program`_
