---
name: n8n-triggers
description: Configure triggers to start n8n workflows from events, schedules, or webhooks
tool: n8n
product: n8n
difficulty: Beginner
---

# Configure n8n Triggers

## Prerequisites
- n8n instance running with at least one workflow
- Access to the event source (app webhook settings, cron schedule, etc.)

## Steps

1. **Choose the right trigger type.** Webhook Trigger: use when your app sends real-time events (user signup, payment, form submission). Schedule Trigger: use for periodic tasks (daily list sync, weekly reporting). App Trigger: use when n8n has a native integration (Attio, Slack, GitHub).

2. **Set up a Webhook trigger.** Add a Webhook node as the first node. n8n generates a unique URL. Copy this URL and configure it in your app's webhook settings. Test by sending a sample event -- n8n will display the received payload for you to map fields.

3. **Set up a Schedule trigger.** Add a Schedule Trigger node. Configure the cron expression for your desired frequency. Common patterns: every hour ("0 * * * *"), daily at 9am ("0 9 * * *"), every Monday ("0 9 * * 1"). Always set the timezone to match your business hours.

4. **Set up an App trigger.** Add the relevant app trigger node (e.g., "Attio Trigger"). Authenticate with your credentials. Select the event type (e.g., "Record Created in Deals"). n8n polls the app for new events at a configurable interval.

5. **Handle trigger data.** After the trigger fires, the data is available to downstream nodes. Use the expression editor to reference trigger fields: {{ $json.email }}, {{ $json.company_name }}. Always test with real data to verify field names match.

6. **Add trigger filters.** Not every trigger event needs a full workflow run. Add an IF node immediately after your trigger to filter: only process signups where plan is "pro", only process webhooks where event_type is "deal.created". This prevents unnecessary processing.
