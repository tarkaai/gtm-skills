---
name: chrome-store-performance-monitor
description: Continuous monitoring of Chrome Web Store listing performance with anomaly detection and automated alerting
category: Chrome Web Store
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-deals
---

# Chrome Store Performance Monitor

This drill builds an always-on monitoring system for Chrome Web Store extension performance. It tracks install velocity, uninstall rate, listing conversion, review sentiment, and lead generation — surfacing anomalies and generating weekly performance reports that feed into the `autonomous-optimization` drill at Durable level.

## Input

- Published Chrome extension with at least 4 weeks of data (Scalable level passed)
- PostHog tracking configured for all extension events
- n8n instance for scheduling monitor workflows
- Attio CRM with extension campaign record

## Steps

### 1. Build the CWS performance dashboard

Using `posthog-dashboards`, create a dedicated Chrome Web Store dashboard with these panels:

| Panel | Metric | Visualization | Alert Threshold |
|-------|--------|---------------|-----------------|
| Daily installs | `extension_installed` events per day | Line chart, 30-day trend | <50% of 4-week average |
| Install-to-lead rate | `waitlist_form_submitted` / `extension_installed` | Percentage, weekly | <5% conversion |
| Popup engagement | `popup_opened` / `extension_installed` | Percentage, weekly | <20% engagement |
| Uninstall rate | Uninstall survey page views / cumulative installs | Percentage, weekly | >40% in 7 days |
| Lead quality | Leads from CWS that progress to demo/trial | Count, monthly | Track trend only |
| Review sentiment | Average rating from `review_received` events | Number, rolling 30-day | <3.5 stars |

### 2. Configure anomaly detection

Using `posthog-anomaly-detection`, set up monitoring rules:

- **Install velocity**: Compare last 7 days against 28-day rolling average. Flag if <60% of average (drop) or >200% (spike).
- **Conversion rate**: Compare popup-to-lead rate weekly. Flag if it drops >30% from 4-week average.
- **Uninstall spike**: Flag if daily uninstalls exceed 2x the 7-day average (indicates broken update or poor experience).
- **Review sentiment**: Flag if average rating drops below 3.5 or if 2+ one-star reviews arrive in a single week.

### 3. Build the monitoring n8n workflow

Using `n8n-scheduling`, create a daily cron workflow:

1. **Trigger**: Daily at 09:00 UTC
2. **Fetch metrics**: Query PostHog for yesterday's extension events (installs, popup opens, form submissions, uninstalls)
3. **Compare**: Calculate percentage change vs 7-day and 28-day averages
4. **Classify**: Normal (within ±15%), Watch (±15-30%), Alert (>30% deviation)
5. **Log**: Write daily metrics to Attio as a note on the extension campaign record
6. **Alert**: If any metric is in Alert state, send notification via Slack with: metric name, current value, average value, percentage change, and recommended investigation steps
7. **Weekly summary**: Every Monday, aggregate the week's data and generate a performance summary

### 4. Track extension updates impact

Using `posthog-custom-events`, log every extension update:

```
Event: extension_version_published
Properties:
  - version: "0.2.1"
  - changes: ["updated popup copy", "added feature preview"]
  - listing_changes: ["new screenshots", "updated description"]
  - published_at: ISO timestamp
```

After each update, the monitor workflow should flag the 7-day post-update period for comparison against the 7-day pre-update period. This creates an automatic before/after analysis for every change.

### 5. Generate weekly performance report

Using `n8n-scheduling`, run weekly on Mondays:

1. Pull all extension metrics for the past 7 days
2. Compare against previous 3 weeks (trend direction)
3. Calculate: installs this week, cumulative installs, leads generated, install-to-lead rate, active users estimate
4. Generate a structured report:
   - **Headline metric**: Installs this week (up/down/flat vs last week)
   - **Conversion**: Popup engagement rate, lead capture rate
   - **Health**: Uninstall rate, review sentiment
   - **Experiments**: Any listing changes and their measured impact
   - **Recommendation**: One specific action for next week based on the data
5. Post to Slack and log in Attio

### 6. Feed into autonomous-optimization

This monitor is the "eyes" for the `autonomous-optimization` drill at Durable level:

- When anomalies are detected, the monitor triggers the optimization loop's Phase 2 (Diagnose)
- The weekly report provides the context data the optimization loop needs for hypothesis generation
- Experiment results from the optimization loop are tracked back through this monitor to measure actual impact

## Output

- PostHog dashboard with 6 core CWS performance panels
- Daily anomaly detection running via n8n
- Weekly performance reports posted to Slack and logged in Attio
- Extension update impact tracking
- Data pipeline feeding the autonomous-optimization drill

## Triggers

Runs continuously at Durable level. Set up once, monitor ongoing.
