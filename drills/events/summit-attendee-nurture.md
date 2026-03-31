---
name: summit-attendee-nurture
description: Post-summit multi-touch nurture workflow that segments attendees by engagement depth and routes high-intent leads to pipeline
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

# Summit Attendee Nurture

This drill builds the post-summit follow-up system that converts attendees into pipeline. A summit generates richer engagement data than a single webinar — session-level attendance, cross-session behavior, Q&A participation, and sponsor interactions — so the nurture must use all of it.

## Prerequisites

- Completed summit with registrant, attendee, and engagement data in Attio
- Loops account with sequences configured
- n8n instance for trigger-based automation
- PostHog tracking events from summit registration and sessions
- Session recordings processed and ready for sharing

## Steps

### 1. Segment registrants by engagement tier

Within 2 hours of summit close, classify every registrant into one of five tiers using `attio-lists`:

- **Tier 1 — Power attendee**: Attended 4+ sessions AND asked questions or clicked CTAs. Highest intent — these people invested hours.
- **Tier 2 — Engaged attendee**: Attended 2-3 sessions AND engaged (question, poll, or CTA click). Strong interest.
- **Tier 3 — Passive attendee**: Attended 1-2 sessions, no engagement beyond watching. Moderate interest.
- **Tier 4 — No-show**: Registered but did not attend any session. Expressed interest but did not follow through.
- **Tier 5 — Replay viewer**: Did not attend live but watches recordings after the event. Late-stage interest.

Using `attio-contacts`, tag each registrant with: summit slug, date, tier, sessions attended (list), questions asked (text), CTAs clicked (list), and company/role from registration.

### 2. Build tier-specific nurture sequences in Loops

Using `loops-sequences`, create five sequences:

**Tier 1 sequence (4 emails over 10 days):**
- Email 1 (within 4 hours): Personal thank-you referencing their specific session attendance. Include recordings for the sessions they attended. CTA: book a 20-minute call to discuss what they learned. If they asked a question, use `loom-recording` to record a 60-90 second video answering it personally.
- Email 2 (day 2): "Based on the sessions you attended, here's a deeper dive" — send the most relevant case study or resource. Reference the specific sessions: "Since you attended [Session X] on [topic], you might find this [resource] useful."
- Email 3 (day 5): Invite to an exclusive post-summit small-group debrief (roundtable or AMA with one of the speakers). Only Tier 1 attendees get this invitation.
- Email 4 (day 10): Direct meeting request. Reference summit engagement: "You spent [X hours] at our summit and asked about [topic]. I'd love to continue that conversation — here are 3 times this week." Include Cal.com link.

**Tier 2 sequence (3 emails over 10 days):**
- Email 1 (within 6 hours): Recording links for the sessions they attended + recordings of the sessions they missed that are most relevant to their role. Key takeaways summary. CTA: reply with which session was most valuable.
- Email 2 (day 4): Deeper resource linked to the session that had the most engagement from this cohort. CTA: book a call to explore how this applies to their company.
- Email 3 (day 10): Invite to the next event (webinar or smaller meetup) + soft CTA for a meeting.

**Tier 3 sequence (2 emails over 7 days):**
- Email 1 (within 8 hours): All session recordings + top 5 takeaways across the summit. CTA: reply with which topic is most relevant to them.
- Email 2 (day 7): Highlight the highest-rated session with a compelling excerpt. Invite to the next event. Soft CTA for a meeting.

**Tier 4 sequence (2 emails over 7 days):**
- Email 1 (within 2 hours of summit end): "Sorry we missed you" with all recordings and a highlight reel. "The most popular session was [X] — here's the recording." CTA: watch the recordings.
- Email 2 (day 5): Top takeaway + invite to the next live event. Frame as "join us live next time."

**Tier 5 sequence (2 emails triggered by replay behavior):**
- Email 1 (triggered when replay watch >50% of any session): "We noticed you're watching [Session Title] — here's the full set of recordings plus a resource on [topic]." CTA: reply with questions.
- Email 2 (7 days after first replay): Invite to the next live event. "Catch the next summit live."

### 3. Build automation triggers in n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create workflows that:

- **Auto-segment on summit close**: Pull the session-level attendee data from the event platform (Riverside API or Zoom API), cross-reference against the Attio registration list, calculate per-registrant engagement scores, and assign tiers.
- **Trigger sequences**: When a registrant is tagged with their tier, enroll them in the corresponding Loops sequence using `loops-audience`.
- **Escalate high-intent signals**: If a Tier 1 or Tier 2 contact replies to any nurture email or books a meeting, create a deal in Attio using `attio-deals` and notify the founder/sales lead via Slack. Include context: which sessions they attended, what questions they asked, and their company profile.
- **Track replay engagement**: When a no-show watches >50% of a session recording, reclassify them as Tier 5 and trigger the Tier 5 sequence. When a Tier 3 attendee watches additional session recordings, upgrade them to Tier 2 and trigger the Tier 2 sequence from email 2.
- **Sponsor lead routing**: If the summit had sponsors, route attendees who interacted with sponsor sessions or CTAs to the sponsor's designated contact in Attio with full engagement context.

### 4. Track nurture performance

Using `posthog-custom-events`, fire events at each step:

- `summit_nurture_email_sent` with properties: tier, sequence_step, summit_slug
- `summit_nurture_email_opened` with properties: tier, sequence_step, summit_slug
- `summit_nurture_reply_received` with properties: tier, summit_slug
- `summit_nurture_meeting_booked` with properties: tier, summit_slug, source_email_step
- `summit_recording_watched` with properties: tier, session_id, percent_watched, summit_slug

### 5. Measure nurture effectiveness

After each summit's nurture window closes (14 days), calculate:

- Reply rate by tier (target: Tier 1 >35%, Tier 2 >15%, Tier 3 >8%, Tier 4 >5%)
- Meetings booked by tier (target: Tier 1 >25%, Tier 2 >10%, Tier 3 >4%)
- Recording watch rate for no-shows (target: >30%)
- Sequence-to-pipeline conversion rate (target: >6% of all registrants enter pipeline)
- Revenue attributed to summit leads (90-day attribution window)

Compare these rates across summits to identify which themes, formats, and speaker lineups generate the most pipeline from follow-up.
