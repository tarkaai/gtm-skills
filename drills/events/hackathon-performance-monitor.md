---
name: hackathon-performance-monitor
description: Continuous monitoring and reporting for hackathon series health, surfacing degradation and opportunities across the full event-to-pipeline funnel
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

# Hackathon Performance Monitor

This drill builds the always-on monitoring layer for your hackathon series. It detects when any part of the hackathon funnel degrades, surfaces optimization opportunities, and generates periodic performance reports. Designed to feed data into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- At least 3 completed hackathons with PostHog tracking (provides baseline comparison data)
- PostHog GTM events configured via the `posthog-gtm-events` drill
- n8n instance for scheduled monitoring workflows
- Attio with hackathon tracking lists populated

## Steps

### 1. Define the hackathon health metrics

Build a monitoring framework around five metric categories:

**Demand metrics (pre-event):**
- Registration count per hackathon (benchmark against rolling average)
- Registration source yield: registrations per channel (email, community, paid, personal invite, organic)
- Registration velocity: registrations per day during the 6-week recruitment window
- Repeat participant rate: % of registrants who participated in a prior hackathon

**Engagement metrics (during event):**
- Kickoff attendance rate: registrants who attend the kickoff (target: >60%)
- Submission rate: registrants who submit a project (target: >40%)
- API/product usage depth: average number of product features used per submission
- Mentor session booking rate: % of participants who book office hours (target: >20%)
- Submission quality distribution: % scoring above median on judging criteria

**Conversion metrics (post-event):**
- Nurture reply rate: email replies / participants (target: >15%)
- Product adoption rate: % of participants who continue using the product 30 days post-hackathon (target: >25%)
- Meeting booking rate: meetings booked / participants (target: >10%)
- Paid conversion rate within 60 days: participants who convert to paying customers (target: >5%)

**Pipeline metrics (lagging):**
- Deals created from hackathon leads (track with 60-day attribution window)
- Average deal value from hackathon-sourced leads
- Hackathon-to-close conversion rate (90-day window)

**Series health metrics (aggregate):**
- Community growth rate: net new developer community members per hackathon
- Challenge theme saturation index: declining registration for similar themes signals developer fatigue
- Developer NPS: post-hackathon survey score (target: >60)
- Cost per qualified lead trend: should decline or stabilize as the series matures

### 2. Build the monitoring dashboard in PostHog

Using `posthog-dashboards`, create a "Hackathon Series Health" dashboard with these panels:

- **Top row (headline metrics)**: Current hackathon registrations vs target, submission rate trend (last 4 hackathons), qualified leads this quarter vs target
- **Middle row (funnel)**: Registration-to-pipeline funnel for the last hackathon, compared to the series average
- **Bottom row (trends)**: Registration trend line (last 8 hackathons), submission rate by format (virtual vs in-person), recruitment channel effectiveness over time, cost per qualified lead trend

Using `posthog-funnels`, create a saved funnel: `hackathon_page_viewed` -> `hackathon_registered` -> `hackathon_kickoff_attended` -> `hackathon_submission_received` -> `hackathon_nurture_reply_received` -> `hackathon_nurture_meeting_booked` -> `hackathon_paid_conversion`

### 3. Configure anomaly detection alerts

Using `posthog-anomaly-detection` and `n8n-scheduling`, build monitoring workflows:

**Post-registration checks (1 week before hackathon):**
- Registration count: if <50% of target with 7 days to go, fire alert: "Registration critically low -- activate emergency recruitment or consider postponing"
- Registration source: if any channel that usually contributes >20% of registrations has contributed <5%, fire alert: "Channel {name} underperforming -- investigate"

**Post-event checks (48 hours after hackathon closes):**
- Submission rate: if <25% (vs target 40%), fire alert: "Submission rate critically low -- review challenge difficulty, duration, and support availability"
- API usage depth: if average features used <2 (vs target 3+), fire alert: "Product engagement shallow -- challenge may not be driving meaningful product usage"

**Post-nurture checks (21 days after hackathon):**
- Nurture reply rate: if <8% (vs target 15%), fire alert: "Nurture engagement low -- review email personalization and tier segmentation"
- Product adoption rate: if <15% (vs target 25%), fire alert: "Post-hackathon retention dropping -- review onboarding materials and follow-up timing"

**Rolling checks (monthly via n8n cron):**
- Compare the last hackathon's full funnel to the series rolling average
- If any metric declines >20% from the rolling average, flag for investigation
- If registrations decline for 2 consecutive hackathons, fire alert: "Registration trend declining -- investigate theme fatigue, competitive events, or recruitment channel saturation"

### 4. Generate hackathon post-mortems

Using `n8n-workflow-basics`, build a workflow triggered 30 days after each hackathon (when nurture window and initial product adoption window close):

1. Pull all PostHog events for this hackathon slug
2. Calculate every metric in the health framework (Step 1)
3. Compare each metric to: (a) the target, (b) the series rolling average, (c) the best-ever hackathon
4. Generate a structured post-mortem:

```
## Hackathon Post-Mortem: {Challenge Title} -- {Date}

### Headline
{One sentence: "Registration exceeded target by X% but submission rate declined Y% from average"}

### Metrics vs Targets
| Metric | Target | Actual | vs Average | Status |
|--------|--------|--------|------------|--------|
| Registrations | 100 | 127 | +22% | PASS |
| Submission rate | 40% | 33% | -15% | WATCH |
| Qualified leads | 10 | 14 | +40% | PASS |
| Product adoption (30d) | 25% | 18% | -20% | FAIL |
| ...

### What Worked
{2-3 bullet points on metrics that exceeded targets, with hypothesized reasons}

### What Needs Attention
{2-3 bullet points on underperforming metrics, with hypothesized causes}

### Product Usage Insights
{Which features got the most usage? Which were ignored? What does this tell us about developer priorities?}

### Recommendations for Next Hackathon
{2-3 specific, actionable suggestions based on the data}
```

5. Store the post-mortem in Attio as a note on the hackathon record using `attio-lists`
6. Post a summary to Slack

### 5. Build the quarterly series report

Using `n8n-scheduling`, create a quarterly workflow that:

1. Aggregates all hackathon post-mortems from the quarter
2. Calculates series-level trends: registration growth, submission rate trend, pipeline generated, cost per qualified lead, community growth
3. Compares this quarter to last quarter and to the series lifetime average
4. Generates a quarterly report:

```
## Quarterly Hackathon Series Report -- {Quarter Year}

### Hackathons This Quarter: {N}
### Total Registrations: {N} (vs {N} last quarter)
### Average Submission Rate: {X}% (trend: {up/down/flat})
### Qualified Leads Generated: {N} (vs {N} last quarter)
### Pipeline Generated: ${X}
### Community Growth: +{N} members ({X}% growth)

### Top Performing Hackathon: {Title} -- {Why}
### Underperforming Hackathon: {Title} -- {Why}

### Series Health: {GREEN/YELLOW/RED}
{One paragraph assessment of overall series health}

### Recommendations
1. {Specific recommendation with supporting data}
2. {Specific recommendation with supporting data}
3. {Specific recommendation with supporting data}
```

5. Store in Attio using `attio-reporting` and post to Slack

### 6. Feed data to autonomous optimization

This drill produces the monitoring signals that the `autonomous-optimization` drill consumes at Durable level. Ensure all metrics are available as PostHog events so the optimization loop can:

- Detect anomalies in any hackathon funnel metric
- Generate hypotheses about what to change (challenge design, prize structure, recruitment approach, nurture sequence, duration, format)
- Design experiments (A/B test different recruitment approaches, challenge structures, prize tiers, or nurture sequences)
- Evaluate results using the same metrics tracked here

The handoff is clean: this drill watches and reports. The `autonomous-optimization` drill acts on what this drill surfaces.
