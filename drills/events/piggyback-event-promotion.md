---
name: piggyback-event-promotion
description: Promote a piggyback meetup to attendees of a target industry conference using outreach, social, and email
category: Events
tools:
  - Clay
  - Attio
  - Loops
  - LinkedIn
  - Instantly
  - PostHog
fundamentals:
  - event-attendee-enrichment
  - clay-people-search
  - clay-enrichment-waterfall
  - attio-lists
  - attio-contacts
  - loops-broadcasts
  - linkedin-organic-posting
  - instantly-campaign
  - posthog-custom-events
---

# Piggyback Event Promotion

This drill builds and executes a promotion campaign for a meetup that piggybacks on an existing industry conference. The goal is to fill a room with conference attendees who match your ICP -- people already in town, already thinking about your industry, and already primed for networking.

## Input

- Target conference details: name, dates, city, venue, expected attendance, speaker list, sponsor list
- Piggyback meetup details: date (evening of conference day 1 or day 2), venue (booked), format, capacity
- ICP definition (from `icp-definition` drill)
- Meetup registration page URL (from `meetup-pipeline` drill or Cal.com event)
- Timeline: promotion starts 3-4 weeks before the conference

## Steps

### 1. Build the target attendee list

Use `event-attendee-enrichment` to extract speakers, sponsors, and any public attendee lists from the target conference website. This produces names, titles, companies, and LinkedIn URLs.

Run `clay-people-search` to expand the list: search for people at companies that are sponsoring or speaking at the conference, filtering by ICP-matching titles. Conference sponsors typically send 3-5 people each -- find the ones in buyer roles.

Run `clay-enrichment-waterfall` on the full list to get verified email addresses and LinkedIn profile URLs. Deduplicate against your existing Attio contacts.

Push the enriched list to Attio using `attio-contacts`. Tag every contact with:
- `source: piggyback-{conference-slug}`
- `event: {meetup-name}`
- `conference: {conference-name}`

Target list size: aim for 5-10x your meetup capacity (e.g., 200 contacts for a 30-person meetup).

### 2. Launch personal email outreach (T-21 days)

Three weeks before the conference, send a personal outreach email via `instantly-campaign`. The email should:

- **Subject line:** Reference the conference by name (e.g., "In town for [Conference]? Join us for [Topic] drinks")
- **Body:** 3-4 sentences. Mention you are hosting an intimate gathering the evening of [date] for people attending [conference]. State the format (roundtable discussion, demo night, casual mixer). Mention 1-2 confirmed notable attendees if possible. Include the registration link.
- **Tone:** Peer-to-peer invitation, not marketing blast. Written as if one person is inviting another.

Segment the send:
- **Hot list (speakers, sponsors, known ICP matches):** Send from founder's personal email
- **Warm list (ICP-matching attendees):** Send from team member's email via Instantly

Track sends and opens with `posthog-custom-events`: fire `piggyback_invite_sent` with properties `conference`, `segment`, `email_template`.

### 3. Launch LinkedIn outreach (T-18 days)

For contacts who did not open the email within 3 days, and for contacts without verified emails:

Using `linkedin-organic-posting`, create a public LinkedIn post announcing the meetup. Tag the conference hashtag and relevant industry hashtags. Post from the founder or host's personal profile.

For high-value targets (speakers, decision-makers at sponsor companies), send a personal LinkedIn message:
- Reference their upcoming talk or session at the conference
- Invite them to the meetup as a follow-on networking opportunity
- Keep it to 3 sentences maximum

Track LinkedIn outreach with `posthog-custom-events`: fire `piggyback_linkedin_outreach_sent`.

### 4. Send email reminders (T-7 and T-1)

Using `loops-broadcasts`, send two reminder emails to the RSVP list:

**T-7 (one week before):**
- Confirm the meetup details (date, time, venue, address)
- Share the current RSVP count to build social proof ("25 people confirmed so far")
- Mention any notable attendees or discussion topics

**T-1 (day before):**
- Final reminder with venue directions and parking/transit info
- Ask RSVPs to confirm or cancel so you can adjust food/drink orders
- Include a link to add the event to their calendar

Track reminder engagement: `piggyback_reminder_sent`, `piggyback_reminder_opened`.

### 5. Day-of amplification

Post a "happening tonight" update on LinkedIn from the host's profile. Include the venue, time, and a "last few spots" CTA if capacity allows walk-ins.

If the conference has an attendee Slack, Discord, or WhatsApp group, post the meetup details there (if allowed by organizers).

### 6. Track the full promotion funnel

Using `posthog-custom-events`, build the complete funnel:
- `piggyback_invite_sent` (properties: conference, channel, segment)
- `piggyback_invite_opened` (properties: conference, channel)
- `piggyback_rsvp_registered` (properties: conference, source_channel)
- `piggyback_rsvp_confirmed` (properties: conference)
- `piggyback_attended` (properties: conference)
- `piggyback_meeting_booked` (properties: conference, days_to_meeting)

## Output

- Enriched target list in Attio tagged by conference
- Personal email outreach campaign running via Instantly
- LinkedIn outreach messages sent to high-value targets
- Reminder emails queued in Loops
- Full promotion funnel tracked in PostHog

## Triggers

- Start T-21 days before the target conference
- Email reminders at T-7 and T-1
- Day-of amplification on conference day
- Run once per piggyback event
