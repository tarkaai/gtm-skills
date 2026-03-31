---
name: webinar-series-automation
description: Automate recurring webinar series operations including topic selection, promotion, registration, and cross-event analytics
category: Events
tools:
  - n8n
  - Loops
  - Attio
  - PostHog
  - Cal.com
  - Riverside
  - Clay
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - loops-broadcasts
  - loops-audience
  - attio-lists
  - attio-contacts
  - attio-automation
  - posthog-custom-events
  - posthog-funnels
  - calcom-event-types
  - riverside-recording
  - clay-people-search
  - clay-enrichment-waterfall
  - linkedin-organic-posting
---

# Webinar Series Automation

This drill transforms one-off webinars into a repeatable, automated series that runs bi-weekly or monthly with minimal manual effort. The agent handles topic scheduling, promotion, registration ops, and cross-event analytics. The human delivers the content.

## Prerequisites

- At least 2 completed webinars with performance data (from Baseline level)
- n8n instance with active connections to Loops, Attio, and PostHog
- Riverside account for recording and production
- A content calendar or topic backlog with at least 6 webinar topics
- Clay table with ICP-matched prospects for targeted invites

## Steps

### 1. Build the series content calendar

Create a topic backlog ranked by expected registration pull. Score each topic on three factors:

- **ICP pain alignment (1-5)**: How directly does this topic address a top-3 pain point for your ICP?
- **Competitive differentiation (1-5)**: Can you say something others cannot? Do you have unique data or experience?
- **Funnel position (1-3)**: 1 = broad awareness, 2 = solution consideration, 3 = product evaluation. Mix across the series.

Using `attio-lists`, create an "Event Calendar" list with fields: topic, date, speaker(s), target audience segment, promotion start date, and status. Schedule events bi-weekly for the next 3 months.

### 2. Automate the promotion engine

Using `n8n-scheduling`, create a workflow that triggers 21 days before each event:

**Day -21: Promotion kickoff**
- Generate the registration page (landing page with form connected to Attio via `attio-contacts`)
- Using `calcom-event-types`, create the event booking for speaker prep calls
- Draft 3 LinkedIn posts (announcement, speaker spotlight, countdown) using topic and speaker info
- Queue email invitations in Loops using `loops-broadcasts`

**Day -14: First email wave**
- Send targeted invitations to the most relevant Attio segment using `loops-audience`
- Using `clay-people-search` and `clay-enrichment-waterfall`, find and enrich new prospects who match the topic's ICP segment and add them to the invite list
- Post the first LinkedIn announcement using `linkedin-organic-posting`

**Day -7: Second wave + reminders**
- Send a second email to non-openers from wave 1
- Post the speaker spotlight on LinkedIn
- Send personal invites from Attio to high-value prospects in active pipeline

**Day -1: Final push**
- Send "tomorrow" reminder to all registrants
- Post the countdown on LinkedIn
- Send calendar reminders

**Day 0: Event day**
- Send 1-hour reminder with join link
- Configure Riverside recording using `riverside-recording`
- Prepare the post-event nurture (hand off to `webinar-attendee-nurture` drill)

**Day +1: Post-event**
- Trigger the `webinar-attendee-nurture` drill with attendee data
- Export the recording from Riverside
- Update the event status in Attio

### 3. Build cross-event analytics

Using `posthog-custom-events` and `posthog-funnels`, track metrics across the entire series:

- **Registration funnel per event**: page_viewed → registered → reminded → attended → engaged → meeting_booked
- **Series-level metrics**: Repeat attendance rate (what % attend 2+ events), topic-to-pipeline correlation, promotion channel effectiveness per event
- **Cumulative pipeline**: Total meetings booked across all events, average meetings per event, trend over time

Create a PostHog dashboard for the series showing: registrations by event (bar chart), show rate trend (line chart), meetings booked per event (bar chart), promotion channel breakdown (pie chart), and repeat attendee count (counter).

### 4. Automate speaker and guest coordination

Using `n8n-workflow-basics`, build a workflow for events with guest speakers:

- Send a speaker prep email 14 days before with: event logistics, audience profile, suggested talking points, and a Cal.com link to schedule a 30-minute prep call
- Send a technical check reminder 3 days before with: Riverside test link, audio/video requirements, backup plan for technical issues
- After the event, send a thank-you email with: recording link, audience engagement stats, and an offer to collaborate again

### 5. Scale registration through targeted prospecting

For each upcoming webinar, use Clay to find net-new prospects who match the topic:

- Using `clay-people-search`, search for people with titles and companies matching the ICP who are active in the topic area (recent LinkedIn posts, conference talks, job changes into relevant roles)
- Using `clay-enrichment-waterfall`, enrich found contacts with email and company data
- Import enriched contacts into Attio using `attio-contacts` with a "Webinar Prospect" tag
- Add them to the targeted invite list in Loops using `loops-audience`

Target: 200-500 net-new, topic-relevant prospects per event to supplement your existing list.

### 6. Implement series-level optimizations

After every 4 events, the agent should analyze:

- Which topics drove the most registrations? Most pipeline?
- Which promotion channels (email, LinkedIn, personal invites) had the highest conversion?
- What day of week and time slot produced the best show rate?
- Which speaker format (solo, panel, interview, workshop) converted best?

Store findings in Attio as notes on the event calendar. Adjust the upcoming schedule based on data: double down on high-performing topic areas, drop formats that underperform, shift to the best-performing time slot.
