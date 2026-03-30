---
name: poc-management-framework-scalable
description: >
  POC Management Framework — Scalable Automation. Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Scalable Automation"
time: "68 hours over 2 months"
outcome: "POCs on ≥75% of qualified opportunities at scale over 2 months with improved conversion"
kpis: ["POC completion rate", "Success criteria achievement", "POC-to-close conversion", "Average POC duration", "Intervention effectiveness"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
---
# POC Management Framework — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Overview
Run structured proof-of-concept with clear success criteria, timeline, and stakeholder alignment to de-risk purchase decision and accelerate close.

**Time commitment:** 68 hours over 2 months
**Pass threshold:** POCs on ≥75% of qualified opportunities at scale over 2 months with improved conversion

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Cal.com** (Scheduling)

---

## Instructions

1. Build n8n workflow that triggers POC qualification assessment when deal reaches aligned stage; auto-generates POC scope based on prospect requirements.

2. Create POC automation: n8n provisions POC environments automatically, sends kickoff materials, schedules check-in meetings, delivers usage reports.

3. Implement POC health monitoring: n8n tracks PostHog usage data from POC environments; alerts when engagement is low, blockers emerge, or timeline is at risk.

4. Set up POC milestone tracking: n8n monitors whether POC milestones are being achieved on schedule; triggers interventions when progress stalls.

5. Connect PostHog to n8n: when POC usage drops below threshold for 48 hours, automatically trigger check-in email and suggest support resources.

6. Build POC intelligence dashboard: track POC pipeline, success criteria achievement rates, usage patterns, conversion rates, time-to-decision.

7. Create POC content library: maintain repository of POC success criteria templates, test scenarios, configuration guides, troubleshooting docs by use case.

8. Set guardrails: POC completion rate must stay ≥75% of Baseline level; POC-to-close conversion must remain ≥45%.

9. Implement predictive POC scoring: flag POCs at risk of failure early based on usage patterns and milestone achievement; prioritize intervention efforts.

10. After 2 months, evaluate POC management impact on close rates and sales cycle length; if metrics hold, proceed to Durable AI-driven POC intelligence.

---

## KPIs to track
- POC completion rate
- Success criteria achievement
- POC-to-close conversion
- Average POC duration
- Intervention effectiveness

---

## Pass threshold
**POCs on ≥75% of qualified opportunities at scale over 2 months with improved conversion**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/poc-management-framework`_
