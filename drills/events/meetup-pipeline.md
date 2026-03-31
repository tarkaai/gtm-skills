---
name: meetup-pipeline
description: Organize local or virtual meetups that build community and generate warm leads
category: Events
tools:
  - Cal.com
  - Attio
  - Loops
  - PostHog
fundamentals:
  - calcom-event-setup
  - attio-list-management
  - loops-broadcast-setup
  - posthog-event-tracking
---

# Meetup Pipeline

This drill builds a repeatable process for organizing meetups — small, focused gatherings that create personal connections with your target audience. Meetups work because they build trust faster than any digital channel.

## Prerequisites

- Local community or audience in your target market
- Venue access (co-working space, office, restaurant, or virtual platform)
- Attio for tracking contacts
- Budget for food/drinks (even $200 makes a difference)

## Steps

### 1. Define the meetup format

Choose a format that matches your goals and audience:

- **Roundtable discussion (10-20 people)**: Pick a hot topic in your industry. Facilitate a discussion. Best for relationship building with senior people.
- **Demo night (20-50 people)**: 3-4 short demos from community members or partners. Good for product awareness.
- **Workshop (10-30 people)**: Hands-on session teaching a skill related to your product domain. Strong lead quality.
- **Casual mixer (15-40 people)**: Networking over drinks. Low effort, good for maintaining community.

Start with monthly frequency. Consistency matters more than scale.

### 2. Plan logistics

Book the venue 3-4 weeks in advance. For in-person: consider location accessibility, capacity, AV equipment, and food/drinks. For virtual: pick a platform that supports breakout rooms or networking features. Using the `calcom-event-setup` fundamental, create an event page with RSVP tracking.

### 3. Promote to the right people

Using `loops-broadcast-setup`, invite your email list filtered by location and interest. Post to relevant LinkedIn groups and local communities. Send personal invitations from Attio using `attio-list-management` to target prospects — a meetup invite feels warmer than a sales email. Cap attendance to keep it intimate. Better to have 15 engaged people than 50 disengaged ones.

### 4. Execute the event

Arrive early to set up and greet people individually. Start with a brief welcome (under 2 minutes). If it is a discussion format, prepare 5-7 questions to keep conversation flowing. Introduce attendees to each other based on shared interests. Collect business cards or LinkedIn connections during the event, not after. End on time with a clear mention of the next event.

### 5. Follow up within 48 hours

Using `loops-broadcast-setup`, send a thank-you email to all attendees with: a recap of key discussion points, photos if available, a link to the next event, and a soft CTA (try the product, book a chat, join the community). For high-value contacts, send a personal LinkedIn message or email referencing a specific conversation you had.

### 6. Track community growth

Using `posthog-event-tracking`, track the meetup funnel: invites sent, RSVPs, attendance, follow-up engagement, and eventual conversions. Using `attio-list-management`, tag attendees by event and track their journey through your pipeline. Measure how many meetup attendees become customers within 90 days. The community effect compounds — each event should bring back returning members and attract new ones.
