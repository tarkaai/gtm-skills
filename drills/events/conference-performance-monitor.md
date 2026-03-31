---
name: conference-performance-monitor
description: Continuous monitoring and year-over-year reporting for annual user conferences, tracking registration funnels, session engagement, pipeline impact, and attendee satisfaction trends
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

# Conference Performance Monitor

This drill builds the always-on monitoring and reporting layer for your annual user conference program. It tracks every stage of the conference funnel across years, detects trends and anomalies in promotion effectiveness, attendee engagement, and pipeline generation, and produces structured post-conference reports that feed into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- At least 1 completed conference with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill with conference-specific events
- n8n instance for scheduled monitoring workflows
- Attio with conference registrant and attendee lists populated

## Steps

### 1. Define the conference health metrics

Build a monitoring framework around six metric categories:

**Demand metrics (pre-conference, tracked during promotion window):**
- Registration rate: page visitors who register (target: >15% -- lower than webinars due to higher commitment)
- Total registrations (benchmark against prior year or capacity target)
- Registration source breakdown: email, LinkedIn, personal invite, paid, referral, organic
- Registration velocity: registrations per week during promotion window, by source
- Early bird conversion rate: what percentage of registrations happen in the first 30% of the promotion window

**Commitment metrics (conference day):**
- Show rate: registrants who attend at least 1 session (target: >60% for virtual, >80% for in-person paid)
- Session coverage: average sessions attended per attendee out of total sessions offered
- Drop-off rate: attendees who leave before the final keynote (target: <30%)
- Engagement rate: attendees who ask a question, respond to a poll, or interact in chat (target: >30%)

**Content metrics (per session):**
- Attendance per session: which sessions drew the most attendees
- Engagement density per session: questions + poll responses per attendee
- Session ratings: from post-event feedback survey (target: >4.0/5.0 average)
- Speaker effectiveness: correlation between speaker engagement and session ratings

**Conversion metrics (post-conference, 30-day window):**
- Follow-up email reply rate: nurture email replies / attendees (target: >15%)
- Meeting booking rate: meetings booked / attendees (target: >10%)
- Feedback survey completion rate: responses / attendees (target: >30%)
- NPS score from feedback survey (target: >50)

**Pipeline metrics (lagging, 90-day window):**
- Deals created from conference attendees
- Expansion revenue from conference-sourced deals
- Conference-to-close conversion rate
- Average deal value from conference leads vs. other sources

**Program health metrics (year-over-year):**
- Attendance growth rate YoY (target: >=15%)
- Repeat attendee rate: what percentage of this year's attendees also attended last year
- Net new attendee acquisition: first-time attendees as percentage of total
- Cost per attendee and cost per pipeline dollar generated
- Attendee LTV: do conference attendees have higher retention and expansion than non-attendees?

### 2. Build the conference dashboard in PostHog

Using `posthog-dashboards`, create a "Conference Program Health" dashboard:

- **Top row (headline metrics)**: Current conference registrations vs target, show rate vs last year, total pipeline generated from conference program
- **Middle row (funnel)**: Full conference funnel for the most recent event: `conference_page_viewed` -> `conference_registered` -> `conference_attended` -> `conference_session_attended` (3+) -> `conference_engaged` -> `conference_meeting_booked`
- **Bottom row (trends)**: Registration trend by week (line chart showing promotion effectiveness over time), session attendance heatmap (which time slots and topics draw the most), promotion channel effectiveness (bar chart by source)

Using `posthog-funnels`, create saved funnels:
- Registration funnel: `conference_page_viewed` -> `conference_registered` -> `conference_reminder_clicked` -> `conference_attended`
- Engagement funnel: `conference_attended` -> `conference_session_attended` (2+) -> `conference_engaged` -> `conference_feedback_submitted` -> `conference_meeting_booked`
- Pipeline funnel: `conference_meeting_booked` -> `deal_created` (source=conference) -> `deal_won`

### 3. Configure promotion-period monitoring

Using `n8n-scheduling`, build workflows that run during the 10-16 week promotion window:

**Weekly promotion health check:**
- Pull registration count from PostHog and compare against the week-by-week target curve (exponential: slow start, acceleration in final 4 weeks)
- Calculate registrations by source channel this week vs. last week
- If total registrations are >20% below the target curve at any checkpoint, fire alert: "Registration pace below target -- consider additional promotion channels or deadline extensions"
- If a previously strong channel drops >30% week-over-week, fire alert: "Channel [X] registration decline -- investigate fatigue or deliverability"

**Daily registration monitoring (final 2 weeks):**
- Track daily registrations and compare against the final-push target
- Monitor email metrics: if invite email open rates drop below 20%, fire alert for subject line refresh

### 4. Configure post-conference analysis

Using `n8n-workflow-basics`, build a workflow triggered 30 days after the conference (when the post-event attribution window closes):

1. Pull all PostHog events with the conference slug
2. Calculate every metric in the health framework (Step 1)
3. Compare each metric to: (a) the pre-conference target, (b) prior year's conference (if available), (c) industry benchmarks
4. Generate a structured post-conference report:

```
## Conference Post-Mortem: [Conference Name] -- [Date]

### Headline
[One sentence: "Attendance exceeded target by X% with Y expansion meetings booked, Z% NPS"]

### Metrics vs Targets
| Metric | Target | Actual | vs Last Year | Status |
|--------|--------|--------|--------------|--------|
| Registrations | 200 | 237 | +31% | PASS |
| Show rate | 60% | 68% | +5pp | PASS |
| Sessions per attendee | 3.0 | 3.4 | +0.6 | PASS |
| Meetings booked | 20 | 18 | +2 | WATCH |
| NPS | 50 | 62 | +8 | PASS |
...

### Top Sessions (by attendance + engagement)
1. [Session title] -- [attendance], [engagement rate], [rating]
2. ...

### Promotion Channel Analysis
| Channel | Registrations | Cost | Cost per Reg | Show Rate |
|---------|--------------|------|--------------|-----------|
| Email (customer list) | 89 | $0 | $0 | 72% |
| Clay prospecting | 43 | $185 | $4.30 | 58% |
| LinkedIn organic | 31 | $0 | $0 | 61% |
...

### What Worked
[2-3 bullet points on metrics that exceeded targets, with hypothesized reasons]

### What Needs Attention
[2-3 bullet points on underperforming metrics, with hypothesized causes]

### Recommendations for Next Year
[3-5 specific, actionable suggestions based on the data]
```

5. Store the post-mortem in Attio using `attio-reporting`
6. Post a summary to Slack

### 5. Build the annual program review

Using `n8n-scheduling`, create a workflow that runs 60 days post-conference to capture lagging pipeline data:

1. Pull all deals with conference source attribution
2. Calculate pipeline generated, deals closed, and revenue from conference leads
3. Compare cost (venue, A/V, catering, promotion, tools) against revenue generated
4. Calculate conference ROI: (Revenue generated - Total cost) / Total cost
5. Generate the annual conference ROI report with recommendations for next year's budget and format

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect when promotion effectiveness declines (topic fatigue, channel saturation)
- Generate hypotheses about what to change (agenda structure, session formats, promotion timing, speaker selection, pricing)
- Design year-over-year experiments (A/B test different registration incentives, session formats, or follow-up approaches)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
