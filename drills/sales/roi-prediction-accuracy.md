---
name: roi-prediction-accuracy
description: Measure projected vs realized ROI across closed deals, compute model accuracy, and calibrate future projections
category: Sales
tools:
  - Attio
  - Anthropic
  - PostHog
  - n8n
fundamentals:
  - attio-deals
  - attio-notes
  - roi-accuracy-scoring
  - posthog-custom-events
  - posthog-retention-analysis
  - n8n-scheduling
  - n8n-workflow-basics
---

# ROI Prediction Accuracy

This drill establishes a feedback loop between projected ROI (from the sales cycle) and realized ROI (from customer outcomes). It measures accuracy per value driver, identifies systematic biases, and produces calibration recommendations that improve future ROI models.

## Input

- Closed-won deals with ROI models stored in Attio (from `roi-calculator-build` or `roi-auto-generation`)
- Customer usage data in PostHog (at least 30 days post-close)
- n8n for scheduled measurement cycles

## Steps

### 1. Set up the measurement schedule

Create an n8n cron workflow that runs monthly:
1. Query Attio for all deals with `status = "closed_won"` AND `roi_model_status = "generated"` AND `close_date` >= 90 days ago AND (`roi_last_measured` is null OR `roi_last_measured` < 30 days ago)
2. For each qualifying deal, trigger the accuracy measurement

Run the first measurement at 90 days post-close (enough time for implementation + ramp). Re-measure every 90 days for the first year to track accuracy trajectory.

### 2. Gather actual outcome data

For each deal, pull from PostHog:
- Feature adoption rate (features used / features available)
- Usage volume (sessions, API calls, data processed — whatever maps to value drivers)
- Time-based metrics (time saved, tasks automated — from product telemetry)

Pull from Attio:
- Customer health score
- Support ticket volume
- Expansion revenue (if any)
- Customer-reported satisfaction (from QBR notes or NPS)

### 3. Run accuracy scoring

For each deal, run the `roi-accuracy-scoring` fundamental. This compares projected savings per value driver against annualized actual data and produces:
- Accuracy percentage per driver
- Overall model accuracy
- Direction of bias (over-projection or under-projection)
- Calibration recommendations
- Data gaps (projected drivers with no actual measurement)

### 4. Aggregate accuracy across all deals

After scoring individual deals, compute portfolio-level metrics:
- **Mean accuracy:** Average `accuracy_pct` across all measured deals
- **Systematic bias:** Are models consistently over or under projecting? By how much?
- **Accuracy by driver:** Which value drivers (time_savings, cost_reduction, revenue_increase, risk_mitigation) are most accurately projected?
- **Accuracy by industry/segment:** Do models perform differently for different prospect profiles?
- **Accuracy trend:** Is accuracy improving over time as models are calibrated?

### 5. Generate calibration report

Build a monthly calibration report:

```json
{
  "period": "2026-Q1",
  "deals_measured": 12,
  "mean_accuracy_pct": 78,
  "bias_direction": "over_projection",
  "bias_magnitude_pct": 15,
  "accuracy_by_driver": [
    {"driver": "time_savings", "mean_accuracy": 85, "bias": "accurate"},
    {"driver": "cost_reduction", "mean_accuracy": 92, "bias": "accurate"},
    {"driver": "revenue_increase", "mean_accuracy": 52, "bias": "over_projection"}
  ],
  "calibration_actions": [
    "Reduce revenue_increase projections by 30% for companies under $5M ARR",
    "Time savings projections are well-calibrated — no change needed",
    "Add implementation ramp factor: assume 50% value in month 1, 80% in month 2, 100% from month 3"
  ],
  "data_gaps_to_fix": [
    "Risk mitigation driver has no PostHog tracking — add compliance_incident_avoided event"
  ]
}
```

Store the report in Attio as a company-level note. Post to Slack for team review.

### 6. Apply calibrations to future models

Update the `roi-model-generation` fundamental's prompt with calibration adjustments:
- If a driver is systematically over-projected, add a discount factor
- If a driver is under-projected, note it but keep conservative (better to over-deliver)
- If a driver has no measurement data, either add tracking or remove the driver from projections

Track whether calibrations improve accuracy in the next measurement cycle.

### 7. Track accuracy metrics in PostHog

Fire PostHog event for each deal measured:
```json
{
  "event": "roi_accuracy_measured",
  "properties": {
    "deal_id": "...",
    "accuracy_pct": 0,
    "bias_direction": "over|under|accurate",
    "months_since_close": 0,
    "projected_roi": 0,
    "actual_roi": 0,
    "measurement_number": 1
  }
}
```

Fire a portfolio-level event monthly:
```json
{
  "event": "roi_accuracy_portfolio_report",
  "properties": {
    "period": "2026-Q1",
    "deals_measured": 12,
    "mean_accuracy_pct": 78,
    "bias_direction": "over_projection",
    "calibrations_applied": 3
  }
}
```

## Output

- Per-deal accuracy scores stored in Attio
- Monthly portfolio accuracy report
- Calibration recommendations applied to future ROI models
- PostHog events enabling long-term accuracy trend analysis
- Data gap identification for improving measurement coverage

## Triggers

Runs monthly via n8n cron. First measurement at 90 days post-close, then every 90 days for the first year. After year 1, annually.
