---
name: template-tool-marketplaces-durable
description: >
  Template or Tool Marketplace — Durable Intelligence. Publish a free template (Notion, Airtable, Figma, etc.
stage: "Marketing > Solution Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline."
kpis: ["Download rate", "Landing page visits"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
---
# Template or Tool Marketplace — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Overview
Publish a free template (Notion, Airtable, Figma, etc.) with a CTA to test if templates as lead magnet drive downloads and a lead.

**Time commitment:** 200 hours over 6 months
**Pass threshold:** Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.

---

## Budget

**Play-specific tools & costs**
- **G2 or Capterra sponsored listings:** ~$1,000–3,000/mo
- **Reputation management tool (optional):** ~$100–300/mo

_Total play-specific: ~$100–3000/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)

---

## Instructions

1. Ensure PostHog is receiving events from all your tools so you have a single view of performance over time; create a dashboard for Download rate, Landing page visits.

2. In n8n, add AI-powered workflows triggered by PostHog: e.g. when a key metric drops week-over-week, trigger an analysis that suggests changes to messaging, timing, or targeting.

3. Configure an AI agent to review weekly performance: compare current week to prior weeks and to Scalable baseline; output concrete recommendations (e.g. change subject line, shift send window, tighten list).

4. Run A/B tests on one variable at a time (e.g. subject line, send time, audience segment); use PostHog to segment events by variant and compute conversion per variant.

5. Have the agent recommend the winning variant and apply the change to the live workflow; document the change and date.

6. Run continuous experiments on messaging, timing, and targeting; log each experiment and outcome in PostHog.

7. Set a guardrail: if performance falls more than 20% below Scalable baseline for two consecutive weeks, trigger an alert and have the agent suggest rollback or corrective actions.

8. Use the agent to monitor deliverability, inbox health, or channel-specific issues; suggest when to rotate or adjust.

9. Monthly: review which experiments improved or maintained results; double down on winning patterns and retire underperformers.

10. Sustain or improve outcomes over 6 months (Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.) by repeating the cycle: measure, recommend, A/B test, apply, and adapt to market changes.

---

## KPIs to track
- Download rate
- Landing page visits

---

## Pass threshold
**Sustained or improving downloads and leads over 6 months via continuous agent-driven experiments and adaptation to market changes; agents learn and tune workflows to stay aligned with or exceed Scalable baseline.**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/template-tool-marketplaces`_
