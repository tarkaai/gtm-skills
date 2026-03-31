---
name: trial-to-paid-conversion-smoke
description: >
  Trial-to-Paid Conversion — Smoke Test. Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Email, Product, Direct"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=40% trial-to-paid conversion rate within trial period"
kpis: ["Trial conversion rate", "Activation milestone completion rate", "Time to first value", "Engagement score"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add sales/won/trial-to-paid-conversion"
drills:
  - icp-definition
  - threshold-engine
---
# Trial-to-Paid Conversion — Smoke Test

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Email, Product, Direct

## Overview
Convert free trial users to paying customers by driving activation, demonstrating value, and creating urgency, from manual trial follow-ups to AI-driven trial orchestration that personalizes interventions and maximizes conversion rates.

**Time commitment:** 8 hours over 1 week
**Pass threshold:** >=40% trial-to-paid conversion rate within trial period

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)

---

## Instructions

1. Define trial success criteria in a spreadsheet: 3-5 activation milestones that predict paid conversion (e.g., completed setup, invited team, used core feature 3x, integrated with tool, achieved first outcome).

2. Track 10 active trial users in Attio; for each, monitor which activation milestones they hit and when; identify patterns in users who convert vs those who don't.

3. Set pass threshold: >=40% of trial users convert to paid within trial period (typically 14 days), and users who hit >=3 activation milestones convert at >=2x rate vs users who hit <3.

4. Send manual check-in emails at days 3, 7, and 12 of trial: offer help, share tips for hitting activation milestones, schedule calls with users stuck on setup.

5. For users who hit activation milestones, send success confirmation: "Congrats on [milestone]! You're getting great value—here's what to try next." For users who don't, send targeted help: "Noticed you haven't [action]—here's a 2-minute guide."

6. Log trial activity in PostHog: track trial_started, activation_milestone_hit, trial_engaged, trial_converted, trial_expired events with properties for milestone completion and engagement level.

7. Call high-intent trial users (hit >=2 milestones) at day 10 to discuss upgrade: "You've been getting great results—let's talk about moving to paid so you can [unlock benefit]."

8. Create urgency as trial end approaches: "Your trial expires in 2 days—upgrade now to keep your data and momentum" with clear upgrade CTA.

9. After 1-2 weeks, analyze conversion rate overall and by activation milestone completion; if >=40% convert and milestone completion predicts conversion, you have a working trial-to-paid motion.

10. If threshold met, document activation milestones and touchpoint cadence, then proceed to Baseline; otherwise refine activation criteria or improve trial experience.

---

## KPIs to track
- Trial conversion rate
- Activation milestone completion rate
- Time to first value
- Engagement score

---

## Pass threshold
**>=40% trial-to-paid conversion rate within trial period**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/trial-to-paid-conversion`_
