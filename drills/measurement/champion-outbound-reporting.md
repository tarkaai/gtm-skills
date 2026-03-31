---
name: champion-outbound-reporting
description: Build champion-specific funnel dashboards and weekly pipeline reports tracking champion profiling through meeting conversion
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - attio-champion-tracking
  - attio-reporting
  - champion-engagement-scoring
  - n8n-scheduling
---

# Champion Outbound Reporting

This drill builds the monitoring and reporting layer specific to champion-driven outbound. It tracks the entire champion funnel — from initial profiling through recruitment, enablement, and meeting conversion — and surfaces actionable signals about where the funnel is leaking.

## Input

- Active champion-driven-outbound play running at Scalable or Durable level
- PostHog champion events configured (from `posthog-gtm-events` drill)
- Attio champion records with `champion_status`, `champion_score`, and deal linkage
- n8n instance for scheduled reporting

## Steps

### 1. Build the Champion Funnel Dashboard

Using `posthog-dashboards`, create a dedicated "Champion Outbound Pipeline" dashboard with these panels:

**Panel 1 — Champion Funnel (weekly):**
Funnel visualization:
- Accounts targeted → Champions profiled → Champions contacted → Champions recruited → Champions active → Meetings facilitated → Deals created
- Show conversion rate between each stage
- Filter by week, month, quarter

**Panel 2 — Champion Yield by Account Segment:**
Bar chart comparing champion-to-meeting conversion rate across:
- Company size bands (1-50, 51-200, 201-1000, 1000+)
- Industries
- Champion title/seniority
- Recruitment track (signal-led vs value-led)

**Panel 3 — Champion Engagement Health Distribution:**
Pie chart showing current distribution of all champions by status:
- Active (engaged in last 14 days)
- Recruited (enabled but not yet advocating)
- At Risk (score dropped >15 points or no contact in 14+ days)
- Disengaged (no contact in 21+ days)
- Lost (explicitly declined or left company)

**Panel 4 — Time-to-Meeting by Champion Source:**
Histogram showing days from first champion contact to first meeting facilitated. Break down by:
- Signal type that triggered profiling (job change, funding, competitor engagement)
- Recruitment track (A vs B)
- Enablement kit engagement (high vs low)

**Panel 5 — Pipeline Value from Champion Pathway:**
Line chart (weekly) showing total pipeline value of deals where `deal_source` = "champion-outbound". Overlay with non-champion outbound pipeline for comparison.

### 2. Set Up Anomaly Detection

Using `posthog-anomaly-detection`, configure monitoring for these champion-specific metrics:

| Metric | Alert when | Severity |
|--------|-----------|----------|
| Champion profiling → contacted rate | Drops >20% below 4-week average | Medium |
| Champion recruitment reply rate | Drops below 8% for 7+ days | High |
| Enablement kit forward rate | Drops below 15% for 2 weeks | Medium |
| Champion-facilitated meetings/week | Drops to zero for 2+ weeks | High |
| Average champion score | Drops >10 points from 4-week average | Medium |
| Champion-sourced pipeline value/month | Drops >30% from 8-week average | High |

Route alerts via n8n:
- Medium severity: post to Slack channel, log in Attio
- High severity: Slack DM to founder + create urgent task in Attio

### 3. Generate Weekly Champion Pipeline Report

Using `n8n-scheduling`, create a workflow that runs every Monday at 7:00 AM:

**Step 1:** Query Attio for all champion records updated in the last 7 days:
```
POST https://api.attio.com/v2/objects/people/records/query
{
  "filter": {
    "champion_status": {"not_empty": true}
  },
  "sorts": [{"attribute": "champion_score", "direction": "desc"}]
}
```

**Step 2:** Query PostHog for the last 7 days of champion funnel events.

**Step 3:** Generate a weekly report using Claude:

```
"Generate a weekly champion outbound pipeline report from this data:

Champion funnel this week:
- Accounts targeted: {count}
- Champions profiled: {count}
- Champions contacted: {count}
- Positive replies: {count}
- Champions recruited: {count}
- Meetings facilitated: {count}
- Deals created: {count}

Week-over-week changes: {deltas}
Champion health distribution: {counts by status}
Top 3 performing accounts: {details}
At-risk champions requiring action: {list}

Format as a brief executive summary (5-7 sentences) followed by an action items section. Focus on what changed, what needs attention, and what is working best."
```

**Step 4:** Post the report to Slack and store as an Attio note on the champion-outbound campaign record.

### 4. Monthly Cohort Analysis

On the first Monday of each month, generate a cohort analysis:

- For each month's cohort of profiled champions, track: what percentage reached each funnel stage by week 1, week 2, week 4, week 8
- Identify whether recent cohorts are performing better or worse than historical cohorts
- Flag if the champion recruitment cycle is lengthening (market saturation signal)
- Compare champion-sourced deals vs non-champion deals on: close rate, deal size, sales cycle length

Store the monthly cohort report in Attio and post to Slack.

## Output

- PostHog dashboard with 5 champion-specific panels
- Anomaly detection for 6 champion funnel metrics
- Automated weekly pipeline report (Slack + Attio)
- Monthly cohort analysis tracking champion pathway efficiency over time

## Triggers

- Dashboard: always-on, refreshes in real time
- Anomaly detection: runs daily via n8n
- Weekly report: Monday 7:00 AM via n8n cron
- Monthly cohort: first Monday of each month via n8n cron
