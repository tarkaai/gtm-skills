---
name: gift-tracking-attribution
description: Track gift delivery status and attribute downstream responses (meetings, replies, pipeline) to specific gift sends
tool: PostHog
product: PostHog
difficulty: Config
---

# Gift Tracking & Attribution

Set up event tracking and response attribution for outbound gift campaigns. This fundamental configures the PostHog event taxonomy and attribution logic that connects a gift send to downstream outcomes (meeting booked, email reply, deal created).

## Event Taxonomy

Define these PostHog events for gift campaign tracking:

### Send Events
- `gift_sent` — A gift was sent to a prospect
  - Properties: `contact_id`, `campaign_id`, `gift_type` (physical|egift|book|swag), `gift_value`, `platform` (sendoso|tremendous|reachdesk|giftsenda), `variant_id`, `signal_type`
- `gift_delivered` — Platform confirms delivery
  - Properties: `contact_id`, `campaign_id`, `gift_type`, `days_to_deliver`, `platform`
- `gift_failed` — Delivery failed (returned, bad address, etc.)
  - Properties: `contact_id`, `campaign_id`, `failure_reason`, `platform`

### Response Events
- `gift_response` — Any response attributed to a gift
  - Properties: `contact_id`, `campaign_id`, `response_type` (email_reply|meeting_booked|linkedin_reply|phone_call|url_visit), `days_since_delivery`, `gift_type`, `gift_value`
- `gift_meeting_booked` — Meeting specifically attributed to a gift
  - Properties: `contact_id`, `campaign_id`, `gift_type`, `days_since_delivery`, `meeting_source` (direct|follow_up_email|follow_up_linkedin)
- `gift_url_visited` — Prospect visited the personalized tracking URL
  - Properties: `contact_id`, `campaign_id`, `variant_id`

### Pipeline Events
- `gift_deal_created` — Deal in CRM attributed to a gift campaign
  - Properties: `contact_id`, `campaign_id`, `deal_value`, `days_since_gift`

## Attribution Window

A response is attributed to a gift if it occurs within 30 days of confirmed delivery. For physical gifts, the attribution clock starts at delivery confirmation; for eGifts, it starts at send time (instant delivery).

## Tracking URL Setup

For each gift recipient, generate a personalized tracking URL:
```
https://{{your_domain}}/gift?ref={{contact_id}}&c={{campaign_id}}&v={{variant_id}}
```

This URL should:
1. Fire a PostHog `gift_url_visited` event with the contact_id, campaign_id, and variant_id
2. Redirect to your booking page (Cal.com) or landing page

Implement via a lightweight redirect handler (Vercel edge function, Cloudflare Worker, or n8n webhook).

## PostHog Configuration

### Create Event Definitions

Use the PostHog MCP or API to define each event with its properties:

```
POST https://app.posthog.com/api/projects/{{project_id}}/event_definitions/
Authorization: Bearer {{POSTHOG_API_KEY}}
Content-Type: application/json

{
  "name": "gift_sent",
  "description": "A gift was sent to a prospect via an outbound gift campaign"
}
```

Repeat for each event in the taxonomy above.

### Create Attribution Dashboard

Use `posthog-dashboards` fundamental to create a dashboard with:
- Gift send volume (daily/weekly trend)
- Delivery success rate
- Response rate by gift type
- Response rate by signal type
- Cost per response
- Cost per meeting
- Pipeline attributed to gifts

## CRM Sync

After tracking events in PostHog, sync key status updates back to the CRM (Attio) using the `attio-contacts` fundamental:
- Update contact record with `gift_sent_date`, `gift_type`, `gift_status`, `gift_response_date`, `gift_response_type`
- Log each gift as a note on the contact timeline

## Error Handling

- If a gift delivery webhook arrives but the contact_id is unknown in PostHog, log the event with a `contact_unknown` flag and alert for investigation
- If attribution window passes with no response, fire a `gift_no_response` event for funnel analysis
- If multiple gifts are sent to the same contact, attribute responses to the most recent delivered gift
