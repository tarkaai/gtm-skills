---
name: ai-meeting-prep-baseline
description: >
  AI-Powered Meeting Preparation — Baseline Run. Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=60% prep time reduction and >=25% higher next-step conversion for AI-prepped calls over 2 weeks"
kpis: ["Prep time reduction", "Next-step conversion rate", "AI brief usefulness score", "Discovery quality improvement"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# AI-Powered Meeting Preparation — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** >=60% prep time reduction and >=25% higher next-step conversion for AI-prepped calls over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Apollo (includes dialer) or Aircall:** ~$50–100/mo

_Total play-specific: ~$50–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **OpenAI** (AI/LLM)
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)

---

## Instructions

1. Expand AI prep to 15-20 calls over 2 weeks; create standardized AI prep workflows using Claude API or GPT-4 API with company name, call type (discovery, demo, close), and rep notes as inputs.

2. Build a Notion or Attio template for AI-generated call briefs; for each call, run AI research and populate template sections automatically; reps review and customize before call.

3. Set pass threshold: AI prep reduces average prep time by >=60% (from 20 min to <=8 min) and AI-prepped calls have >=25% higher next-step conversion rate over 2 weeks.

4. Enhance AI prompts with specific instructions: "Identify 3 likely pain points based on [company's industry and size]. For each pain, suggest a discovery question to validate. Find competitors they might be evaluating. Suggest 2 case studies from similar companies."

5. Integrate AI prep with Attio: before each scheduled call, auto-trigger AI research via n8n workflow; AI pulls company data from Attio + web research, generates brief, saves to call record in Attio.

6. Add competitive intelligence to AI briefs: AI searches for mentions of your competitors in prospect's content, job postings, tech stack, or G2 reviews; prepares battlecard talking points.

7. Sync AI prep data from Attio to PostHog; create a funnel showing ai_prep_completed → call_conducted → next_step_scheduled; measure impact of AI prep on call outcomes.

8. After calls, have reps rate AI brief usefulness and provide feedback on what was helpful vs not; use feedback to refine AI prompts iteratively.

9. After 2 weeks, compare call outcomes for AI-prepped vs non-prepped calls: measure next-step rate, discovery quality (# of pain points uncovered), and rep confidence scores.

10. If AI prep reduces time by >=60% and improves next-step rate by >=25%, move to Scalable; otherwise refine AI prompts, add data sources, or improve brief templates.

---

## KPIs to track
- Prep time reduction
- Next-step conversion rate
- AI brief usefulness score
- Discovery quality improvement

---

## Pass threshold
**>=60% prep time reduction and >=25% higher next-step conversion for AI-prepped calls over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/ai-meeting-prep`_
