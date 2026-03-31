---
name: field-event-ops
description: End-to-end operations for in-person field events (dinners, happy hours, lunches) including venue sourcing, RSVP management, catering coordination, and day-of logistics
category: Events
tools:
  - Attio
  - Loops
  - Cal.com
  - Clay
  - Google Maps
  - PostHog
fundamentals:
  - attio-lists
  - attio-contacts
  - attio-notes
  - loops-broadcasts
  - loops-sequences
  - calcom-event-types
  - calcom-booking-links
  - clay-people-search
  - clay-enrichment-waterfall
  - google-maps-place-search
  - posthog-custom-events
---

# Field Event Ops

This drill manages the full operational lifecycle of a single in-person field event: a dinner, happy hour, or lunch in a target market. It handles everything except content delivery (which is human-led) and post-event nurture (handled by `field-event-attendee-nurture`).

Field events differ from webinars or virtual roundtables because they have physical constraints: venue capacity, food/drink minimums, travel logistics, and day-of coordination. This drill accounts for all of them.

## Input

- Target market: city and metro area
- Event format: dinner (8-15 people, seated), happy hour (15-40 people, casual), or lunch (8-20 people, seated)
- Target date range: window of 2-3 weeks to schedule within
- ICP definition (from `icp-definition` drill)
- Budget ceiling for venue and F&B

## Steps

### 1. Source and evaluate venues

Use `google-maps-place-search` to find candidate venues in the target city. Search parameters:

- **Dinner:** Private dining rooms or semi-private spaces at restaurants. Search queries: "private dining room [city]", "restaurant private event space [city]". Filter by capacity (8-15), cuisine type appropriate for business dining, and price range ($60-150/person).
- **Happy hour:** Bars or restaurants with reservable semi-private areas. Search queries: "bar private event [city]", "happy hour venue [city]". Filter by capacity (15-40), accessibility, and bar service availability.
- **Lunch:** Restaurants with group seating or private rooms. Search queries: "lunch private dining [city]", "business lunch venue [city]". Filter by capacity (8-20) and proximity to the local business district.

For each candidate venue, capture:
- Name, address, phone, website
- Private/semi-private space availability
- Capacity range
- F&B minimum spend (most private dining rooms require one)
- Cancellation policy
- AV capabilities (for any brief presentations)

Score venues on: location accessibility (transit/parking), capacity fit, ambiance for business networking, and cost. Rank top 3.

### 2. Book the venue

**Human action required:** Call or email the top-ranked venue to book. Confirm: date, time, room, headcount range, F&B package or minimum, deposit if required, and cancellation window.

Log the confirmed booking in Attio as a custom object or note on the event record. Include: venue name, address, confirmed date/time, capacity, cost commitment, and cancellation deadline.

### 3. Build the invitee list

Use `clay-people-search` to find prospects in the target metro matching the ICP. Filter by:
- Title/seniority matching your buyer persona
- Company size and industry matching ICP
- Location: within the metro area of the event city

Run `clay-enrichment-waterfall` to get verified emails and LinkedIn URLs.

Push enriched contacts to Attio using `attio-contacts`. Create an Attio list for this event using `attio-lists` with fields:
- Name, email, company, title
- Invited (boolean), RSVP status (invited/confirmed/declined/no-response), attended (boolean)
- Source (Clay, existing pipeline, referral, personal network)

Target invitee list size: 3-5x your venue capacity. For a 15-person dinner, invite 45-75 people. Field event show rates for confirmed RSVPs typically run 70-85%.

### 4. Send invitations

Using `loops-sequences`, build a 3-touch invitation sequence:

**Touch 1 (T-21 days):** Personal invitation. Subject line references the city and a peer-relevant topic ("Dinner conversation: [topic] in [city]"). Body: 4-5 sentences. Frame it as an exclusive gathering of [N] [role] leaders in [city] to discuss [topic] over [dinner/drinks/lunch]. Include date, time, general location (neighborhood, not exact address), and RSVP link.

**Touch 2 (T-14 days):** Social proof follow-up to non-responders. Mention confirmed attendees by title/company (not name, unless they consented). "We have [N] [title]s from companies like [X] confirmed so far." Include the RSVP link again.

**Touch 3 (T-7 days):** Final seat availability. "A few spots remain for [date]. Confirming the final headcount with the venue this week." Create urgency without pressure.

Create the RSVP page using `calcom-event-types`. Configure it as a group booking with a max capacity matching the venue. Use `calcom-booking-links` to generate the shareable link.

Track all invitation events with `posthog-custom-events`:
- `field_event_invite_sent` (properties: event_slug, city, touch_number, channel)
- `field_event_rsvp_page_viewed` (properties: event_slug, city, source)
- `field_event_rsvp_confirmed` (properties: event_slug, city, company, title)
- `field_event_rsvp_declined` (properties: event_slug, city, reason)

### 5. Manage RSVPs and headcount

Monitor RSVP confirmations daily starting at T-14. Update the Attio event list as RSVPs come in.

**Headcount triggers:**
- If confirmations reach venue capacity at any point: close the RSVP page, move remaining invitees to a waitlist
- If confirmations are below 50% of capacity at T-7: activate backup outreach — send personal LinkedIn messages to high-value non-responders, ask existing confirmed attendees to refer a peer
- If confirmations are below 50% of capacity at T-3: **Human action required** — decide whether to proceed, downsize, or postpone. Alert via Slack.

Send a confirmation email to all confirmed attendees at T-3 using `loops-broadcasts`:
- Exact venue address and directions
- Parking/transit recommendations (use `google-maps-place-search` to find nearby parking)
- Dress code if relevant
- Arrival time
- Your phone number for day-of coordination

### 6. Coordinate day-of logistics

**Human action required:** The host manages the event in person. Agent supports with:

- T-2 hours: Send a "Looking forward to tonight" text/email to all confirmed attendees with a reminder of the address
- Prepare name badges or a seating chart if dinner format (agent generates from the Attio list)
- Prepare a brief topic guide or conversation starters for the host (3-5 discussion questions related to the event topic)
- Log any last-minute cancellations or walk-ins in Attio

### 7. Capture attendance

During or immediately after the event, mark attendance in Attio:
- Set `attended: true` for each person who showed up
- Add notes on any notable conversations or expressed needs
- Log any new contacts met at the event (walk-ins, plus-ones) as new Attio contacts with `source: field-event-walkin`

Fire `field_event_attended` PostHog event for each attendee (properties: event_slug, city, company, title).

## Output

- Booked venue with confirmed logistics
- Enriched invitee list in Attio with RSVP tracking
- 3-touch invitation sequence running in Loops
- RSVP page live on Cal.com
- Full attendance logged in Attio and PostHog
- Ready for `field-event-attendee-nurture` drill to handle follow-up

## Triggers

- Start T-28 days before the target event date (venue sourcing)
- Invitations begin at T-21
- Confirmation email at T-3
- Day-of coordination on event day
- Run once per event
