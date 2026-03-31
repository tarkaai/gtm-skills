---
name: postcard-response-tracking
description: Track postcard delivery events and correlate with inbound responses to measure direct mail ROI
category: DirectMail
tools:
  - Lob
  - PostHog
  - Attio
  - n8n
fundamentals:
  - lob-campaign-tracking
  - posthog-custom-events
  - attio-contacts
  - attio-deals
  - n8n-triggers
  - n8n-workflow-basics
---

# Postcard Response Tracking

This drill sets up the measurement infrastructure to know whether your postcards drove responses. It connects Lob delivery webhooks to your CRM and analytics, then correlates inbound activity (URL visits, meeting bookings, emails) with postcard delivery dates to calculate true direct mail ROI.

## Input

- A completed postcard campaign with postcard IDs stored in Attio (from the `postcard-campaign-send` drill)
- PostHog with event tracking on your website/booking page
- n8n instance for webhook processing
- Lob webhook configured to send events to your n8n endpoint

## Steps

### 1. Configure Lob webhooks

In the Lob dashboard (https://dashboard.lob.com/webhooks), create a webhook pointing to your n8n webhook URL. Subscribe to these events:
- `postcard.in_transit`
- `postcard.in_local_area`
- `postcard.delivered`
- `postcard.returned_to_sender`

Use the `lob-campaign-tracking` fundamental for details on webhook payload format.

### 2. Build the n8n delivery tracking workflow

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow:

**Trigger:** Webhook node receiving Lob events

**Steps:**
1. Parse the event type and postcard ID from the payload
2. Look up the contact in Attio by the `direct_mail_postcard_id` field using `attio-contacts`
3. Update the contact record:
   - `direct_mail_status` = event type (in_transit, delivered, returned_to_sender)
   - `direct_mail_delivered_date` = event timestamp (if delivered)
4. Fire a PostHog event using `posthog-custom-events`:
   - Event name: `direct_mail_{{event_type}}` (e.g., `direct_mail_delivered`)
   - Properties: contact_id, campaign_id, variant, delivered_date
5. If event is `returned_to_sender`, tag the contact as `bad_address` in Attio

### 3. Set up response attribution

Responses to direct mail come through multiple channels. Track each:

**Tracking URL visits:**
- The personalized URL (`/dm?ref={{contact_id}}&v={{variant}}&c={{campaign}}`) should fire a PostHog event: `direct_mail_url_visited` with the parsed query parameters
- In n8n, when this event fires, update Attio: `direct_mail_responded = true`, `direct_mail_response_type = url_visit`, `direct_mail_response_date`

**Meeting bookings (via Cal.com or similar):**
- When a meeting is booked, check if the booker's email matches a contact who received a postcard in the last 14 days
- If match: attribute the meeting to direct mail. Update Attio: `direct_mail_response_type = meeting_booked`
- Fire PostHog event: `direct_mail_meeting_booked` with contact_id, campaign_id, variant, days_since_delivery

**Inbound email replies:**
- If a prospect emails you mentioning the postcard or referencing the offer, manually log in Attio: `direct_mail_response_type = email_reply`

**Phone calls:**
- If using a dedicated phone number or tracking number on the postcard, log calls as `direct_mail_response_type = phone_call`

### 4. Build the attribution window

Direct mail has a longer response window than digital channels. Set the attribution window:
- **Primary window:** 0-14 days after delivery — responses in this window are attributed to the postcard
- **Extended window:** 15-30 days after delivery — responses are attributed as "assisted" (postcard may have contributed but wasn't the only factor)
- **Outside window:** 30+ days — do not attribute to direct mail

In n8n, build this logic: when any inbound event fires for a contact, check if they received a postcard within the attribution window. If yes, tag the response accordingly.

### 5. Calculate campaign metrics

Build a PostHog dashboard (or n8n reporting workflow) that computes:

- **Delivery rate:** postcards_delivered / postcards_sent
- **Response rate:** contacts_responded (within 14 days) / postcards_delivered
- **Meeting rate:** meetings_booked (attributed) / postcards_delivered
- **Cost per response:** total_campaign_cost / contacts_responded
- **Cost per meeting:** total_campaign_cost / meetings_booked
- **Pipeline generated:** total deal value of meetings attributed to direct mail
- **ROI:** (pipeline_generated - total_campaign_cost) / total_campaign_cost

### 6. Generate the campaign report

At the end of the attribution window (14 days after last delivery), generate a summary:
- Postcards sent, delivered, returned
- Responses by type (URL visit, meeting, email, phone)
- Response rate by variant (for A/B analysis)
- Cost per meeting
- Pipeline generated
- Comparison to digital outreach benchmarks (cold email typical: 1-3% reply, direct mail typical: 2-5% response)

Log the report as a PostHog event: `direct_mail_campaign_report` and store in Attio as a campaign note.

## Output

- Real-time delivery tracking from Lob webhooks to Attio
- Automated response attribution across URL visits, meetings, emails, and calls
- Campaign-level metrics (delivery rate, response rate, cost per meeting, ROI)
- A/B variant performance comparison
- Full campaign report with pipeline attribution

## Triggers

- Webhook-driven (runs automatically as Lob events arrive)
- Campaign report generated 14 days after last postcard delivery
