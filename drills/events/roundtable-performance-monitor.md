---
name: roundtable-performance-monitor
description: Continuous monitoring and reporting for micro-roundtable series health, surfacing degradation and opportunities across the full event funnel
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

# Roundtable Performance Monitor

This drill builds the always-on monitoring layer for your micro-roundtable series. It detects when any part of the roundtable funnel degrades, surfaces opportunities for improvement, and generates periodic performance reports. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

Roundtable monitoring differs from webinar monitoring because the small group size makes statistical comparisons harder. Individual event metrics are noisy. This drill emphasizes rolling averages and trend detection over single-event judgments.

## Prerequisites

- At least 4 completed roundtables with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill
- n8n instance for scheduled monitoring workflows
- Attio with roundtable tracking lists populated

## Steps

### 1. Define the roundtable health metrics

Build a monitoring framework around five metric categories:

**Demand metrics (pre-event):**
- RSVP rate: invitations sent vs confirmed (target: >35%)
- Confirmed count per event: total RSVPs (benchmark against 4-event rolling average, target: 8-10)
- Invitation channel yield: confirmations per channel (personal email, Loops broadcast, LinkedIn DM)
- Waitlist demand: events with waitlist indicate strong demand; events requiring extra outreach indicate weak demand

**Commitment metrics (event day):**
- Show rate: confirmed who attend (target: >75% — higher than webinars because the personal invitation creates stronger commitment)
- Full-session rate: attendees who stay for the entire discussion (target: >90%)
- Engagement rate: attendees who speak at least once (target: >80% — the small format should enable near-universal participation)

**Conversion metrics (post-event):**
- Follow-up reply rate: nurture email replies / attendees (target: >25%)
- Meeting booking rate: 1:1 meetings booked / attendees (target: >20%)
- Discussion summary open rate: % of recipients who open the summary email (target: >70%)

**Pipeline metrics (lagging):**
- Deals created from roundtable attendees (30-day attribution window)
- Average deal value from roundtable-sourced leads
- Roundtable-to-close conversion rate (90-day window)
- Cost per meeting: total roundtable costs / meetings booked

**Series health metrics (aggregate):**
- Guest pool freshness: % of new vs returning guests per event (target: 50-70% new)
- Guest pool depth: total available ICP contacts who have not yet been invited
- Topic repetition index: declining RSVPs for similar topics signals audience fatigue
- Net promoter signal: attendees who refer other contacts or request the next session unprompted

### 2. Build the monitoring dashboard in PostHog

Using `posthog-dashboards`, create a "Roundtable Series Health" dashboard:

- **Top row (headline metrics)**: Next event confirmed count vs target, trailing 4-event show rate, trailing 4-event meeting booking rate
- **Middle row (funnel)**: Invitation-to-meeting funnel for the last event, compared to the series average
- **Bottom row (trends)**: RSVP rate trend (last 8 events), show rate trend, meetings booked per event, guest freshness ratio over time

Using `posthog-funnels`, create a saved funnel: `roundtable_invited` -> `roundtable_confirmed` -> `roundtable_reminded` -> `roundtable_attended` -> `roundtable_engaged` -> `roundtable_nurture_replied` -> `roundtable_nurture_meeting_booked`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build monitoring workflows:

**Post-event checks (2 hours after each roundtable):**
- Show rate: if <60% (vs target 75%), fire alert: "Show rate below threshold — review confirmation cadence and attendee commitment signals"
- Engagement rate: if <50% (vs target 80%), fire alert: "Low engagement — review facilitation approach, topic selection, or group composition"

**48-hour post-nurture checks:**
- Tier 1 reply rate: if <20% (vs target 40%), fire alert: "High-intent attendee replies low — review personalization quality and reference specificity"
- Discussion summary open rate: if <40% (vs target 70%), fire alert: "Summary underperforming — review subject line and send timing"

**Rolling checks (weekly via n8n cron):**
- Compare each metric to the 4-event rolling average
- If RSVP rate declines >15% from rolling average, flag: "Demand declining — investigate topic selection, guest pool exhaustion, or invitation fatigue"
- If show rate declines for 3 consecutive events, flag: "Commitment trend declining — review confirmation process and attendee value proposition"
- If guest pool depth drops below 30 uninvited ICP contacts, flag: "Guest pool running low — activate Clay prospecting for fresh contacts"

### 4. Generate event-level post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 14 days after each roundtable:

1. Pull all PostHog events for this roundtable slug
2. Calculate every metric in the health framework
3. Compare each metric to: (a) the target, (b) the 4-event rolling average, (c) the best-ever event
4. Generate a structured post-mortem:

```
## Roundtable Post-Mortem: [Topic] — [Date]

### Headline
[One sentence: "Show rate hit 88% but only 1 meeting booked from 8 attendees"]

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Confirmed | 8-10 | 9 | +1 | PASS |
| Show rate | 75% | 88% | +5% | PASS |
| Engagement rate | 80% | 100% | +8% | PASS |
| Meetings booked | 20% of attendees | 12.5% | -6% | WATCH |

### Guest Composition
- New guests: [N] / Returning: [N]
- Industries represented: [list]
- Key participants and their contributions: [2-3 bullet points]

### What Worked
[2-3 bullet points with hypothesized reasons]

### What Needs Attention
[2-3 bullet points with hypothesized causes]

### Recommendations for Next Roundtable
[2-3 specific, actionable suggestions]
```

5. Store the post-mortem in Attio using `attio-lists`
6. Post a summary to Slack

### 5. Build the monthly series report

Using `n8n-scheduling`, create a monthly workflow that aggregates:

```
## Monthly Roundtable Series Report — [Month Year]

### Events This Month: [N]
### Total Attendees: [N] (vs [N] last month)
### Average Show Rate: [X]% (trend: [up/down/flat])
### Meetings Booked: [N] (vs [N] last month)
### Pipeline Generated: $[X]
### Guest Pool Status: [N] available / [N] invited / [N] exhausted

### Top Performing Roundtable: [Topic] — [Why]
### Underperforming Roundtable: [Topic] — [Why]

### Series Health: [GREEN/YELLOW/RED]
[One paragraph assessment]

### Recommendations
1. [Specific recommendation with supporting data]
2. [Specific recommendation with supporting data]
3. [Specific recommendation with supporting data]
```

Store in Attio using `attio-reporting` and post to Slack.

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect anomalies in any roundtable funnel metric
- Generate hypotheses about what to change (topic, guest mix, time slot, invitation copy, facilitation approach, follow-up sequence)
- Design experiments (A/B test different invitation approaches, discussion formats, follow-up timing)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
