---
name: founder-guest-podcasts-durable
description: >
    Founder Guest Podcast — Durable Intelligence. Pitch a handful of micro podcasts for one guest
  spot to test whether podcast exposure drives at least one inbound lead.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Podcast listens", "Referral traffic"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - dashboard-builder
---
# Founder Guest Podcast — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Overview
Founder Guest Podcast — Durable Intelligence. Pitch a handful of micro podcasts for one guest spot to test whether podcast exposure drives at least one inbound lead.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build PR dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: media mentions over time, referral traffic from PR, backlink growth, PR-attributed leads, share of voice vs competitors. Set alerts for mention drops.

### 2. Autonomous PR monitoring
Configure the agent to: monitor brand and competitor mentions, flag PR opportunities (industry trends, breaking news where you can comment), generate pitch drafts for time-sensitive opportunities, and track journalist relationship health.

### 3. Sustain and evolve
Monthly: review PR impact on pipeline, identify new publications to target, update story angles based on product and market changes. The agent generates a monthly PR report.

### 4. Evaluate sustainability
Measure against: Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If PR consistently drives awareness and backlinks, the play is durable.

---

## KPIs to track
- Podcast listens
- Referral traffic

---

## Pass threshold
**Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/founder-guest-podcasts`_
