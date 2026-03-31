---
name: value-asset-performance-monitor
description: Track and report on value asset outreach performance with weekly automated briefs and anomaly detection
category: Analytics
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - attio-reporting
  - n8n-workflow-basics
  - n8n-scheduling
  - anthropic-api-patterns
---

# Value Asset Performance Monitor

This drill builds the monitoring and reporting layer for the outbound-with-value-asset play at Durable level. It goes beyond basic dashboards by generating actionable weekly briefs that identify what to change and why.

## Input

- PostHog events flowing from `value-asset-outreach-sequence` drill (at least 4 weeks of data)
- Attio records with prospect tags (asset-reply-positive, asset-engaged, opted-out)
- n8n instance for scheduled workflows
- Anthropic API key for brief generation

## Steps

### 1. Build the master performance dashboard

Using `posthog-dashboards`, create a dedicated dashboard: "Value Asset Outreach — Performance."

**Panel 1: Weekly funnel (trend)**
Funnel: `value_asset_email_sent` -> `value_asset_link_clicked` -> `value_asset_reply_received` (positive) -> `value_asset_meeting_booked`
Show as a weekly trend line with conversion rates at each step.

**Panel 2: Asset click-through rate (trend)**
Formula: `value_asset_link_clicked` / `value_asset_email_sent` per week. Display as a line chart with a target threshold line at 15%.

**Panel 3: Asset-referencing reply rate (trend)**
Formula: replies where `references_asset = true` / total `value_asset_email_sent` per week. Target threshold: 3%.

**Panel 4: Reply sentiment breakdown (stacked bar)**
Group `value_asset_reply_received` by sentiment property (positive, negative, neutral) per week.

**Panel 5: Meeting rate by prospect segment (table)**
Break down `value_asset_meeting_booked` rate by ICP segment, company size tier, and asset version. This identifies which segments convert best.

**Panel 6: Cost per meeting (trend)**
Formula: total tool spend this period / `value_asset_meeting_booked` count. Compare to target CPA.

### 2. Configure anomaly detection

Using `posthog-anomaly-detection`, set up monitoring for:

- **Reply rate drop**: Weekly reply rate falls below 50% of 4-week rolling average. Severity: high. This indicates message fatigue, deliverability issues, or ICP mismatch.
- **Click-through spike**: Asset link clicks increase 2x+ week-over-week without corresponding reply increase. Severity: medium. Asset is interesting but emails are not converting interest to action.
- **Negative reply spike**: Negative sentiment replies exceed 10% of total replies. Severity: high. Messaging or targeting needs immediate review.
- **Deliverability decay**: Email sent volume drops vs. Instantly campaign volume (indicates bounces/blocks). Severity: critical.

### 3. Build the weekly brief generator

Using `n8n-scheduling`, create a workflow that runs every Monday at 8am:

1. **Pull data**: Query PostHog for last 7 days of all `value_asset_*` events. Query Attio for new deals sourced from this play.

2. **Compare to baseline**: Calculate week-over-week change for each KPI. Compare to the Scalable-level baseline numbers.

3. **Generate the brief**: Use `anthropic-api-patterns` to call Claude with the data:

```
System: "You are a GTM analyst generating a weekly performance brief for an outbound-with-value-asset play. Be direct. Start with the headline metric. Flag anything that needs action. Keep it under 300 words."

User: "Here is this week's data:
- Emails sent: {N}
- Asset link clicks: {N} ({X}% CTR, {delta} vs last week)
- Positive replies: {N} ({X}% rate, {delta} vs last week)
- Asset-referencing replies: {N}
- Meetings booked: {N}
- Cost per meeting: ${N}
- Anomalies detected: {list}
- Top performing segment: {segment}
- Worst performing segment: {segment}

Generate a weekly brief with: (1) headline verdict (on track / needs attention / critical), (2) what changed and likely why, (3) recommended actions for this week."
```

4. **Distribute**: Post the brief to Slack and log it as an Attio note on the play's campaign record using `attio-reporting`.

### 4. Build the segment performance tracker

Using `posthog-funnels`, create saved funnels segmented by:

- **ICP segment**: Which firmographic segments respond best to the value asset?
- **Asset version**: If multiple assets exist, which drives the best reply and meeting rates?
- **Sequence step**: Which email step (1, 2, or 3) generates the most positive replies?
- **Day of week**: Are certain send days producing better engagement?

Review these monthly to feed targeting and content decisions into the `autonomous-optimization` drill.

### 5. Pipeline attribution tracking

Using `attio-reporting`, generate a monthly attribution report:

- Total meetings sourced from value asset outreach
- Total pipeline value from those meetings
- Win rate of value-asset-sourced deals vs. other sources
- Average deal size from this play vs. overall average
- Time from first email to meeting booked (velocity)

This data justifies continued investment in the play and identifies whether the value asset attracts better-fit prospects than other outbound methods.

## Output

- A PostHog dashboard with 6 panels tracking the full value asset outreach funnel
- Automated anomaly detection with severity-based alerting
- Weekly AI-generated performance briefs delivered to Slack
- Monthly segment performance and pipeline attribution reports

## Triggers

Dashboard updates in real-time. Anomaly detection runs daily via n8n. Weekly briefs generate every Monday. Monthly attribution reports run on the first of each month.
