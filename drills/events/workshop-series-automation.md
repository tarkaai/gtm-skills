---
name: workshop-series-automation
description: Automate recurring educational workshop operations including topic planning, registration, promotion, attendee prep, and cross-event analytics
category: Events
tools:
  - n8n
  - Loops
  - Attio
  - Clay
  - PostHog
  - Cal.com
  - Riverside
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-crm-integration
  - loops-broadcasts
  - loops-sequences
  - loops-audience
  - attio-lists
  - attio-contacts
  - attio-deals
  - clay-people-search
  - clay-enrichment-waterfall
  - posthog-custom-events
  - posthog-dashboards
  - calcom-event-types
  - calcom-booking-links
  - riverside-recording
---

# Workshop Series Automation

This drill transforms one-off workshops into an automated recurring series. It handles topic scheduling, prospect sourcing, multi-channel promotion, attendee preparation, and cross-event analytics -- reducing per-event effort from 6+ hours to under 2 hours of human time (content delivery only).

## Prerequisites

- At least 2 completed workshops with attendee and outcome data (Baseline proven)
- n8n instance for orchestration
- Loops account for email sequences
- Clay account for prospect sourcing
- Attio with workshop tracking lists
- PostHog with workshop event taxonomy configured

## Steps

### 1. Build the topic backlog and scheduling engine

Create a structured topic backlog in Attio using `attio-lists`:

- Score each topic on three dimensions: ICP pain alignment (1-5), competitive differentiation (1-5), and funnel position (awareness/consideration/decision).
- Queue at least 6 topics before launching the series.
- Assign each topic a difficulty level: beginner, intermediate, advanced. Alternate difficulty across sessions to serve different segments.
- Map each topic to required prerequisites, materials, and exercises. Estimate prep time per topic.

Build an n8n workflow using `n8n-scheduling` that:
- 28 days before each scheduled event: sends a topic confirmation notification and triggers materials preparation
- 21 days before: triggers the promotion engine (Step 3)
- 7 days before: sends a "materials ready" checklist to the facilitator
- 1 day before: sends a final prep reminder with attendee count, notable registrants, and technical check list

Target cadence: bi-weekly for the first month (2 events), then monthly. Evaluate cadence based on registration velocity and audience capacity.

### 2. Configure prospect sourcing per event

Using `clay-people-search` and `clay-enrichment-waterfall`, build a per-event prospecting flow:

- For each workshop topic, define topic-specific search criteria. Example: a workshop on "Building AI Agents" targets engineering managers at companies using Python + cloud infrastructure.
- Source 200-500 topic-relevant prospects per event from Clay.
- Enrich with verified email and current role.
- Deduplicate against existing Attio contacts using `attio-contacts`.
- Import net-new prospects into a topic-specific Loops segment using `loops-audience`.
- Tag all sourced contacts in Attio with workshop_slug and source = "clay_prospecting".

### 3. Launch the automated promotion engine

Build an n8n workflow triggered 21 days before each event that orchestrates multi-channel promotion:

**Email waves (via Loops using `loops-broadcasts`):**
- Day -14: Announcement email to the full relevant segment. Subject line emphasizes the specific skill they will build, not the event format.
- Day -7: Reminder email to non-registrants. Include social proof: "[N] people registered. Here's what one past attendee said."
- Day -3: Last-chance email with urgency. "Only [N] spots remaining" (cap workshops at 25-30 for hands-on quality).
- Day -1: Prep email to all registrants. Include prerequisites, setup instructions, and what to have ready.

**Clay-sourced prospect invites:**
- Day -14: Personalized invite via Loops to Clay-sourced prospects. Reference a specific pain point from their enrichment data.
- Day -5: Follow-up to non-registrants from the Clay batch.

**Attio pipeline re-engagement:**
- Using `attio-lists`, identify active pipeline prospects who match the workshop topic. A workshop invite is a low-friction re-engagement for stalled deals.
- Send via Loops as a separate, personalized segment.

**Promotion tracking:**
- Using `posthog-custom-events`, fire `workshop_invite_sent` with properties: channel, segment, workshop_slug.
- Track registrations by source to calculate cost per registration and conversion rate by channel.

### 4. Automate attendee preparation

Using `n8n-triggers`, build preparation workflows:

- On registration: send a confirmation email via Loops with the workshop date, topic overview, and a "what to prepare" checklist. If the workshop uses your product, include a link to create a free account or sandbox environment.
- Day -3: Send a prep check email. "Have you set up [prerequisite]? Reply if you need help."
- Day -1: Final reminder with join link, agenda, and a 3-minute video preview of what they will build.
- 15 minutes before: Send a "Starting soon" push. Include the direct join link and a note to have their laptop ready.

Using `calcom-event-types` and `calcom-booking-links`, create a dedicated registration type per workshop with custom fields: name, email, company, role, skill level (beginner/intermediate/advanced), and "What specific challenge are you hoping to solve?"

### 5. Build cross-event analytics

Using `posthog-dashboards`, create a "Workshop Series" dashboard:

- **Registrations by event**: Bar chart showing registration count per workshop, colored by source channel.
- **Show rate trend**: Line chart across all events.
- **Exercise completion rate**: Per-event, what percentage of attendees completed the hands-on component.
- **Pipeline generated**: Meetings booked and deals created attributed to each workshop.
- **Topic performance**: Which topic categories drive the most registrations and pipeline.
- **Repeat attendance rate**: Contacts who attended 2+ workshops.

Using `attio-reporting`, build a series-level view in Attio showing: total registrants, total pipeline generated, cost per qualified lead by workshop topic, and average deal velocity for workshop-sourced leads vs other sources.

### 6. Manage speaker and facilitator coordination

If workshops include guest facilitators or co-hosts, automate coordination with n8n:

- 21 days before: Send speaker confirmation with topic brief, audience profile, and format expectations.
- 14 days before: Schedule a 15-minute prep call (auto-create via `calcom-booking-links`).
- 3 days before: Send technical check reminder with platform details and backup plan.
- Day of: Send speaker a 30-minute heads-up with attendee count and notable registrant profiles.
- Day after: Send a thank-you email and share the recording link.

### 7. Output

The automation produces:
- A scheduled series with topics queued months in advance
- Per-event prospect sourcing that delivers 200-500 targeted invites
- Multi-channel promotion that launches and completes without manual intervention
- Attendee preparation that maximizes readiness and show rate
- Cross-event analytics showing which topics, formats, and channels drive the most pipeline
- Facilitator coordination that runs on autopilot
