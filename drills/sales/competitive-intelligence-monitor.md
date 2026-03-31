---
name: competitive-intelligence-monitor
description: Continuous monitoring of competitive objection patterns, positioning effectiveness, battlecard currency, and market positioning shifts — feeds the autonomous optimization loop
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
  - competitor-changelog-monitoring
---

# Competitive Intelligence Monitor

This drill creates the play-specific monitoring layer for competitive objection handling at Durable level. It tracks competitive objection patterns, positioning framework effectiveness, battlecard currency, win/loss trends per competitor, and market positioning shifts — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `competitive_objection_handled` events
- Attio CRM with structured competitive data on deal records and Competitor records
- n8n instance for scheduling
- Runs alongside `autonomous-optimization` — provides the domain-specific metrics and hypotheses the optimization loop acts on

## Steps

### 1. Build the competitive intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Competitive Intelligence" with these panels:

**Panel 1 — Competitive win rate (weekly trend)**
- Query: `competitive_objection_handled` events where deal outcome = "won" / total competitive deals
- Chart: line graph, 12-week view
- Alert: if competitive win rate drops below 45% for 2 consecutive weeks

**Panel 2 — Win rate by competitor (bar chart)**
- Query: `competitive_objection_handled` events grouped by `competitor_name`, showing win rate for each
- Chart: horizontal bar sorted by win rate
- Shows which competitors we beat consistently and which threaten us

**Panel 3 — Positioning framework effectiveness (heatmap)**
- Query: `competitive_objection_handled` events, group by `positioning_framework` x `outcome`
- Chart: heatmap showing win rate per framework
- Identifies which frameworks differentiate best and which underperform

**Panel 4 — Competitor frequency distribution (stacked bar)**
- Query: `competitor_detected` events grouped by `competitor_name`, weekly buckets
- Chart: stacked bar, weekly
- Shows which competitors are appearing more or less frequently in the pipeline

**Panel 5 — Time to competitive response (histogram)**
- Query: `time_to_detection_minutes` property on `competitor_detected` events
- Chart: histogram with 15-minute buckets
- Target: 80th percentile under 120 minutes (2 hours)

**Panel 6 — Battlecard currency score (line graph per competitor)**
- Query: For each competitor, calculate: (deals using current battlecard version with "won" outcome) / (total deals using current battlecard version)
- Chart: line graph per competitor, 12-week view
- A declining score means the battlecard is stale — competitor may have changed

**Panel 7 — Competitive objection-to-win funnel**
- Funnel: `competitor_detected` -> `competitive_objection_handled` -> `positioning_response_sent` -> `deal_closed_won`
- Shows the full conversion path from competitive detection to win

**Panel 8 — Competitive deal revenue impact (scorecard)**
- Query: total deal value of wins in competitive deals vs non-competitive deals
- Shows: average deal size, close rate, and cycle length for competitive vs non-competitive

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of competitive metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Overall competitive win rate: flag if drops >15% from 4-week rolling average
   - Per-competitor win rate: flag if any tracked competitor's win rate drops >20%
   - New competitor surge: flag if a previously unseen competitor appears in 3+ deals in one week
   - Framework decay: flag if a previously strong framework (>65% win rate) drops below 40%
   - Battlecard staleness: flag if any battlecard hasn't been refreshed in 30+ days and deals involving that competitor are active
3. For each detected anomaly, log to Attio and fire PostHog event:

```json
{
  "event": "competitive_anomaly_detected",
  "properties": {
    "anomaly_type": "win_rate_drop|new_competitor_surge|framework_decay|battlecard_stale|competitor_positioning_shift",
    "metric_name": "competitive_win_rate",
    "current_value": 0.38,
    "baseline_value": 0.52,
    "change_percentage": -26.9,
    "competitor_name": "...",
    "severity": "warning|critical"
  }
}
```

### 3. Integrate competitor market monitoring

Using `competitor-changelog-monitoring`, set up automated tracking of competitor product changes:

1. For each tracked competitor, configure Clay + n8n to monitor:
   - Changelog/product updates page (weekly scrape)
   - Pricing page (weekly scrape)
   - G2/Capterra review trends (monthly)
2. When a change is detected with `competitive_impact >= 3`:
   - Create an alert in Attio on the Competitor record
   - Flag the battlecard as potentially stale
   - Generate a hypothesis: "Competitor {name} released {change}. Our battlecard may need updating. Test: update the {section} of the battlecard and track win rate for the next 4 weeks."
3. Feed these hypotheses into the `autonomous-optimization` loop

### 4. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with competitive-objection-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current framework effectiveness rankings per competitor
- Competitor frequency distribution trends
- Recent competitor product/pricing changes
- Battlecard currency scores
- Win/loss pattern shifts

Example hypotheses this play might generate:
- "Win rate against {competitor} dropped from 55% to 35%. They launched {feature} 3 weeks ago. Experiment: update the battlecard to address {feature} with our alternative approach and test for 4 weeks."
- "The pain_alignment framework effectiveness declined from 70% to 42% against {competitor}. Their messaging now leads with pain language similar to ours. Experiment: switch to capability_gap framework for deals against {competitor} and measure for 4 weeks."
- "A new competitor {name} appeared in 5 deals this month (up from 0). Build an initial battlecard using the 5 deal transcripts and test our positioning against them."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 5. Build weekly competitive intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all competitive data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: biggest competitive win or threat this week",
    "overall_competitive_win_rate": {"current": 0.52, "trend": "improving", "vs_target": "+7%"},
    "top_competitor_threat": {"name": "...", "win_rate": 0.35, "deal_count": 8, "trend": "worsening"},
    "strongest_competitor_position": {"name": "...", "win_rate": 0.78, "deal_count": 5},
    "framework_performance": [{"framework": "...", "win_rate": 0.xx, "sample_size": n}],
    "new_competitors_detected": [{"name": "...", "mention_count": n}],
    "battlecard_health": [{"competitor": "...", "version": n, "last_updated": "...", "currency_score": 0.xx}],
    "competitor_market_changes": [{"competitor": "...", "change": "...", "impact": n}],
    "deals_at_competitive_risk": [{"deal_name": "...", "competitor": "...", "risk_reason": "..."}],
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": n}]
  }
}
```

3. Post the report to Slack and store in Attio

### 6. Feed the optimization loop

The key output of this drill is structured metric data that the `autonomous-optimization` drill can act on:

- Anomaly alerts trigger Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- Weekly report provides Phase 5 (Report) content
- Framework effectiveness per competitor informs which variables to experiment on next
- Competitor market changes create external-trigger hypotheses

Without this monitoring drill, `autonomous-optimization` would lack the competitive context needed to generate useful hypotheses for competitive objection handling.

## Output

- PostHog dashboard with 8 panels tracking all competitive metrics
- Daily anomaly detection with automated alerts
- Competitor market monitoring with change detection
- Domain-specific hypothesis generation for the optimization loop
- Weekly competitive intelligence report
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Competitor market monitoring: weekly cron via n8n
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection or competitor market changes
