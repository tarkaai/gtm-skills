---
name: field-event-series-automation
description: Automate a recurring multi-city field event series with territory rotation, prospect sourcing, promotion scheduling, and cross-event analytics
category: Events
tools:
  - n8n
  - Clay
  - Loops
  - Attio
  - PostHog
  - Cal.com
  - Google Maps
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-crm-integration
  - clay-people-search
  - clay-enrichment-waterfall
  - clay-email-verification
  - loops-broadcasts
  - loops-audience
  - loops-sequences
  - attio-lists
  - attio-contacts
  - attio-automation
  - attio-notes
  - attio-reporting
  - posthog-custom-events
  - posthog-funnels
  - posthog-dashboards
  - calcom-event-types
  - google-maps-place-search
---

# Field Event Series Automation

This drill transforms one-off field events into a repeatable multi-city series with automated operations. It manages the cycle: city selection, prospect sourcing, venue coordination, invitation, execution, and cross-event performance comparison. The goal is to run 2-4 events per month across target markets with decreasing per-event manual effort.

## Input

- List of target markets (cities) ranked by ICP density
- Proven event format from Baseline (dinner, happy hour, or lunch — use whichever performed best)
- Baseline metrics: average RSVP rate, show rate, and conversion rate to use as benchmarks
- Budget per event and monthly budget ceiling
- Available hosts (who can travel to which cities)

## Steps

### 1. Build the city rotation calendar

Using `attio-reporting`, pull pipeline and customer data to rank target cities by:
- Number of ICP-matching companies in metro
- Number of open deals or active pipeline in the region
- Number of existing customers who could attend (social proof and referrals)
- Travel logistics for available hosts (direct flights, drive time)

Build a 3-month rotation calendar. Rules:
- Each city gets an event every 6-8 weeks (builds local community, avoids fatigue)
- Alternate between primary markets (high ICP density) and secondary markets (emerging pipeline)
- Schedule 2-4 events per month depending on team capacity
- Never schedule two events in the same week — allow recovery and follow-up time

Store the calendar in Attio as a structured list or custom object. Use `n8n-scheduling` to trigger the event ops workflow 28 days before each scheduled event.

### 2. Automate prospect sourcing per city

Build an n8n workflow that triggers at T-28 for each event:

1. Read the upcoming event city from the Attio calendar
2. Run `clay-people-search` for ICP-matching prospects in that metro. Parameters: title, seniority, company size, industry, location radius
3. Run `clay-enrichment-waterfall` to verify emails and pull LinkedIn URLs
4. Run `clay-email-verification` to remove undeliverable addresses
5. Deduplicate against existing Attio contacts using `n8n-crm-integration`
6. Tag new contacts with `source: field-event-series`, `city: {city}`, `event: {event-slug}`
7. Push to Attio using `attio-contacts`

Target: 200-500 net-new prospects per event, plus re-engage 50-100 existing contacts in the market.

Using `loops-audience`, segment the invitee list:
- **Net-new prospects**: Full 3-touch invitation sequence
- **Previous event attendees in this city**: "We're back in [city]" personalized invite
- **Previous no-shows**: Single re-invitation with social proof from the last event
- **Active pipeline contacts in the region**: Personal invitation from their account owner

### 3. Automate the invitation engine

Build a master n8n workflow that handles the invitation sequence for each event:

**T-21:** Trigger `loops-sequences` for the 3-touch invitation sequence (from `field-event-ops` drill)
**T-14:** Send Touch 2 to non-responders
**T-7:** Send Touch 3 (final seat availability) to non-responders
**T-3:** Send confirmation with logistics to all confirmed RSVPs

The workflow reads the event details (city, date, venue, topic, capacity) from Attio and populates the email templates dynamically. No manual email writing per event — templates are parameterized.

Using `calcom-event-types`, auto-create the RSVP page for each event with the city, date, and capacity pre-configured.

Track all invitation activity with `posthog-custom-events` using a consistent event taxonomy:
- `field_event_invite_sent` (properties: event_slug, city, touch_number, segment)
- `field_event_rsvp_confirmed` (properties: event_slug, city, segment, source)

### 4. Standardize venue management

Maintain a venue database in Attio with fields: city, venue name, address, capacity, F&B minimum, contact info, rating (1-5 based on past events), notes.

After each event, rate the venue and log feedback. For repeat cities, the agent recommends the highest-rated venue automatically. For new cities, the agent runs `google-maps-place-search` and produces a ranked shortlist for human review.

**Human action required:** Venue booking still requires a phone call or email. The agent prepares the request (date, headcount, F&B preferences, budget) and the human executes the booking.

### 5. Build cross-event analytics

Using `posthog-dashboards`, create a series-level dashboard:

**City comparison view:**
- RSVP rate by city (which markets are most responsive)
- Show rate by city (which markets follow through)
- Conversion rate by city (which markets produce pipeline)
- Cost per attendee and cost per meeting by city

**Trend view:**
- Registrations per event over time (series growing or shrinking?)
- Show rate trend (commitment holding?)
- Meetings per event trend (conversion improving?)
- Repeat attendance rate (community building?)

**Funnel view:**
Using `posthog-funnels`, build the series-wide funnel:
`field_event_invite_sent` → `field_event_rsvp_confirmed` → `field_event_attended` → `field_event_meeting_booked` → `field_event_deal_created`

Break down by city, event format, topic, and invitee segment.

### 6. Automate post-event workflows

After each event (triggered by the host marking attendance in Attio), auto-launch:
1. `field-event-attendee-nurture` drill (follow-up sequences)
2. Venue feedback request to the host
3. Series-level metrics update in PostHog
4. Next-event-in-this-city scheduling trigger (queue it 6-8 weeks out)

Using `n8n-triggers`, wire these automations so that marking attendance in Attio kicks off the entire post-event process without manual intervention.

## Output

- 3-month city rotation calendar in Attio
- Automated per-event prospect sourcing via Clay + n8n
- Parameterized invitation sequences in Loops triggered by n8n
- Venue database with ratings in Attio
- Series-level PostHog dashboard with city comparison, trends, and funnels
- Post-event automations triggered by attendance logging

## Triggers

- T-28 per event: prospect sourcing and venue coordination
- T-21 per event: invitation sequence launch
- T+0: post-event automation cascade
- Monthly: series health review from PostHog dashboard
- Quarterly: city rotation refresh based on updated pipeline data
