---
name: calcom-crm-sync
description: Connect Cal.com to Attio via webhooks and n8n so booked meetings automatically create or update CRM records
tool: Cal.com
product: Cal.com
difficulty: Intermediate
---

# Sync Cal.com with Your CRM

## Prerequisites
- Cal.com account with API access
- n8n instance running (see `n8n-mcp-setup`)
- Attio MCP server connected (see `attio-mcp-setup`)

## Steps

1. **Set up a Cal.com webhook via API.** Use the Cal.com API to create a webhook for booking events:
   ```
   POST /api/v1/webhooks
   {
     "subscriberUrl": "https://your-n8n-instance.com/webhook/calcom-booking",
     "eventTriggers": ["BOOKING_CREATED"],
     "active": true
   }
   ```
   This fires when someone books a meeting.

2. **Create an n8n workflow for the webhook.** Build an n8n workflow with a Webhook Trigger node listening at the URL configured above. This workflow will process every new booking.

3. **Parse the webhook payload.** Use a Set node in n8n to extract: booker's name, email, company (from booking form custom fields), event type, and scheduled time from the Cal.com webhook JSON.

4. **Check if contact exists in Attio.** Use the Attio MCP or API to search by email. If the contact exists, update their record with a note about the upcoming meeting and move their deal to "Meeting Scheduled" stage.

5. **Create records for new contacts.** If the contact is new: create a Person record in Attio with their info, create a linked Company record if needed, and create a Deal at the "Meeting Booked" stage. Use the Attio MCP `create_record` operations.

6. **Send tracking events.** Fire a PostHog event via the API:
   ```javascript
   posthog.capture('meeting_booked', { source: eventType, lead_email: bookerEmail })
   ```
   Optionally send a Slack notification to the sales team with booking details so they can prepare.
