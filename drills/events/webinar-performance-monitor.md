---
name: webinar-performance-monitor
description: Continuous monitoring and reporting for webinar series health, surfacing degradation and opportunities across the full event funnel
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

# Webinar Performance Monitor

This drill builds the always-on monitoring layer for your webinar series. It detects when any part of the webinar funnel degrades, surfaces opportunities for improvement, and generates periodic performance reports. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- At least 4 completed webinars with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill
- n8n instance for scheduled monitoring workflows
- Attio with event tracking lists populated

## Steps

### 1. Define the webinar health metrics

Build a monitoring framework around five metric categories:

**Demand metrics (pre-event):**
- Registration rate: page visitors who register (target: >25%)
- Registrations per event: total sign-ups (benchmark against 4-event rolling average)
- Promotion channel yield: registrations per channel (email, LinkedIn, personal, paid)
- Registration velocity: registrations per day during the promotion window

**Commitment metrics (event day):**
- Show rate: registrants who attend (target: >30%)
- Drop-off rate: attendees who leave before the midpoint (target: <20%)
- Engagement rate: attendees who ask a question, respond to a poll, or click a CTA (target: >25%)

**Conversion metrics (post-event):**
- Follow-up reply rate: nurture email replies / attendees (target: >10%)
- Meeting booking rate: meetings booked / attendees (target: >8%)
- Recording consumption rate: no-shows who watch the recording (target: >40%)

**Pipeline metrics (lagging):**
- Deals created from webinar leads (track with 30-day attribution window)
- Average deal value from webinar-sourced leads
- Webinar-to-close conversion rate (90-day window)

**Series health metrics (aggregate):**
- Repeat attendance rate: % of attendees who attend 2+ events in a quarter
- List growth rate: net new registrants per event
- Topic saturation index: declining registration for similar topics signals audience fatigue

### 2. Build the monitoring dashboard in PostHog

Using `posthog-dashboards`, create a "Webinar Series Health" dashboard with these panels:

- **Top row (headline metrics)**: Current event registrations vs target, show rate trend (last 6 events), meetings booked this month vs target
- **Middle row (funnel)**: Registration-to-meeting funnel for the last event, compared to the series average
- **Bottom row (trends)**: Registration trend line (last 12 events), show rate by day-of-week, promotion channel effectiveness over time

Using `posthog-funnels`, create a saved funnel: `webinar_page_viewed` → `webinar_registered` → `webinar_reminder_clicked` → `webinar_attended` → `webinar_question_asked` → `webinar_nurture_reply_received` → `webinar_nurture_meeting_booked`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build a monitoring workflow that runs after each event completes:

**Immediate checks (2 hours post-event):**
- Show rate: if <20% (vs target 30%), fire alert: "Show rate critically low — review reminder cadence and event timing"
- Engagement rate: if <10% (vs target 25%), fire alert: "Engagement critically low — review content format and interactivity"

**48-hour checks (post-nurture launch):**
- Follow-up email open rate: if <30%, fire alert: "Nurture email open rate below threshold — review subject lines and send timing"
- Reply rate: if Tier 1 reply rate <15% (vs target 30%), fire alert: "High-intent attendee replies low — review personalization quality"

**Rolling checks (weekly via n8n cron):**
- Compare the last event's funnel to the 4-event rolling average
- If any metric declines >15% from the rolling average, flag for investigation
- If registrations decline for 3 consecutive events, fire alert: "Registration trend declining — investigate topic fatigue or promotion channel saturation"

### 4. Generate event-level post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 14 days after each event (when nurture window closes):

1. Pull all PostHog events for this webinar slug
2. Calculate every metric in the health framework (Step 1)
3. Compare each metric to: (a) the target, (b) the 4-event rolling average, (c) the best-ever event
4. Generate a structured post-mortem:

```
## Event Post-Mortem: [Topic] — [Date]

### Headline
[One sentence: "Registration exceeded target by X% but show rate declined Y% from average"]

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Registrations | 50 | 63 | +18% | PASS |
| Show rate | 30% | 24% | -12% | WATCH |
| ...

### What Worked
[2-3 bullet points on metrics that exceeded targets, with hypothesized reasons]

### What Needs Attention
[2-3 bullet points on underperforming metrics, with hypothesized causes]

### Recommendations for Next Event
[2-3 specific, actionable suggestions based on the data]
```

5. Store the post-mortem in Attio as a note on the event record using `attio-lists`
6. Post a summary to Slack

### 5. Build the monthly series report

Using `n8n-scheduling`, create a monthly workflow that:

1. Aggregates all event post-mortems from the month
2. Calculates series-level trends: registration growth, show rate trend, pipeline generated, cost per meeting
3. Compares this month's performance to last month and to the series lifetime average
4. Generates a monthly report:

```
## Monthly Webinar Series Report — [Month Year]

### Events This Month: [N]
### Total Registrations: [N] (vs [N] last month)
### Average Show Rate: [X]% (trend: [up/down/flat])
### Meetings Booked: [N] (vs [N] last month)
### Pipeline Generated: $[X]

### Top Performing Event: [Topic] — [Why]
### Underperforming Event: [Topic] — [Why]

### Series Health: [GREEN/YELLOW/RED]
[One paragraph assessment of overall series health]

### Recommendations
1. [Specific recommendation with supporting data]
2. [Specific recommendation with supporting data]
3. [Specific recommendation with supporting data]
```

5. Store in Attio using `attio-reporting` and post to Slack

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect anomalies in any webinar funnel metric
- Generate hypotheses about what to change (topic, timing, format, promotion, nurture sequence)
- Design experiments (A/B test different promotion approaches, nurture sequences, or event formats)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
