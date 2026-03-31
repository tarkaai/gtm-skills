---
name: roi-skepticism-intelligence-monitor
description: Continuous monitoring of ROI skepticism patterns, model effectiveness, proof asset engagement, and validation accuracy across all deals
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - attio-deals
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
  - roi-accuracy-scoring
---

# ROI Skepticism Intelligence Monitor

This drill creates the play-specific monitoring layer for ROI skepticism handling at Durable level. It tracks ROI objection patterns, model effectiveness, proof asset engagement, post-sale validation accuracy, and skeptic conversion signals — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `roi_calculator_presented`, `roi_calculator_validated`, and `roi_accuracy_measured` events
- Attio CRM with structured ROI objection data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides the domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the ROI skepticism intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "ROI Skepticism Intelligence" with these panels:

**Panel 1 — ROI objection resolution rate (weekly trend)**
- Query: deals where ROI skepticism was raised AND deal progressed to next stage / total deals where ROI skepticism was raised
- Chart: line graph, 12-week view
- Alert: if resolution rate drops below 65% for 2 consecutive weeks

**Panel 2 — ROI model acceptance rate (weekly trend)**
- Query: `roi_calculator_validated` events where `prospect_adjusted = false` OR `adjustment_direction = 'up'` / total `roi_calculator_presented` events
- Chart: line graph, 12-week view
- Measures: how often prospects accept the ROI model as presented or adjust it upward (strong signal)

**Panel 3 — Proof asset engagement by type (stacked bar)**
- Query: `objection_asset_engaged` events grouped by `asset_type` (roi_calculator, case_study, business_case, tco_comparison)
- Chart: stacked bar, weekly buckets
- Shows which proof assets prospects actually open and engage with

**Panel 4 — Time from ROI objection to resolution (histogram)**
- Query: time difference between `roi_skepticism_raised` and `roi_skepticism_resolved` events per deal
- Chart: histogram with 1-day buckets
- Target: 80th percentile under 7 days

**Panel 5 — Collaborative model conversion funnel**
- Funnel: `roi_calculator_presented` -> `roi_calculator_validated` -> `roi_referenced_in_decision` -> `deal_closed_won`
- Shows the full path from ROI presentation through deal close
- Measures drop-off at each stage to identify where conviction breaks

**Panel 6 — Post-sale ROI accuracy (scatter plot)**
- Query: `roi_accuracy_measured` events, plot `projected_roi` vs `actual_roi`
- Chart: scatter plot with diagonal reference line (perfect accuracy)
- Shows systematic over/under-projection patterns

**Panel 7 — Skeptic conversion by persona (heatmap)**
- Query: ROI skepticism resolution events, grouped by `exec_persona` (CFO, CEO, VP Eng, etc.) x `resolution_method` (collaborative_model, case_study, roi_proof, peer_reference)
- Chart: heatmap showing which methods work for which personas
- Identifies the best ROI proof strategy per buyer persona

**Panel 8 — Revenue preserved from ROI skeptics (scorecard)**
- Query: total deal value of closed-won deals where ROI skepticism was raised and resolved
- Compared to: total deal value lost to unresolved ROI skepticism
- Shows: average deal size, close rate, and cycle length for ROI-skeptic vs non-skeptic deals

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of ROI skepticism metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Resolution rate: flag if drops >15% from 4-week rolling average
   - Model acceptance rate: flag if drops >20% (prospects rejecting or heavily discounting your ROI claims)
   - Proof asset engagement: flag if any asset type drops to <10% open rate (asset has gone stale)
   - Post-sale accuracy: flag if mean accuracy drops below 60% (models are over-promising)
   - Persona concentration: flag if >60% of unresolved ROI skepticism comes from a single persona (need persona-specific strategy)
3. For each detected anomaly, log to Attio and fire a PostHog event:

```json
{
  "event": "roi_skepticism_anomaly_detected",
  "properties": {
    "anomaly_type": "resolution_rate_drop|model_acceptance_drop|proof_asset_stale|accuracy_decline|persona_concentration",
    "metric_name": "resolution_rate",
    "current_value": 0.55,
    "baseline_value": 0.72,
    "change_percentage": -23.6,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with ROI-skepticism-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current proof asset effectiveness rankings
- Persona-specific resolution rates
- Post-sale accuracy trends (are models over-projecting? which drivers are inaccurate?)
- Recent deal context (larger deals? new verticals? new competitive pressure?)

The hypothesis generator produces 3 ranked hypotheses. Examples of the kinds of hypotheses this play generates:

- "Model acceptance rate dropped because the case study used in roi_proof responses is 8+ months old and prospects question its relevance. Experiment: update the primary case study with Q1 2026 data and test against the current version."
- "CFO personas resolve at 45% vs 75% for VP personas. The ROI model uses revenue-increase framing but CFOs care about cost-avoidance. Experiment: generate CFO-specific ROI narratives using `roi-narrative-generation` with cost-avoidance framing."
- "Post-sale accuracy dropped to 58% — revenue_increase driver is consistently over-projected by 40%. Experiment: apply a 0.6x calibration factor to revenue_increase projections and test whether calibrated models have higher acceptance rates."
- "Collaborative model usage is low (30% of presentations) despite higher conversion. Experiment: make the Google Sheet the default format for all ROI presentations and measure whether acceptance improves."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly ROI intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all ROI skepticism data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst ROI metric this week",
    "resolution_rate": {"current": 0.72, "trend": "improving", "vs_target": "+7%"},
    "model_acceptance_rate": {"current": 0.68, "trend": "stable", "vs_target": "+3%"},
    "top_proof_asset": {"type": "collaborative_roi_calculator", "engagement_rate": 0.85, "conversion_impact": "+22%"},
    "worst_proof_asset": {"type": "generic_case_study", "engagement_rate": 0.18, "recommendation": "retire or update"},
    "accuracy_health": {"mean_accuracy": 0.74, "bias_direction": "over_projection", "worst_driver": "revenue_increase"},
    "persona_breakdown": [
      {"persona": "CFO", "resolution_rate": 0.45, "best_method": "cost_avoidance_model"},
      {"persona": "VP Sales", "resolution_rate": 0.82, "best_method": "collaborative_roi_calculator"}
    ],
    "revenue_preserved": {"total": 245000, "deals_saved": 4},
    "deals_at_risk": [{"deal_name": "...", "risk_reason": "ROI model rejected, no follow-up sent"}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 5}]
  }
}
```

3. Post the report to Slack and store in Attio as a note on the "ROI Skepticism Handling" campaign record

### 5. Run quarterly ROI accuracy calibration

Using `n8n-scheduling`, create a quarterly cron workflow:

1. Pull all `roi_accuracy_measured` events from the quarter
2. Run `roi-accuracy-scoring` aggregated across all measured deals
3. Compute calibration adjustments per value driver:
   - Drivers with mean accuracy >90%: no adjustment needed
   - Drivers with mean accuracy 70-90%: apply a calibration note but keep current projections
   - Drivers with mean accuracy <70%: compute a correction factor and apply it to future `roi-model-generation` prompts
4. Store calibration recommendations in Attio
5. Automatically update the `roi-model-generation` prompt context with correction factors for the next quarter

This creates a self-correcting feedback loop: over-projected claims get automatically calibrated, increasing prospect trust and model acceptance over time.

### 6. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Post-sale accuracy data informs which ROI drivers to emphasize or de-emphasize
- Persona effectiveness data identifies which resolution methods to experiment with next

Without this monitoring drill, `autonomous-optimization` would lack the ROI-skepticism-specific context needed to generate useful hypotheses.

## Output

- PostHog dashboard with 8 panels tracking all ROI skepticism metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly ROI intelligence report
- Quarterly ROI accuracy calibration with self-correcting model updates
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Quarterly calibration: first Monday of Q+1 via n8n
- Hypothesis generation: triggered by anomaly detection
