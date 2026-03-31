---
name: win-loss-analysis-durable
description: >
  Win/Loss Analysis Program — Durable Intelligence. Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving win rates (>=10% lift in addressable categories) over 6 months via continuous agent-driven insight generation, competitive monitoring, and strategic adaptation"
kpis: ["Win rate trend", "Agent-generated insight quality", "Competitive intelligence accuracy", "Roadmap impact on win rate"]
slug: "win-loss-analysis"
install: "npx gtm-skills add sales/won/win-loss-analysis"
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
# Win/Loss Analysis Program — Durable Intelligence

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.

**Time commitment:** 140 hours over 6 months
**Pass threshold:** Sustained or improving win rates (>=10% lift in addressable categories) over 6 months via continuous agent-driven insight generation, competitive monitoring, and strategic adaptation

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
- **Fireflies** (Sales Engagement)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Deploy an AI agent in n8n that continuously analyzes win/loss interview transcripts to identify emerging patterns, competitive threats, and product gaps; auto-generates insights and alerts team to significant changes.

2. Set up the agent to run predictive win/loss analysis: based on deal characteristics (MEDDIC score, competitive situation, pain strength), predict close probability and primary risk factors; enables proactive intervention.

3. Build a feedback loop where every implemented change based on win/loss insights is tracked for impact; agent measures whether win rates improve in affected deal categories and strengthens successful interventions.

4. Deploy AI-driven interview question optimization: agent analyzes which questions yield highest-quality insights and adjusts interview guide over time; retires low-signal questions, adds high-signal questions.

5. Implement real-time competitive intelligence: agent monitors win/loss interviews for competitor mentions and strategy changes; alerts team when competitor gains advantage or loses ground in market.

6. Build automatic insight-to-action workflows: when agent identifies high-priority insight (e.g., "losing 3 deals to competitor X on feature Y"), auto-creates tasks for product, sales, and marketing teams with recommended responses.

7. Create market adaptation logic: if win/loss patterns shift (e.g., ROI becomes top criteria during recession), agent alerts team and suggests adjusting sales messaging, positioning, or qualification criteria.

8. Agent continuously refines win/loss categorization: learns from each interview to improve tagging of reasons, themes, and competitive dynamics; increases accuracy of trend detection.

9. Implement predictive roadmap prioritization: agent analyzes feature gap mentions in loss interviews and calculates potential revenue impact if gap were closed; informs product roadmap decisions.

10. Establish monthly review cycles: agent generates win/loss intelligence reports showing trend analysis, competitive landscape changes, insight impact tracking, and strategic recommendations; team reviews and approves actions or adjusts strategy.

---

## KPIs to track
- Win rate trend
- Agent-generated insight quality
- Competitive intelligence accuracy
- Roadmap impact on win rate

---

## Pass threshold
**Sustained or improving win rates (>=10% lift in addressable categories) over 6 months via continuous agent-driven insight generation, competitive monitoring, and strategic adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/win-loss-analysis`_
