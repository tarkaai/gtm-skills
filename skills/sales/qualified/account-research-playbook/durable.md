---
name: account-research-playbook-durable
description: >
  Account Research & Intelligence — Durable Intelligence. Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation"
kpis: ["Reply rate trend", "Agent experiment win rate", "Signal prediction accuracy", "Research time efficiency"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
---
# Account Research & Intelligence — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation

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
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Deploy an AI agent in n8n that continuously learns which account signals best predict engagement and conversion; auto-prioritizes research focus on highest-signal data points.

2. Set up the agent to monitor accounts in real-time: detect trigger events (funding, hires, launches, competitor mentions) across news, LinkedIn, job boards, and social; auto-update account briefs and alert reps immediately.

3. Build a feedback loop where every replied or booked meeting triggers the agent to analyze which research insights were used in outreach; strengthens effective research patterns.

4. Deploy AI-driven personalization generation: agent analyzes account research data and auto-generates personalized email first lines, discovery questions, and value propositions tailored to that account's context.

5. Implement predictive account intelligence: agent predicts which accounts are entering buying mode based on signal patterns (hiring spree, funding, competitor dissatisfaction); surfaces those accounts for prioritized outreach.

6. Build market adaptation logic: if certain signals become less predictive (e.g., funding announcements correlate less with engagement during bear market), agent adjusts research focus to emphasize other signals.

7. Create automatic research refresh: agent monitors accounts in pipeline and updates research when new information emerges; ensures reps always have current intelligence before calls.

8. Agent continuously experiments with research depth: tests lightweight (5 min, 3 data points) vs deep (20 min, 10 data points) research and measures ROI; optimizes for highest outcomes per minute of research.

9. Implement dynamic signal weighting: agent learns which signals matter most for which segments (tech stack matters for developer tools, funding matters for growth-stage startups) and customizes research focus accordingly.

10. Establish monthly review cycles: agent generates account intelligence reports showing signal effectiveness, research ROI, personalization impact, and recommended research process updates; team reviews and approves changes.

---

## KPIs to track
- Reply rate trend
- Agent experiment win rate
- Signal prediction accuracy
- Research time efficiency

---

## Pass threshold
**Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/account-research-playbook`_
