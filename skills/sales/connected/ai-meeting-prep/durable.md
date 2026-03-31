---
name: ai-meeting-prep-durable
description: >
  AI-Powered Meeting Preparation — Durable Intelligence. Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving call outcomes (>=30% lift vs non-prepped) over 6 months via continuous agent-driven brief optimization, insight prioritization, and market adaptation"
kpis: ["Call outcome trend", "Agent experiment win rate", "Brief personalization impact", "Predictive accuracy"]
slug: "ai-meeting-prep"
install: "npx gtm-skills add sales/connected/ai-meeting-prep"
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
# AI-Powered Meeting Preparation — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Use AI to research accounts and prepare for sales calls automatically, from manual research checklists to AI agents that generate comprehensive call briefs with account intelligence, talk tracks, and objection responses in real-time.

**Time commitment:** 120 hours over 6 months
**Pass threshold:** Sustained or improving call outcomes (>=30% lift vs non-prepped) over 6 months via continuous agent-driven brief optimization, insight prioritization, and market adaptation

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (AI-assisted calling):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

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

1. Deploy an AI agent in n8n that continuously learns which meeting prep insights best predict successful call outcomes; auto-evolves brief templates and research focus based on won deals.

2. Set up the agent to run experiments on brief content: test emphasizing different insight categories (pain points vs tech stack vs competitive intel); promote highest-impact insights.

3. Build a feedback loop where every successful call triggers the agent to analyze which AI-provided insights were used and how; strengthens those research patterns for future briefs.

4. Deploy real-time meeting intelligence: agent monitors scheduled calls and generates updated briefs when new information emerges (funding announcement, executive hire, competitor mention); sends alerts to reps before calls.

5. Implement predictive meeting outcomes: agent analyzes brief quality, rep's historical performance, and deal context to predict call success probability; suggests additional prep for high-stakes, low-probability calls.

6. Build dynamic brief personalization: agent learns each rep's preferences (level of detail, preferred insights, reading time) and customizes briefs accordingly; some reps get bullet points, others get deep dives.

7. Create market adaptation logic: if buyer priorities shift (e.g., focus on cost during recession), agent automatically adjusts brief focus to emphasize cost-savings intel over growth intel.

8. Agent continuously refines data sources: tests different enrichment providers, news sources, and research databases; routes requests to highest-quality sources for each data type.

9. Implement automatic call prep-to-outcome tracking: agent connects brief contents to call recordings and outcomes; calculates which insights contribute most to successful calls and prioritizes those.

10. Establish monthly review cycles: agent generates meeting prep intelligence reports showing brief quality trends, insight effectiveness, adoption rates, and recommended research focus updates; team reviews and approves changes.

---

## KPIs to track
- Call outcome trend
- Agent experiment win rate
- Brief personalization impact
- Predictive accuracy

---

## Pass threshold
**Sustained or improving call outcomes (>=30% lift vs non-prepped) over 6 months via continuous agent-driven brief optimization, insight prioritization, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/ai-meeting-prep`_
