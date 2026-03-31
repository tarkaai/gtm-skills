---
name: local-field-prospecting-smoke
description: >
  Local Field Prospecting — Smoke Test. Founder visits 2-3 coworking spaces or business
  hubs in one session to test whether in-person conversations with local businesses yield
  qualified meetings for your ICP.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Other"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 1 qualified meeting booked from in-person conversations in 1 week"
kpis: ["Conversations held", "Meetings booked", "Conversation-to-meeting rate"]
slug: "local-field-prospecting"
install: "npx gtm-skills add sales/qualified/local-field-prospecting"
drills:
  - icp-definition
  - field-visit-planning
  - field-contact-logging
  - threshold-engine
---

# Local Field Prospecting — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Other (In-Person)

## Outcomes

The founder completes one field session visiting 2-3 local venues (coworking spaces, business parks, coffee shops near offices) and has at least 5 short conversations with people who work at businesses in the target area. At least 1 of those conversations converts to a booked follow-up meeting. This proves that in-person outreach produces qualified meetings before investing in tooling or process.

## Leading Indicators

- Number of venues visited in one session
- Number of conversations initiated (target: 5+)
- Number of business cards or contact details exchanged
- Interest level distribution: what percentage of conversations surface a relevant pain point
- Whether the founder can articulate a working pitch after the session

## Instructions

### 1. Define your ICP for local field prospecting

Run the `icp-definition` drill. For field prospecting specifically, add these criteria to your standard ICP:

- **Geography**: Define the radius you will cover on foot or by car. Field prospecting works within a 15-30 minute drive radius.
- **Venue affinity**: Which types of locations does your ICP frequent? Startups cluster in coworking spaces. Professional services firms are in business parks. Trades and local services are in commercial/industrial districts.
- **In-person receptivity**: Some ICPs respond well to in-person outreach (SMB owners, startup founders, local services). Others do not (enterprise buyers behind security desks). Identify which ICP segments are accessible in-person.

### 2. Plan your first field visit

Run the `field-visit-planning` drill. For the Smoke test, keep scope small:

- Use `google-maps-place-search` to find 2-3 coworking spaces or business hubs within your target area
- Check opening hours and pick a weekday mid-morning (10-11am) when foot traffic is highest
- Look up each venue online: who works there, are there community areas, is there a front desk or open floor plan
- Plan a simple route — no need for route optimization at this scale

**Human action required:** The founder physically visits these venues. The agent cannot do this step. The agent's job is preparation and post-visit processing.

### 3. Prepare the founder's toolkit

Before the visit, the agent prepares:

- **30-second pitch**: A conversational opener tied to the ICP's pain points. Not a sales pitch — a genuine question. Example: "Hey, I noticed a lot of [industry] companies work out of here. We've been talking to [role] who struggle with [pain]. Is that something you run into?"
- **Business card or digital contact exchange method**: Cal.com booking link on a card, QR code, or simply "Can I grab your email and send you something useful?"
- **Conversation guide**: 3-4 questions to qualify on the spot: What do you do? What's your biggest challenge with [area]? How do you handle [problem] today? Would it be useful to chat more about that next week?
- **Note-taking method**: Phone notes app, voice memo, or quick shorthand for capturing name, company, pain, interest level after each conversation

### 4. Execute the field visit

**Human action required:** The founder visits the venues and has conversations. Guidelines for the founder:

- Arrive during a busy time (mid-morning or lunch hour)
- Start with the community manager or front desk person — they often introduce you to members
- Be genuinely curious, not salesy. Ask questions. Listen for pain points.
- After each conversation, immediately jot down: name, company, what they do, pain mentioned, interest level (hot/warm/cold), and agreed next step
- Spend 30-60 minutes per venue. Leave when conversations dry up.
- Target 5+ conversations across the session

### 5. Log all conversations to CRM

Within 1 hour of finishing the session (while details are fresh), run the `field-contact-logging` drill:

- Provide the agent with your raw notes (text or voice memo transcript)
- The agent creates structured CRM records in Attio for every person you spoke with
- Each record gets: contact info, venue, qualification data, interest level, next step
- Hot leads get a Deal record created at "Meeting Requested" stage
- PostHog events fire for analytics tracking

### 6. Send follow-ups

For every conversation where a next step was agreed:

- **"Send me more info"**: Agent drafts a short, personal follow-up email referencing the specific conversation. Not a template — reference the venue, what you discussed, and the pain they mentioned. Include the Cal.com booking link.
- **"Let's meet next week"**: Agent sends the Cal.com booking link with 2-3 suggested times.
- **"Connect on LinkedIn"**: Founder sends a personalized connection request mentioning the in-person meeting.

Follow-ups should go out within 24 hours of the visit.

### 7. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did you book at least 1 qualified meeting from this field session?

- Pull conversation data from Attio and meeting data from Cal.com/PostHog
- Compare against threshold: >= 1 meeting in 1 week
- If **PASS**: The channel works. Proceed to Baseline to systematize it.
- If **FAIL**: Diagnose — was the issue venue selection (wrong ICP density), timing (nobody was there), pitch (conversations but no interest), or follow-up (interest but no conversion)? Adjust and run another session.

## Time Estimate

- 1 hour: ICP definition and venue research (agent)
- 0.5 hours: Visit planning and pitch preparation (agent)
- 2 hours: Field visit execution (founder, human action)
- 0.5 hours: Contact logging and follow-up sending (agent + founder debrief)

Total: ~4 hours over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Maps | Venue discovery and research | Free ($200/mo credit covers this volume) |
| Attio | CRM — log contacts and deals | Free tier (up to 3 users) |
| Cal.com | Booking link for in-field use | Free tier (1 user) |
| PostHog | Event tracking | Free tier (1M events/mo) |

**Total Smoke cost: $0** (all tools within free tiers at this volume)

## Drills Referenced

- `icp-definition` — define who you are looking for in the field
- `field-visit-planning` — research venues, build route, prepare intel
- `field-contact-logging` — log in-person conversations as structured CRM records
- `threshold-engine` — evaluate pass/fail against the meeting threshold
