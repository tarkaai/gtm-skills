---
name: event-piggybacking-baseline
description: >
  Event Piggyback Meetup — Baseline Run. Run 2-3 piggyback meetups across
  different conferences with structured promotion, automated registration, and
  PostHog tracking to validate the motion is repeatable.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Baseline Run"
time: "20 hours over 6 weeks"
outcome: ">= 25 total RSVPs and >= 5 follow-up meetings across 2-3 piggyback events"
kpis: ["Total RSVPs", "Attendance rate", "Meetings booked", "Pipeline created ($)"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - posthog-gtm-events
---

# Event Piggyback Meetup — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Prove the piggyback meetup motion is repeatable across multiple conferences. Run 2-3 piggyback events over 6 weeks with structured outreach, automated registration and confirmation, and full funnel tracking in PostHog. At this level the agent handles promotion orchestration and analytics setup; the human attends and hosts the events.

## Leading Indicators

- Invite-to-RSVP conversion rate improving across successive events (target: 8%+)
- Attendance rate holding steady or improving (target: 60%+)
- Percentage of attendees matching ICP (target: 50%+)
- Follow-up email response rate from attendees (target: 40%+)
- Time from meetup to first follow-up meeting declining

## Instructions

### 1. Build the piggyback event operations stack

Run the the meetup pipeline workflow (see instructions below) drill to create a repeatable template:

- Cal.com event type template for piggyback meetups (clone per event, update date/venue)
- Loops email sequences: registration confirmation, T-7 reminder, T-1 reminder, post-event follow-up
- Attio list template: "Piggyback - {Conference Name}" with standard fields (source conference, RSVP status, attendance status, interest level, next step)
- Standardized venue requirements checklist: capacity 15-30, within walking distance of conference venue, food/drink options, AV if needed

### 2. Configure event analytics

Run the `posthog-gtm-events` drill to implement the piggyback meetup event taxonomy:

- `piggyback_invite_sent` (properties: conference, channel, segment, email_template)
- `piggyback_invite_opened` (properties: conference, channel)
- `piggyback_rsvp_registered` (properties: conference, source_channel, is_icp_match)
- `piggyback_reminder_sent` (properties: conference, reminder_type)
- `piggyback_attended` (properties: conference, interest_level)
- `piggyback_meeting_booked` (properties: conference, days_to_meeting, source_conversation)
- `piggyback_deal_created` (properties: conference, deal_value_estimate)

Build a PostHog funnel: invite_sent -> rsvp_registered -> attended -> meeting_booked -> deal_created. Save as "[Event Piggybacking] - Baseline Funnel."

### 3. Run the first piggyback event with structured promotion

Select the next conference from your event-scouting pipeline. Run the the piggyback event promotion workflow (see instructions below) drill:

- Build the target attendee list via Clay enrichment (aim for 150-200 contacts)
- Launch email outreach at T-21 days via Instantly
- Launch LinkedIn outreach at T-18 days for non-openers and high-value targets
- Send Loops reminders at T-7 and T-1
- Run day-of amplification on LinkedIn

Track every touchpoint in PostHog using the event taxonomy from step 2.

**Human action required:** Book the venue, host the event, capture attendee notes.

### 4. Execute post-event follow-up

Within 48 hours of the meetup:

- Segment attendees by interest level observed at the event (agent can pre-draft emails based on notes):
  - **High interest (discussed a specific use case):** Personal email referencing the conversation, Cal.com booking link, offer a product walkthrough
  - **Medium interest (engaged in discussion):** Email with recap of key discussion points, relevant resource (case study or blog post), soft CTA to book a chat
  - **Low interest (attended but passive):** Group thank-you email, invitation to the next event
- Update all Attio contact records with attendance status, interest level, and next steps
- Fire PostHog events for each follow-up action

### 5. Run events 2 and 3

Repeat steps 3-4 for two more conferences over the next 4 weeks. Between events, review:

- Which conference audience produced the highest RSVP rate?
- Which promotion channel (email vs LinkedIn vs organic) drove the most registrations?
- Which meetup format produced the most follow-up meetings?
- Did the invite copy or timing need adjustment?

Adjust targeting, copy, and format between events based on data.

### 6. Evaluate against threshold

After 2-3 events, measure against: >= 25 total RSVPs AND >= 5 follow-up meetings booked across all piggyback events.

If PASS: the piggyback motion is repeatable and produces pipeline. Proceed to Scalable.
If FAIL: diagnose by event:
- If one event performed well and others did not, the conference selection is the variable. Tighten your conference criteria.
- If RSVPs were strong but meetings were low, the meetup format or follow-up sequence needs work.
- If all events underperformed, revisit the ICP-to-conference match or the meetup value proposition.

## Time Estimate

- 4 hours: operations stack setup (meetup-pipeline, posthog-gtm-events) — one-time
- 3 hours per event: promotion campaign setup and execution (piggyback-event-promotion)
- 3-4 hours per event: event hosting and attendance (human)
- 2 hours per event: post-event follow-up and logging
- 1 hour: cross-event analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Attendee list building and enrichment | Launch: $185/mo (https://www.clay.com/pricing) |
| Attio | Contact management and event tracking | Free for small teams (https://attio.com/pricing) |
| Cal.com | Registration pages and booking links | Free tier (https://cal.com/pricing) |
| Loops | Confirmation, reminder, and follow-up emails | Starter: $49/mo (https://loops.so/pricing) |
| Instantly | Personal outreach email campaigns | Growth: $37/mo (https://instantly.ai/pricing) |
| PostHog | Event tracking and funnel analysis | Free up to 1M events/mo (https://posthog.com/pricing) |

**Play-specific cost at Baseline level:** ~$250-500/event for venue costs. Clay Launch ($185/mo) + Instantly Growth ($37/mo) + Loops Starter ($49/mo) = ~$270/mo in tooling. Total: ~$500-800/mo for 2 events.

## Drills Referenced

- the piggyback event promotion workflow (see instructions below) — structured promotion campaign targeting conference attendees via email, LinkedIn, and community channels
- `posthog-gtm-events` — implement the piggyback event taxonomy for full funnel tracking
- the meetup pipeline workflow (see instructions below) — repeatable event operations: registration, confirmations, attendee management
