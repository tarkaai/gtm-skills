---
name: reddit-ama-series-durable
description: >
    Reddit AMA Series — Durable Intelligence. Host Ask Me Anything sessions on relevant subreddits
  to build brand awareness, engage community, and generate inbound interest from problem-aware
  audiences.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Communities, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained community engagement and ≥35 qualified leads/quarter over 12 months via AI-optimized timing and topic selection"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "reddit-ama-series"
install: "npx gtm-skills add marketing/problem-aware/reddit-ama-series"
drills:
  - dashboard-builder
---
# Reddit AMA Series — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Communities, Social

## Overview
Reddit AMA Series — Durable Intelligence. Host Ask Me Anything sessions on relevant subreddits to build brand awareness, engage community, and generate inbound interest from problem-aware audiences.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained community engagement and ≥35 qualified leads/quarter over 12 months via AI-optimized timing and topic selection

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
Measure against: Sustained community engagement and ≥35 qualified leads/quarter over 12 months via AI-optimized timing and topic selection. This level runs continuously. If community-driven pipeline sustains, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained community engagement and ≥35 qualified leads/quarter over 12 months via AI-optimized timing and topic selection**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/reddit-ama-series`_
