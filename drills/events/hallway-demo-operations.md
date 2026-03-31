---
name: hallway-demo-operations
description: Execute and track guerilla hallway demos at industry events with structured conversation capture and follow-up routing
category: Events
tools:
  - Attio
  - Cal.com
  - Loops
  - PostHog
  - Fireflies
fundamentals:
  - attio-contacts
  - attio-deals
  - calcom-booking-links
  - loops-sequences
  - posthog-custom-events
  - fireflies-action-items
---

# Hallway Demo Operations

This drill covers the execution side of hallway demos: what to do before, during, and after showing up at an event to demo your product in hallways, lobbies, and common areas. It turns ad-hoc conversations into structured pipeline.

## Input

- Event scouting output (from `event-scouting` drill): event details, target list, venue intel
- Product demo environment loaded on laptop/tablet, working offline
- Cal.com booking link for follow-up meetings
- Attio mobile access for real-time logging

## Steps

### 1. Pre-event preparation (day before)

Prepare the demo environment:

- Load your product on a laptop and tablet. Ensure both work offline or on mobile hotspot.
- Prepare 3 demo flows of different lengths: 60-second elevator pitch, 3-minute quick demo, 10-minute deep dive. Each should end with a clear ask (book a follow-up, try the product, connect on LinkedIn).
- Print or save to phone: target contact photos from LinkedIn (for recognition), their company context, and a personalized hook per person ("I saw your talk on X -- we solve that exact problem").
- Create a simple logging form (Typeform, Google Form, or Attio mobile) with fields: name, company, title, email/LinkedIn, interest level (1-5), demo length given, key pain points mentioned, next step agreed.

Using the `calcom-booking-links` fundamental, prepare a shareable booking link. QR code version is ideal for in-person -- generate a QR code image pointing to your Cal.com link.

### 2. Event-day execution

**Positioning strategy:**
- Arrive 30 minutes before the first session starts. Stake out the coffee/registration area.
- During session breaks (the prime window): position yourself in the hallway between session rooms or near the coffee station.
- Lunch breaks: sit at communal tables, not alone. Start conversations about the sessions.
- After the last session: linger in the lobby. People decompress and are more open to conversation.

**Conversation framework:**
1. **Open with context, not pitch**: "What did you think of the [session name] talk?" or "Are you here for the [specific track]?" or "What's bringing you to [event name]?"
2. **Listen for pain signals**: Let them talk about their challenges. If they mention anything your product addresses, that is your opening.
3. **Bridge to demo**: "We actually built something that tackles that exact problem. Want to see a quick 60-second demo?" Show, don't tell.
4. **Close with next step**: If interest is high, book a meeting on the spot using Cal.com QR code. If interest is moderate, exchange LinkedIn connections and agree to a follow-up. If interest is low, thank them and move on.

**Logging in real time:**
After each conversation, immediately log it in your capture form or Attio mobile. Do not trust your memory for more than 2 conversations. Log: name, company, interest level, what you showed, what they said, and agreed next step.

### 3. Same-day enrichment (evening after event)

Within 4 hours of the event ending:

1. Using `attio-contacts`, create or update a contact record for every person you spoke with. Attach: conversation notes, interest level, demo given (yes/no), next step.
2. Using `attio-deals`, create a deal for anyone who agreed to a follow-up meeting or expressed strong interest (level 4-5). Set deal stage to "Meeting Requested" or "Demo Given."
3. Connect on LinkedIn with every person you spoke with. Send a connection request referencing the specific conversation: "Great chatting at [event] about [their challenge]. Let's continue the conversation."

### 4. Follow-up sequences (within 48 hours)

Using `loops-sequences`, trigger different follow-up paths based on interest level:

- **Level 5 (hot)**: Personal email within 12 hours. Reference the specific demo and pain point. Include Cal.com link. If they already booked, send confirmation with a brief recap of what you showed them.
- **Level 4 (warm)**: Personal email within 24 hours. Reference the conversation, share a relevant resource (case study, blog post, one-pager), and suggest a follow-up call.
- **Level 3 (interested)**: Email within 48 hours. Lighter touch -- "Great meeting you at [event]" with a link to your product and an open invitation to chat.
- **Level 1-2 (low)**: LinkedIn connection only. Add to long-term nurture list, no email follow-up.

### 5. Track event outcomes

Using `posthog-custom-events`, fire events for the full hallway demo funnel:

- `hallway_demo_conversation_started` (properties: event_name, city, date)
- `hallway_demo_given` (properties: event_name, demo_length, interest_level)
- `hallway_demo_meeting_booked` (properties: event_name, days_to_meeting)
- `hallway_demo_followup_sent` (properties: event_name, followup_type, interest_level)
- `hallway_demo_deal_created` (properties: event_name, deal_value_estimate)

If you used Fireflies to record any conversations (with permission), run `fireflies-action-items` to extract key discussion points and action items from the transcript.

## Output

- Attio records for every conversation with notes, interest level, and next steps
- Deals created for high-interest contacts
- Follow-up sequences triggered by interest tier
- PostHog event trail for the full hallway demo funnel
- LinkedIn connections sent to all contacts

## Triggers

- Run once per event attended
- Steps 3-4 must execute within 48 hours of the event (conversations go cold fast)
