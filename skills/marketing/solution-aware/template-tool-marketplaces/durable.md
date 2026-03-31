---
name: template-tool-marketplaces-durable
description: >
    Template or Tool Marketplace — Durable Intelligence. Publish a free template (Notion, Airtable,
  Figma, etc.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Download rate", "Landing page visits"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - dashboard-builder
---
# Template or Tool Marketplace — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Template or Tool Marketplace — Durable Intelligence. Publish a free template (Notion, Airtable, Figma, etc.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build directory dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: traffic per directory, conversion rate per directory, review score trends, pipeline attributed to directory traffic. Set alerts for review score drops or traffic declines.

### 2. Autonomous directory management
Configure the agent to: monitor competitor listings for changes, alert when new reviews come in, suggest listing updates based on new features or positioning changes, and track directory ranking positions.

### 3. Sustain and optimize
Monthly: review directory ROI, update listing copy, request new reviews, and respond to recent reviews. The agent generates a monthly directory performance report.

### 4. Evaluate sustainability
Measure against: Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If directories consistently drive qualified traffic, the play is durable.

---

## KPIs to track
- Download rate
- Landing page visits

---

## Pass threshold
**Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/template-tool-marketplaces`_
