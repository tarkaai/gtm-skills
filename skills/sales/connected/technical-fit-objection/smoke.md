---
name: technical-fit-objection-smoke
description: >
  Technical Fit Objection Handling — Smoke Test. Address concerns about technical compatibility, missing features, or capability gaps with roadmap commitments, workarounds, and technical proof to maintain deal momentum.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Technical objections handled on ≥5 opportunities in 1 week"
kpis: ["Technical objection resolution rate", "Workaround acceptance rate", "Deal progression after resolution", "Commitment delivery rate"]
slug: "technical-fit-objection"
install: "npx gtm-skills add sales/connected/technical-fit-objection"
---
# Technical Fit Objection Handling — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Address concerns about technical compatibility, missing features, or capability gaps with roadmap commitments, workarounds, and technical proof to maintain deal momentum.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** Technical objections handled on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When 5-8 prospects raise technical fit concerns, use diagnostic framework: understand specific gap ('Which capability is missing?'), assess criticality ('Is this must-have or nice-to-have?'), explore timeline ('When do you need this?').

2. Categorize technical objections: missing feature, integration limitation, performance concern, security gap, scalability question, architecture mismatch.

3. Respond based on gap type: Feature on roadmap (provide timeline and commitment), Workaround exists (demonstrate alternative approach), Integration buildable (scope custom work), Performance provable (share benchmarks).

4. Provide technical proof: share architecture diagrams, performance data, customer examples of similar use cases working, technical documentation showing depth.

5. Engage technical resources: loop in solutions architect or engineering for complex objections; demonstrate technical depth and commitment to solving their specific needs.

6. Document commitments made: log any roadmap promises, custom development scope, workaround agreements in Attio with clear timelines and ownership.

7. Track PostHog events: technical_objection_raised, gap_type_identified, workaround_demonstrated, roadmap_commitment_made, objection_resolved.

8. Set pass threshold: Handle technical objections on ≥5 opportunities in 1 week with ≥60% reaching satisfactory resolution and advancing deal.

9. Measure effectiveness: track technical objection resolution rate, deals lost to technical gaps, roadmap commitment delivery rate.

10. Document which technical objection responses work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Technical objection resolution rate
- Workaround acceptance rate
- Deal progression after resolution
- Commitment delivery rate

---

## Pass threshold
**Technical objections handled on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/technical-fit-objection`_
