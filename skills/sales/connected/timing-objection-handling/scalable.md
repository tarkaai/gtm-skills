---
name: timing-objection-handling-scalable
description: >
  Timing Objection Handling — Scalable Automation. Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "56 hours over 2 months"
outcome: "Timing objections handled systematically at scale over 2 months with improved resolution rates"
kpis: ["Objection detection rate", "Resolution automation efficiency", "Timeline acceleration rate", "Deal velocity improvement", "Eventually close rate"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Timing Objection Handling — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.

**Time commitment:** 56 hours over 2 months
**Pass threshold:** Timing objections handled systematically at scale over 2 months with improved resolution rates

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

---

## Instructions

1. Build n8n workflow that detects timing objections in Attio notes and emails; automatically triggers timing objection playbook.

2. Create automated cost of inaction analysis: n8n pulls prospect data and generates personalized cost calculations showing financial impact of delay.

3. Implement timing objection intelligence: n8n analyzes historical timing objections to predict which are real constraints vs. avoidance; suggests appropriate response strategy.

4. Set up proactive timeline monitoring: n8n tracks deals approaching stated 'future timing'; triggers reengagement sequence 30 days before target date.

5. Connect PostHog to n8n: when timing objection is logged, automatically deliver relevant urgency content (seasonal prep guides, implementation timeline docs, cost calculators).

6. Build timing objection dashboard: track objection frequency, resolution rates, timeline acceleration success, eventual conversion rates, delay costs.

7. Create urgency content library: maintain repository of urgency drivers (quarter-end incentives, implementation timelines, case studies of delayed decisions, competitive timing risks).

8. Set guardrails: timing objection resolution rate must stay ≥70% of Baseline level; timeline acceleration must occur in ≥45% of cases.

9. Implement timing risk scoring: flag deals with weak urgency drivers or vague timelines as high risk for perpetual delay.

10. After 2 months, evaluate timing objection handling impact on deal velocity and pipeline conversion; if metrics hold, proceed to Durable AI-driven timing intelligence.

---

## KPIs to track
- Objection detection rate
- Resolution automation efficiency
- Timeline acceleration rate
- Deal velocity improvement
- Eventually close rate

---

## Pass threshold
**Timing objections handled systematically at scale over 2 months with improved resolution rates**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/timing-objection-handling`_
