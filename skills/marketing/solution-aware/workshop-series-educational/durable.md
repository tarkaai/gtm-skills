---
name: workshop-series-educational-durable
description: >
    Workshop Series — Durable Intelligence. Run educational workshops teaching relevant skills or
  frameworks to generate leads, demonstrate expertise, and engage solution-aware audiences hands-on.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events, Content"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained workshop attendance and ≥45 qualified leads/quarter over 12 months via AI-driven content optimization"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - dashboard-builder
---
# Workshop Series — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events, Content

## Overview
Workshop Series — Durable Intelligence. Run educational workshops teaching relevant skills or frameworks to generate leads, demonstrate expertise, and engage solution-aware audiences hands-on.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained workshop attendance and ≥45 qualified leads/quarter over 12 months via AI-driven content optimization

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
Measure against: Sustained workshop attendance and ≥45 qualified leads/quarter over 12 months via AI-driven content optimization. This level runs continuously. If events consistently generate pipeline, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained workshop attendance and ≥45 qualified leads/quarter over 12 months via AI-driven content optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/workshop-series-educational`_
