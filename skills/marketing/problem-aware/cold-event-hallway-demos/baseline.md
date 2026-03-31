---
name: cold-event-hallway-demos-baseline
description: >
  Event Hallway Demos — Baseline Run. Attend 3-5 events over 4 weeks with structured
  pre-event scouting, real-time conversation logging, and automated post-event follow-up
  to prove the motion is repeatable.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">= 15 conversations, >= 8 demos, and >= 3 follow-up meetings across 3+ events"
kpis: ["Conversations started", "Demos given", "Follow-up meetings booked", "Demo-to-meeting conversion rate"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - event-scouting
  - hallway-demo-operations
  - posthog-gtm-events
  - meeting-booking-flow
---

# Event Hallway Demos — Baseline Run

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Prove the hallway demo motion is repeatable across multiple events. You attend 3-5 events over 4 weeks with structured pre-event preparation, real-time conversation capture, and same-day follow-up. Results hold across events, not just one lucky outing. The agent handles scouting, enrichment, CRM logging, follow-up sequencing, and analytics. You handle the in-person conversations.

## Leading Indicators

- Conversations-per-event trending stable or up (not declining after the first event)
- Demo-to-meeting conversion rate >= 20% across all events
- Follow-up email response rate >= 30% (from contacts who were interest level 3+)
- LinkedIn connection acceptance rate >= 60%
- At least 1 deal created in CRM from hallway demo source

## Instructions

### 1. Build a 4-week event calendar

Run the `event-scouting` drill to identify 5-8 candidate events in the next 4 weeks. Score each event for ICP density, venue accessibility, and expected ROI (see the drill for scoring criteria). Select 3-5 events to attend, spacing them across the 4-week period to allow for follow-up time between events.

For each selected event, run the attendee enrichment step of `event-scouting` to build a target list of 10-15 ICP-match contacts (speakers, sponsors, known attendees). Store target lists in Attio with the event name as a tag.

### 2. Set up hallway demo analytics

Run the `posthog-gtm-events` drill to configure event tracking for the hallway demo funnel. Create these custom events:
- `hallway_demo_conversation_started` (properties: event_name, city, date)
- `hallway_demo_given` (properties: event_name, demo_length, interest_level)
- `hallway_demo_meeting_booked` (properties: event_name, source_conversation, days_to_meeting)
- `hallway_demo_followup_sent` (properties: event_name, followup_type, interest_level)
- `hallway_demo_deal_created` (properties: event_name, deal_value_estimate)

Build a PostHog funnel: conversation_started -> demo_given -> meeting_booked -> deal_created.

### 3. Configure the meeting booking flow

Run the `meeting-booking-flow` drill to connect Cal.com bookings to Attio. When someone books a follow-up meeting via your Cal.com link, the flow should:
- Create or update the contact in Attio
- Create a deal at "Meeting Booked" stage
- Tag the deal source as "hallway-demo" with the event name
- Fire a `meeting_booked` event in PostHog
- Send a pre-meeting prep email with your product one-pager

### 4. Execute hallway demo operations at each event

For each of the 3-5 events, run the `hallway-demo-operations` drill:

**Pre-event (day before):**
- Review the target contact list for this event (photos, companies, hooks)
- Prepare demo environment on laptop and phone
- Print or save QR code for Cal.com booking link
- Set up mobile logging (Attio mobile or a quick-capture form)

**Event day:**
- Execute the hallway demo approach (see the drill for positioning strategy and conversation framework)
- Log every conversation in real time with: name, company, title, interest level, demo given (y/n), next step agreed

**Human action required:** Attend each event and run conversations in person. The agent handles all pre-event prep, enrichment, and post-event follow-up.

**Same-day follow-up (within 4 hours):**
- The agent creates/updates Attio contacts for everyone you logged
- Creates deals for interest level 4-5 contacts
- Sends LinkedIn connection requests referencing specific conversations
- Triggers follow-up email sequences by interest tier (see hallway-demo-operations drill for the tier logic)

### 5. Compare event performance

After attending 3+ events, compare them in PostHog:
- Which events had the highest conversation count?
- Which events had the best demo-to-meeting conversion?
- What venue types produced the most conversations (hotel lobby vs convention center vs meetup venue)?
- What conversation openers worked best?

Log learnings in Attio as notes on each event record. These feed into the Scalable level's event selection intelligence.

### 6. Evaluate against threshold

Pass threshold: >= 15 conversations started, >= 8 demos given, AND >= 3 follow-up meetings booked across 3+ events.

If PASS: the motion is repeatable. You have data on which events and approaches work. Proceed to Scalable.
If FAIL: diagnose per-event. If one event was great and others flopped, the problem is event selection. If conversations are high but meetings are low, the problem is the demo or CTA. If conversations are low everywhere, the problem is venue accessibility or positioning.

## Time Estimate

- 4 hours: event scouting, attendee enrichment, and analytics setup
- 2 hours per event: pre-event prep and demo preparation
- 3-6 hours per event: attendance and execution
- 1 hour per event: same-day follow-up and logging
- 2 hours: cross-event analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Event scouting and attendee enrichment | Launch: $185/mo (https://www.clay.com/pricing) |
| Attio | Contact/deal management and conversation logging | Free for small teams (https://attio.com/pricing) |
| Cal.com | Follow-up meeting booking | Free tier (https://cal.com/pricing) |
| PostHog | Funnel analytics and event tracking | Free up to 1M events/mo (https://posthog.com/pricing) |
| Loops | Follow-up email sequences | Free up to 1,000 contacts (https://loops.so/pricing) |
| Fireflies | Conversation transcription (if recording demos) | Free: 800 min/mo; Pro: $10/user/mo annual (https://fireflies.ai/pricing) |

**Play-specific cost at Baseline level:** ~$185/mo (Clay Launch plan for scouting/enrichment). All other tools on free tiers. Plus travel costs per event.

## Drills Referenced

- `event-scouting` — discover and rank events, build per-event target lists
- `hallway-demo-operations` — execute demos, capture conversations, route follow-up
- `posthog-gtm-events` — configure hallway demo funnel tracking in PostHog
- `meeting-booking-flow` — connect Cal.com bookings to Attio and PostHog
