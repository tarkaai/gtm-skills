---
name: field-event-attendee-nurture
description: Post-field-event follow-up workflow that segments attendees by engagement signals and converts high-intent participants to pipeline
category: Events
tools:
  - Loops
  - Attio
  - n8n
  - PostHog
  - Cal.com
  - Loom
fundamentals:
  - loops-sequences
  - loops-broadcasts
  - attio-contacts
  - attio-lists
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
  - calcom-booking-links
  - loom-personalized-outreach
---

# Field Event Attendee Nurture

This drill converts in-person field event attendees into pipeline through structured, personalized follow-up. In-person events create stronger relationship signals than digital events, but the window to convert that warmth into action is short — 48 hours max before the conversation fades.

## Input

- Completed field event with attendance logged in Attio (from `field-event-ops` drill)
- Host's notes on conversations: who expressed interest, who asked about the product, who had relevant pain points
- Event type (dinner, happy hour, lunch) — determines follow-up tone and pace

## Steps

### 1. Segment attendees by engagement tier

Within 12 hours of the event, classify every attendee into tiers based on host notes and observable signals:

**Tier 1 — High intent (expressed product interest or clear pain match):**
- Explicitly asked about the product or pricing
- Described a pain point your product solves
- Asked to see a demo or learn more
- Host flagged as "follow up urgently"

**Tier 2 — Warm (engaged in discussion, good fit, no explicit product interest):**
- Active participant in group conversation
- Asked thoughtful questions about the topic
- Matches ICP but did not express specific product interest
- Exchanged contact info with the host

**Tier 3 — Attended (showed up, minimal engagement signal):**
- Attended but did not actively engage in notable conversations
- Arrived late or left early
- Polite but noncommittal

**Tier 4 — No-show (confirmed but did not attend):**
- RSVP confirmed, did not show, did not cancel

Update the Attio event list with tier tags using `attio-lists`. Log the segmentation rationale in `attio-notes` for each Tier 1 and Tier 2 contact.

### 2. Execute Tier 1 follow-up (within 24 hours)

For Tier 1 contacts, send a highly personal follow-up. These are warm leads — treat them accordingly.

Using `loops-sequences`, send a 1:1 email from the host:
- Reference the specific conversation you had ("Great talking about [specific topic] last night")
- Acknowledge their pain point or question ("You mentioned you were looking at [X]")
- Offer a concrete next step: "I'd love to continue that conversation — here's a 15-minute slot this week" with a `calcom-booking-links` link
- Keep it to 4-5 sentences. No marketing language. It should read like a personal email.

Optionally, record a 60-second Loom clip using `loom-personalized-outreach` that references the conversation and walks through one relevant product feature. Embed it in the email. Loom clips in follow-up emails after in-person events convert at 2-3x the rate of text-only emails because they extend the personal connection.

If no reply within 48 hours, send a single LinkedIn message reinforcing the same offer.

Create an Attio deal for each Tier 1 contact using `attio-deals`. Set the deal source to `field-event-{event-slug}`.

Fire `field_event_nurture_sent` PostHog event (properties: event_slug, tier, channel, has_loom).

### 3. Execute Tier 2 follow-up (within 48 hours)

For Tier 2 contacts, maintain the relationship and create a reason to continue the conversation.

Using `loops-sequences`, send a 2-email nurture:

**Email 1 (T+1 day):** Thank-you + value add. "Thanks for joining us at [event] — great discussion on [topic]. I thought you might find this [resource/article/data point] relevant given your work at [company]." Include a soft CTA: "If you'd ever like to dig deeper into [topic], happy to chat" with Cal.com link.

**Email 2 (T+7 days):** Invite to next event or offer. "We're planning our next gathering in [city] — I'll make sure you're on the list. In the meantime, [relevant offer: whitepaper, case study, product trial, newsletter]."

Track opens and clicks. If a Tier 2 contact clicks the Cal.com link or replies, auto-promote them to Tier 1 treatment: create an Attio deal and notify via n8n Slack alert.

### 4. Execute Tier 3 follow-up (within 72 hours)

Using `loops-broadcasts`, send a single group email to all Tier 3 attendees:
- Thank them for attending
- Share 2-3 key takeaways from the discussion
- Include a link to any follow-up resources
- Mention the next event if one is planned
- Soft CTA to join your newsletter or community

No individual follow-up unless they reply.

### 5. Handle no-shows (Tier 4)

Using `loops-broadcasts`, send a "Sorry we missed you" email within 48 hours:
- Brief recap of what was discussed
- Mention it was a great group and you hope they can make the next one
- Offer to connect 1:1 if they're interested in the topic
- Include the next event date if known

No-shows who RSVP'd for a dinner (where a seat was reserved and food was ordered) get one follow-up only. Do not add them to a nurture sequence — they already broke a commitment.

### 6. Log all nurture activity

Using `posthog-custom-events`, track the complete nurture funnel:
- `field_event_nurture_sent` (properties: event_slug, tier, sequence_step, channel)
- `field_event_nurture_opened` (properties: event_slug, tier)
- `field_event_nurture_clicked` (properties: event_slug, tier, cta_type)
- `field_event_nurture_replied` (properties: event_slug, tier)
- `field_event_meeting_booked` (properties: event_slug, tier, days_to_booking)
- `field_event_deal_created` (properties: event_slug, tier, deal_value)

Build an n8n workflow using `n8n-triggers` that monitors for replies and Cal.com bookings, auto-creates Attio deals, and sends Slack notifications for any Tier 1 or promoted Tier 2 activity.

## Output

- All attendees segmented and receiving tier-appropriate follow-up
- Tier 1 contacts have Attio deals created and personal outreach sent
- Tier 2 contacts in a 2-email nurture with promotion triggers
- Tier 3 and 4 handled with appropriate lightweight follow-up
- Full nurture funnel tracked in PostHog
- n8n automation monitoring for replies and bookings

## Triggers

- Start within 12 hours of event completion
- Tier 1 follow-up: T+24 hours
- Tier 2 follow-up: T+24 hours (email 1), T+7 days (email 2)
- Tier 3 follow-up: T+48 hours
- Tier 4 follow-up: T+48 hours
- Run once per event
