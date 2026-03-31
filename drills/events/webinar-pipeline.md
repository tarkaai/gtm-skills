---
name: webinar-pipeline
description: Plan, promote, execute, and follow up on webinars that generate qualified pipeline
category: Events
tools:
  - Cal.com
  - Loops
  - PostHog
  - Attio
  - Intercom
fundamentals:
  - calcom-event-types
  - loops-broadcasts
  - posthog-custom-events
  - attio-lists
  - intercom-in-app-messages
---

# Webinar Pipeline

This drill covers the complete webinar lifecycle: topic selection, promotion, execution, and post-webinar follow-up that converts attendees into pipeline.

## Prerequisites

- Webinar platform (Zoom, Riverside, or similar) configured
- Loops audience with enough subscribers to drive registrations
- Attio workspace for tracking webinar leads
- Landing page builder for the registration page

## Steps

### 1. Choose the topic and format

Pick a topic that sits at the intersection of your expertise and your ICP's pain points. The topic should be specific enough that only your target audience cares about it. Formats that work:

- **Expert panel (45 min)**: You moderate, 2-3 guests discuss. Lower prep, higher credibility.
- **Workshop (60 min)**: Live walkthrough of a process. High engagement, strong lead quality.
- **Product demo + Q&A (30 min)**: Best for bottom-of-funnel prospects already considering you.
- **Fireside chat (30 min)**: Conversation with a customer or industry figure. Good for brand building.

Set the date 3-4 weeks out to allow enough promotion time.

### 2. Build the registration funnel

Create a landing page with: a compelling headline (benefit-focused, not topic-focused), 3 bullet points on what attendees will learn, speaker bios, date/time with timezone, and a simple registration form (name, email, company, role). Use the `calcom-event-types` fundamental if using Cal.com for scheduling. Track registration events in PostHog using `posthog-custom-events`.

### 3. Promote across channels

Using `loops-broadcasts`, send a registration email to your subscriber list. Segment by relevance — do not send a technical webinar invite to your entire list. Promote on LinkedIn using your social content pipeline. Send personal invites via Attio to prospects in active deals — a webinar is a low-friction way to advance a stagnant deal. Promote to existing customers via Intercom using `intercom-in-app-messages` if the topic is relevant.

Send reminders: 1 week before, 1 day before, and 1 hour before. Each reminder should re-sell the value, not just remind.

### 4. Execute the webinar

Start on time. Open with a hook, not housekeeping. Share the agenda in 30 seconds. Encourage chat participation early with a poll or question. Leave 25% of the time for Q&A — this is where the best engagement happens. End with a clear CTA: book a demo, try the product, download a resource.

### 5. Post-webinar follow-up

Within 24 hours, send two different emails using `loops-broadcasts`:

- **Attendees**: Recording link, key takeaways summary, CTA to book a meeting or try the product.
- **Registered but did not attend**: Recording link with "Sorry we missed you" framing and the same CTA.

Using `attio-lists`, tag all registrants with the webinar name and segment by: attended, did not attend, asked a question (highest intent), clicked CTA.

### 6. Measure and optimize

Track the full funnel: page views, registrations, attendance rate (target 40-50%), engagement during webinar, post-webinar CTA clicks, and meetings booked. Calculate cost per lead and compare to other channels. Use `posthog-custom-events` to track which webinar attendees eventually convert to customers. Iterate topic selection based on which webinars produce the most pipeline.
