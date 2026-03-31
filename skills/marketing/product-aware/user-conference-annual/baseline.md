---
name: user-conference-annual-baseline
description: >
    Annual User Conference — Baseline Run. Host annual customer conference for community building,
  product launches, and upsell opportunities with product-aware customers and prospects.
stage: "Marketing > Product Aware"
motion: "Micro Events"
channels: "Events"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥150 attendees and ≥20 expansion opportunities from inaugural conference"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "user-conference-annual"
install: "npx gtm-skills add marketing/product-aware/user-conference-annual"
drills:
  - meetup-pipeline
  - posthog-gtm-events
---
# Annual User Conference — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Annual User Conference — Baseline Run. Host annual customer conference for community building, product launches, and upsell opportunities with product-aware customers and prospects.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥150 attendees and ≥20 expansion opportunities from inaugural conference

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build event operations
Run the `meetup-pipeline` drill to create a repeatable event process: registration page, automated email reminders (1 week, 1 day, 1 hour before), attendee tracking in Attio, and post-event follow-up sequence.

### 2. Configure event analytics
Run the `posthog-gtm-events` drill to track: `user-conference-annual_registered`, `user-conference-annual_attended`, `user-conference-annual_engaged`, `user-conference-annual_follow_up_replied`, `user-conference-annual_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: ≥150 attendees and ≥20 expansion opportunities from inaugural conference. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥150 attendees and ≥20 expansion opportunities from inaugural conference**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/user-conference-annual`_
