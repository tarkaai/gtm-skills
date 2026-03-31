---
name: local-field-prospecting-baseline
description: >
  Local Field Prospecting — Baseline Run. Systematize field visits into a repeatable weekly
  cadence with CRM tracking, automated follow-ups, and a Cal.com booking flow that turns
  in-person conversations into pipeline.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Other"
level: "Baseline Run"
time: "10 hours over 2 weeks"
outcome: "≥ 3 qualified meetings booked over 2 weeks from 2+ field sessions"
kpis: ["Conversations per session", "Meetings booked per session", "Conversation-to-meeting rate", "Follow-up response rate"]
slug: "local-field-prospecting"
install: "npx gtm-skills add sales/qualified/local-field-prospecting"
drills:
  - field-contact-logging
  - meeting-booking-flow
  - posthog-gtm-events
  - follow-up-automation
---

# Local Field Prospecting — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Other (In-Person)

## Outcomes

The founder runs 2+ field sessions per week on a consistent schedule. Each session follows a prepared route with venue intel. Every conversation is logged to CRM within 1 hour. Follow-up emails send automatically based on conversation outcome. Cal.com booking links convert interested contacts into scheduled meetings. At least 3 meetings booked in 2 weeks proves the process is repeatable.

## Leading Indicators

- Sessions completed per week (target: 2+)
- Conversations per session (target: 5+, improving from Smoke)
- Follow-up emails sent within 24 hours (target: 100%)
- Follow-up response rate (email opens and replies)
- Cal.com booking page conversion rate
- Time from conversation to booked meeting (shorter is better)
- Venue diversity: are you covering enough territory or returning to the same spots

## Instructions

### 1. Set up the full meeting booking flow

Run the `meeting-booking-flow` drill to create the end-to-end infrastructure:

- Create Cal.com event types: "Quick Coffee Chat — 15 min" (for in-field offers), "Discovery Call — 30 min" (for qualified follow-ups)
- Set up an n8n workflow that fires when a Cal.com booking is created: create/update Attio Person and Company records, create a Deal at "Meeting Booked" stage, fire a `field_meeting_booked` PostHog event
- Generate a short booking link and a QR code the founder can share in person
- Set up pre-meeting prep automation: when a meeting is booked, the agent pulls company data from Clay and creates a brief in Attio

### 2. Configure field-specific event tracking

Run the `posthog-gtm-events` drill with these field-prospecting-specific events:

| Event | Properties | When to Fire |
|-------|-----------|--------------|
| `field_session_started` | venue_count, territory, day_of_week | When founder begins a field session |
| `field_visit_completed` | venue, duration_minutes, conversations_count | After each venue visit |
| `field_conversation_logged` | venue, interest_level, pain_identified, outcome | After logging each contact |
| `field_followup_sent` | contact_id, followup_type, channel | When follow-up email/message sends |
| `field_followup_replied` | contact_id, sentiment | When contact responds to follow-up |
| `field_meeting_booked` | venue, contact_name, source_channel | When a meeting is scheduled |

Connect PostHog to Attio via n8n webhook so all events are captured without manual entry.

### 3. Build automated follow-up sequences

Run the `follow-up-automation` drill configured for field prospecting:

**Trigger 1 — Hot lead (meeting requested in person):**
- Immediately after logging: send Cal.com booking link via email
- If no booking within 48 hours: send a nudge referencing the conversation
- If no booking within 5 days: final follow-up with a specific proposed time

**Trigger 2 — Warm lead (interested, no commitment):**
- Within 24 hours: send a personalized email with a relevant resource (case study, article, or tool) tied to their stated pain point
- After 3 days: follow up asking if the resource was useful, offer a quick chat
- After 7 days: final touch — share a relevant customer story and booking link

**Trigger 3 — "Send me info" lead:**
- Within 4 hours: send the requested information with a brief note
- After 3 days: follow up asking if they had a chance to review
- After 7 days: offer a 15-minute walkthrough of what you sent

All follow-ups must be personalized with conversation details from the Attio note. Never send template-feeling emails to someone you met face-to-face — it destroys the trust built in person.

**Guardrails:** Maximum 4 follow-up touches per contact. Suppress contacts who reply negatively or unsubscribe. Check Attio deal status before each send.

### 4. Establish a weekly field cadence

Plan a repeatable weekly schedule:

- **Monday**: Agent runs the field visit planning workflow (see instructions below) drill for the week's sessions. Prepares 2 routes covering different areas.
- **Tuesday and Thursday** (or founder's preferred days): Field sessions. 2-3 hours each, visiting 3-5 venues per session.
- **After each session**: Founder does a voice debrief. Agent runs `field-contact-logging` within 1 hour.
- **Wednesday and Friday**: Follow-up day. Agent sends all automated follow-ups. Founder handles any that need a personal touch.

### 5. Run weekly field sessions for 2 weeks

**Human action required:** The founder executes 4+ field sessions over 2 weeks, following the planned routes. Between sessions, the agent handles all logging, follow-ups, and booking coordination.

For each session:
1. Agent prepares venue intel briefs (from the field visit planning workflow (see instructions below))
2. Founder visits venues and has conversations
3. Founder records voice debrief in the car
4. Agent logs all contacts (`field-contact-logging`)
5. Automated follow-ups trigger based on interest level
6. Agent monitors Cal.com bookings and updates Attio

### 6. Evaluate against threshold

After 2 weeks, evaluate: >= 3 meetings booked from field sessions.

Pull data from PostHog and Attio:
- Total sessions completed
- Total conversations logged
- Meetings booked (and which venues/sessions they came from)
- Follow-up conversion rate
- Time from conversation to booked meeting

If **PASS**: The cadence is repeatable. Proceed to Scalable to find the 10x multiplier.
If **FAIL**: Diagnose by funnel stage:
- Low conversations? Wrong venues or wrong timing.
- Conversations but no interest? Pitch needs work or ICP is wrong for this channel.
- Interest but no meetings? Follow-up process is broken or too slow.
- Meetings from follow-ups but not in-person? The in-person conversion needs work — practice the booking ask.

## Time Estimate

- 2 hours/week: Visit planning and preparation (agent)
- 4 hours/week: Field sessions — 2 sessions x 2 hours each (founder, human action)
- 1 hour/week: Contact logging and debrief (agent + founder)
- 1 hour/week: Follow-up monitoring and adjustment (agent)
- 0.5 hours: Threshold evaluation (agent)

Total: ~10 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Maps | Venue discovery and route planning | Free ($200/mo credit covers this volume) |
| Attio | CRM — contacts, deals, notes | Free tier or Plus at $29/user/mo |
| Cal.com | Meeting booking | Free tier (1 user) |
| PostHog | Event tracking and funnels | Free tier (1M events/mo) |
| n8n | Follow-up automation workflows | Community (self-hosted, free) or Starter at $24/mo |

**Total Baseline cost: $0-53/mo** (free tiers cover most needs; n8n Starter if not self-hosting)

## Drills Referenced

- the field visit planning workflow (see instructions below) — weekly venue research, route building, intel briefs
- `field-contact-logging` — structured CRM logging of in-person conversations
- `meeting-booking-flow` — Cal.com to CRM to prep automation pipeline
- `posthog-gtm-events` — field-specific event taxonomy for analytics
- `follow-up-automation` — automated email sequences triggered by conversation outcome
