---
name: timing-intelligence-monitor
description: Continuous monitoring of timing objection patterns, response strategy effectiveness, timeline acceleration rates, and smokescreen detection accuracy across all deals
category: Deal Management
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

# Timing Intelligence Monitor

This drill creates the play-specific monitoring layer for timing objection handling at Durable level. It tracks objection patterns, response strategy effectiveness, smokescreen detection accuracy, reengagement success, and deal velocity impact — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `timing_objection_handled` events
- Attio CRM with structured timing objection data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides the domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the timing intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Timing Objection Intelligence" with these panels:

**Panel 1 — Timeline acceleration rate (weekly trend)**
- Query: `timing_objection_handled` events where `outcome = 'timeline_accelerated'` / total `timing_objection_handled` events
- Chart: line graph, 12-week view
- Alert: if acceleration rate drops below 40% for 2 consecutive weeks

**Panel 2 — Root cause distribution (stacked bar)**
- Query: `timing_objection_handled` events grouped by `root_cause`
- Chart: stacked bar, weekly buckets
- Shows which objection types are increasing or decreasing — a spike in smokescreens may indicate upstream discovery problems

**Panel 3 — Strategy effectiveness (heatmap)**
- Query: `timing_objection_handled` events, group by `strategy_used` x `outcome`
- Chart: heatmap showing acceleration rate per strategy
- Identifies which strategies win and which underperform per root cause

**Panel 4 — Smokescreen detection accuracy (line graph)**
- Query: Objections classified as smokescreen where eventual outcome confirmed the real objection matched the prediction
- Chart: line graph, monthly accuracy percentage
- Target: >=75% accuracy on smokescreen detection

**Panel 5 — Cost-of-delay impact (bar chart)**
- Query: Deals where cost-of-delay analysis was presented vs not, grouped by outcome
- Chart: grouped bar comparing acceleration rates
- Shows whether presenting cost-of-delay actually changes prospect behavior

**Panel 6 — Reengagement success rate (line graph)**
- Query: Deals with `reengagement_scheduled` outcome that eventually converted / total reengagement_scheduled deals
- Chart: line graph, monthly trend
- Target: >=30% reengagement-to-close conversion

**Panel 7 — Objection-to-close funnel (funnel)**
- Funnel: `timing_objection_handled` -> `timing_follow_up_sent` -> `timing_asset_engaged` -> `timeline_accelerated` or `bridging_accepted` -> `deal_closed_won`
- Shows the full conversion path after a timing objection

**Panel 8 — Deal velocity impact (scorecard)**
- Query: Average days from timing objection to close for deals that had objections vs average sales cycle for deals without timing objections
- Shows: deal velocity impact, average delay caused by timing objections, and eventual close rates

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of timing objection metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Acceleration rate: flag if drops >15% from 4-week rolling average
   - Smokescreen concentration: flag if smokescreen classifications exceed 50% of all timing objections (suggests discovery is not surfacing real concerns)
   - Reengagement decay: flag if reengagement conversion rate drops below 20%
   - Strategy decay: flag if a previously strong strategy (>50% acceleration rate) drops below 30%
   - Root cause shift: flag if a single root cause suddenly dominates (>40% of objections) — suggests a systematic issue
3. For each detected anomaly, log to Attio and fire a PostHog event:

```json
{
  "event": "timing_anomaly_detected",
  "properties": {
    "anomaly_type": "acceleration_rate_drop|smokescreen_concentration|reengagement_decay|strategy_decay|root_cause_shift",
    "metric_name": "acceleration_rate",
    "current_value": 0.35,
    "baseline_value": 0.52,
    "change_percentage": -32.7,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with timing-objection-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current strategy effectiveness rankings
- Root cause distribution trends
- Smokescreen detection accuracy trends
- Recent deal context (are deals getting larger? new segments? market changes?)
- Reengagement conversion data

The hypothesis generator produces 3 ranked hypotheses. Examples:
- "Acceleration rate dropped because `competing_priority` objections doubled — a major competitor launched a product that's absorbing prospect attention. Experiment: add competitive urgency content (showing risk of falling behind competitors who adopt now) to the competing_priority follow-up sequence."
- "Smokescreen classifications hit 55% of all timing objections — discovery calls are not going deep enough to surface real concerns. Experiment: add mandatory diagnostic questions to the discovery call script before any timing qualification."
- "Cost-of-delay presentations produce 45% acceleration rate but only 30% of timing objections receive one — the system is under-deploying the highest-impact asset. Experiment: generate cost-of-delay for all timing objections (not just no_urgency and competing_priority root causes)."
- "Reengagement conversion dropped from 35% to 18% — reengagement sequences fire too late. Experiment: trigger reengagement outreach 14 days before the scheduled date instead of 7."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly timing intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all timing objection data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst metric this week",
    "acceleration_rate": {"current": 0.48, "trend": "improving", "vs_target": "+8%"},
    "top_strategy": {"name": "cost_of_delay", "acceleration_rate": 0.62, "sample_size": 13},
    "worst_strategy": {"name": "strategic_patience", "acceleration_rate": 0.15, "sample_size": 7},
    "root_cause_shift": "smokescreen_budget increased from 15% to 28% of objections",
    "smokescreen_accuracy": {"current": 0.78, "trend": "stable"},
    "reengagement_health": {"scheduled": 12, "converted": 4, "rate": 0.33},
    "cost_of_delay_impact": {"presented": 8, "accelerated_after": 5, "rate": 0.625},
    "deals_at_risk": [{"deal_name": "...", "risk_reason": "..."}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 4}]
  }
}
```

3. Post the report to Slack and store in Attio as a note on the "Timing Objection Handling" campaign record

### 5. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Strategy effectiveness data informs which variables to experiment on next

Without this monitoring drill, `autonomous-optimization` would lack the play-specific context needed to generate useful hypotheses for timing objection handling.

## Output

- PostHog dashboard with 8 panels tracking all timing objection metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly timing intelligence report
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection
