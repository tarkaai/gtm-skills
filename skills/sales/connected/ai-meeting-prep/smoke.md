---
name: ai-meeting-prep-smoke
description: >
  AI-Powered Meeting Preparation — Smoke Test. Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=50% reduction in prep time and >=3 actionable insights per call within 1 week"
kpis: ["Prep time reduction", "Insights per call", "AI brief quality score", "Call outcome improvement"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
---
# AI-Powered Meeting Preparation — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** >=50% reduction in prep time and >=3 actionable insights per call within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **OpenAI** (AI/LLM)
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create an AI meeting prep prompt template in Claude or ChatGPT: "Research [Company] for sales call. Find: company overview, recent news, funding, tech stack, competitors, key decision-makers, potential pain points related to [your solution]." 

2. Before 5 upcoming sales calls, spend 10 minutes using AI to generate call briefs; paste company name and context into AI, review output, refine with additional searches if needed.

3. Set pass threshold: AI research reduces prep time by >=50% (from 20 min to <=10 min per call) and yields >=3 actionable insights per call within 1 week.

4. Structure AI-generated brief with sections: Company Overview (what they do, size, stage), Recent News (funding, launches, hires), Tech Stack (tools they use, integration opportunities), Pain Points (likely challenges based on industry/size), Key Stakeholders (names, titles, LinkedIn profiles), Suggested Talk Track (opening, discovery questions, value prop).

5. During calls, reference AI-discovered insights to build rapport: "Saw you just raised Series B—congrats! As you scale, [pain point] becomes critical..." validates research and establishes relevance.

6. After each call, rate AI brief quality (1-5) on accuracy, relevance, and actionability; note which AI-provided insights were most useful during conversation.

7. Log meeting prep metrics in a spreadsheet: prep_time, insights_used_in_call, call_outcome, ai_brief_quality_score; track whether AI prep correlates with better call outcomes.

8. In PostHog, create events for ai_prep_completed and call_conducted with properties for prep time, insights used, and call outcome.

9. After 1 week, measure: Did AI reduce prep time by >=50%? Did AI-prepped calls yield better outcomes (more discovery, stronger rapport, faster progression)?

10. If AI prep saves >=50% time and yields >=3 actionable insights per call, document AI prompts and proceed to Baseline; otherwise refine prompts or add additional data sources.

---

## KPIs to track
- Prep time reduction
- Insights per call
- AI brief quality score
- Call outcome improvement

---

## Pass threshold
**>=50% reduction in prep time and >=3 actionable insights per call within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/ai-meeting-prep`_
