---
name: timing-qualification-durable
description: >
  Timing Qualification Process — Durable Intelligence. Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "125 hours over 6 months"
outcome: "Sustained or improving forecast accuracy over 6 months via continuous AI-driven timeline intelligence"
kpis: ["Forecast accuracy", "Timeline slippage rate", "Deal velocity improvement", "Urgency detection accuracy"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
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
# Timing Qualification Process — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Determine prospect's urgency and buying timeline to prioritize opportunities ready to close now and avoid pipeline bloat from future deals.

**Time commitment:** 125 hours over 6 months
**Pass threshold:** Sustained or improving forecast accuracy over 6 months via continuous AI-driven timeline intelligence

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
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: deal stalls beyond timeline, urgency signals appear, or competitive pressure increases.

2. Build n8n AI timeline intelligence agent analyzing historical data: identifies which timelines prove accurate, which urgency triggers predict fastest closes.

3. Implement AI-powered urgency detection: AI scans call transcripts for true urgency language; auto-adjusts timeline categorization.

4. Create learning loop: PostHog tracks which timing questions yield accurate predictions; AI recommends optimal discovery sequences.

5. Build adaptive timeline forecasting: AI refines close date predictions based on deal progression signals.

6. Deploy proactive timeline risk management: when AI detects slippage signals, triggers intervention playbook.

7. Implement automatic urgency creation: AI identifies legitimate deadline opportunities and suggests urgency tactics.

8. Create timing pattern intelligence: AI analyzes seasonal trends and company-specific buying patterns.

9. Set guardrails: if forecast accuracy drops >20% for 2+ weeks, alert team and suggest refinements.

10. Establish monthly review cycle: analyze accuracy trends, slippage patterns; refine AI intelligence based on outcomes.

---

## KPIs to track
- Forecast accuracy
- Timeline slippage rate
- Deal velocity improvement
- Urgency detection accuracy

---

## Pass threshold
**Sustained or improving forecast accuracy over 6 months via continuous AI-driven timeline intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/timing-qualification`_
