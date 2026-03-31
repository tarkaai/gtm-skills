---
name: technical-deep-dive-demo-smoke
description: >
  Technical Deep-Dive Demo — Smoke Test. Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: "Technical demos completed on ≥5 opportunities in 1 week"
kpis: ["Technical demo completion rate", "Demo-to-POC conversion rate", "Technical stakeholder engagement", "Technical blocker identification"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
drills:
  - icp-definition
  - threshold-engine
---
# Technical Deep-Dive Demo — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** Technical demos completed on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. Schedule 5-8 technical deep-dive demos with prospects who have passed initial discovery and have engaged technical stakeholders.

2. Pre-demo: gather technical requirements from discovery notes in Attio; identify which technical areas to emphasize (APIs, security, integrations, architecture, performance).

3. Structure demo in technical layers: system architecture overview, API capabilities and documentation, data model and schema, security and compliance features, integration patterns, performance and scale characteristics.

4. Demonstrate with technical depth: show actual API calls, review authentication flows, walk through integration code examples, discuss deployment options.

5. Invite technical questions throughout: encourage architects and engineers to probe deeply; treat objections as opportunities to showcase technical rigor.

6. Provide technical resources during demo: share API documentation links, integration guides, SDKs, architecture diagrams, security whitepapers.

7. Track PostHog events: technical_demo_completed, api_demonstrated, security_reviewed, integration_discussed, technical_question_answered.

8. Set pass threshold: Complete technical demos on ≥5 opportunities in 1 week with ≥60% advancing to POC or proposal stage.

9. Gather technical stakeholder feedback: ask 'What technical questions remain?' and 'Do you see any technical blockers?'.

10. Document which technical demo elements drive strongest engagement and progression; proceed to Baseline if threshold met.

---

## KPIs to track
- Technical demo completion rate
- Demo-to-POC conversion rate
- Technical stakeholder engagement
- Technical blocker identification

---

## Pass threshold
**Technical demos completed on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/technical-deep-dive-demo`_
