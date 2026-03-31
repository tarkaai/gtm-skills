---
name: champion-identification-baseline
description: >
  Champion Identification & Development — Baseline Run. Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=60% of deals with active champions and >=35% higher win rate over 2 weeks"
kpis: ["Champion rate per deal", "Champion engagement score", "Win rate (champion vs non-champion)", "Champion recruitment rate"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Champion Identification & Development — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** >=60% of deals with active champions and >=35% higher win rate over 2 weeks

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

1. Expand champion development to 10-15 deals over 2 weeks; create a champion scorecard in Attio with 5 traits scored 1-5 (pain, value recognition, internal influence, willingness to advocate, accessibility).

2. Build a champion enablement kit: executive one-pager, ROI calculator, objection handling guide, internal email templates, case studies by vertical; store in shared folder with tracking links.

3. Set pass threshold: >=60% of deals have an Active Champion (score >=20/25), and champion deals have >=35% higher win rate or >=30% faster velocity over 2 weeks.

4. During discovery, explicitly recruit champions: "You seem to really get this problem—would you be open to partnering with us to evaluate this internally? We can provide materials to help."

5. Send champion enablement kit to identified champions within 24 hours of identification; ask them to share specific assets with internal stakeholders and report back.

6. Track champion engagement in PostHog: log when champions download materials, forward emails, introduce stakeholders, or ask for support; high engagement = strong champion.

7. Schedule champion coaching calls: 15-20 minute sessions to brief champions on how to sell internally, anticipate objections, and navigate approval process.

8. In Attio, create a champion dashboard showing deals by champion status, average champion score, and correlation between champion strength and deal outcome.

9. After 2 weeks, analyze: do deals with Active Champions (>=20/25 score) win at higher rate or close faster? Measure champion vs non-champion cohort performance.

10. If >=60% of deals have Active Champions and champion deals win >=35% more often, champion development is working; move to Scalable. Otherwise, refine recruitment or enablement tactics.

---

## KPIs to track
- Champion rate per deal
- Champion engagement score
- Win rate (champion vs non-champion)
- Champion recruitment rate

---

## Pass threshold
**>=60% of deals with active champions and >=35% higher win rate over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/champion-identification`_
