---
name: cold-event-hallway-demos-smoke
description: >
  Event Hallway Demos — Smoke Test. Pick one upcoming industry event, scout ICP-match
  attendees, show up, and run guerilla demos in the hallway to validate whether
  in-person intercepts generate conversations and follow-up meetings.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">= 5 conversations and >= 1 follow-up meeting booked from a single event day"
kpis: ["Conversations started", "Demos given", "Follow-up meetings booked"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - icp-definition
  - event-scouting
  - threshold-engine
---

# Event Hallway Demos — Smoke Test

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Validate that intercepting people at industry events and giving impromptu product demos produces conversations and at least one follow-up meeting. This is a single-event, manual test. No automation, no always-on process. You attend one event, talk to people, show your product, and see if anyone wants to continue the conversation.

## Leading Indicators

- Number of conversations started in hallways/lobbies (target: 10+)
- Percentage of conversations where you gave a demo (target: 50%+)
- Interest level distribution (more 3-5 than 1-2 means the audience fits)
- LinkedIn connection acceptance rate from people you met (target: 70%+)

## Instructions

### 1. Define your hallway demo ICP

Run the `icp-definition` drill. For hallway demos, specify:
- Which industries and company sizes to target
- Which job titles are worth a conversation (decision-makers vs. practitioners)
- What pain points your demo addresses that would resonate in a 60-second interaction
- What a "good" conversation outcome looks like (meeting booked, trial signup, LinkedIn connection)

### 2. Scout one event to attend

Run the `event-scouting` drill in minimal mode: identify 3-5 upcoming events in your area within the next 2 weeks. For each, evaluate:
- Does the audience match your ICP? (Check speaker list and sponsor companies)
- Is the venue accessible without a badge? (Hotel lobbies and common areas are ideal)
- Is the event large enough for hallway traffic? (200+ attendees preferred)
- Can you get there affordably? (Local events only for the Smoke test)

Pick the single best event. If the event-scouting drill identifies speakers or sponsors matching your ICP, note 5-10 names and faces to look for.

### 3. Prepare your demo kit

- Load your product on a laptop and phone. Ensure it works offline or on mobile hotspot.
- Prepare a 60-second demo script: open with the pain point, show the solution in action, end with "want to see more?"
- Prepare a 3-minute extended demo for people who say yes.
- Generate a Cal.com QR code (or save your booking link to share via AirDrop/text).
- Create a simple logging method: notes app, Google Form on your phone, or a paper notepad. For each conversation, capture: name, company, title, interest level (1-5), key pain point mentioned, agreed next step.

**Human action required:** You must attend the event in person and run the demos yourself. The agent prepares everything but you execute the conversations.

### 4. Execute at the event

Show up 30 minutes before sessions start. Position yourself near coffee, registration, or the lobby. Between sessions (the prime window), stand in hallways between session rooms. At lunch, sit at communal tables. After the last session, linger in the lobby.

Start conversations with context, not pitches: "What did you think of the keynote?" or "Are you working on anything related to [event topic]?" Listen for pain signals. When you hear a match, offer a quick 60-second demo. If they are interested, extend to 3 minutes and book a follow-up meeting on the spot via your booking link.

Log every conversation immediately after it ends. Do not rely on memory for more than 2 conversations.

### 5. Same-day follow-up

Within 4 hours of the event ending:
- Connect on LinkedIn with every person you spoke with. Reference the specific conversation in your connection request.
- Send a personal email to anyone who was interest level 4-5. Reference what you showed them and include your booking link.
- Log all contacts and outcomes in Attio CRM.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Pass threshold: >= 5 conversations started AND >= 1 follow-up meeting booked from a single event day.

If PASS: the hallway demo motion works for your ICP. Proceed to Baseline.
If FAIL: diagnose -- was the event wrong (no ICP matches), was the venue wrong (no hallway access), or was the approach wrong (conversations but no interest)? Adjust and re-run at a different event.

## Time Estimate

- 2 hours: ICP definition and event scouting
- 1 hour: demo preparation and logistics
- 3-6 hours: event attendance and execution (varies by event length)
- 1 hour: same-day follow-up and logging

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Event scouting and attendee research | Launch: $185/mo; Growth: $495/mo (https://www.clay.com/pricing) |
| Attio | Log contacts and conversations | Free for small teams (https://attio.com/pricing) |
| Cal.com | Booking link for follow-up meetings | Free tier (https://cal.com/pricing) |

**Play-specific cost at Smoke level:** Free (excluding travel). Clay credits used for scouting are minimal (20-30 Claygent queries). Use existing Clay plan or free trial.

## Drills Referenced

- `icp-definition` — define who you are looking for at events
- `event-scouting` — find and score events worth attending
- `threshold-engine` — evaluate pass/fail against the outcome threshold
