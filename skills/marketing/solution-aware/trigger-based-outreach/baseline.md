---
name: trigger-based-outreach-baseline
description: >
    Trigger-based Outreach — Baseline Run. Automate outreach based on intent signals like funding,
  hiring, tech stack changes, or job changes to reach solution-aware prospects at optimal timing.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥4% meeting rate from 150 trigger-based outreach over 2 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "trigger-based-outreach"
install: "npx gtm-skills add marketing/solution-aware/trigger-based-outreach"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Trigger-based Outreach — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Overview
Trigger-based Outreach — Baseline Run. Automate outreach based on intent signals like funding, hiring, tech stack changes, or job changes to reach solution-aware prospects at optimal timing.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥4% meeting rate from 150 trigger-based outreach over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `trigger-based-outreach_email_sent`, `trigger-based-outreach_email_replied`, `trigger-based-outreach_meeting_booked`, `trigger-based-outreach_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: ≥4% meeting rate from 150 trigger-based outreach over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥4% meeting rate from 150 trigger-based outreach over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/trigger-based-outreach`_
