---
name: usage-limit-sales-upsell-smoke
description: >
  Usage-Based Upsell — Smoke Test. Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=1 upsell closed from >=3 customers with expansion signals within 1 week"
kpis: ["Expansion signal detection rate", "Upsell conversion rate", "Expansion ARR", "Time from signal to close"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add sales/won/usage-limit-sales-upsell"
drills:
  - icp-definition
  - threshold-engine
---
# Usage-Based Upsell — Smoke Test

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Direct

## Overview
Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=1 upsell closed from >=3 customers with expansion signals within 1 week

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

1. Define 3-5 usage expansion signals in a spreadsheet: approaching plan limits (80%+ of seats, API calls, storage), adding team members, using premium features heavily, achieving strong outcomes, expanding to new use cases.

2. Monitor 10 active customers in Attio; track their usage against plan limits weekly using product data or manual checks; identify customers showing expansion signals.

3. Set pass threshold: identify >=3 customers with expansion signals and successfully upsell >=1 customer (tier upgrade, seat expansion, or add-on purchase) within 1 week.

4. When customer hits usage threshold (e.g., 80% of seats used), send personalized email: "Noticed your team is growing—you're at 8/10 seats. Want to add more seats so new team members can join?"

5. For customers using premium features heavily, reach out: "You're getting great value from [feature]—have you considered [higher tier] to unlock [additional benefit]?"

6. Schedule upsell calls with high-usage customers; come prepared with their usage data: "You've run 45K API calls this month—you're close to your 50K limit. Let's discuss upgrading to 100K so you have headroom."

7. Log expansion signals and upsell attempts in Attio with fields for expansion_signal_type, upsell_offer_made, upsell_value, and outcome; track which signals convert best.

8. In PostHog, create events for usage_threshold_hit, upsell_offer_sent, upsell_call_scheduled, upsell_closed with properties for signal type, expansion value, and time to close.

9. After 1 week, analyze which expansion signals yielded successful upsells; if seat expansion signals convert well but API limit signals don't, prioritize seat-based upsells.

10. If >=1 upsell closed from >=3 customers with expansion signals, usage-based upsell is working; document signals and outreach templates, then proceed to Baseline; otherwise refine signal definitions or offer positioning.

---

## KPIs to track
- Expansion signal detection rate
- Upsell conversion rate
- Expansion ARR
- Time from signal to close

---

## Pass threshold
**>=1 upsell closed from >=3 customers with expansion signals within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/usage-limit-sales-upsell`_
