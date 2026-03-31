---
name: intent-signal-tracking-baseline
description: >
    Intent Signal Tracking — Baseline Run. Monitor and act on buyer intent signals like website
  behavior, content consumption, and G2 research to reach prospects at peak buying moment, from
  manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers
  personalized outreach automatically.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=20 high-intent accounts and >=35% reply rate over 2 weeks"
kpis: ["High-intent accounts per week", "Reply rate by intent tier", "Signal-to-outreach time", "Meeting rate by intent"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Intent Signal Tracking — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Overview
Intent Signal Tracking — Baseline Run. Monitor and act on buyer intent signals like website behavior, content consumption, and G2 research to reach prospects at peak buying moment, from manual tracking in spreadsheets to AI-driven real-time intent orchestration that triggers personalized outreach automatically.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** >=20 high-intent accounts and >=35% reply rate over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up cold outreach tooling
Run the `cold-email-sequence` drill to configure Instantly with warmed-up sending accounts. Import your prospect list from Attio (built during Smoke). Create 3-5 email variants using the ICP pain points validated in Smoke. Set up A/B subject line testing.

### 2. Launch LinkedIn outreach in parallel
Run the `linkedin-outreach` drill to set up a connection request + follow-up message sequence targeting the same prospect list. Coordinate timing so LinkedIn and email touches don't overlap for the same prospect.

### 3. Configure tracking
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `intent-signal-tracking_email_sent`, `intent-signal-tracking_email_replied`, `intent-signal-tracking_meeting_booked`, `intent-signal-tracking_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: >=20 high-intent accounts and >=35% reply rate over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- High-intent accounts per week
- Reply rate by intent tier
- Signal-to-outreach time
- Meeting rate by intent

---

## Pass threshold
**>=20 high-intent accounts and >=35% reply rate over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/intent-signal-tracking`_
