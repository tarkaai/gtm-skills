---
name: competitive-objection-handling-smoke
description: >
  Competitive Objection Handling — Smoke Test. Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Maintain engagement in >=3 out of 5 competitive deals within 1 week"
kpis: ["Competitive win rate", "Differentiator effectiveness", "Prospect engagement post-positioning"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
---
# Competitive Objection Handling — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Address "we're evaluating competitor X" objections by differentiating your solution, highlighting unique value, and leveraging competitive intelligence, from manual battlecards to AI-driven competitive positioning that adapts to each prospect's priorities and decision criteria.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** Maintain engagement in >=3 out of 5 competitive deals within 1 week

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

1. Create basic battlecards in a spreadsheet for your top 3 competitors: list their strengths, weaknesses, pricing, and your key differentiators vs each; keep to 1 page per competitor.

2. When prospect mentions competitor evaluation ("We're also looking at X"), ask diagnostic questions: "What do you like about X?" "What concerns do you have?" "What criteria matter most in your decision?" "What would make you choose one over the other?"

3. Set pass threshold: successfully navigate >=3 out of 5 competitive situations (prospect stays engaged and doesn't eliminate you) within 1 week.

4. Use competitive framework: acknowledge competitor strengths ("X is strong at Y"), position your differentiators ("Where we excel is Z, which matters because of your pain around [discovery insight]"), provide proof (customer story, feature demo).

5. Tie differentiation back to prospect's specific pain: "You mentioned spending 10 hours/week on [task]—competitor X requires manual work there, we automate it fully, saving you those 10 hours."

6. Avoid negative selling or trash-talking competitors; focus on fit: "X is built for [use case A], we're built for [your use case B]—which aligns better with your needs?"

7. Log competitive situations in Attio with fields for competitor_name, prospect_criteria, your_differentiators_emphasized, and outcome; track which differentiators resonate.

8. In PostHog, create events for competitive_objection_received and competitive_positioned with properties for competitor, criteria, and outcome.

9. After 1 week, analyze which differentiators win most often; if ROI is the key criteria, lead with ROI proof; if ease-of-use matters, demo simplicity first.

10. If >=3 out of 5 competitive deals stay engaged after positioning, document winning battlecards and differentiation points, then proceed to Baseline; otherwise refine competitive intelligence or positioning.

---

## KPIs to track
- Competitive win rate
- Differentiator effectiveness
- Prospect engagement post-positioning

---

## Pass threshold
**Maintain engagement in >=3 out of 5 competitive deals within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/competitive-objection-handling`_
