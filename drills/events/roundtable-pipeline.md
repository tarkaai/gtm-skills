---
name: roundtable-pipeline
description: Plan, curate invitees, execute, and capture insights from a micro-roundtable discussion with 5-10 senior prospects
category: Events
tools:
  - Cal.com
  - Loops
  - Attio
  - PostHog
  - Fireflies
fundamentals:
  - calcom-event-types
  - calcom-booking-links
  - loops-broadcasts
  - loops-sequences
  - attio-lists
  - attio-contacts
  - attio-notes
  - posthog-custom-events
  - fireflies-transcription
  - fireflies-action-items
---

# Roundtable Pipeline

This drill covers the complete lifecycle of a single micro-roundtable: topic selection, guest curation, invitation, execution logistics, discussion capture, and post-event data logging. Roundtables are intentionally small (5-10 attendees) and discussion-driven, not presentation-driven. The value is peer conversation, not one-way content.

## Prerequisites

- ICP defined (run `icp-definition` drill first)
- Video conferencing platform (Zoom, Google Meet, or Riverside) configured
- Attio workspace with contacts matching your ICP
- Loops account for email invitations
- Cal.com for RSVP management
- Fireflies.ai connected to your conferencing platform for transcription

## Steps

### 1. Choose the roundtable topic

Select a topic that meets three criteria:

- **Peer-relevant**: Something your target execs discuss with peers but rarely get honest answers about (budget allocation, vendor selection, team structure, emerging technology bets)
- **Non-promotional**: The topic must NOT be about your product. It should be about a problem space your product operates in. "How are you handling X?" not "Why our product solves X."
- **Opinionated**: Pick a topic where reasonable people disagree. This drives discussion. Avoid consensus topics — if everyone agrees, the conversation dies in 10 minutes.

Write a 2-sentence topic description and 3 discussion questions. Store these in Attio as a note on the event record using `attio-notes`.

### 2. Curate the guest list

Using `attio-lists`, create a list called "Roundtable - [Topic] - [Date]". Add 15-20 target invitees (you need 3x your target attendance to account for declines). For each invitee, verify:

- Title is senior enough to contribute meaningfully (VP+, Director+, or Founder)
- Company size and stage match other invitees (a Series A founder and a Fortune 500 VP will not have a productive conversation together)
- No competing companies in the same session (check industry and product overlap)
- Mix of perspectives: include 2-3 people who will likely disagree on the topic

Using `attio-contacts`, tag each invitee with `roundtable-invited` and the event slug.

### 3. Send tiered invitations

Using `loops-broadcasts`, send invitations in two waves:

**Wave 1 (Day -21): Personal invitations to top-tier targets**
- Send from the founder/host's email address
- Subject: direct and specific, e.g., "Invitation: [Topic] discussion with [N] [role] leaders"
- Body: explain the format (small group, off-the-record discussion, no pitches), the topic and why it matters now, who else is being invited (by profile, not name), and the date/time
- Include a Cal.com RSVP link created via `calcom-event-types` (set up as a group event with max capacity matching your target attendance)
- CTA: "Reply to confirm or grab a slot: [Cal.com link]"

**Wave 2 (Day -14): Broader invitation**
- Send to the remaining invitees on your list
- Mention confirmed attendee count: "We have [N] confirmed so far, including leaders from [industry/company type]"
- Same Cal.com link

### 4. Manage RSVPs and confirmations

Track all RSVPs in Attio using `attio-contacts`:
- Update each contact's status: "Confirmed", "Declined", "No Response"
- If confirmations fall below 8 by Day -7, send a follow-up wave using `loops-broadcasts` with urgency framing: "3 spots remaining"
- Cap at 10 confirmed attendees. If you hit 10, move overflow to a waitlist.

Send a confirmation email 3 days before via `loops-sequences`:
- Include: date, time, video link, topic description, 3 discussion questions, and attendee list (first name + company only)
- Send a 1-hour reminder on event day with just the join link

### 5. Execute the roundtable

**Human action required:** The host facilitates the discussion live. The agent prepares everything but cannot run the conversation.

Pre-event checklist (agent-executable):
- Verify Fireflies.ai is connected to the video meeting for transcription using `fireflies-transcription`
- Send the host a briefing: attendee names, companies, roles, and one relevant data point per person (recent LinkedIn post, company news, or Attio notes)
- Post the 3 discussion questions in the meeting chat at start time

Facilitation guidance (for the host):
- Open with a 2-minute frame: "This is off the record, no pitches, pure peer discussion"
- Start with an easy question. Save the controversial one for when the group is warmed up
- Call on quiet participants by name: "Sarah, you're dealing with this at [company] — what's your take?"
- Target 45-60 minutes total. End 5 minutes early with: "What was the most surprising thing you heard today?"

### 6. Capture and log event data

After the event:

1. Pull the Fireflies transcript using `fireflies-transcription` and extract action items using `fireflies-action-items`
2. For each attendee, log in Attio using `attio-notes`:
   - Attended: yes/no
   - Engagement level: high (spoke multiple times, asked questions), medium (spoke once or twice), low (listened only)
   - Key opinions expressed (2-3 bullet points from the transcript)
   - Follow-up interest signals (mentioned a pain point, asked about solutions, requested a connection)
3. Fire PostHog events using `posthog-custom-events`:
   - `roundtable_held` with properties: topic, date, invites_sent, confirmed, attended, engagement_score
   - `roundtable_attended` for each attendee with properties: contact_id, engagement_level, topic
   - `roundtable_meeting_signal` for each attendee who expressed follow-up interest

### 7. Generate discussion summary

Using the Fireflies transcript, generate a 1-page discussion summary:
- 3-5 key themes that emerged
- Points of agreement and disagreement
- Surprising insights or data points shared by attendees
- Open questions that could drive a future session

Store the summary in Attio using `attio-notes`. This summary becomes a valuable follow-up asset — share it with attendees in the nurture sequence.
