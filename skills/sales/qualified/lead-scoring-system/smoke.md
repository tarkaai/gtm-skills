---
name: lead-scoring-system-smoke
description: >
  Lead Scoring System — Smoke Test. Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Hot leads have >=2x meeting rate vs Cold leads in 1 week"
kpis: ["Meeting rate by tier", "Score distribution", "Time to meeting by tier"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - icp-definition
  - threshold-engine
---
# Lead Scoring System — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Prioritize leads by fit (firmographics) and intent (behaviors) to focus sales effort on highest-probability opportunities, from manual spreadsheet scoring to AI-driven dynamic scoring that adapts to market changes and win patterns.

**Time commitment:** 5 hours over 1 week
**Pass threshold:** Hot leads have >=2x meeting rate vs Cold leads in 1 week

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

1. Define 3-5 fit criteria (e.g., company size, industry, role) and 3-5 intent signals (e.g., demo request, pricing page visit, email reply); assign point values (fit: 0-50, intent: 0-50).

2. Pull 20 recent leads from Attio; manually score each lead on fit and intent using your criteria; total score ranges from 0-100.

3. Create score tiers in a spreadsheet: Hot (80-100), Warm (50-79), Cold (0-49); categorize all 20 leads.

4. Set pass threshold: Hot leads must have >=2x meeting rate vs Cold leads within 1 week to validate scoring predicts engagement.

5. Reach out to all 20 leads with the same message/offer; track which leads respond and book meetings in Attio and PostHog.

6. Log lead_scored events in PostHog with properties for fit score, intent score, total score, and tier.

7. After 1 week, compute meeting rate by tier (Hot, Warm, Cold); if Hot leads have >=2x meeting rate vs Cold, scoring is predictive.

8. Analyze which fit criteria and intent signals most strongly correlate with meetings; consider adjusting point values.

9. Test whether calling Hot leads first yields faster pipeline generation than calling leads in random order.

10. If Hot leads convert >=2x better, document scoring criteria and point system, then proceed to Baseline; otherwise refine criteria or signals and retest.

---

## KPIs to track
- Meeting rate by tier
- Score distribution
- Time to meeting by tier

---

## Pass threshold
**Hot leads have >=2x meeting rate vs Cold leads in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/lead-scoring-system`_
