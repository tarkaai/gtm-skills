---
name: event-scouting
description: Discover and rank upcoming industry events for guerilla hallway demos based on ICP attendance density and venue accessibility
category: Events
tools:
  - Clay
  - Attio
  - PostHog
fundamentals:
  - event-discovery-api
  - event-attendee-enrichment
  - clay-claygent
  - clay-scoring
  - attio-lists
  - posthog-custom-events
---

# Event Scouting

This drill finds industry events worth showing up to for hallway demos. The goal is NOT to sponsor or exhibit -- it is to identify events where your ICP congregates so you can intercept them in lobbies, hallways, lunch lines, and after-parties.

## Input

- ICP definition (from `icp-definition` drill): target industries, titles, company sizes
- Target cities or regions where you can travel
- Budget constraints for travel
- Date range to scout (typically 30-90 days out)

## Steps

### 1. Discover events in target markets

Run the `event-discovery-api` fundamental to search for events in each target city. Use multiple keyword strategies:

- **Industry keywords**: e.g., "SaaS conference", "DevOps summit", "AI/ML meetup"
- **Competitor keywords**: events your competitors sponsor or speak at
- **ICP role keywords**: e.g., "CTO roundtable", "engineering leadership"
- **Community keywords**: local tech community names, Slack groups, meetup organizers

Aim for 15-30 candidate events per city per quarter.

### 2. Score events for hallway demo potential

Add a scoring formula in Clay that evaluates each event on hallway demo suitability:

- **ICP density (35%)**: How many speakers/sponsors match your ICP? Use `event-attendee-enrichment` to extract and score attendee lists. An event with 5+ ICP-match speakers scores 100.
- **Venue accessibility (25%)**: Does the venue have public lobbies, hallways, coffee areas accessible without a badge? Hotel venues score high (lobbies are public). Convention centers score lower (badge-gated). Claygent can research this from venue photos and floor plans.
- **Event size (20%)**: Sweet spot is 200-2,000 attendees. Under 100 is too small (you stand out as uninvited). Over 5,000 is too chaotic. Score: 200-500 = 90, 500-2,000 = 100, 100-200 = 60, 2,000-5,000 = 40, <100 or >5,000 = 20.
- **Timing (10%)**: Multi-day events score higher (more hallway time). Single-day events with long breaks score well. Back-to-back sessions with no breaks score low.
- **Cost to attend (10%)**: Free events and events at hotels where you can hang in the lobby = 100. Events requiring a $2,000+ badge to enter the venue = 0. Events where the hallway/lobby is accessible but sessions require a badge = 70.

### 3. Enrich top-scored events with attendee targets

For events scoring 70+, run `event-attendee-enrichment` to build a target contact list per event:

- Extract all speakers, panelists, and workshop leaders
- Extract sponsor company representatives
- If a public attendee list exists, extract and filter for ICP matches
- Enrich each contact with email, LinkedIn, company data
- Score contacts for demo relevance

### 4. Build the event calendar

Push scored events to Attio using `attio-lists`. Create an "Event Calendar" list with fields:

- Event name, date, city, venue
- Hallway demo score (from step 2)
- Number of ICP-match targets identified
- Travel cost estimate (agent can estimate from city distance)
- Expected ROI: (ICP targets x estimated conversion rate) vs travel cost

Track event scouting activity in PostHog using `posthog-custom-events`: log `event_scouted` with event name, score, and number of targets found.

### 5. Plan the approach for each event

For each event you decide to attend, prepare:

- **Target list**: Top 10-15 ICP-match contacts to seek out, with photos (from LinkedIn) for recognition
- **Venue intel**: Lobby layout, coffee area locations, session break schedule
- **Talking points**: 2-3 conversation starters tied to event topics
- **Demo setup**: Laptop or tablet with product loaded, offline-ready if WiFi is unreliable
- **Scheduling link**: Cal.com link ready to share for booking follow-up meetings

## Output

- Scored and ranked event calendar for the next 90 days
- Per-event target contact lists in Attio
- Venue intelligence notes per event
- Event scouting metrics in PostHog

## Triggers

- Run monthly to refresh the 90-day event calendar
- Run ad-hoc when a new event is discovered or suggested
