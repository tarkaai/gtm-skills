---
name: workshop-attendee-nurture
description: Post-workshop multi-touch nurture that segments attendees by participation depth and routes high-intent leads to pipeline
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

# Workshop Attendee Nurture

This drill builds the post-workshop follow-up system that converts hands-on participants into pipeline. Workshops produce higher-intent leads than webinars because attendees invested time doing exercises, so the nurture sequences reflect that deeper engagement.

## Prerequisites

- Completed workshop with registrant, attendee, and exercise completion data
- Loops account with sequences configured
- Attio workspace with workshop-related lists
- n8n instance for trigger-based automation
- PostHog tracking events from the workshop registration and engagement

## Steps

### 1. Segment registrants by participation depth

Immediately after the workshop ends, classify every registrant into one of four tiers using `attio-lists`:

- **Tier 1 -- Active participant**: Attended AND completed at least one hands-on exercise. May have asked questions. These are the highest-intent leads because they practiced with your product or framework.
- **Tier 2 -- Observer**: Attended but did not complete exercises. Watched the teaching segments but did not engage hands-on. Still showed commitment by attending a longer-format event.
- **Tier 3 -- No-show**: Registered but did not attend. Interest in the skill but did not follow through.
- **Tier 4 -- Late registrant**: Registered after the event (from replay promotion). Interest in the topic but no live experience.

Using `attio-contacts`, tag each registrant with the workshop slug, date, their tier, and which exercises they completed (if any).

### 2. Build tier-specific nurture sequences in Loops

Using `loops-sequences`, create four sequences:

**Tier 1 sequence (4 emails over 10 days):**
- Email 1 (within 4 hours): Workshop materials (slides, workbook, cheat sheet) + recording link. Reference their exercise completion: "You built [specific output] during the session -- here are the files to keep working with it." CTA: book a 15-minute call to review their specific implementation.
- Email 2 (day 3): Advanced resource that extends what they practiced. Example: "You learned [skill X] -- here's how to apply it to [specific use case]." Include a Loom clip (recorded via `loom-recording`, 90 seconds) walking through the next step they would take with the product. CTA: reply with their biggest implementation question.
- Email 3 (day 6): Case study or success story from someone who applied the same skill. Connect it to the exercise they completed. CTA: "Want help applying this in your environment? Book a working session."
- Email 4 (day 10): Direct meeting request referencing their participation. "You invested an hour learning [skill]. Let's spend 15 minutes mapping how it applies to [their company]." Include Cal.com link with 3 time slots.

**Tier 2 sequence (3 emails over 10 days):**
- Email 1 (within 6 hours): Recording link + materials + 3 key takeaways summary. CTA: "Try the exercises on your own -- reply if you get stuck and I'll send a walkthrough."
- Email 2 (day 4): The hands-on exercise as a standalone resource with step-by-step instructions. Frame as: "You saw the demo -- now try it yourself in 15 minutes." CTA: reply with results or questions.
- Email 3 (day 10): Invite to the next workshop + soft CTA for a meeting. "The next session covers [related topic]. Register here, or if you want to skip ahead, book a 1-on-1."

**Tier 3 sequence (2 emails over 7 days):**
- Email 1 (within 2 hours): Recording link + materials with "Sorry we missed you" framing. Highlight: "Participants built [specific output] -- watch the recording and follow along to get the same result."
- Email 2 (day 5): Key takeaway + invite to the next live workshop. CTA: register for next session.

**Tier 4 sequence (2 emails over 5 days):**
- Email 1 (immediate upon registration): Recording link + materials. CTA: "Watch and follow along with the exercises -- reply with questions."
- Email 2 (day 5): Invite to the next live session. "The hands-on component is much more valuable live. Join us next time."

### 3. Build automation triggers in n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create workflows that:

- **Auto-segment on workshop end**: Pull the attendee list from the workshop platform (Zoom participant report CSV, Riverside API, or manual export), cross-reference with exercise completion data (poll results, form submissions, or product usage logs), match against registration list, and assign tiers in Attio.
- **Trigger sequences**: When a registrant is tagged with their tier, enroll them in the corresponding Loops sequence using `loops-audience`.
- **Escalate high-intent signals**: If a Tier 1 or Tier 2 contact replies to any nurture email, create a deal in Attio using `attio-deals` and notify the founder or sales lead via Slack.
- **Track replay engagement**: When a no-show watches >75% of the recording AND downloads the exercise materials, upgrade their tier to Tier 2 and trigger the Tier 2 sequence.
- **Track exercise completion post-event**: If a Tier 2 or Tier 3 contact completes the exercises after the event (tracked via product usage), auto-send a congratulatory email and offer a review call.

### 4. Track nurture performance

Using `posthog-custom-events`, fire events at each step:

- `workshop_nurture_email_sent` with properties: tier, sequence_step, workshop_slug
- `workshop_nurture_email_opened` with properties: tier, sequence_step, workshop_slug
- `workshop_nurture_reply_received` with properties: tier, workshop_slug
- `workshop_nurture_meeting_booked` with properties: tier, workshop_slug, source_email_step
- `workshop_recording_watched` with properties: tier, percent_watched, workshop_slug
- `workshop_exercise_completed_post_event` with properties: tier, exercise_id, workshop_slug

### 5. Measure nurture effectiveness

After each workshop's nurture window closes (14 days), calculate:

- Reply rate by tier (target: Tier 1 >35%, Tier 2 >15%, Tier 3 >5%)
- Meetings booked by tier (target: Tier 1 >25%, Tier 2 >10%, Tier 3 >3%)
- Recording watch rate for no-shows (target: >35%)
- Post-event exercise completion rate for Tier 2-4 (target: >15%)
- Sequence-to-pipeline conversion rate (target: >8% of all registrants enter pipeline)

Compare these rates across workshops to identify which topics, exercise formats, and skill levels generate the most pipeline from follow-up. Workshop nurture should outperform webinar nurture by 40-60% on meeting conversion due to the hands-on investment.
