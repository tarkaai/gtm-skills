---
name: communities-slack-discord-durable
description: >
    Slack/Discord Community Rhythm — Durable Intelligence. Join a few groups and post value weekly
  to test repeatable leads and whether to scale or pause low-signal communities.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Communities"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Engagement rate", "Inbound inquiries"]
slug: "communities-slack-discord"
install: "npx gtm-skills add marketing/problem-aware/communities-slack-discord"
drills:
  - dashboard-builder
---
# Slack/Discord Community Rhythm — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Communities

## Overview
Slack/Discord Community Rhythm — Durable Intelligence. Join a few groups and post value weekly to test repeatable leads and whether to scale or pause low-signal communities.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build community dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: traffic from each community, conversion rates by community, engagement trends, pipeline value attributed to community activity. Set alerts for traffic drops from key communities.

### 2. Autonomous community optimization
Configure the agent to: monitor community engagement trends, identify emerging communities in your space, flag when your reputation score drops (fewer upvotes, less engagement), and generate weekly community content briefs.

### 3. Sustain and evolve
The agent runs monthly reviews: which communities are driving the most pipeline, which are declining, what new communities should be tested. Adjust community allocation accordingly.

### 4. Evaluate sustainability
Measure against: Sustained or improving meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If community-driven pipeline sustains, the play is durable.

---

## KPIs to track
- Engagement rate
- Inbound inquiries

---

## Pass threshold
**Sustained or improving meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/communities-slack-discord`_
