---
name: crm-data-quality-reporting
description: Build dashboards and automated reports tracking CRM data quality trends, issue resolution, and impact on sales outcomes
category: Operations
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - attio-lists
  - n8n-scheduling
  - n8n-workflow-basics
---

# CRM Data Quality Reporting

Build the reporting infrastructure that tracks data quality over time, connects data quality to sales outcomes, and provides the data substrate the autonomous optimization loop reads from.

## Input

- PostHog instance receiving data quality events (from `crm-data-audit` and `crm-data-quality-automation` drills)
- Attio workspace with data quality scores on records
- n8n instance for scheduled report generation

## Steps

### 1. Build the PostHog Data Quality Dashboard

Use `posthog-dashboards` to create a "CRM Data Quality" dashboard with 6 panels:

**Panel 1 — Quality Score Trend (line chart):**
- Event: `data_quality_weekly_summary`
- Property: `average_quality_score`
- Time range: last 12 weeks
- Shows whether data quality is improving, plateauing, or declining

**Panel 2 — Issue Breakdown (stacked bar):**
- Event: `data_quality_issue_detected`
- Breakdown by: `issue_type` (missing_field, invalid_value, stale_record, duplicate)
- Time range: last 4 weeks
- Shows which issue types are most frequent

**Panel 3 — Duplicate Rate (line chart):**
- Event: `data_quality_weekly_summary`
- Property: `duplicate_rate`
- Time range: last 12 weeks
- Target line at the current threshold (3% for Baseline, 2% for Scalable)

**Panel 4 — Stale Record Rate (line chart):**
- Event: `data_quality_weekly_summary`
- Property: `stale_rate`
- Time range: last 12 weeks
- Target line at 15%

**Panel 5 — Enrichment Effectiveness (bar chart):**
- Event: `enrichment_completed`
- Breakdown by: `enrichment_source`
- Metric: `fields_filled` (average)
- Shows which enrichment sources provide the most value

**Panel 6 — Quality Score Distribution (histogram):**
- Query Attio for all active record quality scores
- Bucket into ranges: 0-50, 50-70, 70-85, 85-95, 95-100
- Shows the shape of quality across the database

### 2. Build Attio Quality Views

Use `attio-reporting` and `attio-lists` to create saved views:

**"Records Needing Attention" view:**
- Filter: data_quality_score < 70 AND deal_stage NOT IN (Closed Won, Closed Lost)
- Sort: data_quality_score ascending
- This is the daily cleanup queue

**"Compliance by Owner" view:**
- Group deals by owner
- Show average data_quality_score per owner
- Identifies which reps need coaching on data entry

**"Enrichment Candidates" view:**
- Filter: 3+ required fields empty AND contact_status = Active
- These records should be routed to Clay enrichment

### 3. Build the weekly quality report

Use `n8n-scheduling` to trigger a weekly workflow:

1. Query PostHog for this week's quality metrics using `posthog-dashboards`
2. Query Attio for per-rep compliance data
3. Compare against last week and against targets
4. Generate a summary:
   - Overall quality score (and delta from last week)
   - Top 3 issue types this week
   - Reps with lowest compliance
   - Records cleaned/enriched this week
   - Duplicate merges completed
5. Post to Slack and store as Attio note

### 4. Build the data quality impact correlation

Use `posthog-funnels` to correlate data quality with sales outcomes:

**Funnel 1 — Quality vs Close Rate:**
- Segment deals by quality score bucket (high: 85+, medium: 70-84, low: <70)
- Compare win rates across segments
- Hypothesis: higher quality deals close at higher rates

**Funnel 2 — Quality vs Velocity:**
- Same segments
- Compare average days to close
- Hypothesis: higher quality deals close faster

**Funnel 3 — Quality vs Forecast Accuracy:**
- Compare predicted close dates against actual close dates
- Segment by quality score
- Hypothesis: higher quality records have more accurate forecasts

Log these correlations as PostHog insights. They justify continued investment in data quality.

### 5. Build monthly ROI calculation

Use `n8n-scheduling` to run monthly:

1. Calculate time saved: (manual cleanup hours before automation) - (manual cleanup hours this month)
2. Calculate error prevention: issues auto-fixed + duplicates prevented
3. Calculate enrichment value: records enriched x average cost of manual research per record
4. Calculate sales impact: win rate difference x average deal value x deals affected
5. Total ROI = (time saved + error prevention value + enrichment value + sales impact) / (tool costs + setup time investment)

## Output

- 6-panel PostHog dashboard for data quality monitoring
- 3 Attio saved views for daily operations
- Weekly automated quality report
- Sales outcome correlation analysis
- Monthly ROI calculation

## Triggers

- **Dashboard:** always-on, auto-refreshes
- **Weekly report:** every Monday via n8n cron
- **Monthly ROI:** first of each month via n8n cron
