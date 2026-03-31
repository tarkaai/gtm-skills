---
name: webinar-attendee-nurture
description: Post-webinar multi-touch nurture workflow that segments attendees by engagement and routes high-intent leads to pipeline
category: Events
tools:
  - Loops
  - Attio
  - n8n
  - PostHog
  - Loom
fundamentals:
  - loops-sequences
  - loops-audience
  - attio-contacts
  - attio-lists
  - attio-deals
  - n8n-workflow-basics
  - n8n-triggers
  - posthog-custom-events
  - loom-recording
---

# Webinar Attendee Nurture

This drill builds the post-webinar follow-up system that converts attendees into pipeline. It segments registrants by engagement level and runs differentiated nurture sequences for each segment.

## Prerequisites

- Completed webinar with registrant and attendee data
- Loops account with sequences configured
- Attio workspace with webinar-related lists
- n8n instance for trigger-based automation
- PostHog tracking events from the webinar registration page

## Steps

### 1. Segment registrants by engagement tier

Immediately after the webinar ends, classify every registrant into one of four tiers using `attio-lists`:

- **Tier 1 — Active attendee**: Attended AND asked a question or responded to a poll. These are the highest-intent leads.
- **Tier 2 — Passive attendee**: Attended but did not engage beyond watching. Still showed commitment by showing up.
- **Tier 3 — No-show**: Registered but did not attend. They expressed interest but did not follow through.
- **Tier 4 — Late registrant**: Registered after the event (from replay promotion). Interest in the topic but no live engagement.

Using `attio-contacts`, tag each registrant with the webinar slug, date, and their tier. Add company and role data from the registration form.

### 2. Build tier-specific nurture sequences in Loops

Using `loops-sequences`, create four sequences:

**Tier 1 sequence (3 emails over 7 days):**
- Email 1 (within 4 hours): Recording link + personalized note referencing their question. CTA: book a 15-minute call to continue the discussion. Use `loom-recording` to record a 60-second clip answering their specific question if they asked something substantive.
- Email 2 (day 3): Related resource (blog post, case study, template) that extends the webinar topic. CTA: reply with their biggest challenge related to the topic.
- Email 3 (day 7): Direct meeting request. Reference the webinar and their engagement. Include 3 specific time slots via Cal.com link.

**Tier 2 sequence (3 emails over 10 days):**
- Email 1 (within 6 hours): Recording link + key takeaways summary (3-5 bullet points). CTA: reply with which takeaway resonated most.
- Email 2 (day 4): Deeper resource on the highest-rated topic from the webinar. CTA: book a call if they want to explore how this applies to their company.
- Email 3 (day 10): Invite to the next webinar + soft CTA for a meeting.

**Tier 3 sequence (2 emails over 7 days):**
- Email 1 (within 2 hours): Recording link with "Sorry we missed you" framing. Highlight the single most valuable insight from the session. CTA: watch the recording.
- Email 2 (day 5): Key takeaway + invite to the next live session. CTA: register for the next event.

**Tier 4 sequence (2 emails over 5 days):**
- Email 1 (immediate upon registration): Recording link + agenda summary. CTA: watch the recording and reply with questions.
- Email 2 (day 5): Invite to the next live session. Frame as "join us live next time."

### 3. Build automation triggers in n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create workflows that:

- **Auto-segment on webinar end**: Pull the attendee list from the webinar platform (Riverside API, Zoom API, or CSV import), match against registration list, and assign tiers in Attio.
- **Trigger sequences**: When a registrant is tagged with their tier, enroll them in the corresponding Loops sequence using `loops-audience`.
- **Escalate high-intent signals**: If a Tier 1 or Tier 2 contact replies to any nurture email, create a deal in Attio using `attio-deals` and notify the founder or sales lead via Slack.
- **Track replay engagement**: When a no-show or late registrant watches >75% of the recording, upgrade their tier and trigger the next email immediately instead of waiting.

### 4. Track nurture performance

Using `posthog-custom-events`, fire events at each step:

- `webinar_nurture_email_sent` with properties: tier, sequence_step, webinar_slug
- `webinar_nurture_email_opened` with properties: tier, sequence_step, webinar_slug
- `webinar_nurture_reply_received` with properties: tier, webinar_slug
- `webinar_nurture_meeting_booked` with properties: tier, webinar_slug, source_email_step
- `webinar_recording_watched` with properties: tier, percent_watched, webinar_slug

### 5. Measure nurture effectiveness

After each webinar's nurture window closes (14 days), calculate:

- Reply rate by tier (target: Tier 1 >30%, Tier 2 >15%, Tier 3 >5%)
- Meetings booked by tier (target: Tier 1 >20%, Tier 2 >8%, Tier 3 >2%)
- Recording watch rate for no-shows (target: >40%)
- Sequence-to-pipeline conversion rate (target: >5% of all registrants enter pipeline)

Compare these rates across webinars to identify which topics and formats generate the most pipeline from follow-up.
