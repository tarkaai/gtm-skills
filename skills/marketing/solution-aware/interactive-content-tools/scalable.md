---
name: interactive-content-tools-scalable
description: >
  Interactive Content Tools — Scalable Automation. Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: "≥1,200 completions/month and SQL rate ≥20%"
kpis: ["Tool completion rate", "Email capture rate", "SQL conversion rate", "Revenue attributed to tools", "Tool virality (shares)"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - activation-optimization
  - feature-announcement
  - upgrade-prompt
---
# Interactive Content Tools — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.

**Time commitment:** 55 hours over 2 months
**Pass threshold:** ≥1,200 completions/month and SQL rate ≥20%

---

## Budget

**Play-specific tools & costs**
- **Webflow (landing page optimization):** ~$15–40/mo
- **Hotjar (session recording + heatmaps):** ~$30/mo

_Total play-specific: ~$15–40/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Anthropic** (AI/LLM)
- **Attio** (CRM)

---

## Instructions

1. Scale to 8-12 interactive tools covering the full customer journey and multiple ICPs; build tools custom-coded or using advanced platforms for better branding and functionality.

2. Create n8n workflow to automate tool result personalization: based on user inputs, generate custom recommendations, content suggestions, and next steps using AI.

3. Implement advanced lead scoring in n8n: analyze tool responses to score leads by fit and intent; route high-scoring leads to sales, low-scoring to nurture campaigns.

4. Build multi-step tools with conditional logic: show different questions based on previous answers; provide highly personalized results and recommendations.

5. Integrate tools with PostHog and CRM (Attio): sync lead data, tool responses, and behavioral data for complete lead profiles.

6. Create automated content generation: when a user completes a tool, n8n generates a personalized PDF report with their results, benchmarks, and recommendations using AI.

7. Set guardrails: email capture rate must stay ≥50%; if completion rate drops below 40%, review tool UX and simplify or shorten.

8. Use PostHog to track complete funnel: tool_use → email_capture → nurture_email_open → demo_booked; optimize each step for conversion.

9. Run A/B tests on tool elements: question order, visual design, CTA placement, result presentation; use PostHog experiments to measure impact on completion and conversion rates.

10. After 2 months, evaluate total leads generated, SQL conversion rate, and revenue impact; if metrics hold, document the tool creation and automation pipeline and prepare for Durable AI-driven optimization; if metrics decline, improve tool value or lead nurture sequences.

---

## KPIs to track
- Tool completion rate
- Email capture rate
- SQL conversion rate
- Revenue attributed to tools
- Tool virality (shares)

---

## Pass threshold
**≥1,200 completions/month and SQL rate ≥20%**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/interactive-content-tools`_
