---
name: qualified-prospect-calls-durable
description: >
  Founder calls to prospects — Durable Intelligence. Outbound calls from the founder to a tight list of qualified prospects, from a small smoke test through scaled call volume and agent-driven optimization that sustains or improves meeting rate over time.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Connect rate", "Dials attempted", "Time to connect"]
slug: "qualified-prospect-calls"
install: "npx gtm-skills add sales/qualified/qualified-prospect-calls"
---
# Founder calls to prospects — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Overview
Outbound calls from the founder to a tight list of qualified prospects, from a small smoke test through scaled call volume and agent-driven optimization that sustains or improves meeting rate over time.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$100–200/mo
- **Clay (enrichment + continuous list refresh):** ~$200–500/mo
- **LinkedIn Sales Navigator:** ~$100/mo
- **LinkedIn Sales Navigator:** ~$100/mo
- **Dripify or Expandi (LinkedIn automation):** ~$60–100/mo

_Total play-specific: ~$60–500/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **Clay** (Enrichment)
- **Cal.com** (Scheduling)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Instantly** (Email)
- **Apollo** (Enrichment)
- **Loops** (Email)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Ensure PostHog is receiving events from all your tools so you have a single view of performance over time; create a dashboard for Connect rate, Dials attempted, Time to connect.

2. In n8n, add AI-powered workflows triggered by PostHog: e.g. when a key metric drops week-over-week, trigger an analysis that suggests changes to messaging, timing, or targeting.

3. Configure an AI agent to review weekly performance: compare current week to prior weeks and to Scalable baseline; output concrete recommendations (e.g. change subject line, shift send window, tighten list).

4. Run A/B tests on one variable at a time (e.g. subject line, send time, audience segment); use PostHog to segment events by variant and compute conversion per variant.

5. Have the agent recommend the winning variant and apply the change to the live workflow; document the change and date.

6. Run continuous experiments on messaging, timing, and targeting; log each experiment and outcome in PostHog.

7. Set a guardrail: if performance falls more than 20% below Scalable baseline for two consecutive weeks, trigger an alert and have the agent suggest rollback or corrective actions.

8. Use the agent to monitor deliverability, inbox health, or channel-specific issues; suggest when to rotate or adjust.

9. Monthly: review which experiments improved or maintained results; double down on winning patterns and retire underperformers.

10. Sustain or improve outcomes over 6 months (Sustained or improving meeting rate over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.) by repeating the cycle: measure, recommend, A/B test, apply, and adapt to market changes.

---

## KPIs to track
- Connect rate
- Dials attempted
- Time to connect

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

_Install this skill: `npx gtm-skills add sales/qualified/qualified-prospect-calls`_
