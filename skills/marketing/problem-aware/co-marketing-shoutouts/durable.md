---
name: co-marketing-shoutouts-durable
description: >
    Partner Newsletter Shoutout — Durable Intelligence. Run a short co-marketing blurb in a partner
  newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving clicks and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - dashboard-builder
---
# Partner Newsletter Shoutout — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Overview
Partner Newsletter Shoutout — Durable Intelligence. Run a short co-marketing blurb in a partner newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving clicks and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build partnership dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: leads per partner, conversion rate by partner, pipeline value by partnership type, partner engagement trends. Set alerts for declining partner referral volume.

### 2. Autonomous partnership management
Configure the agent to: monitor partner referral quality, flag partnerships with declining returns, suggest new partnership opportunities based on ICP overlap, and generate monthly partner reports.

### 3. Sustain and optimize
Monthly: review partner ROI, retire underperforming partnerships, test new collaboration formats. The agent identifies high-potential new partners from your Attio network data.

### 4. Evaluate sustainability
Measure against: Sustained or improving clicks and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If partnerships consistently generate pipeline, the play is durable.

---

## KPIs to track
- Impressions
- Click-through rate

---

## Pass threshold
**Sustained or improving clicks and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts`_
