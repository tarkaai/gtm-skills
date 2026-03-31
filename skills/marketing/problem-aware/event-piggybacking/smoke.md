---
name: event-piggybacking-smoke
description: >
  Event Piggyback Meetup — Smoke Test. Pick one upcoming industry conference,
  host a single evening meetup nearby to ride the attendee halo, and validate
  whether piggybacking generates RSVPs and follow-up meetings.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: ">= 10 RSVPs and >= 2 follow-up meetings booked within 2 weeks"
kpis: ["RSVPs", "Attendance rate", "Follow-up meetings booked"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - event-scouting
  - meetup-pipeline
  - threshold-engine
---

# Event Piggyback Meetup — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Validate that hosting a meetup timed to coincide with a major industry conference produces RSVPs from conference attendees and at least 2 follow-up meetings. This is a single-event, manual test. You pick one conference, organize one evening meetup nearby, promote it personally, and measure whether the conference halo effect draws your ICP into the room.

## Leading Indicators

- Number of target conference attendees who RSVP (target: 10+)
- Percentage of RSVPs that come from ICP-matching companies (target: 50%+)
- LinkedIn connection acceptance rate from people you invited (target: 60%+)
- Day-of attendance rate relative to RSVPs (target: 60%+)
- Number of meaningful conversations at the meetup (target: 5+)

## Instructions

### 1. Select a conference to piggyback on

Run the `event-scouting` drill in minimal mode. Identify 3-5 industry conferences happening within the next 4-6 weeks in a city you can reach affordably. Evaluate each conference for piggyback potential:

- **ICP density:** Do the speakers, sponsors, and advertised attendee profile match your ICP? Check the speaker list and sponsor logos on the conference website.
- **Conference size:** Sweet spot is 500-5,000 attendees. Smaller conferences do not create enough overflow; larger ones disperse attendees across too many competing side events.
- **Timing opportunity:** Does the conference agenda leave an open evening? Day 1 or day 2 evenings work best (attendees have arrived but are not yet exhausted). Avoid the final evening (people leave early or have dinners booked).
- **Venue accessibility:** Is there a restaurant, bar, co-working space, or hotel meeting room near the conference venue that you can book for 15-30 people on short notice?

Pick the single best conference. Note 10-15 speakers and sponsor contacts who match your ICP.

### 2. Set up the meetup

Run the `meetup-pipeline` drill to create the event infrastructure:

- Create a registration page via Cal.com event type or a simple form (Typeform, Google Form). Include: meetup title, date/time, venue address, format description (roundtable, demo night, or casual mixer), and capacity limit.
- Set up an email confirmation via Loops that fires when someone registers. Include venue directions, parking or transit info, and a calendar invite attachment.
- Create an Attio list called "Piggyback - {Conference Name}" to track registrants.

Choose a meetup format:
- **Roundtable discussion (10-20 people):** Best for Smoke test. Pick a topic relevant to the conference theme. Low cost, high relationship value.
- **Casual mixer (15-30 people):** Works if you prefer networking over structured content. Budget $200-400 for drinks and appetizers.

**Human action required:** Book the venue. Negotiate food/drink minimums. Confirm AV equipment if needed for a presentation.

### 3. Promote the meetup manually

For the Smoke test, promotion is manual and personal. Do not use automation.

- **Email (founder's personal inbox):** Write a short, peer-to-peer invitation email. Reference the conference by name. Mention the meetup topic, date, time, venue, and that you are hosting an intimate gathering for people in town for the conference. Send to: the 10-15 speakers/sponsor contacts you identified in step 1, plus any existing contacts who you know are attending the conference. Aim for 30-50 personal emails.
- **LinkedIn:** Post a public announcement about the meetup from the host's profile. Tag the conference hashtag. Send personal messages to 10-15 high-value targets referencing their conference attendance or talk.
- **Conference community channels:** If the conference has an attendee Slack, Discord, or WhatsApp group, post the meetup details (with permission from organizers).

Track who you invited and who responded in the Attio list.

### 4. Execute the meetup

**Human action required:** You must attend and host the meetup in person.

- Arrive 30 minutes early to set up and greet early arrivals individually.
- Start with a 2-minute welcome. Introduce yourself, explain the format, and set expectations.
- If roundtable: prepare 5-7 discussion questions tied to the conference theme. Moderate to ensure everyone participates.
- If mixer: work the room. Introduce attendees to each other based on shared interests or roles.
- During the event, note who attends, who engages deeply, and who you want to follow up with.
- End with a clear mention of how to stay in touch (LinkedIn, your website, booking a call).

### 5. Follow up within 48 hours

Within 24 hours after the meetup:
- Connect on LinkedIn with every attendee. Reference a specific conversation from the meetup.
- Send a personal email to anyone you want a follow-up meeting with. Reference what you discussed and propose a specific next step (demo, call, introduction).
- Send a group thank-you email to all attendees via Loops with a recap and an invitation to stay connected.

Log all contacts, conversation notes, and next steps in Attio.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pass threshold: >= 10 RSVPs AND >= 2 follow-up meetings booked within 2 weeks of the meetup.

If PASS: the piggyback motion works for your ICP and conference selection. Proceed to Baseline.
If FAIL: diagnose the failure point:
- **Low RSVPs (<10):** Promotion was too narrow, conference audience did not match ICP, or the meetup topic did not resonate. Try a different conference or adjust the topic.
- **Good RSVPs but low attendance:** Venue was inconvenient, timing conflicted with conference dinners, or reminders were insufficient.
- **Good attendance but no meetings:** The attendees did not match your ICP, or the meetup format did not create opportunities for meaningful conversation.

## Time Estimate

- 2 hours: conference selection and target identification (event-scouting)
- 1 hour: meetup setup (registration page, confirmation email, Attio list)
- 1.5 hours: promotion (personal emails, LinkedIn posts/messages, community posts)
- 2-4 hours: event execution (including setup and teardown)
- 1 hour: follow-up emails, LinkedIn connections, Attio logging
- 0.5 hours: threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference attendee research and enrichment | Launch: $185/mo (https://www.clay.com/pricing) |
| Attio | Track registrants, contacts, and follow-ups | Free for small teams (https://attio.com/pricing) |
| Cal.com | Registration page and booking links | Free tier (https://cal.com/pricing) |
| Loops | Confirmation and follow-up emails | Free up to 1,000 contacts (https://loops.so/pricing) |
| PostHog | Track funnel events if desired | Free up to 1M events/mo (https://posthog.com/pricing) |

**Play-specific cost at Smoke level:** $200-400 for venue food/drinks. Clay credits for attendee research are minimal (20-30 queries). All other tools on free tiers.

## Drills Referenced

- `event-scouting` — find and evaluate conferences worth piggybacking on
- `meetup-pipeline` — set up registration, confirmations, and attendee tracking
- `threshold-engine` — evaluate pass/fail against the outcome threshold
