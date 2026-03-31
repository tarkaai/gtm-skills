---
name: pricing-intelligence-monitor
description: Weekly monitoring report on pricing presentation effectiveness — acceptance rates, discount trends, tier mix, and pattern analysis across all deals
category: Deal Management
tools:
  - PostHog
  - Attio
  - Anthropic
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - attio-reporting
  - attio-notes
  - hypothesis-generation
  - n8n-scheduling
  - n8n-workflow-basics
---

# Pricing Intelligence Monitor

This drill generates a weekly pricing intelligence report analyzing all pricing presentations from the past 7 days. It detects trends (improving/declining acceptance, discount drift, tier mix shifts), flags anomalies, and generates recommendations for the upcoming week. At Durable level, this report feeds into the `autonomous-optimization` drill.

## Input

- PostHog with pricing events flowing (from `pricing-outcome-tracking` drill)
- Attio with deal-level pricing data
- At least 2 weeks of pricing presentation data (need history for trend detection)
- n8n instance for scheduled weekly execution

## Steps

### 1. Schedule the weekly report workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 8:00 AM:

1. Query PostHog for all pricing events from the past 7 days
2. Query Attio for all deals with `pricing_proposal_status` changes in the past 7 days
3. Aggregate and analyze
4. Generate the intelligence report
5. Post to Slack and store in Attio

### 2. Aggregate pricing metrics

Pull from PostHog using `posthog-dashboards`:

**Volume metrics:**
- Proposals generated this week
- Proposals presented this week
- Pricing conversations completed

**Outcome metrics:**
- Acceptance rate (accepted / presented)
- Rejection rate and top reasons
- Average days from presentation to decision
- Deals still pending (presented but no outcome)

**Discount metrics:**
- Discount request rate (how often prospects ask)
- Average discount given (when given)
- Discount-to-close correlation (do discounted deals close at higher rates?)
- Zero-discount acceptance rate (deals closed at list price)

**Tier metrics:**
- Tier recommendation distribution (how often Good/Better/Best is recommended)
- Tier selection distribution (what prospects actually choose)
- Tier match rate (did they pick the recommended tier?)
- Average deal size by tier selected

**Presentation quality metrics:**
- Value recap rate (how often sellers lead with value)
- Acceptance rate by format (live call vs email vs video)
- Average presentation score (from `pricing-presentation-scoring`)

### 3. Detect trends and anomalies

Compare this week's metrics against the 4-week rolling average:

- **Improving** (>10% better): flag with positive indicator
- **Normal** (within ±10%): no flag
- **Declining** (>10% worse): flag with warning
- **Anomaly** (>30% change): flag for urgent review

Key anomaly patterns to watch:
- Acceptance rate drop + discount rate increase = value story weakening
- Tier match rate declining = recommendation algorithm may need recalibration
- Days to acceptance increasing = deals stalling at pricing stage
- Discount-to-close correlation weakening = discounts not driving closes (stop giving them)

### 4. Generate the intelligence report

Run `hypothesis-generation` with the aggregated data to produce:

```json
{
  "report_period": "2026-03-23 to 2026-03-30",
  "headline": "One-sentence summary of the week's pricing performance",
  "metrics_summary": {
    "proposals_presented": 0,
    "acceptance_rate": "0%",
    "acceptance_rate_trend": "improving|stable|declining",
    "avg_discount_pct": 0,
    "discount_trend": "improving|stable|worsening",
    "top_tier_selected": "Good|Better|Best",
    "avg_deal_size": 0
  },
  "anomalies": [
    {"metric": "name", "expected": 0, "actual": 0, "severity": "warning|urgent"}
  ],
  "winning_patterns": ["What's working well this week"],
  "risk_patterns": ["What's declining or concerning"],
  "recommendations": [
    {"action": "Specific recommendation", "expected_impact": "What this should improve", "priority": "high|medium|low"}
  ],
  "experiment_candidates": [
    {"hypothesis": "If we change X, then Y will improve by Z%", "variable": "what to test", "priority_score": 0}
  ]
}
```

### 5. Distribute and store

1. Post the report summary to Slack (headline + metrics_summary + top 2 recommendations)
2. Store the full report as an Attio note on the team's pricing campaign record
3. Fire PostHog event `pricing_intelligence_report_generated` with the metrics_summary
4. If any anomalies have severity "urgent," send a separate Slack alert immediately

## Output

- Weekly pricing intelligence report with metrics, trends, anomalies, and recommendations
- Experiment candidates for the `autonomous-optimization` drill to act on
- Slack notification with summary
- Full report archived in Attio

## Triggers

Runs weekly via n8n cron (Monday 8:00 AM). Can also be triggered manually when the team needs an ad-hoc pricing review after a significant week.
