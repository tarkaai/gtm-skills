---
name: sms-performance-monitor
description: Build dashboards, anomaly alerts, and automated weekly briefs for SMS outbound performance
category: SMS
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# SMS Performance Monitor

Build the monitoring and reporting layer for SMS outbound. Tracks delivery rates, reply rates, sentiment, opt-out rates, and pipeline impact. Feeds data to the `autonomous-optimization` drill at Durable level.

## Prerequisites

- PostHog tracking configured with SMS events (from `posthog-gtm-events` drill)
- Attio with contacts and deals tracking SMS activity
- Twilio status callbacks flowing to PostHog via n8n
- At least 1 week of SMS outbound data

## Steps

### 1. Define the SMS event taxonomy

Using the `posthog-custom-events` fundamental, verify these events are firing:

**Send events:**
- `sms_sent` — properties: campaign_id, sequence_step, message_variant, prospect_tier, send_hour, timezone
- `sms_delivered` — properties: campaign_id, sequence_step, delivery_time_seconds
- `sms_failed` — properties: campaign_id, error_code, error_message
- `sms_undelivered` — properties: campaign_id, carrier_error

**Response events:**
- `sms_replied` — properties: campaign_id, sequence_step, sentiment (positive/negative/neutral/question), time_to_reply_hours
- `sms_opt_out` — properties: campaign_id, sequence_step, opt_out_keyword

**Conversion events:**
- `sms_meeting_booked` — properties: campaign_id, sequence_step, prospect_tier, first_touch_channel
- `sms_deal_created` — properties: campaign_id, deal_value, prospect_tier

### 2. Build the SMS outbound dashboard

Using the `posthog-dashboards` fundamental, create "SMS Outbound — Performance":

**Row 1 — Volume & Delivery:**
- Daily SMS send volume (bar chart, 30-day view)
- Delivery rate trend (line chart: delivered / (delivered + failed + undelivered))
- Failed/undelivered breakdown by error code (pie chart)

**Row 2 — Response Funnel:**
- SMS funnel: sent -> delivered -> replied -> meeting_booked
- Reply rate by sequence step (bar chart: step 1/2/3)
- Sentiment breakdown of replies (stacked bar: positive/negative/neutral/question)

**Row 3 — Conversion & Pipeline:**
- Meetings booked from SMS this month (number)
- SMS-sourced pipeline value (number)
- Response rate trend (line chart, weekly)
- Average time-to-reply in hours (number)

**Row 4 — Health & Compliance:**
- Opt-out rate trend (line chart — alarm if >5%)
- Delivery rate by carrier (if available from Twilio)
- Suppression list growth (cumulative)
- Cost per reply (total SMS spend / positive replies)

### 3. Configure anomaly detection

Using `posthog-anomaly-detection`, set alerts:

- Delivery rate drops below 90% for 2 consecutive days
- Reply rate drops below 1% for 5 consecutive days (at 50+ daily sends)
- Opt-out rate exceeds 5% of sends in any single day
- Zero replies for 3 consecutive business days (at 20+ daily sends)
- Failed message rate exceeds 10% in any single day
- Negative sentiment replies exceed 40% of all replies in a week

Route alerts to Slack and log in Attio as campaign notes.

### 4. Build weekly SMS brief

Create an n8n workflow via `n8n-scheduling`, triggered every Monday 8am:

1. Pull last 7 days of SMS events from PostHog
2. Pull Attio deal data for SMS-sourced pipeline
3. Calculate: delivery rate, reply rate per step, positive reply rate, opt-out rate, meetings booked, cost per meeting
4. Compare against 4-week rolling average
5. Generate brief:
   - Volume: X messages sent, Y delivered, Z replied
   - Response rate: X% (delta from last week)
   - Best-performing message variant and segment
   - Opt-out rate: X% (flag if trending up)
   - Meetings booked: X (pipeline value: $Y)
   - Recommended actions for next week
6. Post to Slack and store in Attio

### 5. Build monthly trend report

Monthly n8n workflow:

1. Aggregate 30 days of SMS data
2. Calculate: cost per meeting from SMS, response rate trend, opt-out trend, message fatigue indicators
3. Compare SMS performance against other outbound channels (email, LinkedIn, calls) if data available
4. Generate recommendations: scale, maintain, reduce, or pause SMS based on relative cost-per-meeting

## Output

- Live PostHog dashboard for SMS outbound
- Weekly automated briefs with response rates and pipeline impact
- Monthly trend reports with channel comparison
- Anomaly alerts for delivery, compliance, and performance degradation
- Structured event data feeding the autonomous optimization loop
