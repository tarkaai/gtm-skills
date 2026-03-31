---
name: event-performance-reporting
description: Monitor per-event and per-partner event ROI, surface format/topic winners, and generate weekly event performance briefs
category: Events
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Event Performance Reporting

This drill builds the monitoring and reporting layer for co-hosted partner events. It tracks per-event and per-partner performance, identifies which event formats, topics, and partners produce the most pipeline, and generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- PostHog tracking configured for event registration, attendance, and follow-up events
- Attio event records with partner associations and attendee lists
- Minimum 8 weeks of event data across 3+ events (enough for meaningful comparisons)

## Steps

### 1. Build the event performance dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Co-Hosted Partner Events — Performance" with these panels:

- **Registrations by event** (bar chart): `cohosted_event_registered` events grouped by `event_name`, last 90 days
- **Attendance rate by event** (table): `cohosted_event_attended` / `cohosted_event_registered` per event, sorted descending
- **Engagement by event** (stacked bar): attendees segmented by `engagement_level` (hot/warm/cool) per event
- **Pipeline by partner** (bar chart): `meeting_booked` events where `source = cohosted_event` grouped by `source_partner`, last 90 days
- **Registration-to-pipeline funnel**: `cohosted_event_registered` → `cohosted_event_attended` → `follow_up_replied` → `meeting_booked` → `deal_created`
- **Format comparison** (table): attendance rate, engagement rate, and pipeline per attendee by event format (webinar vs workshop vs roundtable vs dinner)
- **Topic performance** (table): registrations, attendance rate, and pipeline by event topic category
- **Cost per qualified lead by event** (table): total event cost / qualified leads per event

### 2. Create event performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **High-converting events**: Events where >15% of attendees booked a follow-up meeting
- **High-volume partners**: Partners who co-hosted events with >50 registrations
- **Declining partners**: Partners whose event registrations dropped >30% event-over-event
- **Best format**: The event format with the highest attendance-to-pipeline conversion rate

These cohorts feed the `autonomous-optimization` drill's anomaly detection.

### 3. Build the weekly event performance brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Monday 9am):

1. Pull last 7 days of event data from PostHog: registrations for upcoming events, attendance for past events, follow-up engagement
2. Pull event pipeline data from Attio: meetings booked, deals created from event attendees
3. Compare current event cycle metrics to the 4-event rolling average
4. Use the `hypothesis-generation` fundamental to produce insights:
   - Which event formats and topics are overperforming?
   - Which partners drive the highest-quality attendees?
   - What promotion timing/channel produces the most registrations?
   - What should change for the next event?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Co-Hosted Events Weekly Brief — {date}

**Upcoming events**: {count} in next 14 days ({total_registrations} registrations)
**Last event**: {event_name} — {attendees}/{registrations} attended ({attendance_rate}%)
**Pipeline this month**: {meetings_booked} meetings, {deals_created} deals from event attendees

### Partner leaderboard (last 90 days)
1. {partner_1}: {events} events, {total_attendees} attendees, {meetings} meetings
2. {partner_2}: {events} events, {total_attendees} attendees, {meetings} meetings

### Format insights
- Best format: {format} ({attendance_rate}% attendance, {pipeline_rate}% pipeline rate)
- Best topic: {topic} ({registrations} avg registrations)

### Anomalies
- {partner}: Registration rate dropped {pct}% — {hypothesis}
- {format}: Attendance rate spiked {pct}% — {hypothesis}

### Recommended actions for next event
1. {action_1}
2. {action_2}
```

### 4. Build per-partner event ROI tracker

In Attio, maintain these fields on each partner record (updated after each event by n8n):

- **Total co-hosted events**: Count of events with this partner
- **Total attendees sourced**: Attendees who registered through this partner's promotion
- **Total pipeline generated**: Meetings + deals from this partner's events
- **Average attendance rate**: Across all events with this partner
- **Best event format**: The format that performed best with this partner
- **Best event topic**: The topic that drove the most registrations
- **Next event date**: When the next co-hosted event is scheduled
- **Partner event health score**: Composite of recency, attendance trend, and pipeline conversion

### 5. Set up performance alerts

Using PostHog and n8n, configure alerts for:

- Event registrations <50% of target 7 days before event → alert to boost promotion
- Attendance rate drops below 30% for any event → investigate and adjust reminder cadence
- A partner's event produces zero pipeline in 2+ consecutive events → flag for partner review
- An event format achieves >20% attendee-to-meeting conversion → flag as "winning format" for replication
- Total monthly event pipeline drops below Scalable baseline for 2 consecutive months → trigger `autonomous-optimization` investigation

## Output

- PostHog dashboard with per-event, per-partner, and per-format performance
- Weekly automated event brief with insights and recommendations
- Per-partner event ROI tracking in Attio
- Alert system for registration, attendance, and pipeline anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts at the start of Durable level. The weekly brief runs every Monday. Partner ROI fields update after each event via n8n.
