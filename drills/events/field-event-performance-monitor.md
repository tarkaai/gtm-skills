---
name: field-event-performance-monitor
description: Continuous monitoring and reporting for a multi-city field event series, surfacing degradation, city-level comparison, and optimization opportunities
category: Events
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
  - attio-lists
---

# Field Event Performance Monitor

This drill builds the always-on monitoring layer for a multi-city field event series. It detects when any part of the event funnel degrades, compares city-level performance, identifies seasonal patterns, and generates periodic health reports. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

Field event monitoring is more complex than webinar monitoring because each event is a small-sample, high-touch interaction. Individual event metrics are noisy due to small attendee counts (8-40 per event). This drill emphasizes rolling averages across 4+ events, city-level comparisons, and trend detection rather than single-event judgments.

## Input

- PostHog tracking configured with the field event taxonomy (from `posthog-gtm-events` and `field-event-ops` drills)
- At least 4 completed events in the series (minimum data for rolling averages)
- Attio event records with venue, city, cost, and attendance data

## Steps

### 1. Build post-event automated health checks

Using `n8n-scheduling`, create a workflow that fires 48 hours after each event (triggered by the `field_event_attended` PostHog event):

**Immediate health check metrics:**
- Show rate: confirmed RSVPs who attended / total confirmed RSVPs. Alert if <60% (field events should be 70-85%)
- RSVP conversion: confirmed RSVPs / invitations sent. Compare against 4-event rolling average
- Engagement distribution: % Tier 1 + Tier 2 / total attendees. Alert if <40% (too many low-engagement attendees)
- Cost per attendee: total venue + F&B cost / attendees. Compare against city average

**Post-event check (T+14 days):**
- Meetings booked from this event's nurture sequences
- Deals created attributed to this event
- Nurture reply rate by tier
- No-show rate for confirmed RSVPs

Log all metrics in PostHog as `field_event_health_check` events and in Attio on the event record.

### 2. Build rolling trend analysis

Using `n8n-scheduling`, create a weekly cron job that:

1. Pulls all field event metrics for the last 8 events using `posthog-dashboards`
2. Computes 4-event rolling averages for: RSVP rate, show rate, meetings per event, cost per meeting, Tier 1 percentage
3. Compares the most recent 2 events against the rolling average
4. Classifies each metric:
   - **Healthy:** Within +/-15% of rolling average
   - **Watch:** 15-25% below rolling average for 2+ events
   - **Alert:** >25% below rolling average or >30% drop from previous event
   - **Improving:** >15% above rolling average for 2+ events

If any metric hits "Alert" status, trigger a Slack notification with the metric, current value, rolling average, and a suggested diagnostic action.

### 3. Build city-level comparison

Using `posthog-dashboards`, create a city comparison dashboard updated after each event:

**Per-city scorecard:**
- RSVP rate (invites → confirmed)
- Show rate (confirmed → attended)
- Tier 1 rate (attended → high-intent)
- Conversion rate (attended → meeting booked)
- Cost per meeting
- Pipeline generated
- Repeat attendance rate across events in this city

**City health ratings:**
- GREEN: RSVP rate >15%, show rate >70%, conversion rate above series average
- YELLOW: Any metric 10-25% below series average
- RED: Any metric >25% below series average for 2+ consecutive events in that city

Using `attio-reporting`, flag cities that are consistently RED for strategic review: should the event format change? Is the ICP density lower than estimated? Should this city be deprioritized?

### 4. Detect seasonal and market patterns

Over a 6+ month series, the monitoring system should track:

- **Seasonal patterns:** Do events in certain months perform better? (Avoid holiday weeks, end-of-quarter budget-freeze periods, summer vacation windows)
- **Day-of-week patterns:** Do Tuesday dinners outperform Thursday happy hours in the same city?
- **Format patterns:** Compare dinner vs happy hour vs lunch performance across the series
- **Topic fatigue:** Are events on the same topic category performing worse over time?
- **List fatigue:** Is the RSVP rate declining in cities where you have run 3+ events? (audience exhaustion signal)

Store pattern findings in Attio as series-level notes. Feed them into the `autonomous-optimization` drill for hypothesis generation.

### 5. Generate monthly series health reports

Using `n8n-scheduling`, create a monthly cron that aggregates all events in the past 30 days:

**Monthly report structure:**
- Events held: count, cities, formats
- Total attendees, total meetings booked, total pipeline generated
- Series-level funnel: invites → RSVPs → attended → meetings → deals
- City scorecard summary (GREEN/YELLOW/RED per city)
- Cost analysis: total spend, cost per attendee, cost per meeting, cost per $ pipeline
- Metric trends: which metrics improved, which degraded
- Top insight: the most notable pattern or finding from this month's events
- Recommendation: what to change, test, or investigate next month

Post the report to Slack and store in Attio.

### 6. Generate event post-mortems

14 days after each event (when the nurture window closes), auto-generate a structured post-mortem:

- **Metrics vs targets:** RSVP rate, show rate, engagement distribution, meetings booked
- **What worked:** Which invitation segment had the best RSVP rate? Which tier converted best?
- **What needs attention:** Any metric below the 4-event rolling average? Venue issues? Topic mismatch?
- **Venue rating update:** Was the venue appropriate? Rate and update the venue database.
- **Recommendations:** Specific suggestions for the next event in this city

Store the post-mortem in Attio on the event record.

## Output

- Post-event health checks firing 48 hours and 14 days after each event
- Weekly rolling trend analysis with alert system
- City comparison dashboard in PostHog
- Monthly series health reports posted to Slack
- Event post-mortems generated and stored in Attio
- Seasonal and market pattern detection feeding into optimization

## Triggers

- Post-event: T+48 hours (immediate health check), T+14 days (post-mortem)
- Weekly: rolling trend analysis (n8n cron)
- Monthly: series health report (n8n cron)
- On-demand: city comparison dashboard always available in PostHog
