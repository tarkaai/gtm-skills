---
name: demo-storytelling-framework-durable
description: >
  Demo Storytelling Framework — Durable Intelligence. Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Durable Intelligence"
time: "145 hours over 6 months"
outcome: "Sustained or improving demo engagement and conversion over 6 months via continuous AI-driven story intelligence and narrative optimization"
kpis: ["Demo-to-proposal conversion", "Engagement score", "Story matching accuracy", "Emotional connection rate", "Close rate improvement"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
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
# Demo Storytelling Framework — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Transform product demos from feature walkthroughs into compelling narratives using customer stories and prospect-specific scenarios to drive emotional engagement and conviction.

**Time commitment:** 145 hours over 6 months
**Pass threshold:** Sustained or improving demo engagement and conversion over 6 months via continuous AI-driven story intelligence and narrative optimization

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (AI-assisted calling):** ~$100–300/mo
- **Intercom or Loops (agent-driven messaging):** ~$150–400/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)
- **Gong** (Sales Engagement)

---

## Instructions

1. Deploy PostHog event streams triggering n8n AI agents when: demo is scheduled, prospect shows low engagement signals, or story selection is needed.

2. Build n8n AI story intelligence agent analyzing demo recordings and outcomes: identifies which narratives drive highest engagement and conversion by prospect type.

3. Implement AI-powered story customization: AI agent takes base customer story and adapts it in real-time to prospect's specific context, industry nuances, and pain points.

4. Create learning loop: PostHog and Gong track engagement signals during storytelling demos; AI agent learns which narrative elements create strongest emotional connection and conviction.

5. Build adaptive story recommendations: AI agent continuously refines which stories to use for which prospects based on latest conversion data and engagement patterns.

6. Deploy real-time demo coaching: AI agent monitors demo in real-time; suggests which story elements to emphasize, which customer outcomes to highlight based on prospect reactions.

7. Implement automatic story generation: AI agent creates new customer stories from case study interviews and customer conversations; generates narrative frameworks optimized for different segments.

8. Create predictive engagement modeling: AI agent predicts which stories will resonate most with each prospect; helps reps select narratives with highest probability of driving conviction.

9. Set guardrails: if demo-to-proposal conversion improvement drops below 10% or storytelling adoption falls below Scalable benchmark for 2+ weeks, alert team and suggest refinements.

10. Establish monthly review cycle: analyze story performance, engagement patterns, narrative effectiveness; refine AI agent intelligence and story library based on demo outcomes and close rates.

---

## KPIs to track
- Demo-to-proposal conversion
- Engagement score
- Story matching accuracy
- Emotional connection rate
- Close rate improvement

---

## Pass threshold
**Sustained or improving demo engagement and conversion over 6 months via continuous AI-driven story intelligence and narrative optimization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-storytelling-framework`_
