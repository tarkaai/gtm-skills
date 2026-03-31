---
name: business-case-development-durable
description: >
  Business Case Development — Durable Intelligence. Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: "Sustained or improving executive approval rates over 6 months via AI-driven business case intelligence"
kpis: ["Executive approval rate", "Time to approval", "Business case ROI accuracy", "Enterprise win rate", "Deal size optimization"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
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
# Business Case Development — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Help prospects build compelling internal business case with quantified ROI, strategic alignment, and risk mitigation to secure executive and CFO approval.

**Time commitment:** 160 hours over 6 months
**Pass threshold:** Sustained or improving executive approval rates over 6 months via AI-driven business case intelligence

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

1. Deploy PostHog streams triggering n8n AI agents when: enterprise deal requires business case, executive review is scheduled, or approval stalls.

2. Build n8n AI business case intelligence agent analyzing historical approvals: identifies which financial metrics drive CFO approval, which strategic alignments resonate with CEOs, which risk mitigations satisfy boards.

3. Implement AI-powered business case generation: AI creates sophisticated business cases incorporating prospect-specific data, industry benchmarks, validated customer outcomes, and tailored executive messaging.

4. Create learning loop: PostHog tracks which business case elements correlate with executive approval and deal closure; AI refines recommendations by company size and industry.

5. Build adaptive financial modeling: AI generates realistic ROI projections based on latest customer outcome data; adjusts assumptions to maintain credibility.

6. Deploy intelligent approval navigation: AI analyzes approval chain dynamics; recommends stakeholder engagement strategy and timeline.

7. Implement proactive objection handling: AI predicts likely executive concerns based on company characteristics; prepares preemptive responses.

8. Create dynamic business case optimization: AI monitors which sections executives engage with; suggests emphasis adjustments in real-time.

9. Set guardrails: if approval rate drops >15% or time-to-approval increases significantly, alert team and suggest refinements.

10. Establish monthly review: analyze approval patterns, financial model accuracy, executive engagement; refine AI intelligence based on outcomes.

---

## KPIs to track
- Executive approval rate
- Time to approval
- Business case ROI accuracy
- Enterprise win rate
- Deal size optimization

---

## Pass threshold
**Sustained or improving executive approval rates over 6 months via AI-driven business case intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/business-case-development`_
