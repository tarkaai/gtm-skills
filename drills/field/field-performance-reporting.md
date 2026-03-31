---
name: field-performance-reporting
description: Generate weekly and monthly field prospecting performance reports with visit-level attribution
category: Field
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - attio-reporting
  - attio-deals
  - n8n-scheduling
  - n8n-workflow-basics
---

# Field Performance Reporting

This drill builds automated reporting for field prospecting that tracks the full funnel from venue visit to closed deal. It connects in-person activity to pipeline and revenue so the founder can make data-driven decisions about where and how often to be in the field.

## Input

- Active PostHog tracking with field visit events (from `field-contact-logging` drill)
- Attio deals with `source: field-visit` attribution
- At least 2 weeks of field data for weekly reports

## Steps

### 1. Define the field prospecting funnel

Using `posthog-custom-events`, ensure these events are being captured with consistent properties:

| Event | Properties | Trigger |
|-------|-----------|---------|
| `field_session_started` | venue_count, planned_duration, territory | Start of a field session |
| `field_visit_completed` | venue, duration_minutes, conversations_count | After each venue visit |
| `field_conversation_logged` | venue, interest_level, pain_identified, outcome | After logging each contact |
| `field_meeting_booked` | venue, contact_name, deal_value_estimate | When a meeting is scheduled |
| `field_deal_created` | venue, contact_name, deal_value, deal_stage | When a deal enters pipeline |
| `field_deal_won` | venue, deal_value, days_to_close | When a field-sourced deal closes |

### 2. Build the weekly report automation

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow that runs every Monday at 8am:

1. **Pull last 7 days of field events from PostHog**: Query the events API for all `field_*` events in the date range.

2. **Pull deal updates from Attio**: Use `attio-deals` to query deals where source = "field-visit" and modified in the last 7 days.

3. **Calculate weekly metrics**:
   - Sessions completed
   - Venues visited
   - Total conversations
   - Meetings booked (and conversion rate: meetings / conversations)
   - Deals created
   - Pipeline value added
   - Deals won (and revenue)
   - Average conversations per session
   - Cost per meeting (estimated: travel time in hours x founder hourly rate)

4. **Compare to previous week and rolling 4-week average**. Flag metrics that changed >20% as noteworthy.

5. **Generate the report**:

```
## Field Prospecting Weekly Report — Week of [Date]

### Activity
- Sessions: [X] (prev: [Y])
- Venues visited: [X]
- Conversations: [X] (prev: [Y])

### Results
- Meetings booked: [X] ([Z]% conversion)
- Deals created: [X] ($[V] pipeline)
- Deals won: [X] ($[V] revenue)

### Trends
- Conversation-to-meeting rate: [X]% (4-wk avg: [Y]%)
- Pipeline per session: $[X] (4-wk avg: $[Y])
- [Notable change: e.g., "Meeting rate up 35% this week — likely due to Tuesday WeWork sessions"]

### Top Performing This Week
- Best venue: [Venue] — [X] meetings from [Y] conversations
- Best day: [Day] — [X]% conversion rate

### Next Week Plan
- Planned sessions: [X]
- Venues: [list]
- Focus: [specific goal, e.g., "Test 2 new venues in North Austin"]
```

6. **Deliver the report**: Post to Slack channel and store as a note on the "Field Prospecting" campaign record in Attio.

### 3. Build the monthly report automation

A separate n8n workflow running on the 1st of each month that produces a deeper analysis:

- All weekly metrics aggregated
- Venue-level performance rankings
- Territory-level ROI (pipeline / time invested)
- Month-over-month trend comparison
- Cohort analysis: of meetings booked this month, how many converted to deals?
- Recommendations: which venues to keep, drop, or add

### 4. Set up alert thresholds

Using `n8n-workflow-basics`, add alert conditions to the weekly workflow:

- **Meeting rate drops below 10%**: Alert — "Field conversion declining. Review messaging or venue selection."
- **Zero meetings in a week with 2+ sessions**: Alert — "No meetings from field visits this week. Diagnose: wrong venues, wrong times, or wrong pitch?"
- **Deal win from field source**: Celebration alert — "Field-sourced deal won: [Company] for $[Value]!"

### 5. Connect to the threshold engine

Integrate with the play-level threshold engine:
- Smoke: >= 1 meeting in 1 week
- Baseline: >= 2 meetings over 2 weeks
- Scalable: >= 8 meetings over 2 months
- Durable: Sustained or improving metrics over 6 months

The weekly report should explicitly state: "Current level: [Level]. Progress toward threshold: [X/Y meetings]."

## Output

- Automated weekly field report delivered every Monday
- Automated monthly deep-dive report on the 1st
- Alert notifications for metric anomalies
- All reports stored in Attio for historical reference
- Clear threshold tracking showing progress toward the next level

## Triggers

- Weekly report: runs automatically via n8n cron every Monday at 8am
- Monthly report: runs automatically on the 1st of each month
- Alerts: fire in real-time when conditions are met
