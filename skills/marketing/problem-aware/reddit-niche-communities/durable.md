---
name: reddit-niche-communities-durable
description: >
  Reddit and community participation — Durable Intelligence. Authentic posting and commenting in Reddit and Slack/Discord communities where your ICP spends time, from a one-week smoke test through scaled participation and agent-driven optimization that sustains or improves referral traffic and signups over time.
stage: "Marketing > Problem Aware"
motion: "Communities & Forums"
channels: "Social, Communities"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving referral sessions or signups over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Referral traffic", "Comment engagement", "Link clicks"]
slug: "reddit-niche-communities"
install: "npx gtm-skills add marketing/problem-aware/reddit-niche-communities"
---
# Reddit and community participation — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Communities & Forums | **Channels:** Social, Communities

## Overview
Authentic posting and commenting in Reddit and Slack/Discord communities where your ICP spends time, from a one-week smoke test through scaled participation and agent-driven optimization that sustains or improves referral traffic and signups over time.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving referral sessions or signups over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Community management tool (Common Room or Orbit):** ~$50–200/mo
- **Premium community memberships:** ~$50–200/mo

_Total play-specific: ~$50–200/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Reddit** (Channel)
- **PostHog** (Product analytics)
- **n8n** (Automation)
- **Discord** (Communication)
- **Slack** (Communication)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Ensure PostHog receives all community-sourced referral and signup events so you have a single view of performance by community and over time.

2. In n8n, add AI-powered workflows triggered by PostHog: e.g. when referral or signup rate drops week-over-week, trigger an analysis that suggests which communities or content to emphasize or change.

3. Configure an AI agent to review weekly metrics: compare referral sessions and signups to prior weeks and to Scalable baseline; output recommendations (e.g. shift focus to higher-converting communities, test different CTA or value asset).

4. Run A/B tests on one variable at a time: e.g. CTA in comment vs in post; or one value asset vs another; use PostHog to segment by variant and measure signups per variant.

5. Have the agent recommend the winning variant and update your content or CTA approach; document the change and date.

6. Continuously test new communities or threads; log each experiment in PostHog and retire low-signal channels so the mix evolves.

7. Set a guardrail: if referral or signup volume falls more than 20% below Scalable baseline for two consecutive weeks, trigger an alert and have the agent suggest corrective actions.

8. Use the agent to monitor community rules and sentiment; suggest when to adjust tone or frequency to avoid fatigue or moderation issues.

9. Monthly: review which experiments improved or maintained referral and signup volume; double down on winning patterns.

10. Sustain or improve referral traffic and signups over 6 months by repeating measure-recommend-test-apply so the system adapts to community and platform changes.

---

## KPIs to track
- Referral traffic
- Comment engagement
- Link clicks

---

## Pass threshold
**Sustained or improving referral sessions or signups over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/reddit-niche-communities`_
