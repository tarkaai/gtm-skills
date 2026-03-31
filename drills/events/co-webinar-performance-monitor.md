---
name: co-webinar-performance-monitor
description: Continuous monitoring of co-webinar series health including partner contribution balance, cross-event funnel trends, and partner portfolio ROI
category: Events
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
  - attio-lists
  - attio-notes
  - hypothesis-generation
---

# Co-Webinar Performance Monitor

This drill builds the always-on monitoring layer for co-webinar series that tracks not just webinar funnel health (registrations, attendance, pipeline) but also the partner dimension: which partners drive the most registrations, which partner audiences convert best, and when a partner relationship is yielding diminishing returns. Feeds data directly into the `autonomous-optimization` drill at Durable level.

## Prerequisites

- At least 4 completed co-webinars with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill with partner attribution
- n8n instance for scheduled monitoring workflows
- Attio with co-webinar partner records and event tracking lists populated

## Steps

### 1. Define the co-webinar health metrics

Build a monitoring framework around six metric categories:

**Demand metrics (pre-event):**
- Total registrations per event (benchmark against 4-event rolling average)
- Partner-sourced registrations vs your-sourced registrations (the split shows partner promotional effectiveness)
- Registration rate: page visitors who register (target: >25%)
- Registration velocity: registrations per day during the promotion window, broken down by source
- Promotion channel yield: registrations from email, LinkedIn, personal invites, partner promotion

**Commitment metrics (event day):**
- Show rate: registrants who attend (target: >35%)
- Show rate by source: do partner-sourced registrants show at the same rate as yours?
- Drop-off rate: attendees who leave before the midpoint (target: <20%)
- Engagement rate: attendees who ask a question, respond to a poll, or click a CTA (target: >25%)

**Conversion metrics (post-event):**
- Follow-up reply rate: nurture email replies / attendees (target: >10%)
- Meeting booking rate: meetings booked / attendees (target: >8%)
- Recording consumption rate: no-shows who watch the recording (target: >40%)
- Partner-sourced-attendee conversion: do leads from the partner's audience convert at the same rate?

**Pipeline metrics (lagging, 30-day attribution):**
- Deals created from co-webinar leads
- Average deal value from co-webinar-sourced leads
- Co-webinar-to-close conversion rate (90-day window)

**Partner health metrics:**
- Partner promotional contribution ratio: what % of registrations did the partner drive vs you?
- Partner audience quality: conversion rate of partner-sourced attendees vs your-sourced attendees
- Partner engagement score: does the partner actively promote, or do you carry the promotional load?
- Repeat partner performance: are subsequent webinars with the same partner improving, flat, or declining?
- Partner diversity: concentration risk — is >40% of pipeline coming from a single partner?

**Series health metrics (aggregate):**
- Repeat attendance rate: % of attendees who attend 2+ co-webinars in a quarter
- List growth rate: net new registrants per event
- Topic saturation index: declining registration for similar topics signals audience fatigue
- Partner pipeline health: ratio of active partners to total pipeline

### 2. Build the co-webinar dashboard in PostHog

Using `posthog-dashboards`, create a "Co-Webinar Series Health" dashboard:

- **Top row (headline metrics)**: Current event registrations vs target, show rate trend (last 6 events), meetings booked this month vs target, active partner count
- **Middle row (funnel)**: Registration-to-meeting funnel for the last event compared to series average. Second funnel: partner-sourced registrant journey vs your-sourced registrant journey
- **Bottom row (trends)**: Registration trend line by partner (stacked area chart, last 12 events), partner contribution ratio over time, show rate by day-of-week, topic performance heatmap
- **Partner row**: Bar chart of meetings by partner (last 90 days), partner audience conversion rate comparison table, partner promotional contribution scorecard

Using `posthog-funnels`, create saved funnels:
- Full co-webinar funnel: `cowebinar_page_viewed` → `cowebinar_registered` → `cowebinar_reminder_clicked` → `cowebinar_attended` → `cowebinar_engaged` → `cowebinar_nurture_reply` → `cowebinar_meeting_booked`
- Partner comparison funnel: same steps filtered by `registration_source = partner` vs `registration_source = own`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build monitoring workflows:

**Immediate checks (2 hours post-event):**
- Show rate: if <20% (vs target 35%), fire alert: "Show rate critically low — review reminder cadence, event timing, and partner promotional quality"
- Engagement rate: if <10% (vs target 25%), fire alert: "Engagement critically low — review content format, interactivity, and whether the topic matched the audience"
- Partner contribution ratio: if partner drove <20% of registrations, fire alert: "Partner underperformed on promotion — investigate partner commitment"

**48-hour checks (post-nurture launch):**
- Follow-up open rate: if <30%, flag for subject line review
- Tier 1 reply rate: if <15%, flag for personalization quality review

**Rolling checks (weekly via n8n cron):**
- Compare the last event's funnel to the 4-event rolling average
- If any metric declines >15% from the rolling average, flag for investigation
- If registrations decline for 3 consecutive events, fire alert: "Registration trend declining — investigate topic fatigue, partner promotional fatigue, or channel saturation"
- If partner-sourced conversion rate drops >25% from historical average, fire alert: "Partner audience quality declining — investigate if partner's audience composition has shifted"
- If concentration risk exceeds 40% (one partner drives >40% of total pipeline), fire alert: "Partner concentration risk — diversify partner portfolio"

### 4. Generate co-webinar post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 14 days after each event:

1. Pull all PostHog events for this co-webinar slug
2. Calculate every metric in the health framework (Step 1)
3. Compare each metric to: (a) the target, (b) the 4-event rolling average, (c) the best-ever event
4. Generate a structured post-mortem using `hypothesis-generation`:

```
## Co-Webinar Post-Mortem: [Topic] with [Partner] — [Date]

### Headline
[One sentence: "Registration exceeded target by X% driven by strong partner promotion but show rate declined Y%"]

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Total registrations | 50 | 63 | +18% | PASS |
| Partner-sourced regs | 25 (50%) | 38 (60%) | +22% | PASS |
| Show rate | 35% | 28% | -8% | WATCH |
| Meetings booked | 5 | 3 | -20% | FAIL |

### Partner Contribution
- Registrations: {partner_pct}% partner-sourced, {own_pct}% your-sourced
- Attendance: Partner-sourced show rate {pct}% vs your-sourced {pct}%
- Conversion: Partner-sourced meeting rate {pct}% vs your-sourced {pct}%
- Partner effort level: {assessment}

### What Worked
[2-3 bullet points with hypothesized reasons]

### What Needs Attention
[2-3 bullet points with hypothesized causes]

### Recommendations for Next Event
[2-3 specific, actionable suggestions]
```

5. Store the post-mortem in Attio as a note on the event record using `attio-notes`
6. Post a summary to Slack

### 5. Build the monthly series report

Using `n8n-scheduling`, create a monthly workflow:

1. Aggregate all event post-mortems from the month
2. Calculate series-level trends including partner portfolio health
3. Generate a monthly report:

```
## Co-Webinar Monthly Report — {month}

### Events This Month: {N}
### Total Registrations: {N} (vs {N} last month)
### Average Show Rate: {X}% (trend: {up/down/flat})
### Meetings Booked: {N} (vs {N} last month)
### Pipeline Generated: ${X}

### Partner Portfolio
| Partner | Events | Regs Driven | Meetings | Audience CVR | Status |
|---------|--------|-------------|----------|-------------|--------|
| {name}  | {n}    | {n}         | {n}      | {pct}%      | Active |

### Top Performing Event: {topic} with {partner} — {why}
### Underperforming Event: {topic} with {partner} — {why}

### Series Health: {GREEN/YELLOW/RED}
{One paragraph assessment}

### Partner Health: {GREEN/YELLOW/RED}
- Partners performing above average: {list}
- Partners declining: {list}
- Partners to replace: {list}
- Pipeline in partner prospect stage: {count}

### Recommendations
1. {Specific recommendation with supporting data}
2. {Specific recommendation with supporting data}
3. {Specific recommendation with supporting data}
```

5. Store in Attio using `attio-reporting` and post to Slack

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect anomalies in any co-webinar funnel metric or partner health metric
- Generate hypotheses about what to change (topic, partner selection, timing, format, promotion split, nurture sequence)
- Design experiments (A/B test different topic angles with similar partners, test different promotion splits, test different post-event nurture strategies)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.

## Output

- Co-webinar health dashboard in PostHog with partner attribution
- Automated post-mortem for every event (14 days post-event)
- Monthly series report with partner portfolio analysis
- Anomaly alerts for funnel degradation and partner health issues
- Data pipeline feeding the autonomous optimization loop

## Triggers

Configure all monitoring at the start of Durable level. Post-mortems run automatically 14 days after each event. Monthly report runs on the 1st of each month. Weekly anomaly checks run every Monday.
