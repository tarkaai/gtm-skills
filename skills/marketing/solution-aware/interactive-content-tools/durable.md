---
name: interactive-content-tools-durable
description: >
  Interactive Content Tools — Durable Intelligence. Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Durable Intelligence"
time: "85 hours over 6 months"
outcome: "Sustained or improving lead generation and SQL conversion rate over 6 months via continuous AI-driven tool optimization and personalization"
kpis: ["Tool completion rate trend", "SQL conversion rate", "Revenue per tool lead", "Tool engagement depth", "Personalization effectiveness"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
  - churn-prevention
  - dashboard-builder
---
# Interactive Content Tools — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.

**Time commitment:** 85 hours over 6 months
**Pass threshold:** Sustained or improving lead generation and SQL conversion rate over 6 months via continuous AI-driven tool optimization and personalization

---

## Budget

**Play-specific tools & costs**
- **Webflow:** ~$15–40/mo
- **Hotjar or FullStory:** ~$30–100/mo

_Total play-specific: ~$15–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)
- **Attio** (CRM)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: tool usage patterns shift, completion rates decline, or high-intent leads are identified.

2. Build n8n AI tool optimization agent that analyzes PostHog data weekly: identifies which tool questions predict conversion, which answer patterns indicate high intent, which drop-off points need improvement.

3. Implement continuous tool experimentation: AI agent tests different question sequences, visual designs, result formats, and CTA placements; automatically promotes winning variants.

4. Create dynamic personalization system: AI agent analyzes user behavior (pages visited, content consumed, tool responses) and generates real-time personalized tool questions and results.

5. Build learning loop: PostHog tracks complete journey from tool use to closed revenue; AI agent identifies which tool types and result profiles correlate with highest win rates; adjusts tool strategy accordingly.

6. Deploy AI result generation: instead of static formulas, AI agent generates personalized recommendations, benchmarks, and next steps based on user inputs and industry data; continuously improves recommendations based on user feedback.

7. Implement automatic tool discovery: AI agent monitors customer conversations, support tickets, and sales calls for common questions or calculations; suggests new tool ideas; generates tool prototypes for testing.

8. Create competitive tool intelligence: n8n monitors competitor interactive content; AI agent identifies gaps and opportunities; generates differentiated tool concepts.

9. Set guardrails: if tool completion rate drops >15% or SQL conversion rate falls below Scalable threshold for 2+ weeks, n8n alerts team and agent suggests UX improvements.

10. Establish monthly review cycle: analyze which tool experiments succeeded, which tools drive most revenue, which new tool concepts to develop; refine AI agent prompts and tool strategy based on conversion and revenue data.

---

## KPIs to track
- Tool completion rate trend
- SQL conversion rate
- Revenue per tool lead
- Tool engagement depth
- Personalization effectiveness

---

## Pass threshold
**Sustained or improving lead generation and SQL conversion rate over 6 months via continuous AI-driven tool optimization and personalization**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/interactive-content-tools`_
