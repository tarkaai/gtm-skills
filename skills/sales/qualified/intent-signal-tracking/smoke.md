---
name: intent-signal-tracking-smoke
description: >
  Intent Signal Tracking — Smoke Test. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week"
kpis: ["Intent signals per day", "Reply rate (intent vs non-intent)", "Time from signal to outreach"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - icp-definition
  - threshold-engine
---
# Intent Signal Tracking — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** >=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Clay** (Enrichment)

---

## Instructions

1. Define 5-7 high-intent signals in a spreadsheet: demo request, pricing page >=2 visits, case study download, product comparison page, LinkedIn company page view, job posting for relevant role, funding announcement.

2. Set up PostHog to track key website intent events (pricing_page_viewed, demo_requested, case_study_downloaded) with properties for visitor company and timestamp.

3. Manually check PostHog daily for high-intent events; export 10-15 accounts that triggered >=2 signals in the past 7 days to a spreadsheet.

4. Set pass threshold: >=5 accounts show >=2 intent signals in 1 week, and outreach to these accounts yields >=30% reply rate vs <15% for non-intent accounts.

5. For each high-intent account, research company (LinkedIn, website, news) and identify 2-3 stakeholders; find emails using Apollo or Clay.

6. Send personalized emails referencing specific intent signals (e.g., "Saw you checked out our ROI calculator—here's how customers save 40% on X") within 24 hours of signal.

7. Log all outreach in Attio with custom field for intent_signal_type; track responses and meetings booked.

8. In PostHog, create events for intent_account_identified and intent_outreach_sent with properties for signal type and response outcome.

9. After 1 week, compare reply rate and meeting rate for intent-based outreach vs non-intent cold outreach.

10. If intent-based outreach has >=2x reply rate, document signal definitions and outreach templates, then proceed to Baseline; otherwise refine signals or messaging.

---

## KPIs to track
- Intent signals per day
- Reply rate (intent vs non-intent)
- Time from signal to outreach

---

## Pass threshold
**>=5 high-intent accounts and >=30% reply rate from intent-based outreach in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
