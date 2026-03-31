---
name: joint-content-campaigns-durable
description: >
    Joint Content Campaigns — Durable Intelligence. Co-create content (ebooks, guides, reports) with
  partners to combine expertise, share audiences, and generate leads from problem-aware and
  solution-aware prospects.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Content, Email"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained content output and ≥70 qualified leads over 12 months via AI-driven topic and partner selection"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "joint-content-campaigns"
install: "npx gtm-skills add marketing/problem-aware/joint-content-campaigns"
drills:
  - dashboard-builder
---
# Joint Content Campaigns — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Content, Email

## Overview
Joint Content Campaigns — Durable Intelligence. Co-create content (ebooks, guides, reports) with partners to combine expertise, share audiences, and generate leads from problem-aware and solution-aware prospects.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained content output and ≥70 qualified leads over 12 months via AI-driven topic and partner selection

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
Measure against: Sustained content output and ≥70 qualified leads over 12 months via AI-driven topic and partner selection. This level runs continuously. If partnerships consistently generate pipeline, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained content output and ≥70 qualified leads over 12 months via AI-driven topic and partner selection**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/joint-content-campaigns`_
