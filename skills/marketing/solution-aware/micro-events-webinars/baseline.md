---
name: micro-events-webinars-baseline
description: >
  Micro-Event or Webinar — Baseline Run. Run one short session with manual invites to test registrations, show rate, and at least one meeting before trying other topics or formats.
stage: "Marketing > Solution Aware"
motion: "Micro Events"
channels: "Events"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 30 regs, ≥ 30% show rate, ≥ 2 meetings over 2 weeks"
kpis: ["Registration rate", "Show rate"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
---
# Micro-Event or Webinar — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Micro Events | **Channels:** Events

## Overview
Run one short session with manual invites to test registrations, show rate, and at least one meeting before trying other topics or formats.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 30 regs, ≥ 30% show rate, ≥ 2 meetings over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Riverside (webinar + recording):** ~$25/mo
- **Event promotion (LinkedIn posts, email invite):** Free

_Total play-specific: ~$25/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)

---

## Instructions

1. Define your 2-week experiment scope: list size, channels, and success criteria aligned with your pass threshold (e.g. ≥ 30 regs, ≥ 30% show rate, ≥ 2 meetings over 2 weeks).

2. Choose where you will log every outcome: PostHog and optionally your CRM; create or use events for each key action.

3. Build your list and run enrichment (e.g. Clay, Apollo) so you have enough qualified contacts for the 2-week window.

4. Execute the campaign: send sequences, make calls, or run touchpoints according to your plan; cap time and budget as defined for Baseline.

5. Log every outcome in PostHog: track Registration rate, Show rate so you can compute rates and compare to threshold.

6. At the end of week 1, review mid-point metrics; adjust cadence or targeting for week 2 if needed.

7. At the end of 2 weeks, compute final metrics (e.g. meeting rate, reply rate, signups) and compare to your pass threshold.

8. Document what worked (list source, message, channel mix) so you can repeat or scale.

9. If metrics hold, proceed to Scalable; if not, iterate on list, offer, or channel and re-run Baseline.

10. Record qualitative notes (who responded, objections) in PostHog or CRM for future optimization.

---

## KPIs to track
- Registration rate
- Show rate

---

## Pass threshold
**≥ 30 regs, ≥ 30% show rate, ≥ 2 meetings over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/micro-events-webinars`_
