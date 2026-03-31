---
name: calcom-crm-sync
description: Connect Cal.com to Attio so that booked meetings automatically create or update CRM records and trigger follow-up workflows.
tool: Cal.com
difficulty: Config
---

# Sync Cal.com with Your CRM

### Step-by-step
1. In Cal.com, go to Settings > Integrations or use Cal.com webhooks.
2. Set up a webhook for 'Booking Created' events: this fires when someone books a meeting.
3. Point the webhook to your n8n instance URL.
4. In n8n, create a workflow triggered by the Cal.com webhook.
5. Parse the webhook payload: extract the booker's name, email, company (from booking form), event type, and scheduled time.
6. Check if the contact exists in Attio: use the Attio API to search by email.
7. If the contact exists: update their record with a note about the upcoming meeting and move their deal to the appropriate stage (e.g., 'Meeting Scheduled').
8. If the contact is new: create a Person record in Attio with their info, create a linked Company record if needed, and create a Deal.
9. Send a PostHog event: meeting_booked with properties like source, event_type, and lead_email for tracking.
10. Optionally, send a Slack notification to the sales team with the booking details so they can prepare.
