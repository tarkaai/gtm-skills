---
name: meeting-booking-flow
description: Set up a seamless meeting booking flow from Cal.com through CRM and follow-up automation
category: Operations
tools:
  - Cal.com
  - Attio
  - n8n
  - PostHog
fundamentals:
  - calcom-event-types
  - calcom-booking-links
  - calcom-crm-sync
  - attio-deals
  - n8n-triggers
  - posthog-custom-events
---

# Meeting Booking Flow

This drill creates the end-to-end flow from a prospect clicking your booking link to a CRM record being created, prep materials being sent, and the meeting being tracked in analytics.

## Prerequisites

- Cal.com account configured
- Attio CRM set up (run `crm-pipeline-setup` drill first)
- n8n instance running

## Steps

### 1. Configure event types

Use the `calcom-event-types` fundamental to create your meeting types: Discovery Call (30 min), Product Demo (45 min), Quick Chat (15 min). Set availability, buffers, and booking form questions.

### 2. Distribute booking links

Use the `calcom-booking-links` fundamental to add your links to: email signature, LinkedIn profile, website contact page, and cold email CTAs. Use UTM parameters for source tracking.

### 3. Connect Cal.com to CRM

Use the `calcom-crm-sync` fundamental to build an n8n workflow that creates or updates Attio records when meetings are booked. New contacts get a Person record, Company record, and Deal at "Meeting Booked" stage.

### 4. Track bookings in PostHog

Use the `posthog-custom-events` fundamental to capture `meeting_booked` events with properties: source, event_type, lead_email. This connects booking data to your GTM funnel.

### 5. Automate prep and follow-up

Build n8n workflows for: pre-meeting research brief (pull company data from Clay), reminder email 1 hour before, and post-meeting follow-up task creation in Attio.

### 6. Monitor the booking funnel

Track: booking page visits vs completed bookings (conversion rate), no-show rate, and meeting-to-opportunity conversion rate. Optimize the booking form and availability to improve conversion.
