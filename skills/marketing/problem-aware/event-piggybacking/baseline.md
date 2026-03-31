---
name: event-piggybacking-baseline
description: >
  Event Piggyback Meetup — Baseline Run. Host a one-night meetup near a major conference to ride the halo effect and see if RSVPs and meetings justify event-led demand gen.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 20 RSVPs and ≥ 4 meetings over 2 weeks"
kpis: ["10 RSVPs", "2 meetings"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - meetup-pipeline
  - webinar-pipeline
  - crm-pipeline-setup
  - threshold-engine
---
# Event Piggyback Meetup — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Other

## Overview
Host a one-night meetup near a major conference to ride the halo effect and see if RSVPs and meetings justify event-led demand gen.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 20 RSVPs and ≥ 4 meetings over 2 weeks

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

1. Define your 2-week experiment scope: list size, channels, and success criteria aligned with your pass threshold (e.g. ≥ 20 RSVPs and ≥ 4 meetings over 2 weeks).

2. Choose where you will log every outcome: PostHog and optionally your CRM; create or use events for each key action.

3. Build your list and run enrichment (e.g. Clay, Apollo) so you have enough qualified contacts for the 2-week window.

4. Execute the campaign: send sequences, make calls, or run touchpoints according to your plan; cap time and budget as defined for Baseline.

5. Log every outcome in PostHog: track 10 RSVPs, 2 meetings so you can compute rates and compare to threshold.

6. At the end of week 1, review mid-point metrics; adjust cadence or targeting for week 2 if needed.

7. At the end of 2 weeks, compute final metrics (e.g. meeting rate, reply rate, signups) and compare to your pass threshold.

8. Document what worked (list source, message, channel mix) so you can repeat or scale.

9. If metrics hold, proceed to Scalable; if not, iterate on list, offer, or channel and re-run Baseline.

10. Record qualitative notes (who responded, objections) in PostHog or CRM for future optimization.

---

## KPIs to track
- 10 RSVPs
- 2 meetings

---

## Pass threshold
**≥ 20 RSVPs and ≥ 4 meetings over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/event-piggybacking`_
