---
name: warm-intro-performance-reporting
description: Monitor per-partner intro conversion, surface optimization levers, and generate weekly warm-intro performance briefs
category: Partnerships
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

# Warm Intro Performance Reporting

This drill builds the monitoring and reporting layer specific to the partnerships & warm intros play. It tracks per-partner intro volume, intro-to-meeting conversion, and meeting quality, then generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active partner/connector records in Attio with intro request history
- PostHog tracking for warm intro events (UTM parameters, custom events)
- At least 4 weeks of intro data (minimum for meaningful trends)

## Steps

### 1. Build the warm intro dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Warm Intros — Partner Performance" with these panels:

- **Intro requests sent by partner** (bar chart): `warm_intro_request_sent` events grouped by `partner_name`, last 30 days
- **Intros received by partner** (bar chart): `warm_intro_received` events grouped by `partner_name`, last 30 days
- **Request-to-intro conversion rate by partner** (table): intros received / requests sent per partner, sorted descending
- **Meetings booked from intros** (bar chart): `meeting_booked` events where `source = warm_intro`, grouped by `partner_name`, last 30 days
- **Intro-to-meeting conversion rate** (table): meetings / intros per partner, sorted descending
- **Intros over time** (trend line): weekly `warm_intro_received` events, last 90 days
- **Full intro funnel** (funnel): `warm_intro_request_sent` -> `warm_intro_received` -> `meeting_booked` -> `deal_created`, filtered to warm intro source

### 2. Create partner performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **High-converting connectors**: Partners whose intros convert to meetings at >60% rate
- **Volume connectors**: Partners who provide 3+ intros per month but with lower conversion
- **Declining connectors**: Partners whose intro volume dropped >50% month-over-month
- **New connectors**: Partners with first intro in the last 30 days (need more data before judging)
- **Dormant connectors**: Partners with no intro activity in 60+ days despite being asked

These cohorts feed the `autonomous-optimization` drill's anomaly detection.

### 3. Build the weekly warm intro brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of warm intro data from PostHog (requests sent, intros received, meetings booked per partner)
2. Pull partner relationship data from Attio (new connectors activated, intro requests pending, meeting outcomes)
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which connectors over/underperformed this week and why?
   - Which ask templates produced the highest intro rate?
   - What should change next week?
5. Compile into a structured brief and post to Slack

Brief format:
```
## Warm Intros Weekly Brief — {date}

**This week**: {requests_sent} requests, {intros_received} intros, {meetings_booked} meetings
**Request-to-intro rate**: {request_to_intro_pct}%
**Intro-to-meeting rate**: {intro_to_meeting_pct}%
**vs 4-week avg**: {change_pct}% {up/down}

### Top connectors this week
1. {connector_1}: {intros} intros, {meetings} meetings
2. {connector_2}: {intros} intros, {meetings} meetings

### Underperformers
- {connector}: {requests} requests sent, {intros} intros received ({pct}% conversion) — {hypothesis}

### Ask template insights
- Best template: {template} ({conversion_pct}% request-to-intro rate)
- Worst template: {template} ({conversion_pct}% request-to-intro rate)

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build the per-partner ROI tracker

In Attio, maintain these fields on each partner/connector record (updated weekly by n8n):

- **Total intro requests sent**: Count of requests made to this connector
- **Total intros received**: Count of intros that were actually made
- **Total meetings booked**: Meetings resulting from this connector's intros
- **Request-to-intro rate**: intros received / requests sent
- **Intro-to-meeting rate**: meetings / intros received
- **Best ask template**: The request template that produced the highest intro rate with this connector
- **Last intro date**: When the most recent intro was made
- **Connector health score**: Composite of recency, conversion rate, and volume (calculated by n8n)
- **Relationship depth**: Strong / Medium / Weak — based on response rates and intro quality

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:

- Any connector's intro rate drops below 20% for 2 consecutive weeks -> flag in Slack, investigate relationship health
- A new connector delivers their first intro within 48 hours of being asked -> celebrate in Slack, mark as responsive
- Total weekly meetings from warm intros drop below Scalable baseline for 2 consecutive weeks -> trigger `autonomous-optimization` investigation
- A connector's intros produce >80% meeting conversion -> flag as "high-value connector" and prioritize their relationship

## Output

- PostHog dashboard with per-partner and per-template performance
- Weekly automated warm intro brief with insights and recommendations
- Per-partner ROI tracking in Attio
- Alert system for performance anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Durable level. The weekly brief runs every Friday. Partner ROI fields update weekly via n8n.
