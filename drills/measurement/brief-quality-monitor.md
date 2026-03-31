---
name: brief-quality-monitor
description: Track meeting brief quality metrics, adoption rates, and correlation with call outcomes over time
category: Analytics
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - attio-reporting
  - n8n-scheduling
---

# Brief Quality Monitor

This drill creates the monitoring layer for the AI meeting preparation play. It tracks brief generation volume, quality scores, adoption rates, and the correlation between brief usage and call outcomes. At Durable level, it feeds the `autonomous-optimization` loop with the data it needs to detect anomalies and run experiments on brief quality.

## Input

- PostHog events: `meeting_brief_generated`, `meeting_brief_scored` (from `account-research-brief` and `call-brief-feedback-loop` drills)
- Attio deal records with outcomes
- At least 2 weeks of brief generation data for meaningful trends

## Steps

### 1. Build the Brief Quality Dashboard

Create a PostHog dashboard named "AI Meeting Prep — Brief Quality" with these panels:

**Panel 1: Brief Generation Volume** (trend line, last 30 days)
- Query: count of `meeting_brief_generated` events per day
- Breakdown by `meeting_type`
- Target: increasing adoption over time

**Panel 2: Brief Adoption Rate** (single number + trend)
- Query: `meeting_brief_generated` count / total meetings scheduled (from Cal.com events synced to PostHog)
- Target: >=80% at Scalable level

**Panel 3: Brief Quality Scores** (trend line, last 30 days)
- Query: average `overall_accuracy` and `overall_usefulness` from `meeting_brief_scored` events
- Target: both scores >=3.5 out of 5

**Panel 4: Data Completeness** (bar chart)
- Query: distribution of `data_completeness_score` from `meeting_brief_generated` events
- Buckets: 0-0.3 (sparse), 0.3-0.6 (partial), 0.6-0.8 (good), 0.8-1.0 (comprehensive)
- Target: >=70% of briefs in "good" or "comprehensive" buckets

**Panel 5: Best/Worst Sections** (table)
- Query: aggregate `best_section` and `worst_section` from `meeting_brief_scored`
- Shows which brief sections are consistently valuable vs need improvement

**Panel 6: Outcome Correlation** (funnel comparison)
- Query: compare meeting outcomes (`next_step_committed` rate) for meetings WITH briefs vs WITHOUT
- This is the core ROI metric: do briefs actually improve call outcomes?

### 2. Configure Alerts

Set up n8n workflows triggered by PostHog metric thresholds:

- **Brief quality drop**: If average `overall_usefulness` drops below 3.0 for 5 consecutive days, alert to Slack
- **Adoption drop**: If brief generation count drops >30% week-over-week, alert to Slack
- **Data source failure**: If `data_completeness_score` suddenly drops (suggesting a Clay or enrichment integration broke), alert immediately
- **Outcome divergence**: If AI-prepped call outcomes drop below non-prepped call outcomes for any week, alert — this means the briefs may be doing harm

### 3. Build the Weekly Metrics Export

Create an n8n workflow that runs every Monday:

1. Query PostHog for last 7 days of brief metrics
2. Calculate: briefs generated, average quality score, adoption rate, outcome lift
3. Format as a summary and post to Slack:
   ```
   Weekly Meeting Prep Report:
   - Briefs generated: {N}
   - Adoption rate: {X}% ({up/down} from last week)
   - Avg quality: accuracy {X}/5, usefulness {X}/5
   - Outcome lift: AI-prepped calls {X}% better than non-prepped
   - Worst section this week: {section} — consider adjusting prompt
   ```
4. Store the summary as an Attio note on the campaign/play record

### 4. Feed the Autonomous Optimization Loop (Durable level)

At Durable level, this monitor's data feeds the `autonomous-optimization` drill:

- **Anomaly detection inputs**: daily brief quality scores, adoption rate, outcome correlation
- **Experiment targets**: brief prompt modifications, data source prioritization, section ordering, meeting type-specific templates
- **Success criteria for experiments**: improved `overall_usefulness` score AND maintained or improved outcome correlation

The monitor provides the observation layer; the optimizer provides the action layer.

## Output

- PostHog dashboard with 6 panels tracking brief quality and impact
- Automated alerts for quality drops and data source failures
- Weekly summary reports posted to Slack
- Data feed for autonomous optimization at Durable level

## Triggers

- Dashboard is always-on after initial setup
- Alerts fire based on threshold breaches (configured in n8n)
- Weekly report runs every Monday via n8n cron
