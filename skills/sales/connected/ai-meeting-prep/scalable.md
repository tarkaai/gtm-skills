---
name: ai-meeting-prep-scalable
description: >
  AI-Powered Meeting Preparation — Scalable Automation. Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "AI prep used in >=80% of calls with >=30% better outcomes vs non-prepped calls over 2 months"
kpis: ["AI prep adoption rate", "Call outcome improvement", "Prep time savings", "Brief quality score"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
---
# AI-Powered Meeting Preparation — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** AI prep used in >=80% of calls with >=30% better outcomes vs non-prepped calls over 2 months

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (calling at volume):** ~$100–200/mo

_Total play-specific: ~$100–200/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **OpenAI** (AI/LLM)
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale AI prep to 100+ calls per quarter; build fully automated n8n workflows that trigger 24 hours before every scheduled call: pull company data from Attio, enrich with Clay, run AI research via OpenAI API, generate brief, send to rep via email/Slack.

2. Create call-type-specific AI prep templates: Discovery (pain points, org structure, current solutions), Demo (feature priorities, competitive context, proof points), Proposal (budget signals, decision process, stakeholder map), Close (urgency factors, risk mitigation, next steps).

3. Set up PostHog to track AI prep effectiveness: monitor prep time, brief open rate (do reps actually read briefs?), insights referenced in calls (via call recording analysis), and correlation with call outcomes.

4. Implement AI-powered competitive intel: AI scans prospect's tech stack, job postings, G2 reviews, and social mentions to identify which competitors they're evaluating; auto-generates competitive positioning for that call.

5. Build persona-specific AI briefs: if meeting with CFO, AI emphasizes financial metrics, ROI, and risk; if CTO, emphasizes architecture, security, and integrations; if VP Sales, emphasizes ease-of-use and time-to-value.

6. Integrate AI prep with call recording tools: after call, AI compares brief to actual call topics; learns which insights were used, which weren't, and adjusts future briefs accordingly.

7. Create AI prep quality scoring: measure accuracy (were AI insights correct?), relevance (did insights apply to conversation?), actionability (could insights be used in call?); use scores to improve prompts.

8. Each week, analyze which AI-provided insights drive best call outcomes; prioritize those insights in future briefs (e.g., if competitive mentions improve conversion, emphasize competitor research).

9. Test AI brief length experiments: short (5 bullet points, 2 min read) vs detailed (2 pages, 5 min read); measure which reps prefer and which yields better outcomes.

10. After 2 months, if AI prep is used in >=80% of calls and call outcomes improve >=30% vs non-AI-prepped calls, move to Durable; otherwise refine brief quality or rep adoption.

---

## KPIs to track
- AI prep adoption rate
- Call outcome improvement
- Prep time savings
- Brief quality score

---

## Pass threshold
**AI prep used in >=80% of calls with >=30% better outcomes vs non-prepped calls over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/ai-meeting-prep`_
