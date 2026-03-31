---
name: executive-roundtables-durable
description: >
    Executive Roundtables — Durable Intelligence. Invite senior leaders for intimate, topic-focused
  discussions to build relationships and generate high-value pipeline with solution-aware
  executives.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained executive engagement and ≥25 opportunities/quarter over 12 months via AI-optimized topic selection"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - dashboard-builder
---
# Executive Roundtables — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Executive Roundtables — Durable Intelligence. Invite senior leaders for intimate, topic-focused discussions to build relationships and generate high-value pipeline with solution-aware executives.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained executive engagement and ≥25 opportunities/quarter over 12 months via AI-optimized topic selection

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build event dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: registration trends, attendance rates over time, pipeline generated per event, cost per attendee, content topic performance. Set alerts for declining registration or attendance rates.

### 2. Autonomous event optimization
Configure the agent to: analyze which event topics drive the most pipeline, suggest next event topics based on ICP pain point trends, auto-generate promotion copy for upcoming events, and flag when attendance rates are declining.

### 3. Sustain and evolve
Monthly: review event ROI, test new formats, and adjust cadence. The agent generates a monthly events report with recommendations.

### 4. Evaluate sustainability
Measure against: Sustained executive engagement and ≥25 opportunities/quarter over 12 months via AI-optimized topic selection. This level runs continuously. If events consistently generate pipeline, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained executive engagement and ≥25 opportunities/quarter over 12 months via AI-optimized topic selection**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/executive-roundtables`_
