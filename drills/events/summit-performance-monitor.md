---
name: summit-performance-monitor
description: Continuous monitoring and reporting for virtual summit series health, surfacing degradation and opportunities across the full event funnel
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

# Summit Performance Monitor

This drill builds the always-on monitoring layer for your virtual summit series. It detects when any part of the summit funnel degrades, surfaces optimization opportunities, and generates periodic performance reports. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- At least 3 completed summits with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill
- n8n instance for scheduled monitoring workflows
- Attio with summit tracking lists populated

## Steps

### 1. Define the summit health metrics

Build a monitoring framework around six metric categories:

**Demand metrics (pre-event):**
- Registration rate: page visitors who register (target: >15%)
- Total registrations per summit (benchmark against 3-summit rolling average)
- Promotion channel yield: registrations per channel (email, LinkedIn, personal, paid, speaker-driven, sponsor-driven)
- Registration velocity: registrations per day during the 8-week promotion window
- Speaker pull: registrations attributable to each speaker's promotion efforts

**Commitment metrics (event day):**
- Show rate: registrants who attend at least 1 session (target: >35%)
- Multi-session rate: attendees who stay for 2+ sessions (target: >40% of attendees)
- Full-day rate: attendees who attend 4+ sessions (target: >15% of attendees)
- Drop-off curve: session-by-session attendance decline

**Engagement metrics (during event):**
- Questions asked per session (target: >5 per session)
- Poll participation rate (target: >30% of session attendees)
- CTA click rate per session (target: >10%)
- Chat activity volume (messages per minute)

**Conversion metrics (post-event):**
- Nurture reply rate by tier (Tier 1 target: >35%, Tier 2: >15%)
- Meeting booking rate by tier (Tier 1 target: >25%, Tier 2: >10%)
- Recording consumption rate for no-shows (target: >30%)
- Replay-to-meeting conversion (target: >3% of replay viewers book a meeting)

**Pipeline metrics (lagging):**
- Deals created from summit leads (30-day attribution window)
- Average deal value from summit-sourced leads
- Summit-to-close conversion rate (90-day window)
- Revenue per summit (180-day attribution)

**Series health metrics (aggregate):**
- Repeat attendee rate: % of attendees who attend 2+ summits per year
- List growth rate: net new registrants per summit
- Theme saturation index: declining registration for similar themes signals audience fatigue
- Speaker pipeline health: ratio of available speakers to planned summits
- Sponsor retention rate: % of sponsors who return for the next summit

### 2. Build the monitoring dashboard in PostHog

Using `posthog-dashboards`, create a "Summit Series Health" dashboard with these panels:

- **Top row (headline metrics)**: Current summit registrations vs target, show rate trend (last 4 summits), pipeline generated per summit trend
- **Middle row (funnel)**: Registration-to-meeting funnel for the last summit compared to the series average. Session-level drop-off curve for the last summit.
- **Bottom row (trends)**: Registration trend line (all summits), multi-session attendance rate trend, promotion channel effectiveness over time, speaker pull ranking

Using `posthog-funnels`, create a saved funnel: `summit_page_viewed` → `summit_registered` → `summit_reminder_clicked` → `summit_session_joined` → `summit_question_asked` → `summit_cta_clicked` → `summit_nurture_reply_received` → `summit_nurture_meeting_booked`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build monitoring workflows:

**During promotion window (runs daily):**
- Registration velocity: if daily registrations drop >40% from the 7-day average, fire alert: "Registration velocity declining — review promotion cadence and messaging."
- Channel yield: if any primary channel (email, LinkedIn) drops to zero registrations for 3+ consecutive days, fire alert: "Channel [X] has gone silent — check for delivery issues."

**Immediate post-summit (2 hours after close):**
- Show rate: if <25% (vs target 35%), fire alert: "Show rate critically low — review reminder cadence, event timing, and topic alignment."
- Multi-session rate: if <25% (vs target 40%), fire alert: "Multi-session attendance low — review session transitions, agenda flow, and break timing."
- Engagement rate: if average questions per session <2, fire alert: "Engagement critically low — review content format, moderation approach, and interactivity."

**Post-nurture (48 hours after summit):**
- Nurture email open rate: if <30%, fire alert: "Post-summit email open rate below threshold — review subject lines and send timing."
- Tier 1 reply rate: if <20% (vs target 35%), fire alert: "High-intent attendee replies low — review personalization quality and CTA relevance."

**Rolling checks (monthly via n8n cron):**
- Compare the last summit's full funnel to the 3-summit rolling average.
- If any metric declines >15% from the rolling average, flag for investigation.
- If registrations decline for 2 consecutive summits, fire alert: "Registration trend declining — investigate theme fatigue, competitive events, or promotion channel saturation."
- If repeat attendee rate drops below 10%, fire alert: "Repeat attendance declining — review content novelty and attendee experience quality."

### 4. Generate summit-level post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 21 days after each summit (when the nurture window fully closes):

1. Pull all PostHog events for this summit slug.
2. Calculate every metric in the health framework (Step 1).
3. Compare each metric to: (a) the target, (b) the 3-summit rolling average, (c) the best-ever summit.
4. Pull speaker-level metrics: session attendance, engagement rate, questions asked, and registrations attributable to each speaker's promotion.
5. Generate a structured post-mortem:

```
## Summit Post-Mortem: [Theme] — [Date]

### Headline
[One sentence: "Registration exceeded target by X% but multi-session retention declined Y%"]

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Registrations | 300 | 380 | +22% | PASS |
| Show rate | 35% | 31% | -8% | WATCH |
| Multi-session rate | 40% | 45% | +6% | PASS |
| ...

### Speaker Performance
| Speaker | Session | Attendance | Engagement Rate | Registrations Driven |
|---------|---------|------------|-----------------|---------------------|
| ...

### What Worked
[2-3 bullet points on metrics that exceeded targets, with hypothesized reasons]

### What Needs Attention
[2-3 bullet points on underperforming metrics, with hypothesized causes]

### Recommendations for Next Summit
[2-3 specific, actionable suggestions based on the data]
```

6. Store the post-mortem in Attio as a note on the summit record using `attio-lists`.
7. Post a summary to Slack.

### 5. Build the quarterly series report

Using `n8n-scheduling`, create a quarterly workflow that:

1. Aggregates all summit post-mortems from the quarter.
2. Calculates series-level trends: registration growth, show rate trend, multi-session rate trend, pipeline generated, cost per meeting, speaker ROI ranking.
3. Compares this quarter to last quarter and to the series lifetime.
4. Generates a quarterly report:

```
## Quarterly Summit Series Report — [Quarter Year]

### Summits This Quarter: [N]
### Total Registrations: [N] (vs [N] last quarter)
### Average Show Rate: [X]% (trend: [up/down/flat])
### Average Multi-Session Rate: [X]%
### Total Meetings Booked: [N] (vs [N] last quarter)
### Pipeline Generated: $[X]
### Cost Per Qualified Lead: $[X] (trend: [up/down/flat])

### Top Performing Summit: [Theme] — [Why]
### Underperforming Summit: [Theme] — [Why]

### Top Speakers (by pipeline generated):
1. [Name] — [Pipeline $] from [N] sessions
2. ...

### Series Health: [GREEN/YELLOW/RED]
[One paragraph assessment of overall series health and trajectory]

### Recommendations for Next Quarter
1. [Theme recommendation with supporting data]
2. [Operational recommendation with supporting data]
3. [Speaker pipeline recommendation with supporting data]
```

5. Store in Attio using `attio-reporting` and post to Slack.

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect anomalies in any summit funnel metric
- Generate hypotheses about what to change (theme, speaker lineup, timing, format, promotion, nurture)
- Design experiments (A/B test different promotion approaches, session formats, or nurture sequences across successive summits)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
