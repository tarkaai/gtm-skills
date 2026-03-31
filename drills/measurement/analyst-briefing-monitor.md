---
name: analyst-briefing-monitor
description: Monitor analyst briefing pipeline health, track referral outcomes, and generate weekly status reports
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Analyst Briefing Monitor

This drill creates the monitoring and reporting layer for the analyst briefing play. It tracks the full pipeline from briefing request to referral conversion and generates weekly status reports.

## Input

- PostHog events being logged from the analyst briefing play (analyst_update_sent, analyst_briefing_requested, analyst_referral_received, etc.)
- Attio records for all analysts with briefing statuses
- At least 4 weeks of data for meaningful trend analysis

## Steps

### 1. Build the analyst briefing dashboard in PostHog

Use the `posthog-dashboards` fundamental to create an "Analyst Briefing Program" dashboard with these panels:

**Panel 1 — Briefing Pipeline Funnel:**
Use `posthog-funnels` to build: `analyst_outreach_sent` -> `analyst_briefing_scheduled` -> `analyst_briefing_completed` -> `analyst_followup_requested` -> `analyst_referral_received`

**Panel 2 — Monthly Briefing Volume:**
Trend chart showing `analyst_briefing_completed` events per month. Target line at the Scalable threshold.

**Panel 3 — Referral Conversion:**
Count of `analyst_referral_received` events, broken down by analyst tier. This is the ultimate ROI metric.

**Panel 4 — Analyst Engagement Health:**
Stacked bar chart showing analyst counts by status (Healthy, Cooling, Cold, Active) over time. Healthy should trend up, Cold should trend down.

**Panel 5 — Time to Briefing:**
Average time from `analyst_outreach_sent` to `analyst_briefing_completed`, broken down by analyst tier. Tier 1 will be slower (weeks), Tier 3-4 should be faster (days).

**Panel 6 — Referral Pipeline Value:**
If Attio deals are tagged with source = "analyst_referral," show total pipeline value from analyst referrals.

### 2. Configure alert thresholds

Using `posthog-custom-events` and n8n, set up alerts:

- **Briefing volume drop:** If completed briefings drop >50% month-over-month, alert the team. Possible causes: outreach quality declining, analyst list exhausted, seasonal dip.
- **Referral drought:** If no `analyst_referral_received` events in 4 weeks despite active briefings, alert. May indicate briefing quality issues or misaligned analyst targeting.
- **Response rate decline:** If briefing request acceptance rate drops below 30%, alert. May indicate outreach messaging needs refresh or analyst list needs updating.

### 3. Generate weekly status report

Use `n8n-scheduling` to run a weekly cron (Monday 8am):

1. Query PostHog for last 7 days of analyst events
2. Query Attio for current pipeline of analyst-sourced deals
3. Generate a report using Claude API:

```
## Analyst Briefing Weekly Report — Week of {date}

### Pipeline Activity
- Briefing requests sent: {count}
- Briefings completed: {count}
- Follow-ups requested by analysts: {count}
- Referrals received: {count}

### Referral Pipeline
- New analyst-sourced deals: {count}
- Total analyst-sourced pipeline: ${value}
- Deals progressed this week: {list}

### Analyst Relationship Health
- Healthy: {count} | Cooling: {count} | Cold: {count} | Active: {count}
- Changes from last week: {deltas}

### Action Items
- {Auto-generated based on alerts and trends}
```

4. Post to Slack and store in Attio

### 4. Track ROI metrics

Maintain running calculations in PostHog:
- **Cost per briefing:** Total time invested / briefings completed (track agent and human hours separately)
- **Briefings per referral:** How many briefings does it take to generate one referral?
- **Referral-to-meeting rate:** What percentage of analyst referrals convert to meetings?
- **Analyst-sourced pipeline velocity:** How fast do analyst-referred deals move through the funnel vs. other sources?

These metrics feed into the `autonomous-optimization` drill at Durable level.

### 5. Build the attribution model

Tag all Attio deals with an "Analyst Source" field when created from a referral. Track:
- Which analyst referred them
- Which tier generates the most valuable referrals
- Time from briefing to first referral (by analyst)
- Referral quality (do analyst-referred prospects convert at higher rates?)

This data determines which analysts to invest more time in and which to deprioritize.

## Output

- PostHog dashboard: "Analyst Briefing Program"
- Weekly automated status reports (Slack + Attio)
- Alert system for pipeline health issues
- ROI attribution model connecting briefings to pipeline value

## Triggers

- Dashboard: updates in real-time as events flow into PostHog
- Weekly report: automated via n8n cron every Monday
- Alerts: triggered by threshold breaches in real-time
