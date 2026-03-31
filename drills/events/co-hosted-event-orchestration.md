---
name: co-hosted-event-orchestration
description: Coordinate a co-hosted event with a partner from planning through execution — shared agenda, co-promotion, joint registration, and attendee handoff
category: Events
tools:
  - Luma
  - Attio
  - Loops
  - Clay
  - Cal.com
  - PostHog
fundamentals:
  - event-platform-management
  - attio-lists
  - attio-contacts
  - attio-notes
  - loops-broadcasts
  - clay-people-search
  - calcom-event-types
  - posthog-custom-events
---

# Co-Hosted Event Orchestration

This drill coordinates the full lifecycle of a co-hosted event between you and a partner company. It covers partner alignment, shared logistics, co-promotion, joint registration, live execution support, and post-event attendee splitting.

## Input

- Partner company name and primary contact (from `partner-prospect-research` or Attio)
- Event format: webinar, workshop, roundtable, AMA, or field dinner
- Event topic aligned to both audiences' pain points
- Target attendee count and date range

## Steps

### 1. Align with the partner on event scope

Create a shared event brief in Attio using `attio-notes`. The brief must include:

- **Event title**: Co-branded, names both companies
- **Format**: Webinar (30-60 min), Workshop (60-90 min), Roundtable (45-60 min), or Field Dinner (2-3 hours)
- **Topic**: Must be relevant to both audiences — find the overlap between your ICP's pain points and the partner's customer base
- **Speakers**: At least 1 from each company. Assign who presents what.
- **Date and time**: Pick a slot 3-4 weeks out. Avoid partner's existing event dates.
- **Target attendees**: Split responsibility — each side commits to a registration target (e.g., 20 each for a 40-person webinar)
- **Lead sharing rules**: Define upfront who gets access to which attendees. Standard: both sides get full attendee list. Alternative: each side keeps only their own registrants plus opt-ins.
- **Success criteria**: Agree on what "success" means (e.g., 30+ attendees, 5+ qualified leads each)

**Human action required:** Schedule a 20-minute alignment call with the partner contact to finalize the brief. The agent prepares the brief and talking points; the human runs the call.

### 2. Set up the event registration

Using the `event-platform-management` fundamental, create the event on your chosen platform (Luma recommended for virtual, Eventbrite for in-person). Configure:

- Co-branded event title and description
- Registration fields: name, email, company, role, "How did you hear about this?" (to attribute registrations to each partner)
- Cover image with both company logos
- Calendar invite with agenda and join link

Using `calcom-event-types`, create a Cal.com link for post-event meeting booking ("Book a follow-up with {your company}").

Track registration in PostHog using `posthog-custom-events`: fire `cohosted_event_registered` with properties `event_name`, `source_partner`, `registrant_company`, `registrant_role`.

### 3. Co-promote across both audiences

Each partner promotes to their own audience. The agent prepares assets for your side:

**Email promotion (via `loops-broadcasts`):**
- Send 3 emails: announcement (3 weeks out), reminder (1 week out), last chance (2 days out)
- Subject line formula: "{Pain point}? Join us + {Partner Name} on {date}"
- Body: 3 bullet points on what attendees learn, speaker bios, single CTA to register

**Social promotion:**
- Draft 3 LinkedIn posts: announcement, speaker spotlight, day-of reminder
- Tag the partner company and speakers in each post
- Share draft posts with the partner so they can reshare from their account

**Direct invitations (via `attio-lists`):**
- Pull prospects from Attio who match the event topic's ICP
- Send personal invitation emails (not mass broadcast) to top 20-30 prospects
- For each invite, reference something specific about their situation that makes this event relevant

Using `clay-people-search`, enrich the partner's recommended invite list (if they share one) with email and LinkedIn for your follow-up.

### 4. Manage registrations and reminders

Build an n8n workflow (or manual process for Smoke level) that:

1. Monitors new registrations daily via the event platform API
2. Adds each registrant to an Attio list tagged with the event name
3. Enriches registrants with company data using `attio-contacts`
4. Sends reminder emails via `loops-broadcasts`: 1 day before and 1 hour before
5. Tags each registrant with their attribution source (your audience vs partner's vs organic)

Share registration progress with the partner weekly so both sides can adjust promotion if one is behind target.

### 5. Execute the event

**Human action required:** Run the live event. The agent prepares:

- Speaker run-of-show document (who speaks when, for how long)
- 5-7 discussion questions or poll questions to drive engagement
- Backup talking points if Q&A is slow
- A shared Google Doc or Notion page for live note-taking

During the event, track engagement signals:
- Who asks questions (highest intent)
- Who answers polls
- Who stays for the full duration vs drops off early
- Chat messages (capture for follow-up personalization)

### 6. Post-event attendee processing

Within 24 hours of the event:

1. Export the full attendee list from the event platform using `event-platform-management`
2. Tag attendees in Attio using `attio-lists` with engagement level:
   - **Hot**: Asked a question or chatted actively
   - **Warm**: Attended full event
   - **Cool**: Registered but did not attend
3. Share the attendee list with the partner per the agreed lead-sharing rules
4. Track `cohosted_event_attended` in PostHog with properties: `event_name`, `engagement_level`, `source_partner`, `attendee_company`

### 7. Follow up within 48 hours

Send two different follow-up emails via `loops-broadcasts`:

- **Attendees**: Thank you, recording link, key takeaways, CTA to book a follow-up meeting (Cal.com link)
- **No-shows**: "Sorry we missed you" + recording link + same CTA

For **hot** attendees: send a personal email (not automated) referencing their specific question or comment. Include a direct meeting booking link.

Log all follow-up activity in Attio using `attio-notes`.

## Output

- Co-branded event created on event platform with tracking configured
- Both audiences promoted to with attribution tracking
- Attendee list enriched and segmented by engagement level in Attio
- Follow-up sequences sent within 48 hours
- Full event metrics logged in PostHog

## Triggers

- Run once per co-hosted event at Smoke/Baseline level
- At Scalable level, this drill runs on a recurring cadence (monthly or bi-weekly) with templated event configurations
