---
name: workshop-pipeline
description: Design and deliver hands-on workshops that educate prospects and demonstrate product value
category: Events
tools:
  - Cal.com
  - Loops
  - PostHog
  - Attio
  - Intercom
fundamentals:
  - calcom-event-setup
  - loops-broadcast-setup
  - posthog-event-tracking
  - attio-list-management
  - intercom-in-app-messages
---

# Workshop Pipeline

This drill builds a structured workshop program that teaches prospects a skill related to your product's domain. Workshops position you as the expert, let prospects experience your product hands-on, and produce the highest-quality leads of any event format.

## Prerequisites

- Expertise in a topic your ICP needs to learn
- Product or sandbox environment attendees can use during the session
- Platform for hosting (Zoom for virtual, venue for in-person)
- Materials prepared: slides, workbook, or exercises

## Steps

### 1. Design the workshop curriculum

Build a 60-90 minute workshop around a specific outcome the attendee will achieve. Structure:

- **Introduction (10 min)**: Context on why this skill matters. Hook with a stat or problem statement.
- **Teaching block 1 (15 min)**: Core concept explanation with examples.
- **Hands-on exercise 1 (15 min)**: Attendees practice the concept, ideally using your product.
- **Teaching block 2 (15 min)**: Advanced technique or second concept.
- **Hands-on exercise 2 (15 min)**: More complex application.
- **Wrap-up and Q&A (10 min)**: Key takeaways, resources, and next steps.

The workshop should be genuinely useful even if someone never buys your product. Generosity builds trust.

### 2. Build registration and prep

Using `calcom-event-setup`, create a registration page with prerequisites (what attendees should prepare or install before the session). Using `loops-broadcast-setup`, send a confirmation email with prep instructions immediately after registration and a reminder email the day before with final setup steps.

Cap attendance at 20-30 people. Larger groups make hands-on exercises impossible to facilitate. Track registrations in PostHog using `posthog-event-tracking`.

### 3. Promote strategically

Use the same promotion channels as the `webinar-pipeline` drill, but emphasize the hands-on, practical nature. Workshop-specific messaging: "You will leave with [specific deliverable]." Target mid-funnel prospects in Attio using `attio-list-management` — workshops work well for prospects evaluating solutions. Offer existing customers spots too, via `intercom-in-app-messages`, as a retention and upsell play.

### 4. Deliver the workshop

Be over-prepared. Have a co-facilitator to handle chat questions and technical issues while you teach. Walk through exercises step by step. Pause and check in: "How is everyone doing? Anyone stuck?" Share your screen for exercises so attendees can follow along. Record the session for those who could not attend and for future content repurposing.

### 5. Post-workshop engagement

Within 24 hours, send via `loops-broadcast-setup`:

- Recording and slides
- A cheat sheet or one-page reference summarizing key takeaways
- Links to relevant product features or documentation
- CTA: "Want help applying this to your specific situation? Book a 1-on-1 session."

For attendees who were particularly engaged (asked questions, completed exercises), send a personal follow-up.

### 6. Measure workshop ROI

Track the full funnel: registrations, attendance, engagement (exercise completion, questions asked), post-workshop CTA conversion, and pipeline generated. Workshops typically convert at 15-25% to meetings or trials, significantly higher than webinars. Using `attio-list-management`, tag workshop attendees and track their progression through your sales pipeline over 90 days.
