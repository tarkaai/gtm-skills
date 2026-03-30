---
name: success-criteria-definition-durable
description: >
  Success Criteria Definition — Durable Intelligence. Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "145 hours over 6 months"
outcome: "Sustained or improving success criteria achievement and customer satisfaction over 6 months via continuous AI-driven success intelligence"
kpis: ["Success criteria achievement rate", "Customer satisfaction score", "Close rate with AI-recommended criteria", "Renewal rate correlation", "Expectation alignment accuracy"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
---
# Success Criteria Definition — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Co-create specific, measurable success criteria with prospects to align expectations and provide clear evaluation framework for purchase decision.

**Time commitment:** 145 hours over 6 months
**Pass threshold:** Sustained or improving success criteria achievement and customer satisfaction over 6 months via continuous AI-driven success intelligence

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

1. Deploy PostHog event streams triggering n8n AI agents when: opportunity reaches connection stage without defined success criteria, criteria appear unrealistic, or historical similar deals failed to achieve similar goals.

2. Build n8n AI success intelligence agent analyzing historical customer outcomes: identifies which success criteria are most achievable, which predict highest satisfaction, which correlate with expansion and renewal.

3. Implement AI-powered success criteria recommendation: AI agent analyzes prospect characteristics and suggests optimal success criteria based on what similar customers have successfully achieved.

4. Create learning loop: PostHog tracks which success criteria definition approaches lead to highest close rates and best post-sale outcomes; AI agent recommends optimal success workshops by prospect type.

5. Build adaptive achievability scoring: AI agent continuously refines predictions of whether specific success criteria can be met based on latest product capabilities and customer achievement data.

6. Deploy proactive expectation management: when AI agent identifies success criteria that historically underperform, suggests alternative metrics or timeline adjustments to prevent post-sale disappointment.

7. Implement automatic success validation: AI agent monitors post-sale customer data in PostHog; tracks whether defined success criteria are being achieved; alerts if metrics are trending below targets.

8. Create predictive success scoring: AI agent predicts likelihood of achieving stated success criteria for each deal; flags high-risk commitments for sales leadership review.

9. Set guardrails: if success criteria achievement rate drops >15% or definition rate falls below Scalable benchmark for 2+ weeks, alert team and suggest criteria refinements.

10. Establish monthly review cycle: analyze success criteria achievement trends, definition effectiveness, customer outcome patterns; refine AI agent intelligence and success frameworks based on actual results.

---

## KPIs to track
- Success criteria achievement rate
- Customer satisfaction score
- Close rate with AI-recommended criteria
- Renewal rate correlation
- Expectation alignment accuracy

---

## Pass threshold
**Sustained or improving success criteria achievement and customer satisfaction over 6 months via continuous AI-driven success intelligence**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/success-criteria-definition`_
