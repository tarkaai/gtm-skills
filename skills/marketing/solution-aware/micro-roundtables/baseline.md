---
name: micro-roundtables-baseline
description: >
    Micro-Roundtable — Baseline Run. Host an invite-only Zoom roundtable with 8–10 execs to test if
  deep conversations yield multiple meetings and justify the format.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 12 attendees and ≥ 4 meetings over 2 weeks"
kpis: ["RSVPs", "Show rate"]
slug: "micro-roundtables"
install: "npx gtm-skills add marketing/solution-aware/micro-roundtables"
drills:
  - meetup-pipeline
  - posthog-gtm-events
---
# Micro-Roundtable — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Micro-Roundtable — Baseline Run. Host an invite-only Zoom roundtable with 8–10 execs to test if deep conversations yield multiple meetings and justify the format.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 12 attendees and ≥ 4 meetings over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `micro-roundtables_registered`, `micro-roundtables_attended`, `micro-roundtables_engaged`, `micro-roundtables_follow_up_replied`, `micro-roundtables_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: ≥ 12 attendees and ≥ 4 meetings over 2 weeks. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert).

---

## KPIs to track
- RSVPs
- Show rate

---

## Pass threshold
**≥ 12 attendees and ≥ 4 meetings over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/micro-roundtables`_
