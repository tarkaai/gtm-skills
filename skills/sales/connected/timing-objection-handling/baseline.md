---
name: timing-objection-handling-baseline
description: >
    Timing Objection Handling — Baseline Run. Address 'not the right time' objections by uncovering
  true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate
  deal timeline.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Timing objections handled on ≥80% of instances over 2 weeks"
kpis: ["Objection resolution rate", "Timeline acceleration success", "Cost of inaction conversion", "Bridging solution acceptance", "Eventual close rate"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - posthog-gtm-events
---
# Timing Objection Handling — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Timing Objection Handling — Baseline Run. Address 'not the right time' objections by uncovering true urgency drivers, quantifying cost of inaction, and creating legitimate urgency to accelerate deal timeline.

**Time commitment:** 14 hours over 2 weeks
**Pass threshold:** Timing objections handled on ≥80% of instances over 2 weeks

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
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `timing-objection-handling_email_sent`, `timing-objection-handling_email_replied`, `timing-objection-handling_meeting_booked`, `timing-objection-handling_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: Timing objections handled on ≥80% of instances over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings).

---

## KPIs to track
- Objection resolution rate
- Timeline acceleration success
- Cost of inaction conversion
- Bridging solution acceptance
- Eventual close rate

---

## Pass threshold
**Timing objections handled on ≥80% of instances over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/timing-objection-handling`_
