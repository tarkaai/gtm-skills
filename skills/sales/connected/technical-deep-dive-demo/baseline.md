---
name: technical-deep-dive-demo-baseline
description: >
  Technical Deep-Dive Demo — Baseline Run. Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: "Technical demos on ≥80% of technical opportunities over 2 weeks"
kpis: ["Technical demo rate", "Demo-to-POC conversion", "Technical validation speed", "Technical close rate"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
---
# Technical Deep-Dive Demo — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Deliver detailed technical demonstration for engineers and architects covering architecture, APIs, security, integrations, and implementation details.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** Technical demos on ≥80% of technical opportunities over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Apollo (includes dialer) or Aircall:** ~$50–100/mo
- **Intercom or Loops (in-app/email triggers):** ~$75–150/mo

_Total play-specific: ~$50–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Expand technical demos to 25-35 opportunities over 2 weeks; develop standardized technical demo framework.

2. Create technical demo modules: build reusable demo segments for architecture, APIs, security, integrations, performance; customize combination based on prospect's priorities.

3. Build technical demo environment: set up sandbox with realistic data, working integrations, and API playground for live interaction.

4. Set up PostHog event tracking: technical_demo_scheduled, demo_module_shown, live_api_call, integration_tested, technical_validation_achieved.

5. Develop technical stakeholder engagement rubric: measure depth of questions, level of technical scrutiny, hands-on participation, enthusiasm signals.

6. Track technical demo effectiveness: measure conversion to POC, proposal acceptance rate, technical objections surfaced, time to technical validation.

7. Create follow-up technical package: after demo, send architecture diagrams, API documentation, integration code samples, security documentation, performance benchmarks.

8. Set pass threshold: Technical demos on ≥80% of technically complex opportunities over 2 weeks with ≥50% converting to POC or proposal.

9. Analyze technical patterns: which demo modules drive highest engagement, which technical proof points are most compelling, which objections arise most frequently.

10. If threshold met, document technical demo playbook and proceed to Scalable; if not, refine technical presentation approach.

---

## KPIs to track
- Technical demo rate
- Demo-to-POC conversion
- Technical validation speed
- Technical close rate

---

## Pass threshold
**Technical demos on ≥80% of technical opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/technical-deep-dive-demo`_
