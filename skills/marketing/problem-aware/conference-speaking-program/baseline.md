---
name: conference-speaking-program-baseline
description: >
    Conference Speaking — Baseline Run. Secure speaking slots at industry conferences for brand
  building, thought leadership, and lead generation with solution-aware and problem-aware attendees.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Events, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥3 speaking slots and ≥30 qualified leads in 10 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - meetup-pipeline
  - posthog-gtm-events
---
# Conference Speaking — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Events, Social

## Overview
Conference Speaking — Baseline Run. Secure speaking slots at industry conferences for brand building, thought leadership, and lead generation with solution-aware and problem-aware attendees.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥3 speaking slots and ≥30 qualified leads in 10 weeks

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
Run the `posthog-gtm-events` drill to track: `conference-speaking-program_registered`, `conference-speaking-program_attended`, `conference-speaking-program_engaged`, `conference-speaking-program_follow_up_replied`, `conference-speaking-program_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: ≥3 speaking slots and ≥30 qualified leads in 10 weeks. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert).

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥3 speaking slots and ≥30 qualified leads in 10 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/conference-speaking-program`_
