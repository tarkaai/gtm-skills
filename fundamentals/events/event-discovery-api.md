---
name: event-discovery-api
description: Search for upcoming industry events, conferences, and meetups using web scraping and event platform APIs
tool: Clay
product: Clay
difficulty: Config
---

# Event Discovery via API

Search for upcoming industry events that match your ICP's interests using Clay's web scraping (Claygent) and event platform data. This fundamental feeds event scouting drills with a structured list of events worth attending.

## Authentication

- Clay account with Claygent credits
- Optional: Luma API key (public events API), Eventbrite API key, Lu.ma calendar access

## Method 1: Claygent Web Scraping (Recommended)

1. **Create a Clay table** with seed data: industry keywords, competitor names, ICP job titles, and target cities.

2. **Add a Claygent column** with a prompt that discovers events:
   ```
   Search the web for upcoming {Industry Keyword} conferences, meetups, and events
   in {City} in the next 90 days. For each event found, return:
   - Event name
   - Date
   - Venue name and address
   - Estimated attendance
   - Event website URL
   - Whether it has a public attendee list or speaker list
   Format as JSON array.
   ```

3. **Parse the output** using Clay's JSON extraction column to split multi-event results into separate rows.

4. **Enrich each event** with a second Claygent column:
   ```
   Visit {Event URL} and extract:
   - Registration cost
   - Speaker names and companies
   - Sponsor companies
   - Agenda topics
   - Whether the venue has a lobby, hallway, or common area accessible without a badge
   ```

## Method 2: Luma API (for tech/startup events)

1. **GET** `https://api.lu.ma/public/v2/event/search`
   - Query params: `query={keyword}`, `location={city}`, `after={ISO date}`
   - Headers: `x-luma-api-key: {your_key}`

2. **Response** contains: event name, date, location, host, RSVP count, and description.

3. **Filter** for events with 50+ RSVPs (enough foot traffic for hallway demos) and relevant industry keywords in the description.

## Method 3: Eventbrite API

1. **GET** `https://www.eventbriteapi.com/v3/events/search/`
   - Query params: `q={keyword}`, `location.address={city}`, `start_date.range_start={ISO date}`, `categories={category_id}`
   - Headers: `Authorization: Bearer {token}`

2. **Response** includes: event name, venue, capacity, ticket types, and description.

3. **Filter** for events with capacity > 100 and relevant categories (Technology, Business, Science & Tech).

## Output Format

Each discovered event should be stored as a row with these fields:

| Field | Description |
|-------|-------------|
| `event_name` | Full event name |
| `event_date` | Start date (ISO 8601) |
| `city` | City name |
| `venue_name` | Venue name |
| `venue_address` | Full address |
| `estimated_attendance` | Number or range |
| `event_url` | Registration or info page |
| `has_public_attendee_list` | Boolean |
| `registration_cost` | Cost or "Free" |
| `hallway_accessible` | Whether common areas are accessible without a badge |
| `relevance_score` | 0-100 based on ICP keyword overlap |

## Error Handling

- If Claygent returns no results for a city/keyword combo, broaden the date range to 180 days.
- If event URLs are dead or redirected, flag the row and skip enrichment.
- Rate limit Claygent queries to avoid burning credits on low-quality results; batch 20-30 events at a time.
