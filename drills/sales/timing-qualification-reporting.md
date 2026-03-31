---
name: timing-qualification-reporting
description: Build dashboards and automated reports tracking timeline accuracy, forecast precision, and deal velocity by urgency category
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-anomaly-detection
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Timing Qualification Reporting

Build the measurement infrastructure for the timing-qualification play: dashboards that show timeline distribution, forecast accuracy, deal velocity by category, and slippage patterns. Supports all four play levels with increasing sophistication.

## Input

- PostHog project with timing qualification events configured (from `timing-scorecard-setup`)
- Attio workspace with timeline custom fields populated
- n8n instance for automated report generation

## Steps

### 1. Create PostHog dashboards

Using `posthog-dashboards`, create a "Timing Qualification" dashboard with the following panels:

**Panel 1 — Timeline Distribution (pie chart):**
- Query: count of `timeline_category_assigned` events grouped by `category`
- Shows what percentage of pipeline is Immediate vs Near-term vs Medium-term vs Long-term
- Healthy target: 20-30% Immediate + Near-term

**Panel 2 — Qualification Rate (line chart, weekly):**
- Query: count of deals with `timeline_qualified = true` / total deals created, by week
- Shows whether qualification rate is improving over time
- Target: >=80% at Baseline, >=70% at Scalable

**Panel 3 — Forecast Accuracy (bar chart, monthly):**
- Query: average `forecast_accuracy_score` (days between predicted and actual close) by month
- Lower is better. Shows whether timeline predictions are getting more accurate.
- Target: <=14 days average variance at Durable

**Panel 4 — Deal Velocity by Category (grouped bar chart):**
- Query: average days from `timeline_category_assigned` to `deal_closed` grouped by `timeline_category`
- Validates that Immediate deals actually close faster than Long-term
- If not, the categorization system needs recalibration

**Panel 5 — Slippage Tracker (line chart, weekly):**
- Query: count of `timeline_shift_detected` events by week, split by shift direction (earlier vs later)
- Rising later-shifts = forecast becoming less reliable
- Healthy: slippage rate < 20% of qualified deals

**Panel 6 — Confidence Calibration (scatter plot):**
- Query: `timeline_confidence` at qualification vs `forecast_accuracy_score` at close
- Should show inverse correlation: higher confidence = better accuracy
- If no correlation, the confidence scoring is not calibrated

### 2. Build pipeline velocity funnel

Using `posthog-funnels`, create:

**Funnel: Timeline to Close**
- Step 1: `timeline_category_assigned`
- Step 2: `timeline_validated` (multi-stakeholder confirmation)
- Step 3: `proposal_sent` (or equivalent deal stage event)
- Step 4: `deal_closed_won`

Track conversion rates and time between steps. Break down by `timeline_category` to see where each category drops off.

### 3. Set up anomaly alerts

Using `posthog-anomaly-detection`, configure alerts for:

- Qualification rate drops below 50% for 7+ days
- Average forecast accuracy degrades by >30% week-over-week
- Slippage rate exceeds 40% for 2+ consecutive weeks
- Immediate pipeline drops to zero for 5+ days (no urgent deals = pipeline health concern)

Route alerts via n8n to Slack and/or email.

### 4. Build weekly automated report

Using `n8n-scheduling`, create a Monday morning workflow that:

1. Pulls the past week's timing qualification metrics from PostHog
2. Queries Attio for current pipeline snapshot by timeline category
3. Generates a summary via Claude:
   - Deals qualified this week: N (by category)
   - Qualification rate: X%
   - Forecast accuracy: avg Y days variance
   - Slippage events: N (net direction)
   - Top urgency driver this week: {driver}
   - Action items: {recommendations}
4. Posts the summary to Slack and logs it as an Attio note

### 5. Durable-level additions

At Durable level, extend reporting with:

**Prediction Accuracy Over Time:**
- Track auto-score prediction accuracy (from `timing-auto-scoring`) vs human-validated scores
- If accuracy drops below 65%, trigger scoring model recalibration

**Experiment Impact Tracking:**
- Cumulative impact of all autonomous-optimization experiments on forecast accuracy
- Which experiment types (scoring changes, cadence changes, signal weighting) produce the biggest gains

**Seasonal Pattern Analysis:**
- Overlay timeline distribution against calendar months
- Detect patterns: e.g., more Immediate deals in Q4 (budget expiration), more Long-term in Q1 (planning phase)
- Use patterns to adjust expectations and outreach strategy by quarter

**Signal Decay Analysis:**
- Which enrichment signals lose predictive value fastest?
- If "recent funding" predicted Near-term 3 months ago but those deals haven't closed, the signal has decayed
- Feed decay data back into the auto-scoring model

## Output

- PostHog dashboard with 6 panels covering the full timing qualification funnel
- Automated weekly Slack report
- Anomaly alerts for metric degradation
- (Durable) Prediction accuracy, experiment impact, and seasonal analysis
