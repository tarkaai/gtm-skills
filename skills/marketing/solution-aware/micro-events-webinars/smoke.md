---
name: micro-events-webinars-smoke
description: >
  Micro-Event or Webinar — Smoke Test. Run one short session with manual invites to test registrations, show rate, and at least one meeting before trying other topics or formats.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 15 regs, ≥ 30% show rate, ≥ 1 meeting in 2 weeks"
kpis: ["Registration rate", "Show rate"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - meetup-pipeline
  - threshold-engine
---
# Micro-Event or Webinar — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Run one short session with manual invites to test registrations, show rate, and at least one meeting before trying other topics or formats.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 15 regs, ≥ 30% show rate, ≥ 1 meeting in 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Webinar platform — Zoom free tier or Google Meet:** Free
- **Cal.com (scheduling, optional):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
_No specialized tools required at this level._

---

## Instructions

1. Define the scope of your smoke test: what you will run, for how long (within the 1-week cap), and what success looks like (e.g. ≥ 15 regs, ≥ 30% show rate, ≥ 1 meeting in 2 weeks).

2. Before you start, set your pass threshold and where you will log every outcome (PostHog or CRM).

3. Set up PostHog or your CRM with properties for Registration rate, Show rate so you can compare results to your threshold.

4. Prepare your list, asset, or touchpoints so you can execute within the time cap (e.g. a few hours over 1 week).

5. Execute the smoke test: send emails, publish posts, make calls, or run the planned touchpoints according to your plan.

6. As outcomes occur (replies, clicks, meetings, signups), log each one in PostHog or your CRM with date and source.

7. At the end of the test window, stop and count: total touches, positive outcomes, and any meetings or signups.

8. Compute the key metrics (e.g. reply rate, meeting rate) and compare to your pass threshold.

9. If you met or exceeded the threshold, document what you did and proceed to Baseline; if not, iterate on list, offer, or channel and re-test.

10. Record qualitative notes (who responded, objections, what worked) so you can repeat or refine in Baseline.

---

## KPIs to track
- Registration rate
- Show rate

---

## Pass threshold
**≥ 15 regs, ≥ 30% show rate, ≥ 1 meeting in 2 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/micro-events-webinars`_
