---
name: regional-field-events-smoke
description: >
  Regional Field Events — Smoke Test. Host one dinner, happy hour, or lunch
  in a single target market. Validate that you can fill a room with ICP-matching
  prospects, that the format creates meaningful conversations, and that at least
  one attendee converts to a qualified meeting within 14 days.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Direct"
level: "Smoke Test"
time: "5 hours over 2 weeks"
outcome: ">=10 attendees from >=15 confirmed RSVPs, >=1 meeting booked within 14 days"
kpis: ["RSVP count", "Show rate", "Meetings booked"]
slug: "regional-field-events"
install: "npx gtm-skills add marketing/solution-aware/regional-field-events"
drills:
  - icp-definition
  - meetup-pipeline
  - threshold-engine
---

# Regional Field Events — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events, Direct

## Outcomes

- Confirm that ICP-matching prospects in a target market will accept an invitation to an in-person gathering
- Achieve a show rate that proves commitment (>=65% of confirmed RSVPs attend)
- Generate at least 1 qualified meeting from attendees within 14 days
- Validate which event format (dinner, happy hour, or lunch) works for your audience and budget

## Leading Indicators

- RSVP confirmations reach 15+ at least 5 days before the event
- At least 3 attendees have titles matching your buyer persona
- At least 2 attendees engage in conversation directly with the host about a relevant pain point
- At least 1 attendee asks about your product or requests follow-up unprompted

## Instructions

### 1. Define your field event ICP and format

Run the `icp-definition` drill to document who should attend. Focus on: title/role, company size, industry, and — critically — metro area. Field events only work if your ICP has sufficient density in the target city.

Choose your format based on budget and audience:
- **Dinner (8-15 people):** Highest engagement, highest cost ($60-150/person for F&B). Best for senior executives. Seated format forces conversation.
- **Happy hour (15-30 people):** Moderate engagement, moderate cost ($20-50/person for bar tab). Best for mid-level practitioners. Casual format allows people to self-select conversations.
- **Lunch (8-20 people):** Moderate engagement, moderate cost ($30-80/person for F&B). Best for time-constrained buyers. Weekday-friendly.

For smoke test: pick the format you can execute with the least logistical risk. Happy hours are the easiest to organize (no seating, flexible headcount, lower per-person cost).

### 2. Set up the event infrastructure

Run the `meetup-pipeline` drill to configure the event:

- Find a venue using local knowledge or Google Maps search. For the smoke test, use a familiar restaurant or bar — do not optimize venue selection yet. Book a private or semi-private space that fits your target headcount +20% buffer.
- Create an RSVP page with Cal.com: event name, date, time, neighborhood (not exact address — share the full address after RSVP), and a brief description framing the event as a gathering of [N] [role] peers to discuss [topic]
- Set up an Attio list for invitees and RSVPs with fields: name, email, company, title, RSVP status, attended
- Configure a confirmation email via Loops: send immediately on RSVP with date, time, and "we'll share the exact venue closer to the date"

### 3. Invite manually from your existing network

**Human action required:** This is a smoke test — invitations are personal, not automated.

- Build a list of 40-60 people in the target city who match the ICP. Sources: existing CRM contacts, LinkedIn connections, portfolio network, personal referrals.
- Send personal emails or LinkedIn messages to each. The invitation should feel peer-to-peer: "I'm hosting a [dinner/happy hour/lunch] with a small group of [role] leaders in [city] on [date]. We'll be discussing [topic]. Would love to have you."
- Do NOT use a marketing email template. Do NOT send via a bulk email tool. Personal invitations convert 3-5x better for first-time field events.
- Ask early confirmed attendees to invite one peer. Referral invites have the highest show rate.

### 4. Execute the event

**Human action required:** The host manages the event in person.

- Arrive 30 minutes early. Greet every attendee individually as they arrive. Introduce people to each other based on shared interests or roles.
- If dinner format: prepare 3-5 discussion questions related to the event topic. Start with a broad, non-threatening question ("What's the biggest shift in [domain] you've seen this year?"). Let the conversation evolve naturally.
- If happy hour: no formal structure needed. Circulate and facilitate introductions. Spend 5-10 minutes in focused conversation with each attendee.
- If lunch: similar to dinner but shorter. 2-3 discussion questions max.
- Do NOT pitch your product. The goal is to build relationships and identify pain points. If someone asks about your product, answer briefly and offer to follow up after the event.
- Note who expressed interest, who described relevant pain points, and who you want to follow up with. Capture these notes immediately after the event while memory is fresh.

### 5. Follow up within 48 hours

Within 24 hours:
- Send a personal thank-you email to each attendee. Reference something specific from your conversation.
- For anyone who expressed product interest or described a pain point: offer a 15-minute follow-up call with a Cal.com booking link.
- For all attendees: mention you're planning to host another gathering and ask if they'd like to be included.

Log all follow-up in Attio. Tag attendees by engagement level: high-intent, warm, attended-only.

### 6. Evaluate against the threshold

Run the `threshold-engine` drill to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Confirmed RSVPs | >=15 | Count in Attio event list |
| Attendees | >=10 | Attendees marked in Attio |
| Show rate | >=65% | Attendees / Confirmed RSVPs |
| Meetings booked | >=1 | Cal.com bookings within 14 days |

**PASS**: RSVPs, attendance, and at least 1 meeting met. Proceed to Baseline. The format works and your market has density.

**FAIL**: Diagnose which metric missed:
- Low RSVPs (<15): ICP density insufficient in this city, or topic/format not compelling. Try a different city with more ICP-matching companies, or change the format.
- Low show rate (<65%): Commitment was soft. Try dinner format (harder to no-show a reserved seat) or stronger social proof in the confirmation email.
- Zero meetings: Conversations stayed surface-level. The event topic may not be close enough to your product's problem space. Choose a topic that naturally surfaces the pain you solve.

## Time Estimate

- ICP definition and invitee list: 30 minutes
- Venue selection and booking: 30 minutes
- RSVP page and confirmation email setup: 30 minutes
- Personal invitations (40-60 messages): 1.5 hours
- Event execution: 1.5 hours (including 30 min early arrival)
- Follow-up emails and CRM logging: 30 minutes
- **Total: ~5 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | RSVP page and follow-up booking | Free tier: 1 user, unlimited events — [cal.com/pricing](https://cal.com/pricing) |
| Loops | Confirmation emails | Free tier: 1,000 contacts, 4,000 sends/mo — [loops.so/pricing](https://loops.so/pricing) |
| Attio | Invitee tracking and follow-up | Free tier: up to 3 users — [attio.com](https://attio.com) |
| Venue | Dinner/HH/lunch F&B | $200-2,000 depending on format and headcount |

**Estimated play-specific cost at Smoke: $200-2,000** (venue and F&B only — all software on free tiers)

## Drills Referenced

- `icp-definition` — define who should attend and validate ICP density in target market
- `meetup-pipeline` — set up RSVP infrastructure, promotion, and basic event operations
- `threshold-engine` — evaluate pass/fail against RSVP, attendance, and meeting targets
