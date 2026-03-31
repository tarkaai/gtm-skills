---
name: technical-objection-intelligence-monitor
description: Continuous monitoring of technical objection patterns, resolution effectiveness, gap trends, and roadmap impact across all deals
category: Competitive
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

# Technical Objection Intelligence Monitor

This drill creates the play-specific monitoring layer for technical fit objection handling at Durable level. It tracks technical gap patterns, response strategy effectiveness, proof asset performance, and roadmap commitment delivery — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `tech_gap_assessment_completed` and `tech_objection_resolved` events
- Attio CRM with structured technical objection data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the technical objection intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Technical Objection Intelligence" with these panels:

**Panel 1 — Objection resolution rate (weekly trend)**
- Query: `tech_objection_resolved` events where `outcome = 'resolved'` / total `tech_objection_raised` events
- Chart: line graph, 12-week view
- Alert: if resolution rate drops below 55% for 2 consecutive weeks

**Panel 2 — Gap type distribution (stacked bar)**
- Query: `tech_gap_assessment_completed` events grouped by `gap_type`
- Chart: stacked bar, weekly buckets
- Shows which gap types (integration, security, performance, feature) are increasing or decreasing

**Panel 3 — Response strategy effectiveness (heatmap)**
- Query: `tech_objection_resolved` events, group by `response_strategy` x `outcome`
- Chart: heatmap showing resolution rate per strategy (roadmap_commit, workaround, custom_dev, partner, honest_no_fit)
- Identifies which strategies resolve objections most and which underperform

**Panel 4 — Time to resolution (histogram)**
- Query: `days_to_resolution` property on `tech_objection_resolved` events
- Chart: histogram with 1-day buckets
- Target: 80th percentile under 7 days

**Panel 5 — Technical loss rate (line graph)**
- Query: deals closed-lost where `tech_fit_verdict` was `weak_fit` or `no_fit` / total deals closed-lost
- Chart: line graph with target line at 15%
- Alert: if technical losses exceed 20% for any month

**Panel 6 — Roadmap commitment tracking (scorecard)**
- Query: roadmap commitments made (from `roadmap_commitment_made` events) vs delivered on time
- Chart: scorecard showing: commitments made, delivered, overdue, % on-time delivery
- Alert: if on-time delivery rate drops below 80%

**Panel 7 — Proof asset utilization funnel**
- Funnel: `tech_objection_raised` -> `proof_asset_retrieved` -> `proof_asset_delivered` -> `tech_objection_resolved`
- Shows how effectively proof assets convert objections to resolutions

**Panel 8 — Competitive technical positioning (table)**
- Query: `tech_objection_raised` events grouped by `competitor_mentioned`, showing resolution rate per competitor
- Table: competitor name, objection count, resolution rate, common gap types
- Identifies which competitors create the hardest technical objections

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of technical objection metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Resolution rate: flag if drops >15% from 4-week rolling average
   - New gap type concentration: flag if any single gap type exceeds 50% of all objections
   - Response strategy decay: flag if a previously strong strategy (>70% resolve rate) drops below 50%
   - Proof asset utilization: flag if proof retrieval rate drops below 60% (objections going unproved)
   - Roadmap delivery slippage: flag if overdue commitments exceed 3
3. For each detected anomaly, log to Attio and fire a PostHog event:

```json
{
  "event": "tech_objection_anomaly_detected",
  "properties": {
    "anomaly_type": "resolution_rate_drop|gap_concentration|strategy_decay|proof_underuse|roadmap_slippage",
    "metric_name": "resolution_rate",
    "current_value": 0.48,
    "baseline_value": 0.65,
    "change_percentage": -26.2,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with technical-objection-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current response strategy effectiveness rankings
- Gap type distribution trends
- Proof asset effectiveness scores
- Roadmap commitment status
- Recent deal context (are deals getting more technically complex? new buyer personas? new verticals?)

Example hypotheses:
- "Resolution rate dropped because integration objections increased 40% — prospects are asking for systems we do not integrate with. Experiment: prioritize top 3 requested integrations in roadmap and test 'coming soon' commitment responses."
- "Workaround strategy effectiveness declined from 72% to 45%. Experiment: replace text-based workaround descriptions with live demo recordings and test whether visual proof improves acceptance."
- "Proof asset utilization is below 50% — agents are not retrieving proof during technical calls. Experiment: add auto-push of relevant proof assets to the call brief instead of relying on in-call retrieval."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly technical intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all technical objection data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst technical metric this week",
    "resolution_rate": {"current": 0.62, "trend": "improving", "vs_target": "-3%"},
    "top_strategy": {"name": "workaround_demo", "resolve_rate": 0.78, "sample_size": 9},
    "worst_strategy": {"name": "roadmap_commit", "resolve_rate": 0.40, "sample_size": 5},
    "gap_shift": "Security objections increased from 15% to 30% — new enterprise prospects entering pipeline",
    "proof_health": {"utilization_rate": 0.65, "avg_effectiveness": 0.72, "gaps_identified": 2},
    "roadmap_status": {"commitments_active": 4, "on_track": 3, "overdue": 1},
    "deals_at_technical_risk": [{"deal_name": "...", "risk_reason": "...", "gap_type": "..."}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 5}]
  }
}
```

3. Post the report to Slack and store in Attio as a note on the "Technical Fit Objection" campaign record

### 5. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Response strategy effectiveness data informs which variables to experiment on next
- Proof asset performance identifies which assets need replacement or creation

Without this monitoring drill, `autonomous-optimization` would lack the play-specific context needed to generate useful hypotheses for technical objection handling.

## Output

- PostHog dashboard with 8 panels tracking all technical objection metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly technical intelligence report
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection
