---
name: micro-events-webinars-durable
description: >
    Micro-Event or Webinar — Durable Intelligence. Run one short session with manual invites to test
  registrations, show rate, and at least one meeting before trying other topics or formats.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving regs, show rate, meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Registration rate", "Show rate"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - dashboard-builder
---
# Micro-Event or Webinar — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Micro-Event or Webinar — Durable Intelligence. Run one short session with manual invites to test registrations, show rate, and at least one meeting before trying other topics or formats.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving regs, show rate, meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

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
Measure against: Sustained or improving regs, show rate, meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If events consistently generate pipeline, the play is durable.

---

## KPIs to track
- Registration rate
- Show rate

---

## Pass threshold
**Sustained or improving regs, show rate, meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/micro-events-webinars`_
