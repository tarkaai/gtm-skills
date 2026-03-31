---
name: win-loss-analysis-scalable
description: >
  Win/Loss Analysis Program — Scalable Automation. Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=50% interview completion rate and measurable win rate improvement from implemented insights over 2 months"
kpis: ["Interview completion rate", "Win rate trend", "Insight implementation rate", "Impact of changes on metrics"]
slug: "win-loss-analysis"
install: "npx gtm-skills add sales/won/win-loss-analysis"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Win/Loss Analysis Program — Scalable Automation

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.

**Time commitment:** 75 hours over 2 months
**Pass threshold:** >=50% interview completion rate and measurable win rate improvement from implemented insights over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Fireflies** (Sales Engagement)
- **Cal.com** (Scheduling)

---

## Instructions

1. Scale to 50+ interviews per quarter; build an n8n workflow that triggers when deal closes in Attio: send automated interview request email to key stakeholder, schedule interview via Cal.com, send reminder 24 hours before.

2. Integrate call recording tools (Fireflies, Gong) to auto-transcribe win/loss interviews; use AI to extract key themes (win reasons, loss reasons, competitive mentions, feature requests) and populate Attio fields.

3. Create a win/loss intelligence dashboard in PostHog showing: win rate trends, primary win/loss reasons over time, competitor win rates, feature gap impact, sales process effectiveness metrics.

4. Set up PostHog to track patterns: if loss rate increases for specific competitor, alert team; if feature gap appears in multiple losses, flag for product team; if pricing objections spike, review pricing strategy.

5. Build an automated win/loss report generator in n8n: monthly report compiling interview insights, win/loss trends, competitive intelligence, and recommended actions; distribute to sales, product, and leadership.

6. Implement structured follow-up on insights: create Attio tasks for each actionable insight, assign owners, track completion; measure impact of implemented changes on subsequent win rates.

7. Develop persona-specific interview questions: CFO interviews focus on ROI and business case, CTO interviews focus on technical fit, VP Sales interviews focus on sales process and value delivery.

8. Each month, compare win rate before vs after implementing win/loss insights; target >=10% win rate improvement or >=20% loss rate reduction in addressable loss categories.

9. Create a competitive intelligence repository fed by win/loss interviews: track competitor strengths, weaknesses, pricing changes, feature launches; use intel to update battlecards and positioning.

10. After 2 months, if interview completion rate >=50% and implemented changes show measurable impact on win rates, move to Durable; otherwise refine interview process or stakeholder engagement tactics.

---

## KPIs to track
- Interview completion rate
- Win rate trend
- Insight implementation rate
- Impact of changes on metrics

---

## Pass threshold
**>=50% interview completion rate and measurable win rate improvement from implemented insights over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/win-loss-analysis`_
