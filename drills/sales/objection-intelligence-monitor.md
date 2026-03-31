---
name: objection-intelligence-monitor
description: Continuous monitoring of objection patterns, response effectiveness, pricing optimization signals, and discount impact across all deals
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
---

# Objection Intelligence Monitor

This drill creates the play-specific monitoring layer for price objection handling at Durable level. It tracks objection patterns, response framework effectiveness, discount optimization, and objection prevention signals — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `price_objection_handled` events
- Attio CRM with structured objection data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides the domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the objection intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Price Objection Intelligence" with these panels:

**Panel 1 — Objection overcome rate (weekly trend)**
- Query: `price_objection_handled` events where `outcome = 'resolved'` / total `price_objection_handled` events
- Chart: line graph, 12-week view
- Alert: if overcome rate drops below 60% for 2 consecutive weeks

**Panel 2 — Root cause distribution (stacked bar)**
- Query: `price_objection_handled` events grouped by `root_cause`
- Chart: stacked bar, weekly buckets
- Shows which objection types are increasing or decreasing

**Panel 3 — Framework effectiveness (heatmap)**
- Query: `price_objection_handled` events, group by `framework_used` x `outcome`
- Chart: heatmap showing resolve rate per framework
- Identifies which frameworks win most and which underperform

**Panel 4 — Time to resolution (histogram)**
- Query: `days_to_resolution` property on `price_objection_handled` events
- Chart: histogram with 1-day buckets
- Target: 80th percentile under 10 days

**Panel 5 — Discount leakage (line graph)**
- Query: average `discount_percentage` on `price_objection_handled` events, weekly
- Chart: line graph with target line at 5% average discount
- Alert: if average discount exceeds 10% for any week

**Panel 6 — Objection prevention rate (line graph)**
- Query: deals that reached Closed Won without any `price_objection_handled` event / total deals that reached Closed Won
- Chart: line graph, monthly trend
- Higher is better — means upstream discovery and value positioning are improving

**Panel 7 — Objection-to-close conversion (funnel)**
- Funnel: `price_objection_handled` -> `objection_follow_up_sent` -> `objection_asset_engaged` -> `deal_closed_won`
- Shows the full conversion path after an objection

**Panel 8 — Revenue impact (scorecard)**
- Query: total deal value of `deal_closed_won` events where the deal had at least one `price_objection_handled` event
- Compared to: total deal value of `deal_closed_won` events with no objections
- Shows: average deal size, close rate, and cycle length for objection vs non-objection deals

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of objection metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Overcome rate: flag if drops >15% from 4-week rolling average
   - New root cause concentration: flag if any single root cause exceeds 50% of all objections (suggests a systematic issue)
   - Discount escalation: flag if average discount is trending upward week over week for 3+ weeks
   - Framework decay: flag if a previously strong framework (>70% resolve rate) drops below 50%
3. For each detected anomaly, log to Attio and fire a PostHog event:

```json
{
  "event": "objection_anomaly_detected",
  "properties": {
    "anomaly_type": "overcome_rate_drop|root_cause_concentration|discount_escalation|framework_decay",
    "metric_name": "overcome_rate",
    "current_value": 0.52,
    "baseline_value": 0.68,
    "change_percentage": -23.5,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with price-objection-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current framework effectiveness rankings
- Root cause distribution trends
- Recent deal context (are deals getting larger? new ICP segments? new competitors?)
- Discount trends

The hypothesis generator will produce 3 ranked hypotheses. Examples of the kinds of hypotheses this play might generate:
- "Overcome rate dropped because value_gap objections increased — discovery calls are not quantifying pain deeply enough. Experiment: require pain_to_price_ratio >= 7x before advancing to proposal stage."
- "The roi_proof framework's effectiveness declined from 75% to 48%. Experiment: update the case study from 2024 data to 2025 data and test the updated version."
- "Average discount increased from 5% to 12%. Experiment: remove discount authority from the first objection response — only offer discounts after 2 value-first attempts."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly pricing intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all objection data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst metric this week",
    "overcome_rate": {"current": 0.67, "trend": "stable", "vs_target": "+2%"},
    "top_framework": {"name": "anchor_to_pain", "resolve_rate": 0.82, "sample_size": 11},
    "worst_framework": {"name": "payment_flexibility", "resolve_rate": 0.35, "sample_size": 8},
    "root_cause_shift": "value_gap increased from 30% to 45% of objections",
    "discount_health": {"avg_discount": 0.06, "trend": "flat", "vs_target": "+1%"},
    "prevention_rate": 0.42,
    "deals_at_risk": [{"deal_name": "...", "risk_reason": "..."}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 4}]
  }
}
```

3. Post the report to Slack and store in Attio as a note on the "Price Objection Handling" campaign record

### 5. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Framework effectiveness data informs which variables to experiment on next

Without this monitoring drill, `autonomous-optimization` would lack the play-specific context needed to generate useful hypotheses for price objection handling.

## Output

- PostHog dashboard with 8 panels tracking all objection metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly pricing intelligence report
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection
