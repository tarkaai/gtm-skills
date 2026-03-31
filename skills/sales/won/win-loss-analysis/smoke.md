---
name: win-loss-analysis-smoke
description: >
  Win/Loss Analysis Program — Smoke Test. Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=4 win/loss interviews completed and >=3 actionable insights identified within 1 week"
kpis: ["Interview completion rate", "Insights per interview", "Actionable insight quality", "Time from close to interview"]
slug: "win-loss-analysis"
install: "npx gtm-skills add sales/won/win-loss-analysis"
drills:
  - icp-definition
  - threshold-engine
---
# Win/Loss Analysis Program — Smoke Test

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** >=4 win/loss interviews completed and >=3 actionable insights identified within 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create a win/loss interview template with 10-15 questions covering decision criteria, evaluation process, competitors considered, why you won/lost, pricing perception, champion strength, objections encountered.

2. Identify 5 recent closed deals (3 wins, 2 losses); schedule 20-30 minute interviews with key stakeholders (champion, economic buyer, or evaluator) within 2 weeks of close.

3. Set pass threshold: complete interviews for >=4 out of 5 deals, and identify >=3 actionable insights (sales process improvements, product gaps, positioning opportunities, competitive intel).

4. During interviews, ask open-ended questions: "What made you choose us?" "What almost made you not choose us?" "How did we compare to [competitor]?" "What could we have done better?" Take detailed notes.

5. For wins, understand what worked: Which features mattered most? Was pricing competitive? Was sales process smooth? Was champion strong? Use insights to replicate in future deals.

6. For losses, diagnose why: Missing feature? Too expensive? Competitor advantage? Weak champion? Poor sales execution? Identify if loss was preventable or unwinnable.

7. Log win/loss data in Attio with fields for primary_win_reason, primary_loss_reason, competitors_evaluated, decision_criteria, and actionable_insights; tag insights by category (product, pricing, sales process, competitive).

8. In PostHog, create events for deal_closed_won and deal_closed_lost with properties for win/loss reasons; track patterns over time.

9. After 1 week, synthesize findings: Are you losing on price? Specific features? Sales execution? Compile top 3 insights and share with team.

10. If >=4 interviews completed and >=3 actionable insights identified, win/loss analysis is valuable; document interview process and proceed to Baseline; otherwise refine questions or improve stakeholder access.

---

## KPIs to track
- Interview completion rate
- Insights per interview
- Actionable insight quality
- Time from close to interview

---

## Pass threshold
**>=4 win/loss interviews completed and >=3 actionable insights identified within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/win-loss-analysis`_
