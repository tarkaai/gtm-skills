---
name: competitive-situation-analysis-smoke
description: >
  Competitive Situation Assessment — Smoke Test. Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Competitive situation identified in ≥8 opportunities in 1 week"
kpis: ["Competitive discovery completion rate", "Competitor identification rate", "Decision criteria clarity", "Competitive intelligence quality"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - icp-definition
  - threshold-engine
---
# Competitive Situation Assessment — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Discover which competitors prospects are evaluating to position differentiation effectively and develop winning strategies against specific alternatives.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Competitive situation identified in ≥8 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. On first 10 discovery calls, ask directly: 'What other solutions are you currently evaluating?' and 'How are you comparing alternatives?'.

2. Identify competitive set: direct competitors, indirect alternatives, status quo (doing nothing), build vs buy options.

3. Understand evaluation criteria: ask 'What's most important to you in selecting a solution?' to learn how they're making the decision.

4. Probe competitor engagement level: 'How far along are you with [competitor]?' to understand deal stage with alternatives.

5. Uncover competitive gaps: 'What do you wish [competitor] could do that it doesn't?' to find opportunities for differentiation.

6. Log competitive situation in Attio: competitors being evaluated, evaluation stage, decision criteria, gaps identified.

7. Track PostHog events: competitive_situation_identified, competitor_named, status_quo_bias_detected, build_option_considered.

8. Set pass threshold: Competitive situation identified in ≥8 opportunities in 1 week with ≥60% having active competitor evaluation.

9. Analyze win rates: compare close rates when competing against specific competitors vs status quo.

10. Document which competitive discovery questions reveal most useful intelligence; proceed to Baseline if threshold met.

---

## KPIs to track
- Competitive discovery completion rate
- Competitor identification rate
- Decision criteria clarity
- Competitive intelligence quality

---

## Pass threshold
**Competitive situation identified in ≥8 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/competitive-situation-analysis`_
