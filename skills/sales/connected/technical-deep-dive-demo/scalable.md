---
name: technical-deep-dive-demo-scalable
description: >
  Technical Deep-Dive Demo — Scalable Automation. Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Scalable Automation"
time: "64 hours over 2 months"
outcome: "Technical demos on ≥75% of technical opportunities at scale over 2 months with improved POC conversion"
kpis: ["Technical demo completion rate", "POC conversion rate", "Technical validation speed", "Solutions engineer efficiency", "Technical close rate"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
---
# Technical Deep-Dive Demo — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.

**Time commitment:** 64 hours over 2 months
**Pass threshold:** Technical demos on ≥75% of technical opportunities at scale over 2 months with improved POC conversion

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (calling at volume):** ~$100–200/mo
- **Intercom or Loops (automated sequences):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Gong** (Sales Engagement)

---

## Instructions

1. Build n8n workflow that triggers technical demo prep checklist when technical stakeholder is identified; auto-generates customized demo agenda.

2. Create technical demo intelligence: n8n analyzes prospect's tech stack and generates recommended demo focus areas; pre-populates technical questions likely to arise.

3. Implement automated demo environment setup: n8n provisions sandbox with prospect-relevant configurations, data, and integrations before each technical demo.

4. Set up technical demo recording: automatically record and transcribe technical demos; extract technical questions and commitments made for follow-up.

5. Connect PostHog to n8n: after technical demo, trigger automated delivery of technical package (docs, code samples, architecture diagrams) customized to topics discussed.

6. Build technical demo performance dashboard: track demo completion rates, module effectiveness, POC conversion, technical validation time, close rates.

7. Create technical demo library: maintain library of demo recordings, code examples, architecture patterns, integration demos organized by use case and tech stack.

8. Set guardrails: technical demo rate must stay ≥75% of Baseline level; POC conversion must remain ≥45%.

9. Implement technical stakeholder engagement scoring: measure quality of technical demos based on question depth, hands-on participation, and validation achievement.

10. After 2 months, evaluate technical demo impact on deal velocity and technical close rates; if metrics hold, proceed to Durable AI-driven technical intelligence.

---

## KPIs to track
- Technical demo completion rate
- POC conversion rate
- Technical validation speed
- Solutions engineer efficiency
- Technical close rate

---

## Pass threshold
**Technical demos on ≥75% of technical opportunities at scale over 2 months with improved POC conversion**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/technical-deep-dive-demo`_
