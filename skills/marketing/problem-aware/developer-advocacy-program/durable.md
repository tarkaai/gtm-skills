---
name: developer-advocacy-program-durable
description: >
    Developer Advocacy Program — Durable Intelligence. Build developer relations function to create
  technical content, speak at events, and engage developer communities for brand awareness and lead
  generation.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Events, Communities"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained content output and ≥50 qualified leads/quarter over 12 months via AI-assisted content creation and topic optimization"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "developer-advocacy-program"
install: "npx gtm-skills add marketing/problem-aware/developer-advocacy-program"
drills:
  - dashboard-builder
---
# Developer Advocacy Program — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Events, Communities

## Overview
Developer Advocacy Program — Durable Intelligence. Build developer relations function to create technical content, speak at events, and engage developer communities for brand awareness and lead generation.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained content output and ≥50 qualified leads/quarter over 12 months via AI-assisted content creation and topic optimization

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build performance dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard tracking: weekly impressions trend, engagement rate by content pillar, follower growth rate, DMs and leads from content, content-attributed pipeline value. Set alerts for engagement rate drops.

### 2. Autonomous content optimization
Configure the agent to: monitor which content pillars are trending up or down, suggest retirement of underperforming topics, propose new topics based on ICP pain point research, and auto-generate content briefs for the next week based on what performed best.

### 3. Run monthly content reviews
The agent generates a monthly report: top-performing posts, engagement trends, audience growth, content-to-pipeline attribution. Review and approve the next month's content strategy.

### 4. Evaluate sustainability
Measure against: Sustained content output and ≥50 qualified leads/quarter over 12 months via AI-assisted content creation and topic optimization. This level runs continuously. If engagement sustains or grows, the play is durable. If engagement decays, test new content formats or platforms.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained content output and ≥50 qualified leads/quarter over 12 months via AI-assisted content creation and topic optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/developer-advocacy-program`_
