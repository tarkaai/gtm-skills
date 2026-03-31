---
name: event-platform-management
description: Create, configure, and manage events on virtual and hybrid event platforms via API
tool: Luma
product: Events
difficulty: Config
---

# Event Platform Management

Create and manage events programmatically on virtual/hybrid event platforms. This fundamental covers registration page creation, attendee tracking, and event configuration via API.

## Authentication

- **Luma**: API key from https://lu.ma/settings/api → `x-luma-api-key` header
- **Riverside**: API access via https://riverside.fm (OAuth2, contact support for API access)
- **Zoom**: JWT or OAuth2 app at https://marketplace.zoom.us → `Authorization: Bearer {token}`
- **Hopin**: API at https://api.hopin.com → `Authorization: Bearer {API_KEY}`
- **Eventbrite**: OAuth2 at https://www.eventbrite.com/platform → `Authorization: Bearer {token}`

## Method 1: Luma (Recommended for tech/startup events)

### Create an event

```
POST https://api.lu.ma/public/v2/event/create
Headers:
  x-luma-api-key: {LUMA_API_KEY}
  Content-Type: application/json

Body:
{
  "name": "Co-hosted Event: {topic}",
  "description": "{event description with partner branding}",
  "start_at": "2026-04-15T18:00:00Z",
  "end_at": "2026-04-15T19:30:00Z",
  "timezone": "America/New_York",
  "geo_address_json": {
    "description": "Virtual"
  },
  "meeting_url": "{zoom_or_riverside_link}",
  "cover_url": "{branded_cover_image_url}",
  "require_rsvp_approval": false,
  "visibility": "public"
}
```

### Get registrants

```
GET https://api.lu.ma/public/v2/event/{event_id}/guests
Headers:
  x-luma-api-key: {LUMA_API_KEY}
```

Response: array of guest objects with `email`, `name`, `created_at`, `approval_status`.

### Update event

```
PATCH https://api.lu.ma/public/v2/event/{event_id}
Headers:
  x-luma-api-key: {LUMA_API_KEY}
Body: { fields to update }
```

## Method 2: Zoom (for webinar-style events)

### Create a meeting

```
POST https://api.zoom.us/v2/users/me/meetings
Headers:
  Authorization: Bearer {ZOOM_JWT}
  Content-Type: application/json

Body:
{
  "topic": "Co-hosted Event: {topic}",
  "type": 2,
  "start_time": "2026-04-15T18:00:00Z",
  "duration": 90,
  "timezone": "America/New_York",
  "settings": {
    "host_video": true,
    "participant_video": true,
    "join_before_host": false,
    "registration_type": 1,
    "approval_type": 0,
    "meeting_authentication": false
  }
}
```

### Get registrants

```
GET https://api.zoom.us/v2/meetings/{meeting_id}/registrants
Headers:
  Authorization: Bearer {ZOOM_JWT}
```

## Method 3: Eventbrite

### Create an event

```
POST https://www.eventbriteapi.com/v3/organizations/{org_id}/events/
Headers:
  Authorization: Bearer {EB_TOKEN}
Body:
{
  "event": {
    "name": { "html": "Co-hosted Event: {topic}" },
    "start": { "timezone": "America/New_York", "utc": "2026-04-15T22:00:00Z" },
    "end": { "timezone": "America/New_York", "utc": "2026-04-15T23:30:00Z" },
    "currency": "USD",
    "listed": true
  }
}
```

### Get attendees

```
GET https://www.eventbriteapi.com/v3/events/{event_id}/attendees/
Headers:
  Authorization: Bearer {EB_TOKEN}
```

## Output Format

Regardless of platform, normalize event data to:

| Field | Description |
|-------|-------------|
| `event_id` | Platform-specific event identifier |
| `event_url` | Public registration URL |
| `registrant_count` | Total registrations |
| `attendee_count` | Actual attendees (post-event) |
| `registrants` | Array of {name, email, company, registered_at} |

## Error Handling

- If API rate limits hit, implement exponential backoff (start 1s, max 60s)
- If event creation fails, check required fields per platform (Luma requires start_at + name minimum)
- If registrant export is capped, paginate using `next_cursor` or `page_number` parameter

## Pricing

- **Luma**: Free for unlimited events; paid tiers for custom branding ($30/mo)
- **Zoom**: Free for 40-min meetings; Pro $13.33/mo for unlimited duration
- **Eventbrite**: Free for free events; 3.7% + $1.79 per paid ticket
- **Hopin**: Contact for pricing; typically $99/mo+
- **Riverside**: $15/mo (Basic) for recording; free for hosting
