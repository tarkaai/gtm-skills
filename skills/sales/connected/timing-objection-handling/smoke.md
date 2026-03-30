---
name: timing-objection-handling-smoke
description: >
  Timing Objection Handling — Smoke Test. Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Timing objections handled on ≥5 opportunities in 1 week"
kpis: ["Timing objection resolution rate", "Timeline acceleration rate", "Cost of inaction presentation impact", "Eventually close rate"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
---
# Timing Objection Handling — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Timing objections handled on ≥5 opportunities in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)

---

## Instructions

1. When first 5-8 prospects say 'not the right time', use diagnostic questions: 'What needs to happen for this to become a priority?' and 'What's driving the current timeline?'.

2. Uncover competing priorities: 'What's taking precedence right now?' to understand what's blocking decision; assess whether objection is real constraint or avoidance.

3. Quantify cost of delay: calculate specific impact of waiting (revenue lost, costs incurred, competitive disadvantage, technical debt accumulated).

4. Present cost of inaction analysis: 'If we wait 6 months, here's what that delay will cost you: [specific calculations]'.

5. Explore bridging options: offer phased approach, pilot program, or interim solution that addresses urgent needs while deferring full implementation.

6. Create legitimate urgency: identify real deadlines (fiscal year-end, seasonal peaks, compliance dates, contract expirations) that align with their priorities.

7. Track PostHog events: timing_objection_raised, urgency_diagnostic_completed, cost_of_inaction_presented, bridging_option_offered, objection_overcome.

8. Set pass threshold: Handle timing objections on ≥5 opportunities in 1 week with ≥60% either accelerating timeline or accepting bridging solution.

9. Measure effectiveness: track how many timing objections convert to active opportunities, time from objection to reengagement, eventual close rate.

10. Document which timing objection approaches work best; proceed to Baseline if threshold met.

---

## KPIs to track
- Timing objection resolution rate
- Timeline acceleration rate
- Cost of inaction presentation impact
- Eventually close rate

---

## Pass threshold
**Timing objections handled on ≥5 opportunities in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/timing-objection-handling`_
