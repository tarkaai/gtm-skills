---
name: calcom-event-types
description: Set up different meeting types in Cal.com via API -- discovery calls, demos, team meetings
tool: Cal.com
difficulty: Setup
---

# Configure Cal.com Event Types

## Prerequisites
- Cal.com account with API access
- Calendar connected (Google Calendar, Outlook, or Apple Calendar)

## Steps

1. **Create event types via API.** Use the Cal.com REST API to create meeting types:
   ```
   POST /api/v1/event-types
   {
     "title": "30-min Discovery Call",
     "slug": "discovery",
     "length": 30,
     "description": "Explore how we can help solve your problem"
   }
   ```
   Create separate types for: Discovery Call (30 min), Product Demo (45 min), Quick Chat (15 min).

2. **Configure availability.** Set which days and hours you are bookable via the API. Add buffer time between meetings (15 min recommended):
   ```
   PATCH /api/v1/event-types/<id>
   { "beforeEventBuffer": 15, "afterEventBuffer": 15 }
   ```

3. **Set booking constraints.** Require minimum notice (24 hours) and set how far in advance people can book (2-4 weeks):
   ```
   PATCH /api/v1/event-types/<id>
   { "minimumBookingNotice": 1440, "periodDays": 28 }
   ```

4. **Add booking form questions.** Configure custom questions on the booking form: "What would you like to discuss?", "Company name", "How did you hear about us?". These feed into your CRM via the webhook integration (see `calcom-crm-sync`).

5. **Set up confirmation emails.** Customize the confirmation email with meeting details, prep instructions, and any required reading. Include your calendar link for rescheduling.

6. **Generate and distribute booking links.** Each event type has a unique URL: `cal.com/yourname/discovery`. Add to your email signature, LinkedIn profile Featured section, website contact page, and cold email CTAs. Track booking sources with UTM parameters: `cal.com/yourname/demo?utm_source=linkedin`.
