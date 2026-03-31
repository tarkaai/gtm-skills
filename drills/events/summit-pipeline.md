---
name: summit-pipeline
description: Plan, build, promote, and execute a multi-session virtual summit with speakers, sponsors, and attendee engagement
category: Events
tools:
  - Cal.com
  - Loops
  - PostHog
  - Attio
  - Riverside
  - Clay
  - Intercom
fundamentals:
  - calcom-event-types
  - calcom-booking-links
  - loops-broadcasts
  - loops-sequences
  - loops-audience
  - posthog-custom-events
  - attio-lists
  - attio-contacts
  - attio-deals
  - riverside-recording
  - clay-people-search
  - clay-enrichment-waterfall
  - intercom-in-app-messages
  - linkedin-organic-posting
---

# Summit Pipeline

This drill builds the complete lifecycle for a multi-session virtual summit: speaker recruitment, sponsor coordination, registration, promotion, live production, and post-event follow-up. A summit is distinct from a webinar — it runs 4-8 sessions over a half-day or full day, features multiple speakers, may include sponsor tracks, and generates concentrated demand in a single event.

## Prerequisites

- Virtual event platform (Riverside, Zoom Webinar, or StreamYard) configured for multi-session streaming
- Attio workspace with contacts and pipeline
- Loops account for email sequences
- Landing page builder for the registration site
- At least 8 weeks lead time before event date

## Steps

### 1. Define summit theme and structure

Choose a theme that sits at the intersection of your ICP's top pain points and your product's unique positioning. The theme must be specific enough to attract only your target audience — broad themes attract unqualified registrants.

Define the summit structure:
- **Session count**: 4-8 sessions (half-day = 4 sessions at 30 min each with breaks; full-day = 6-8 sessions)
- **Session formats**: Keynote (1 speaker, 20-30 min), Panel (3-4 speakers, 30-40 min), Workshop (hands-on, 45-60 min), Fireside chat (interviewer + guest, 20-30 min), Lightning talks (3-5 speakers at 5-7 min each)
- **Tracks**: For summits with 6+ sessions, split into 2 parallel tracks (e.g., technical + business). Single-track is simpler for first-time summits.
- **Timing**: Schedule the event for a weekday (Tuesday-Thursday). Start at 9am or 10am in the primary timezone of your ICP. Avoid Mondays and Fridays.

Create an Attio list using `attio-lists` with fields: session_title, speaker_name, speaker_company, session_format, session_time, track, status.

### 2. Recruit speakers

Speakers are the primary draw for registrations. Recruit 6-12 speakers across these categories:

- **Customer speakers (2-3)**: Your best customers sharing real results. Most credible session type.
- **Industry experts (2-3)**: Recognized names in your space who draw registrations by name alone.
- **Partner speakers (1-2)**: Representatives from integration partners or adjacent companies. They bring their audience.
- **Internal speakers (1-2)**: Your founder or product lead presenting roadmap, live demo, or unique data.

Using `clay-people-search`, identify potential speakers by: LinkedIn engagement on relevant topics, conference speaking history, company relevance to your ICP, and follower count. Enrich with `clay-enrichment-waterfall` for email.

Send speaker invitations from Attio using `attio-contacts`. The invitation should include: event theme, expected audience size and profile, session format options, date and time commitment, promotion expectations (they promote to their audience), and any speaker perks (recording rights, cross-promotion).

Track speaker pipeline in Attio: invited → accepted → confirmed → prepped → delivered.

### 3. Secure sponsors (optional)

If monetizing the summit or adding credibility, approach 2-4 sponsors. Sponsor tiers:
- **Title sponsor**: Logo on all materials, dedicated session slot, attendee list share
- **Session sponsor**: Branding on one session, 5-minute intro slot
- **Booth sponsor**: Virtual booth or breakout room access

Using `attio-deals`, create a sponsorship pipeline: prospected → pitched → negotiated → confirmed → delivered.

### 4. Build the registration funnel

Create a summit landing page with: event theme and value proposition (what attendees will learn), full agenda with session titles and speaker bios, date/time with timezone converter, registration form (name, email, company, role, company size), and social proof (speaker logos, sponsor logos, past event stats if available).

Using `calcom-event-types`, create a summit event for attendee tracking. Using `posthog-custom-events`, instrument the registration page:
- `summit_page_viewed` with properties: source, utm_campaign
- `summit_registered` with properties: company_size, role, source
- `summit_agenda_expanded` (tracks which sessions interest registrants)

Using `attio-lists`, create a "Summit Registrants" list. Auto-add every registrant with: registration date, company, role, source channel, and which sessions they expressed interest in.

### 5. Execute the promotion engine

**Week 1-2 (T-8 to T-6 weeks): Soft launch**
- Announce the summit on LinkedIn using `linkedin-organic-posting`. Lead with the theme and one headline speaker.
- Send a save-the-date email to your subscriber list via `loops-broadcasts`.
- Activate speaker promotion: each confirmed speaker posts to their audience.

**Week 3-4 (T-6 to T-4 weeks): Main push**
- Send the full invitation email to your subscriber list via `loops-broadcasts`, segmented by ICP relevance.
- Using `clay-people-search` and `clay-enrichment-waterfall`, build a net-new prospect list (500-1000 people) matching the summit ICP. Import into Loops via `loops-audience` and send targeted invitations.
- Run a 3-post LinkedIn series: speaker spotlight, agenda reveal, early-bird stats.
- Send personal invitations from Attio to high-value prospects and active pipeline — a summit invite is a high-value touchpoint.
- If you have an Intercom user base, promote via `intercom-in-app-messages` to users who match the summit audience.

**Week 5-6 (T-4 to T-2 weeks): Urgency push**
- Send second email wave to non-openers from the first wave.
- Speaker-specific email: "Hear [Name] from [Company] share [specific insight]."
- LinkedIn countdown posts.
- Partner cross-promotion: sponsors and partners email their lists.

**Week 7-8 (T-2 weeks to event): Final push and prep**
- Send "limited spots" or "final week" email.
- Using `loops-sequences`, configure reminder sequence: registered → 1-week reminder → 1-day reminder → 1-hour reminder → join link.
- Prepare event production: test all speaker connections via Riverside, prepare slide decks, create session transition graphics, brief the moderator.

**Human action required:** Moderate the summit live. The agent handles all preparation and promotion, but a human moderates sessions, manages Q&A, and handles live technical issues.

### 6. Execute summit day operations

Pre-event (2 hours before):
- Send the final join link email to all registrants via `loops-broadcasts`
- Open the virtual venue 30 minutes early for speaker tech checks using `riverside-recording`
- Post a "We're live in 30 minutes" update on LinkedIn

During event:
- Track attendance per session using `posthog-custom-events`: `summit_session_joined` with properties: session_id, attendee_id, join_time
- Log chat questions and engagement: `summit_question_asked`, `summit_poll_responded`, `summit_cta_clicked`
- Record every session via `riverside-recording` for replay content

Post-event (within 2 hours):
- Send immediate thank-you email to all attendees via `loops-broadcasts` with: highlight reel, "recordings coming soon" message, and CTA to book a meeting
- Tag all attendees in Attio using `attio-lists`: attended (which sessions), engaged (asked questions, clicked CTAs), VIP (attended 4+ sessions)
- Update speaker status to "delivered" in Attio

### 7. Measure summit performance

Track the full funnel using PostHog:
- Page views → Registrations (target: >15% conversion)
- Registrations → Attendance (target: >35% show rate)
- Attendance → Multi-session attendance (target: >40% attend 2+ sessions)
- Attendance → Engagement (questions, polls, CTA clicks) (target: >20%)
- Engagement → Meetings booked (target: >8% of attendees)

Calculate: cost per registrant, cost per attendee, cost per qualified lead, pipeline generated per summit, and promotion channel attribution.
