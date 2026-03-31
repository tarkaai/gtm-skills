---
name: win-loss-analysis-baseline
description: >
  Win/Loss Analysis Program — Baseline Run. Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks"
kpis: ["Interview completion rate", "Insights identified", "Changes implemented", "Win/loss reason distribution"]
slug: "win-loss-analysis"
install: "npx gtm-skills add sales/won/win-loss-analysis"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Win/Loss Analysis Program — Baseline Run

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically analyze won and lost deals to improve sales effectiveness, product positioning, and competitive strategy, from manual post-deal interviews to AI-driven continuous win/loss intelligence that auto-identifies patterns and recommends strategic adjustments.

**Time commitment:** 24 hours over 2 weeks
**Pass threshold:** >=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Expand to 15-20 win/loss interviews over 2 weeks; create a structured interview guide in Attio with questions organized by category (decision process, evaluation criteria, competitive comparison, sales experience, product feedback).

2. Aim for 50%+ interview completion rate (interviews for 50% of closed deals); prioritize interviewing losses (higher learning value) and large wins (understand what's working).

3. Set pass threshold: complete >=10 interviews, identify >=5 high-priority insights, and implement >=2 changes based on insights (sales process, positioning, product roadmap, pricing strategy).

4. Use a consistent interview framework: open with gratitude ("Thanks for your time—this helps us improve"), ask open-ended questions first ("Tell me about your buying process"), then drill into specifics ("How did our pricing compare?").

5. Record and transcribe interviews (with permission) using tools like Fireflies or manual notes; store transcripts in Attio for future analysis and pattern identification.

6. Categorize win/loss reasons in Attio: Win reasons (product fit, ROI, champion, ease of use, integrations, pricing), Loss reasons (price, missing feature, competitor advantage, timing, no champion, poor sales experience).

7. Sync win/loss data from Attio to PostHog; create dashboards showing win rate by reason, loss rate by reason, competitor mentions, and trends over time.

8. After 2 weeks, synthesize findings into a win/loss report: Top 3 win patterns, Top 3 loss patterns, Competitive intelligence, Recommended actions; present to team and leadership.

9. Implement quick wins: If losing on specific objection, update sales playbook; if competitor has messaging advantage, update positioning; if feature gap is costing deals, prioritize in roadmap.

10. If >=10 interviews completed, >=5 insights identified, and >=2 changes implemented, move to Scalable; otherwise improve interview access or stakeholder engagement.

---

## KPIs to track
- Interview completion rate
- Insights identified
- Changes implemented
- Win/loss reason distribution

---

## Pass threshold
**>=10 interviews, >=5 high-priority insights, and >=2 implemented changes over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/win-loss-analysis`_
