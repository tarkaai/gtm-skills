---
name: trade-show-booth-operations
description: Prepare and execute trade show booth presence including pre-show target research, demo environment setup, booth staff coordination, real-time lead capture, and same-day CRM import
category: Events
tools:
  - Attio
  - Clay
  - Cal.com
  - PostHog
  - Fireflies
fundamentals:
  - badge-scan-lead-import
  - event-attendee-enrichment
  - clay-people-search
  - clay-enrichment-waterfall
  - attio-contacts
  - attio-deals
  - attio-lists
  - calcom-booking-links
  - posthog-custom-events
---

# Trade Show Booth Operations

This drill covers everything an agent and team do before, during, and after a trade show to turn a booth into a pipeline machine. It converts booth traffic from random badge scans into qualified, enriched, segmented leads routed into the right follow-up path.

## Input

- Event details: show name, dates, venue, booth number, expected attendee count
- ICP definition (from `icp-definition` drill): target industries, titles, company sizes
- Product demo environment loaded on booth devices
- Booth staff roster and their assigned roles

## Steps

### 1. Pre-show target research (2-4 weeks before)

Build a target list of high-value attendees to seek out proactively, not just wait for them to walk by:

- Use `event-attendee-enrichment` to extract the published attendee list, speaker roster, and exhibitor directory. Most trade shows publish these on their website or app (Bizzabo, Swapcard, Cvent, Grip).
- Run `clay-people-search` to find ICP-match contacts at companies on the attendee list. Filter for target titles and company sizes.
- Use `clay-enrichment-waterfall` to enrich each target: email, LinkedIn profile, company size, funding stage, tech stack, recent news.
- Score targets by ICP fit and prioritize the top 50 for proactive outreach. Push to an Attio list using `attio-lists` with fields: name, company, title, ICP score, booth visit priority, and a pre-show outreach status.

**Pre-show outreach:** For the top 25 targets, send a personal email or LinkedIn message 1-2 weeks before the show: "We're at booth #{booth_number} at {show_name}. I'd love to show you how we handle {their pain point}. Want me to save a 10-minute slot?" Track reply status in Attio.

### 2. Booth infrastructure preparation (1 week before)

Configure the lead capture and demo systems:

- **Demo environment**: Load product on 2+ devices (laptop + tablet). Prepare 3 demo paths:
  - 60-second elevator: problem → solution → proof point → CTA. For high-traffic moments.
  - 3-minute guided demo: targeted at a specific ICP pain point. The default for engaged visitors.
  - 10-minute deep dive: full product walkthrough for high-interest prospects who want details.
- **Lead capture form**: Create a mobile-friendly Tally form (webhook to n8n) or configure the conference lead retrieval app. Fields: name, email, company, title, interest level (1-5), demo given (yes/no), demo path (elevator/guided/deep), key pain points mentioned (multi-select), agreed next step (demo follow-up / trial / meeting / nurture / not interested), booth staff notes.
- **Meeting booking**: Use `calcom-booking-links` to create a booth-specific booking page. Generate a QR code that points to it. Print the QR code for the booth and have it saved on every booth staff member's phone.
- **Booth staff brief**: Create a one-page reference doc per staff member: ICP criteria (who to prioritize), conversation openers, demo flow for their assigned path, objection responses for top 3 objections, and the qualification criteria for each interest tier.

### 3. Show-day execution

**Traffic capture strategy:**

- Station one person at the booth entrance for initial qualification. Their job: greet, ask one qualifying question ("What brings you to {show_name}?"), and route to the right demo path or politely disengage non-ICP traffic.
- Station demo-givers inside the booth. They run the appropriate demo path based on the visitor's expressed pain point.
- One person (or rotating role) handles lead capture logging. After every conversation, they log the contact in the capture form before the next conversation starts.

**Proactive targeting:**

- Between booth traffic peaks, booth staff should walk the show floor targeting pre-identified high-value attendees. Use the target list from step 1 with LinkedIn profile photos for recognition.
- Visit competitor booths and adjacent-category exhibitors. Note their messaging, demo approach, and traffic volume. Log competitive intel in Attio notes.

**Real-time logging:**

- Every booth conversation gets logged in the capture form within 5 minutes of ending. Do not batch at end of day — context decays fast.
- For high-interest leads (level 4-5), take a photo of their badge (with permission) as backup for any data entry errors.
- Fire PostHog events via `posthog-custom-events` in real time (or batch at end of day if WiFi is unreliable):
  - `trade_show_booth_visit` (properties: show_name, visitor_company, visitor_title, interest_level)
  - `trade_show_demo_given` (properties: show_name, demo_path, duration_minutes, interest_level)
  - `trade_show_meeting_booked` (properties: show_name, booking_type, days_until_meeting)

### 4. Same-day lead import (each evening)

At the end of each show day, run the lead import process:

1. Export badge scan data from the conference platform (if available). Use `badge-scan-lead-import` to push into Attio.
2. Sync the Tally capture form submissions to Attio via n8n webhook.
3. Deduplicate: match by email, then by company+name. Merge badge scan data with manual capture form data (the capture form has richer qualification data; the badge scan has guaranteed email accuracy).
4. Using `attio-contacts`, create or update a contact record for every interaction. Tag with: show name, date, booth staff who spoke with them, interest level, demo path, and agreed next step.
5. For interest level 4-5, create Attio deals using `attio-deals`. Set stage to "Demo Given" or "Meeting Requested." Assign to the booth staff member who ran the demo.

### 5. End-of-show reconciliation

After the final show day:

- Cross-reference the full badge scan export against the manual capture forms. Flag any badge scans with no matching capture form entry (these are "drive-by" scans that need enrichment).
- Run `clay-enrichment-waterfall` on any contacts missing email or company data.
- Generate a show summary: total booth visits, demos given, meetings booked, interest level distribution, top companies visited, competitive intel collected.
- Push the summary metrics to PostHog: `trade_show_completed` with aggregate properties.

## Output

- Pre-show target list in Attio (top 50 ICP-match attendees)
- Booth staff briefing documents
- Cal.com booking QR code
- Real-time lead capture via Tally + badge scans
- All leads imported to Attio with enrichment, scoring, and next-step routing
- Show summary with aggregate metrics in PostHog
- Competitive intel notes in Attio

## Triggers

- Pre-show: run 2-4 weeks before each trade show
- During show: lead capture and logging runs continuously
- Post-show: same-day import runs each evening; reconciliation runs day after final show day
