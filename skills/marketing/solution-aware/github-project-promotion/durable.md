---
name: github-project-promotion-durable
description: >
    GitHub Project Promotion — Durable Intelligence. Promote open-source projects on GitHub to build
  developer awareness, drive repository stars, and generate inbound technical leads.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Communities, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained star growth (≥20% QoQ) and ≥40 qualified leads/quarter over 12 months via AI-driven promotion and community engagement"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - dashboard-builder
---
# GitHub Project Promotion — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Communities, Social

## Overview
GitHub Project Promotion — Durable Intelligence. Promote open-source projects on GitHub to build developer awareness, drive repository stars, and generate inbound technical leads.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained star growth (≥20% QoQ) and ≥40 qualified leads/quarter over 12 months via AI-driven promotion and community engagement

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
Measure against: Sustained star growth (≥20% QoQ) and ≥40 qualified leads/quarter over 12 months via AI-driven promotion and community engagement. This level runs continuously. If directories consistently drive qualified traffic, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained star growth (≥20% QoQ) and ≥40 qualified leads/quarter over 12 months via AI-driven promotion and community engagement**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/github-project-promotion`_
