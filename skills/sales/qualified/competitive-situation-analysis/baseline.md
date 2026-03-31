---
name: competitive-situation-analysis-baseline
description: >
  Competitive Situation Assessment — Baseline Run. Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Competitive situation assessed on ≥80% of opportunities over 2 weeks"
kpis: ["Competitive discovery rate", "Win rate by competitor", "Competitive positioning effectiveness", "Intelligence accuracy"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Competitive Situation Assessment — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.

**Time commitment:** 15 hours over 2 weeks
**Pass threshold:** Competitive situation assessed on ≥80% of opportunities over 2 weeks

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

---

## Instructions

1. Expand competitive discovery to 40-60 opportunities over 2 weeks; develop standardized competitive intelligence framework.

2. Build competitor battlecards: for top 5-7 competitors, document their strengths, weaknesses, typical objections, winning strategies, and proof points.

3. Create competitive question bank: questions to uncover competitor engagement, prospect sentiment, specific features they're evaluating, pricing discussions, decision timeline.

4. Set up PostHog event tracking: competitor_evaluated, competitive_positioning_delivered, battlecard_accessed, competitive_win, competitive_loss.

5. Implement competitive positioning playbook: when specific competitor is identified, deliver tailored differentiation narrative highlighting your unique advantages.

6. Track competitive win/loss metrics: measure close rate against each major competitor, analyze why you win or lose, identify patterns.

7. Build competitive response library: objection handlers, comparison docs, customer case studies showing wins from competitor switches.

8. Set pass threshold: Competitive situation assessed on ≥80% of opportunities over 2 weeks with competitive intelligence accurately predicting deal strategies.

9. Analyze competitive patterns: which competitors appear most often, in which segments, at what deal stages, with what success rates.

10. If threshold met, document competitive intelligence playbook and proceed to Scalable; if not, refine competitor discovery and positioning.

---

## KPIs to track
- Competitive discovery rate
- Win rate by competitor
- Competitive positioning effectiveness
- Intelligence accuracy

---

## Pass threshold
**Competitive situation assessed on ≥80% of opportunities over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/competitive-situation-analysis`_
