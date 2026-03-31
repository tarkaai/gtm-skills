---
name: call-performance-reporting
description: Build automated call performance reports tracking connect rates, meeting conversion, and call quality trends over time
category: Outreach
tools:
  - PostHog
  - Attio
  - n8n
  - Fireflies
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - attio-reporting
  - attio-deals
  - n8n-scheduling
  - n8n-workflow-basics
  - fireflies-action-items
---

# Call Performance Reporting

This drill builds the reporting layer that tracks call-based outreach performance over time. It captures per-call outcomes, aggregates them into weekly trends, detects degradation, and generates actionable briefs. Designed for plays where the founder or a small team makes direct calls to qualified prospects.

## Prerequisites

- Attio CRM with call activity logging in place (each call logged as a note with structured outcome data)
- PostHog tracking configured for call events (`call_attempted`, `call_connected`, `call_meeting_booked`)
- Fireflies transcribing prospect calls (for call quality analysis)
- n8n instance running

## Steps

### 1. Define the call event taxonomy

Using the `posthog-custom-events` fundamental, ensure these events are firing:

- `call_attempted` — properties: prospect_id, prospect_tier, signal_type, time_of_day, day_of_week
- `call_connected` — properties: prospect_id, duration_seconds, talk_ratio (agent vs prospect), disposition (meeting_set, follow_up, not_interested, callback, voicemail)
- `call_meeting_booked` — properties: prospect_id, meeting_type, days_to_meeting, source_signal
- `call_no_answer` — properties: prospect_id, attempt_number, voicemail_left (boolean)

If any events are missing, implement them before proceeding.

### 2. Build the call performance dashboard

Using the `posthog-dashboards` fundamental, create a dashboard named "Qualified Prospect Calls — Performance" with these panels:

- **Weekly call volume**: trend line of `call_attempted` events per week
- **Connect rate**: `call_connected` / `call_attempted` as a percentage, trended weekly
- **Meeting conversion rate**: `call_meeting_booked` / `call_connected` as a percentage, trended weekly
- **Best call windows**: heatmap of connect rate by day_of_week and time_of_day
- **Signal effectiveness**: meeting rate broken down by signal_type property
- **Pipeline value from calls**: sum of deal values in Attio where source = "qualified-prospect-calls"
- **Average call duration**: trend of duration_seconds for connected calls

Add threshold indicators: connect rate target (20%), meeting conversion target (10%), minimum weekly call volume.

### 3. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set up alerts for:

- Connect rate drops below 15% for 3 consecutive days
- Meeting conversion rate drops below 5% for 1 week
- Call volume drops below 50% of 4-week average (indicates execution stall)
- Average call duration drops below 60 seconds (conversations are getting cut short)

Route alerts to Slack and log them in Attio as campaign notes.

### 4. Build the weekly call quality report

Create an n8n workflow using `n8n-scheduling` set to run every Monday at 8am:

1. Query PostHog for last 7 days of call events
2. Query Fireflies API using `fireflies-action-items` for transcripts of connected calls
3. Calculate: total calls, connect rate, meeting rate, avg duration, top-performing time slots, top-performing signals
4. Analyze Fireflies transcripts: extract common objections, questions asked, and sentiment patterns
5. Compare this week vs previous 4-week average for each metric
6. Generate a structured weekly brief:
   - Metrics summary with week-over-week delta
   - Top 3 performing signals (which triggers led to most meetings)
   - Most common objections heard this week
   - Recommended call script adjustments based on objection patterns
   - Recommended time windows to prioritize next week
7. Post the brief to Slack and store in Attio as a campaign note

### 5. Build the monthly trend report

Create a separate n8n workflow using `n8n-scheduling` running on the 1st of each month:

1. Query PostHog for last 30 days vs previous 30 days
2. Query Attio using `attio-reporting` for pipeline value and deal progression from call-sourced deals
3. Calculate: month-over-month trend for all core KPIs, cost per meeting (time invested / meetings booked), pipeline velocity (days from first call to meeting to deal)
4. Identify: which ICP segments have the highest meeting rate, which have decayed, whether any segments should be added or retired
5. Generate the monthly report and distribute to Slack

### 6. Feed data back to optimization

The reports from this drill are the primary input for the `autonomous-optimization` drill at Durable level. Ensure all anomaly detections and weekly metric summaries are stored in a format that the optimization loop can consume: PostHog events with structured properties, not just Slack messages.

## Output

- A live PostHog dashboard with real-time call metrics
- Weekly automated briefs with actionable recommendations
- Monthly trend reports connecting call activity to pipeline value
- Anomaly alerts that catch degradation before it compounds
