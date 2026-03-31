---
name: workshop-series-educational-baseline
description: >
    Workshop Series — Baseline Run. Run educational workshops teaching relevant skills or frameworks
  to generate leads, demonstrate expertise, and engage solution-aware audiences hands-on.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥50 attendees and ≥18 qualified leads across 3 workshops in 6 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - meetup-pipeline
  - posthog-gtm-events
---
# Workshop Series — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events, Content

## Overview
Workshop Series — Baseline Run. Run educational workshops teaching relevant skills or frameworks to generate leads, demonstrate expertise, and engage solution-aware audiences hands-on.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥50 attendees and ≥18 qualified leads across 3 workshops in 6 weeks

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
Run the `posthog-gtm-events` drill to track: `workshop-series-educational_registered`, `workshop-series-educational_attended`, `workshop-series-educational_engaged`, `workshop-series-educational_follow_up_replied`, `workshop-series-educational_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: ≥50 attendees and ≥18 qualified leads across 3 workshops in 6 weeks. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥50 attendees and ≥18 qualified leads across 3 workshops in 6 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/workshop-series-educational`_
