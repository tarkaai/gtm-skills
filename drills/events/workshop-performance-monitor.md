---
name: workshop-performance-monitor
description: Continuous monitoring and reporting for educational workshop series health, tracking hands-on engagement depth alongside funnel metrics
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

# Workshop Performance Monitor

This drill builds the always-on monitoring layer for your educational workshop series. It tracks workshop-specific signals that webinar monitors miss: exercise completion rates, hands-on engagement depth, skill acquisition progression, and post-workshop implementation rates. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- At least 4 completed workshops with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill with workshop-specific events
- n8n instance for scheduled monitoring workflows
- Attio with workshop tracking lists populated

## Steps

### 1. Define workshop health metrics

Build a monitoring framework around six metric categories:

**Demand metrics (pre-event):**
- Registration rate: page visitors who register (target: >20%)
- Registrations per workshop: total sign-ups (benchmark against 4-event rolling average)
- Skill level distribution: beginner vs intermediate vs advanced registrants (target: match to workshop difficulty)
- Promotion channel yield: registrations per channel (email, LinkedIn, Clay prospecting, personal, paid)
- Registration velocity: registrations per day during the promotion window

**Commitment metrics (event day):**
- Show rate: registrants who attend (target: >40% -- workshops command higher commitment than webinars)
- Completion rate: attendees who stay through the full session (target: >80%)
- Exercise participation rate: attendees who attempt at least one exercise (target: >60%)
- Exercise completion rate: attendees who complete all exercises (target: >40%)

**Engagement depth metrics (during event):**
- Questions asked per attendee (target: >0.5 -- more questions indicates effective teaching)
- Help requests during exercises (monitor for exercises that are too hard or poorly explained)
- Chat activity rate: messages per attendee (target: >2)
- Exercise quality score: if exercises produce measurable output, track quality/correctness

**Conversion metrics (post-event):**
- Follow-up reply rate: nurture email replies / attendees (target: >12%)
- Meeting booking rate: meetings booked / attendees (target: >12%)
- Recording consumption rate: no-shows who watch the recording (target: >35%)
- Post-event exercise completion: non-attendees who complete exercises after watching recording (target: >10%)

**Pipeline metrics (lagging):**
- Deals created from workshop leads (track with 30-day attribution window)
- Average deal value from workshop-sourced leads
- Workshop-to-close conversion rate (90-day window)
- Deal velocity: workshop-sourced leads vs other sources (workshops should shorten cycle)

**Series health metrics (aggregate):**
- Repeat attendance rate: % of attendees who attend 2+ workshops in a quarter
- Skill progression: attendees who move from beginner to intermediate workshops
- List growth rate: net-new registrants per event
- Topic performance index: which topics drive the most pipeline per registrant
- Topic saturation index: declining registration for similar topics signals fatigue

### 2. Build the monitoring dashboard in PostHog

Using `posthog-dashboards`, create a "Workshop Series Health" dashboard:

- **Top row (headline metrics)**: Current workshop registrations vs target, show rate trend (last 6 events), meetings booked this month vs target, exercise completion rate trend
- **Middle row (engagement funnel)**: Registration -> Attendance -> Exercise attempted -> Exercise completed -> Nurture replied -> Meeting booked (for last event vs series average)
- **Bottom row (trends)**: Registration trend line (last 12 events), exercise completion by topic category, promotion channel effectiveness over time, pipeline generated per workshop

Using `posthog-funnels`, create saved funnels:
- **Primary**: `workshop_page_viewed` -> `workshop_registered` -> `workshop_attended` -> `workshop_exercise_started` -> `workshop_exercise_completed` -> `workshop_nurture_reply_received` -> `workshop_meeting_booked`
- **Engagement depth**: `workshop_attended` -> `workshop_question_asked` -> `workshop_exercise_completed` -> `workshop_cta_clicked`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build monitoring workflows:

**Immediate checks (2 hours post-event):**
- Show rate: if <25% (vs target 40%), fire alert: "Show rate critically low -- review prep email sequence and event timing"
- Exercise participation: if <30% (vs target 60%), fire alert: "Exercise participation critically low -- review exercise difficulty and facilitation approach"
- Completion rate: if <60% (vs target 80%), fire alert: "High drop-off during workshop -- review pacing and content density"

**48-hour checks (post-nurture launch):**
- Nurture email open rate: if <30%, fire alert: "Workshop nurture open rate below threshold -- review subject lines"
- Tier 1 reply rate: if <20% (vs target 35%), fire alert: "Active participant replies low -- review personalization and exercise-reference quality in follow-up"

**Rolling checks (weekly via n8n cron):**
- Compare the last workshop's full funnel to the 4-event rolling average
- If any metric declines >15% from the rolling average, flag for investigation
- If exercise completion rate declines for 2 consecutive events, fire alert: "Exercise quality declining -- review difficulty level and instructions"
- If registrations decline for 3 consecutive events, fire alert: "Registration trend declining -- investigate topic fatigue or promotion saturation"

### 4. Generate workshop post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 14 days after each workshop (when nurture window closes):

1. Pull all PostHog events for this workshop slug
2. Calculate every metric in the health framework (Step 1)
3. Compare each metric to: (a) the target, (b) the 4-event rolling average, (c) the best-ever workshop
4. Generate a structured post-mortem:

```
## Workshop Post-Mortem: [Topic] -- [Date]

### Headline
[One sentence: "Exercise completion exceeded target at X% but show rate declined Y%"]

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Registrations | 25 | 31 | +12% | PASS |
| Show rate | 40% | 36% | -8% | WATCH |
| Exercise completion | 40% | 52% | +15% | PASS |
| Meetings booked | 3 | 4 | +20% | PASS |

### Exercise Analysis
[Which exercises had highest completion? Which caused the most help requests?]

### What Worked
[2-3 bullet points with data]

### What Needs Attention
[2-3 bullet points with hypothesized causes]

### Recommendations for Next Workshop
[2-3 specific, actionable suggestions]
```

5. Store the post-mortem in Attio as a note on the workshop record using `attio-lists`
6. Post a summary to Slack

### 5. Build the monthly series report

Using `n8n-scheduling`, create a monthly workflow that:

1. Aggregates all workshop post-mortems from the month
2. Calculates series-level trends: registration growth, show rate trend, exercise completion trend, pipeline generated, cost per meeting
3. Compares this month to last month and to series lifetime average
4. Generates a monthly series health report:

```
## Monthly Workshop Series Report -- [Month Year]

### Workshops This Month: [N]
### Total Registrations: [N] (vs [N] last month)
### Average Show Rate: [X]% (trend: up/down/flat)
### Average Exercise Completion: [X]% (trend: up/down/flat)
### Meetings Booked: [N] (vs [N] last month)
### Pipeline Generated: $[X]

### Top Performing Workshop: [Topic] -- [Why]
### Best Exercise Engagement: [Topic] -- [X]% completion

### Series Health: [GREEN/YELLOW/RED]
[One paragraph assessment]

### Recommendations
1. [Specific recommendation with data]
2. [Specific recommendation with data]
3. [Specific recommendation with data]
```

5. Store in Attio using `attio-reporting` and post to Slack

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Workshop-specific optimization surfaces include:

- **Topic selection**: Which topic categories drive the most registrations AND pipeline (not just attendance)
- **Exercise design**: Which exercise formats produce the highest completion and post-event implementation
- **Difficulty calibration**: Whether beginner vs intermediate vs advanced sessions convert differently
- **Timing optimization**: Which day/time produces the best show rate for the hands-on format
- **Facilitation format**: Solo vs co-facilitated vs guest expert -- which produces the best engagement
- **Prep sequence effectiveness**: Does a more thorough prep sequence improve exercise completion rates

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
