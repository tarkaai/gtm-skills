---
name: pr-campaign-launch-durable
description: >
    PR Campaign Launch — Durable Intelligence. Coordinated press outreach for product launches or
  milestones to generate media coverage and awareness with problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting"
kpis: ["Sustained conversion rate", "AI experiment win rate", "Market adaptation speed", "Cost efficiency trend", "Lead quality score"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - dashboard-builder
---
# PR Campaign Launch — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
PR Campaign Launch — Durable Intelligence. Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.

**Time commitment:** 180 hours over 12 months
**Pass threshold:** Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting

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
Measure against: Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting. This level runs continuously. If PR consistently drives awareness and backlinks, the play is durable.

---

## KPIs to track
- Sustained conversion rate
- AI experiment win rate
- Market adaptation speed
- Cost efficiency trend
- Lead quality score

---

## Pass threshold
**Sustained media presence and ≥50 qualified leads/quarter over 12 months via AI-optimized press targeting**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/pr-campaign-launch`_
