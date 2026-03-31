---
name: event-piggybacking-scalable
description: >
    Event Piggyback Meetup — Scalable Automation. Host a one-night meetup near a major conference to
  ride the halo effect and see if RSVPs and meetings justify event-led demand gen.
stage: "Marketing > Problem Aware"
motion: "Micro Events"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 80 RSVPs and ≥ 16 meetings over 2 months"
kpis: ["10 RSVPs", "2 meetings"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---
# Event Piggyback Meetup — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Micro Events | **Channels:** Other

## Overview
Event Piggyback Meetup — Scalable Automation. Host a one-night meetup near a major conference to ride the halo effect and see if RSVPs and meetings justify event-led demand gen.

**Time commitment:** 60 hours over 2 months
**Pass threshold:** ≥ 80 RSVPs and ≥ 16 meetings over 2 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate event operations
Run the `follow-up-automation` drill to build n8n workflows: auto-send post-event follow-ups based on engagement level (active participants get a different email than passive attendees), auto-create Attio deals for qualified attendees, and auto-schedule next event invitations.

### 2. Test event variations
Run the `ab-test-orchestrator` drill to test: event formats (webinar vs workshop vs AMA), event lengths, topics, speakers, and promotion channels. Use registration and attendance data to identify winning combinations.

### 3. Scale to regular cadence
Move to bi-weekly or monthly events. Automate as much of the operations as possible. Focus your manual effort on content quality and live delivery.

### 4. Evaluate against threshold
Measure against: ≥ 80 RSVPs and ≥ 16 meetings over 2 months. If PASS, proceed to Durable. If FAIL, reduce frequency and focus on the event format that converts best.

---

## KPIs to track
- 10 RSVPs
- 2 meetings

---

## Pass threshold
**≥ 80 RSVPs and ≥ 16 meetings over 2 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/event-piggybacking`_
