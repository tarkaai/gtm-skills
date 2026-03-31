---
name: cold-event-hallway-demos-durable
description: >
    Event Hallway Demos — Durable Intelligence. Run a single day of lobby or hallway demos at a
  venue to get instant feedback and a few meetings and validate whether in-person fits your ICP.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving demos and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Conversations started", "Follow-up requests"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - dashboard-builder
---
# Event Hallway Demos — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Other

## Overview
Event Hallway Demos — Durable Intelligence. Run a single day of lobby or hallway demos at a venue to get instant feedback and a few meetings and validate whether in-person fits your ICP.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving demos and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

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
Measure against: Sustained or improving demos and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If events consistently generate pipeline, the play is durable.

---

## KPIs to track
- Conversations started
- Follow-up requests

---

## Pass threshold
**Sustained or improving demos and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos`_
