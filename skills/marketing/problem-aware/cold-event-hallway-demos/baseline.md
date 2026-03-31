---
name: cold-event-hallway-demos-baseline
description: >
    Event Hallway Demos — Baseline Run. Run a single day of lobby or hallway demos at a venue to get
  instant feedback and a few meetings and validate whether in-person fits your ICP.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 10 demos and ≥ 2 meetings over 2 weeks"
kpis: ["Conversations started", "Follow-up requests"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - meetup-pipeline
  - posthog-gtm-events
---
# Event Hallway Demos — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Other

## Overview
Event Hallway Demos — Baseline Run. Run a single day of lobby or hallway demos at a venue to get instant feedback and a few meetings and validate whether in-person fits your ICP.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 10 demos and ≥ 2 meetings over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `cold-event-hallway-demos_registered`, `cold-event-hallway-demos_attended`, `cold-event-hallway-demos_engaged`, `cold-event-hallway-demos_follow_up_replied`, `cold-event-hallway-demos_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: ≥ 10 demos and ≥ 2 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert).

---

## KPIs to track
- Conversations started
- Follow-up requests

---

## Pass threshold
**≥ 10 demos and ≥ 2 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos`_
