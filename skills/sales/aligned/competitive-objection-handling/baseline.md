---
name: competitive-objection-handling-baseline
description: >
  Competitive Objection Handling — Baseline Run. Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=40% win rate in competitive deals and >=70% engagement retention over 2 weeks"
kpis: ["Competitive win rate", "Engagement retention", "Differentiator effectiveness by competitor", "Asset impact on outcomes"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Competitive Objection Handling — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.

**Time commitment:** 22 hours over 2 weeks
**Pass threshold:** >=40% win rate in competitive deals and >=70% engagement retention over 2 weeks

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
- **Loom** (Video)

---

## Instructions

1. Expand to 10-15 competitive situations over 2 weeks; build comprehensive battlecards in Attio for top 5 competitors with sections: Overview, Strengths, Weaknesses, Pricing, Key Differentiators, When We Win, When They Win, Proof Points.

2. Develop competitor-specific positioning guides: for each competitor, create 3-5 talk tracks based on common decision criteria (ROI, ease of use, integrations, support, security).

3. Set pass threshold: win >=40% of competitive deals (prospect chooses you over competitor) and maintain engagement in >=70% of competitive situations over 2 weeks.

4. When competitive objection arises, send competitive comparison asset within 24 hours: side-by-side feature comparison, TCO analysis, or case study from customer who switched from that competitor.

5. Use discovery insights to position against competitors: "You said integration with [system] is critical—competitor X has basic API, we have native integration that saves 20 hours of setup time."

6. Schedule competitive differentiation calls: dedicate 15-20 minutes to walk through why your solution fits their needs better; use demos, case studies, and proof points specific to their criteria.

7. Sync competitive data from Attio to PostHog; create a funnel showing competitive_objection → differentiation_call → competitive_asset_sent → prospect_engaged → deal_won.

8. Track which competitors you win against most often and which are hardest to beat; for tough competitors, develop specialized positioning or consider conceding if fit is genuinely poor.

9. After 2 weeks, analyze competitive win rate by competitor, decision criteria, and deal size; identify patterns (e.g., "We win on ease-of-use criteria, lose on enterprise feature depth").

10. If win rate >=40% in competitive deals and >=70% stay engaged, move to Scalable; otherwise strengthen battlecards, gather more competitive intel, or improve differentiation messaging.

---

## KPIs to track
- Competitive win rate
- Engagement retention
- Differentiator effectiveness by competitor
- Asset impact on outcomes

---

## Pass threshold
**>=40% win rate in competitive deals and >=70% engagement retention over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/competitive-objection-handling`_
