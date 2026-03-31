---
name: outbound-performance-monitor
description: Build always-on dashboards and automated reports tracking multi-channel outbound performance across email, LinkedIn, and calls
category: Outreach
tools:
  - PostHog
  - Attio
  - n8n
  - Instantly
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - instantly-tracking
---

# Outbound Performance Monitor

This drill builds the monitoring and reporting layer for multi-channel outbound plays (email + LinkedIn + calls). It tracks per-channel metrics, cross-channel attribution, and generates automated weekly briefs with recommendations. This is the primary data input for the `autonomous-optimization` drill at Durable level.

## Prerequisites

- PostHog tracking configured for outbound events (from `posthog-gtm-events` drill)
- Attio with deals and contacts tracking outbound activity
- Instantly campaign analytics flowing to PostHog
- n8n instance running
- At least 2 weeks of multi-channel outbound data

## Steps

### 1. Define the outbound event taxonomy

Using the `posthog-custom-events` fundamental, verify these events are firing with correct properties:

**Email events:**
- `email_sent` — properties: campaign_id, sequence_step, subject_variant, prospect_tier
- `email_opened` — properties: campaign_id, sequence_step, open_count
- `email_replied` — properties: campaign_id, sentiment (positive/negative/neutral), sequence_step
- `email_bounced` — properties: campaign_id, bounce_type (hard/soft)

**LinkedIn events:**
- `linkedin_connection_sent` — properties: campaign_id, prospect_tier, message_variant
- `linkedin_connection_accepted` — properties: campaign_id, days_to_accept
- `linkedin_message_sent` — properties: campaign_id, sequence_step, message_variant
- `linkedin_message_replied` — properties: campaign_id, sentiment

**Call events:**
- `call_attempted` — properties: campaign_id, prospect_tier, signal_type, time_of_day
- `call_connected` — properties: campaign_id, duration_seconds, disposition
- `call_meeting_booked` — properties: campaign_id, meeting_type

**Cross-channel events:**
- `meeting_booked` — properties: source_channel (email/linkedin/call), prospect_tier, first_touch_channel, last_touch_channel
- `deal_created` — properties: source_play, source_channel, prospect_tier, deal_value

### 2. Build the multi-channel outbound dashboard

Using the `posthog-dashboards` fundamental, create a dashboard named "Outbound Email/LI/Calls — Performance" with these panels:

**Row 1 — Volume & Activity:**
- Weekly send volume by channel (stacked bar: email, LinkedIn, calls)
- Daily activity heatmap (touches per day of week and hour)

**Row 2 — Channel Conversion Funnels:**
- Email funnel: sent -> opened -> replied -> meeting_booked
- LinkedIn funnel: connection_sent -> accepted -> message_replied -> meeting_booked
- Call funnel: attempted -> connected -> meeting_booked

**Row 3 — Cross-Channel Attribution:**
- Meetings by first-touch channel
- Meetings by last-touch channel
- Average touches to meeting by prospect tier

**Row 4 — Health Metrics:**
- Email deliverability rate (1 - bounce_rate), trended weekly
- LinkedIn acceptance rate, trended weekly
- Call connect rate, trended weekly
- Negative reply rate across channels (guardrail metric)

**Row 5 — Pipeline Impact:**
- Total meetings booked this month
- Pipeline value created from outbound
- Cost per meeting (tool spend / meetings)
- Average days from first touch to meeting

Add threshold indicators from the play's pass criteria at each level.

### 3. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set alerts for:

- Email reply rate drops below 2% for 5 consecutive business days
- LinkedIn acceptance rate drops below 20% for 1 week
- Call connect rate drops below 10% for 1 week
- Meeting volume drops to zero for 5 consecutive business days
- Negative reply rate exceeds 5% on any channel
- Email bounce rate exceeds 3% (domain health risk)

Route all alerts to Slack and log in Attio as campaign notes.

### 4. Build the weekly outbound brief

Create an n8n workflow using `n8n-scheduling` set to run every Monday at 8am:

1. Pull last 7 days of outbound events from PostHog API
2. Pull Instantly campaign analytics using `instantly-tracking`
3. Pull Attio deal data using `attio-reporting` for pipeline created from outbound
4. Calculate per-channel metrics: volume, reply/connect rates, meeting conversion
5. Calculate cross-channel metrics: which channel combinations produce the most meetings, average multi-touch sequence length
6. Compare this week vs 4-week rolling average for each metric
7. Generate the weekly brief:
   - Channel-by-channel metrics summary with week-over-week delta
   - Top-performing prospect segments (by tier, industry, signal)
   - Best-performing message variants per channel
   - Channel mix recommendation (shift effort toward highest-converting channel)
   - Specific action items for next week
8. Post to Slack and store in Attio

### 5. Build the monthly trend report

Create a monthly n8n workflow:

1. Aggregate 30 days of data across all channels
2. Calculate: cost per meeting by channel, pipeline velocity by channel, total ROI
3. Identify decaying channels (declining conversion over 4 weeks)
4. Identify emerging winners (improving conversion over 4 weeks)
5. Generate the monthly report with strategic recommendations:
   - Which channels to scale, maintain, or reduce
   - Which ICP segments to add or retire
   - Budget reallocation recommendations based on per-channel CPM (cost per meeting)
6. Distribute to Slack and store in Attio

### 6. Feed data to optimization loop

Ensure all metrics, anomalies, and weekly summaries are stored as structured PostHog events (not just Slack messages) so the `autonomous-optimization` drill can consume them. Each weekly brief should fire a `outbound_weekly_summary` event with properties containing all computed metrics. This creates the data foundation for automated hypothesis generation and experiment design.

## Output

- Live PostHog dashboard with real-time multi-channel outbound metrics
- Weekly automated briefs with per-channel performance and action items
- Monthly trend reports with strategic channel allocation recommendations
- Anomaly alerts that catch degradation before it compounds
- Structured data feed for the autonomous optimization loop

## Triggers

Weekly briefs fire every Monday via n8n cron. Monthly reports fire on the 1st of each month. Dashboard refreshes with live data. Anomaly alerts check daily.
