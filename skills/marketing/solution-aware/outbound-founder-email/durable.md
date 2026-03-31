---
name: outbound-founder-email-durable
description: >
  Outbound founder-led email — Durable Intelligence. Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Durable Intelligence"
time: "250 hours over 6 months"
outcome: "Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Reply rate", "Time to first reply", "Emails sent"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - multi-channel-cadence
  - dashboard-builder
  - ab-test-orchestrator
---
# Outbound founder-led email — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Overview
Founder-sent cold email sequences to solution-aware prospects, from a small smoke test through scaled automation to agent-driven durable optimization that keeps or improves meeting rate over time.

**Time commitment:** 250 hours over 6 months
**Pass threshold:** Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo

_Total play-specific: ~$100–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Instantly** (Email)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Apollo** (Enrichment)
- **Loops** (Email)

---

## Instructions

1. Ensure PostHog is receiving events from Instantly, Attio, and n8n for every email sent, replied, and meeting booked; create a single dashboard for reply rate and meeting rate.

2. In n8n, add AI-powered workflows that are triggered by PostHog: e.g. when reply rate drops below a threshold, trigger an analysis workflow that suggests sequence or send-time changes.

3. Configure an AI agent (in n8n or external) to review weekly performance: compare current week to prior weeks and to Baseline; output recommendations (e.g. change subject line, shift send window, tighten list criteria).

4. Implement A/B tests for one variable at a time: e.g. subject line A vs B, or send time 9am vs 2pm; use PostHog to segment events by variant and compute conversion per variant.

5. Have the agent recommend which variant won and apply the change to the live sequence (e.g. update copy in Instantly or n8n); document the change and the date.

6. Run continuous experiments on sequence length, follow-up cadence, and targeting (e.g. industry or role); log each experiment and outcome in PostHog.

7. Set a guardrail: if meeting rate falls more than 20% below the Scalable baseline for two consecutive weeks, trigger an alert and have the agent suggest rollback or corrective actions.

8. Use the agent to monitor deliverability and inbox health across domains; suggest rotation or warm-up changes when needed.

9. Monthly: review which experiments improved or maintained meeting rate; double down on winning patterns and retire underperformers.

10. Sustain or improve meeting rate over 6 months by repeating the cycle: measure, recommend, A/B test, apply, and adapt to seasonal or market changes.

---

## KPIs to track
- Reply rate
- Time to first reply
- Emails sent

---

## Pass threshold
**Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-founder-email`_
