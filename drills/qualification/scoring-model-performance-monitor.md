---
name: scoring-model-performance-monitor
description: Monitor lead scoring model accuracy, detect drift, and generate weekly scoring performance reports
category: Qualification
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-funnels
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
---

# Scoring Model Performance Monitor

This drill creates always-on monitoring for the lead scoring model's predictive accuracy. It tracks whether Hot leads actually convert better than Cold leads, detects when the model drifts out of calibration, and generates weekly reports on scoring health.

## Input

- Lead scoring model running at Scalable or Durable level (output from `lead-score-automation`)
- PostHog with `lead_scored`, `meeting_booked`, `deal_created`, `deal_won`, `deal_lost` events flowing
- At least 4 weeks of scoring data for meaningful analysis
- n8n instance for scheduling

## Steps

### 1. Build the scoring accuracy dashboard in PostHog

Using `posthog-dashboards`, create a dashboard named "Lead Scoring Model Health" with these panels:

**Panel 1: Conversion rate by tier (primary accuracy metric)**
- Funnel: `lead_scored` -> `meeting_booked` -> `deal_created` -> `deal_won`
- Breakdown by `lead_tier` property (Hot, Warm, Cold)
- Time range: last 30 days, compare to previous 30 days
- Target: Hot tier converts at >=4x rate vs Cold tier

**Panel 2: Score distribution**
- Histogram of `lead_score` values from `lead_scored` events
- Shows whether scores cluster (bad) or spread across the range (good)
- Target: 15-25% Hot, 30-50% Warm, 30-50% Cold

**Panel 3: False negative rate**
- Count of leads that scored Cold (<50) but eventually booked meetings or created deals
- Breakdown by which fit/intent criteria they failed on
- Target: <10% false negative rate

**Panel 4: False positive rate**
- Count of leads that scored Hot (>=80) but never responded or booked
- Breakdown by which criteria inflated their score
- Target: <20% false positive rate

**Panel 5: Score-to-close correlation**
- Scatter: lead_score at time of scoring vs. days to close (for closed deals)
- Shows whether higher scores predict faster closes
- Target: negative correlation (higher score = fewer days to close)

**Panel 6: Model drift indicator**
- Week-over-week change in Hot tier conversion rate
- Alert threshold: if Hot conversion drops >20% for 2+ consecutive weeks, model may be drifting

### 2. Build the weekly accuracy check workflow in n8n

Using `n8n-scheduling`, create a workflow that runs every Monday at 9 AM:

1. Query PostHog for last 7 days of `lead_scored` events, grouped by tier
2. Query PostHog for last 7 days of `meeting_booked` events, joined to lead tier at time of scoring
3. Calculate: conversion rate by tier, false negative count, false positive count
4. Compare to 4-week rolling average using `posthog-anomaly-detection`
5. Classify model health: **Healthy** (Hot >=4x Cold, stable), **Degrading** (Hot 2-4x Cold or declining), **Broken** (Hot <2x Cold)

### 3. Generate the weekly scoring performance report

In the same n8n workflow, after computing metrics:

1. Build a report with:
   - Overall model accuracy: Hot vs Cold conversion ratio this week
   - Score distribution: % in each tier
   - False negatives this week (leads that scored Cold but converted)
   - False positives this week (leads that scored Hot but did not engage)
   - Criteria contribution: which fit/intent dimensions contributed most to correct predictions
   - Drift status: stable, degrading, or broken
   - Recommended actions (if degrading: which criteria to re-weight)
2. Post the report to Slack
3. Store the report as an Attio note on the lead scoring campaign record

### 4. Set up drift alerts

Using n8n, create alert triggers:

- **Amber alert:** Hot conversion rate drops below 3x Cold for 1 week. Action: flag for review next week.
- **Red alert:** Hot conversion rate drops below 2x Cold for 2+ weeks OR false negative rate exceeds 15%. Action: trigger `autonomous-optimization` drill to diagnose and generate improvement hypotheses.
- **Distribution alert:** If >40% of leads score as Hot or <10% score as Hot, thresholds may need adjustment.

### 5. Track criteria contribution over time

For each closed-won deal, log which fit and intent criteria the lead matched. Over time, this reveals which criteria are most predictive:

1. Query PostHog for `deal_won` events in the last 30 days
2. Join to the original `lead_scored` event to get individual criteria scores
3. Rank criteria by correlation with closed deals
4. Flag criteria that never appear in won deals (candidates for removal)
5. Flag new patterns in won deals that the model does not capture (candidates for addition)

Store this analysis in PostHog as a `scoring_criteria_audit` event.

## Output

- Real-time scoring accuracy dashboard in PostHog
- Weekly automated performance reports with specific metrics
- Drift detection alerts when model accuracy degrades
- Criteria contribution analysis showing which scoring dimensions are actually predictive

## Triggers

- Dashboard: always available, refreshes in real-time
- Weekly report: every Monday at 9 AM via n8n cron
- Drift alerts: checked with every weekly report; red alerts also checked daily
- Criteria audit: monthly (first Monday of the month)
