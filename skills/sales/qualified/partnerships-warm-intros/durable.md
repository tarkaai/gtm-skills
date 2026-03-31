---
name: partnerships-warm-intros-durable
description: >
    Partnerships & Warm Intros — Durable Intelligence. Ask advisors, angels, or partners for intros
  to test whether warm routes yield a few intros and meetings before refining ask and materials.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving intros and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Briefings scheduled", "Follow-up requests"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - dashboard-builder
---
# Partnerships & Warm Intros — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Overview
Partnerships & Warm Intros — Durable Intelligence. Ask advisors, angels, or partners for intros to test whether warm routes yield a few intros and meetings before refining ask and materials.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving intros and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

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
Measure against: Sustained or improving intros and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.. This level runs continuously. If partnerships consistently generate pipeline, the play is durable.

---

## KPIs to track
- Briefings scheduled
- Follow-up requests

---

## Pass threshold
**Sustained or improving intros and meetings over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/partnerships-warm-intros`_
