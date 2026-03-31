---
name: case-study-content-program-durable
description: >
  Case Study Content Program — Durable Intelligence. Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Durable Intelligence"
time: "90 hours over 6 months"
outcome: "Sustained or improving case study impact on deal close rate over 6 months via continuous AI-driven story optimization and intelligent case study deployment"
kpis: ["Deal close rate impact", "Case study engagement rate", "Sales usage rate", "Story refresh velocity", "Conversion rate trend"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
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
# Case Study Content Program — Durable Intelligence

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.

**Time commitment:** 90 hours over 6 months
**Pass threshold:** Sustained or improving case study impact on deal close rate over 6 months via continuous AI-driven story optimization and intelligent case study deployment

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
- **Riverside** (Video)
- **Cal.com** (Scheduling)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: new high-value customers emerge, case study performance degrades, or prospects show interest in specific use cases.

2. Build n8n AI case study strategist that analyzes PostHog and CRM data weekly: identifies which customer profiles and use cases drive highest conversion impact; prioritizes case study production accordingly.

3. Implement continuous story optimization: AI agent analyzes which case study narratives, metrics, and formats drive highest engagement and conversion; generates recommendations for improving existing case studies.

4. Create automatic case study refresh system: AI agent monitors customer results over time; when customers achieve new milestones, triggers update workflow to refresh case study with latest metrics.

5. Build learning loop: PostHog tracks which case studies are viewed at each sales stage and correlates with win/loss data; AI agent identifies most effective case study deployment patterns and shares insights with sales team.

6. Deploy AI case study matching engine: analyzes prospect's industry, use case, pain points, and company profile; automatically surfaces the 2-3 most relevant case studies for sales to use; learns from which recommendations drive meetings and closes.

7. Implement automatic content derivation: when a new case study is published, AI agent generates 10+ derivative content pieces (blog post, social posts, email copy, ad copy, sales talking points) and distributes via n8n.

8. Create competitive case study intelligence: n8n monitors competitor case studies and win stories; AI agent identifies their positioning patterns and suggests differentiated angles for your stories.

9. Set guardrails: if case study engagement drops >15% or conversion impact falls below Scalable benchmark for 2+ weeks, n8n alerts team and agent suggests story improvements or format changes.

10. Establish monthly review cycle: analyze which case study strategies worked, which customer segments to prioritize, which story formats to expand; refine AI agent prompts and production strategy based on conversion and sales impact data.

---

## KPIs to track
- Deal close rate impact
- Case study engagement rate
- Sales usage rate
- Story refresh velocity
- Conversion rate trend

---

## Pass threshold
**Sustained or improving case study impact on deal close rate over 6 months via continuous AI-driven story optimization and intelligent case study deployment**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/case-study-content-program`_
