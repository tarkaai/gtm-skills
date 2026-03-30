---
name: linkedin-founder-threads-durable
description: >
  Founder LinkedIn content — Durable Intelligence. Founder-led LinkedIn posts and short video with clear CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and agent-driven optimization that sustains or improves lead volume over time.
stage: "Marketing > Unaware"
motion: "Founder Social Content"
channels: "Social"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Impressions", "Engagement rate", "Profile visits", "CTA clicks"]
slug: "linkedin-founder-threads"
install: "npx gtm-skills add marketing/unaware/linkedin-founder-threads"
---
# Founder LinkedIn content — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Founder-led LinkedIn posts and short video with clear CTAs to build awareness and inbound leads, from a one-week smoke test through scaled content and agent-driven optimization that sustains or improves lead volume over time.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving inbound leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Taplio (analytics + AI content engine):** ~$50/mo
- **Buffer or Typefully:** ~$10–20/mo
- **Descript or Loom (repurposing content to video):** ~$15–30/mo

_Total play-specific: ~$10–50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **LinkedIn** (Channel)
- **Taplio** (Analytics)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Typefully** (Channel)
- **Buffer** (Channel)
- **Loom** (Video)
- **Descript** (Video)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Ensure PostHog receives all LinkedIn-sourced lead events and content events (impressions, engagement) so you have a single view of lead volume and content performance over time.

2. In n8n, add AI-powered workflows triggered by PostHog: e.g. when lead volume drops week-over-week, trigger an analysis that suggests content or CTA changes.

3. Configure an AI agent to review weekly metrics: compare leads, engagement, and profile visits to prior weeks and to Scalable baseline; output recommendations (e.g. try different hook style, test video vs text, adjust posting time).

4. Run A/B tests on one variable at a time: e.g. CTA "DM me" vs "Link in comments"; or post length short vs long; use PostHog to segment by variant and measure leads per variant.

5. Have the agent recommend the winning variant and update your content template or calendar; document the change and date.

6. Continuously test new topics and formats; log each experiment in PostHog and retire underperformers so the content mix evolves with what drives leads.

7. Set a guardrail: if lead volume falls more than 20% below Scalable baseline for two consecutive weeks, trigger an alert and have the agent suggest corrective actions (e.g. revert CTA, increase frequency).

8. Use the agent to monitor seasonal or platform changes (e.g. LinkedIn algorithm updates) and suggest adaptations to keep lead flow stable or growing.

9. Monthly: review which experiments improved or maintained lead volume; double down on winning patterns.

10. Sustain or improve inbound lead volume over 6 months by repeating measure-recommend-test-apply so the system adapts to market and stays aligned with or above Scalable results.

---

## KPIs to track
- Impressions
- Engagement rate
- Profile visits
- CTA clicks

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

_Install this skill: `npx gtm-skills add marketing/unaware/linkedin-founder-threads`_
