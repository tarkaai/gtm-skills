---
name: roundtable-attendee-nurture
description: Post-roundtable follow-up workflow that segments attendees by discussion engagement and converts high-intent participants to meetings
category: Events
tools:
  - Loops
  - Attio
  - n8n
  - PostHog
  - Cal.com
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
---

# Roundtable Attendee Nurture

This drill builds the post-roundtable follow-up system. Roundtable follow-up is fundamentally different from webinar follow-up: attendees had a real conversation, shared their opinions, and heard from peers. The follow-up must reference specific discussion points, not generic content. The personal nature of the event demands personal follow-up.

## Prerequisites

- Completed roundtable with Fireflies transcript and attendee engagement data logged in Attio (from `roundtable-pipeline` drill)
- Discussion summary generated
- Loops account with sequences configured
- Attio workspace with roundtable attendee data
- Cal.com booking links for follow-up meetings

## Steps

### 1. Segment attendees by engagement and intent

Using `attio-lists`, classify every confirmed invitee into one of three tiers based on data from the `roundtable-pipeline` drill:

- **Tier 1 — High engagement**: Spoke multiple times, expressed a pain point related to your product domain, or directly asked about solutions. These are warm leads.
- **Tier 2 — Medium engagement**: Attended and contributed to the discussion but did not express direct pain or solution interest. These are relationship-building contacts.
- **Tier 3 — No-show**: Confirmed but did not attend. They expressed interest in the topic but did not follow through.

Using `attio-contacts`, update each contact's tier tag and engagement notes.

### 2. Build tier-specific follow-up sequences

Using `loops-sequences`, create three sequences. Each email must reference the specific roundtable discussion — generic follow-up wastes the intimacy you built.

**Tier 1 sequence (3 emails over 7 days):**

- Email 1 (within 4 hours of event): Subject: "Great discussing [topic] today." Body: reference a specific point they made during the discussion. Attach the discussion summary. CTA: "I'd love to continue this conversation 1:1 — here are a few times: [Cal.com link]" generated via `calcom-booking-links`.
- Email 2 (day 3): Share a resource directly relevant to the pain point they expressed. This should NOT be your product — it should be a genuinely useful article, framework, or data point. Add a one-line note: "This reminded me of what you said about [specific thing]."
- Email 3 (day 7): Direct meeting request. Reference the roundtable and their specific situation. Frame it as: "Based on what you shared about [pain], I think there's something specific I can show you that addresses this. 20 minutes — [Cal.com link]."

**Tier 2 sequence (2 emails over 10 days):**

- Email 1 (within 6 hours): Subject: "Discussion notes from [topic] roundtable." Body: share the discussion summary. Highlight 2-3 insights that were particularly interesting. CTA: "Reply with which point resonated most — I'm curious what you think."
- Email 2 (day 10): Invite to the next roundtable if one is planned. Frame as: "We're doing another session on [next topic] — thought you'd find this one relevant too." Include the registration link.

**Tier 3 sequence (2 emails over 5 days):**

- Email 1 (within 2 hours of event): Subject: "Missed you at the [topic] roundtable." Body: share 3 key takeaways from the discussion (not the full summary — create FOMO). CTA: "We're planning the next one on [tentative topic/date]. Want me to save you a spot?"
- Email 2 (day 5): Share the full discussion summary. CTA: "We'd love to have you at the next one. Reply 'in' and I'll make sure you get a spot."

### 3. Build automation triggers in n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create workflows that:

- **Auto-enroll on event close**: When the host marks the roundtable complete in Attio, pull attendee tiers and enroll each person in the appropriate Loops sequence.
- **Escalate meeting signals**: When a Tier 1 contact replies to any email or books via Cal.com, create a deal in Attio using `attio-deals` with source "micro-roundtable" and notify the host via Slack or email.
- **Track no-show re-engagement**: When a Tier 3 contact opens Email 1 or replies to either email, flag them in Attio for priority invite to the next roundtable.

### 4. Track nurture performance

Using `posthog-custom-events`, fire events at each step:

- `roundtable_nurture_sent` with properties: tier, sequence_step, roundtable_slug
- `roundtable_nurture_opened` with properties: tier, sequence_step, roundtable_slug
- `roundtable_nurture_replied` with properties: tier, roundtable_slug
- `roundtable_nurture_meeting_booked` with properties: tier, roundtable_slug, source_email_step

### 5. Measure nurture effectiveness

After each roundtable's nurture window closes (14 days), calculate:

- Reply rate by tier (target: Tier 1 >40%, Tier 2 >15%, Tier 3 >8%)
- Meetings booked from Tier 1 (target: >30% of Tier 1 attendees book a meeting)
- Discussion summary open rate (target: >60%)
- No-show recovery rate: Tier 3 contacts who engage with follow-up (target: >25%)
- Next-event pre-registration rate: contacts who express interest in the next roundtable (target: >40%)

Compare across roundtables to identify which topics and attendee mixes produce the highest follow-up conversion.
