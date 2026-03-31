---
name: budget-intelligence-monitor
description: Continuous monitoring of budget objection patterns, navigation effectiveness, payment structure acceptance, and budget cycle intelligence across all deals
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

# Budget Intelligence Monitor

This drill creates the play-specific monitoring layer for budget objection handling at Durable level. It tracks budget objection patterns, navigation framework effectiveness, payment structure acceptance rates, and budget cycle intelligence — feeding data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog instance with 4+ weeks of `budget_objection_handled` events
- Attio CRM with structured budget objection data on deal records
- n8n instance for scheduling
- This drill runs alongside `autonomous-optimization` — it provides the domain-specific metrics and hypotheses that the optimization loop acts on

## Steps

### 1. Build the budget intelligence dashboard

Using `posthog-dashboards`, create a dashboard called "Budget Objection Intelligence" with these panels:

**Panel 1 -- Budget navigation success rate (weekly trend)**
- Query: `budget_objection_handled` events where `outcome = 'resolved'` / total `budget_objection_handled` events
- Chart: line graph, 12-week view
- Alert: if success rate drops below 50% for 2 consecutive weeks

**Panel 2 -- Root cause distribution (stacked bar)**
- Query: `budget_objection_handled` events grouped by `root_cause`
- Chart: stacked bar, weekly buckets
- Insight: tracks whether budget constraints are shifting (e.g., more `budget_exhausted` as fiscal year end approaches)

**Panel 3 -- Navigation framework effectiveness (heatmap)**
- Query: `budget_objection_handled` events, group by `framework_used` x `outcome`
- Chart: heatmap showing resolution rate per framework
- Identifies which budget navigation strategies work best for each root cause

**Panel 4 -- Payment structure acceptance rate (bar chart)**
- Query: `budget_objection_handled` events grouped by `payment_structure_accepted`
- Chart: bar chart showing which payment structures get accepted most often
- Insight: if `standard` (no creative structure needed) is most common, the budget objection may be weaker than expected

**Panel 5 -- Deal value preservation (line graph)**
- Query: average `deal_value_preserved` rate (deals where final value = original proposed value) on `budget_objection_handled` events, weekly
- Chart: line graph with target line at 90% preservation
- Alert: if average preservation drops below 80% (too many discounts being given for budget objections)

**Panel 6 -- Budget cycle timing heatmap**
- Query: `budget_objection_detected` events grouped by prospect fiscal month (months relative to fiscal year end)
- Chart: heatmap showing when budget objections peak
- Insight: expect spikes at fiscal year end (budget exhausted) and beginning (budget not yet allocated)

**Panel 7 -- Smokescreen detection rate (line graph)**
- Query: `budget_objection_handled` events where `was_smokescreen = true` / total events
- Chart: line graph, monthly trend
- Insight: high smokescreen rate means upstream qualification or discovery is weak

**Panel 8 -- Budget objection-to-close conversion funnel**
- Funnel: `budget_objection_handled` -> `budget_follow_up_sent` -> `budget_asset_engaged` -> `budget_asset_forwarded` -> `deal_closed_won`
- Shows the full conversion path after a budget objection, including the critical signal of the champion forwarding the justification memo

### 2. Build automated anomaly detection

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 14 days of budget metrics
2. Run `posthog-anomaly-detection` on each metric:
   - Navigation success rate: flag if drops >15% from 4-week rolling average
   - Root cause concentration: flag if any single root cause exceeds 50% of all budget objections (suggests a systematic issue)
   - Smokescreen rate: flag if rising above 30% (upstream qualification problem)
   - Payment structure drift: flag if non-standard payment structures exceed 40% of resolutions (may signal pricing misalignment with market)
   - Deal value erosion: flag if deal value preservation rate declining for 3+ consecutive weeks
3. For each detected anomaly, log to Attio and fire PostHog event:

```json
{
  "event": "budget_anomaly_detected",
  "properties": {
    "anomaly_type": "success_rate_drop|root_cause_concentration|smokescreen_spike|payment_structure_drift|value_erosion",
    "metric_name": "navigation_success_rate",
    "current_value": 0.42,
    "baseline_value": 0.58,
    "change_percentage": -27.6,
    "severity": "warning|critical"
  }
}
```

### 3. Generate domain-specific hypotheses

When an anomaly is detected, use `hypothesis-generation` with budget-objection-specific context:

Feed the hypothesis generator with:
- The anomaly data
- Current navigation framework effectiveness rankings
- Root cause distribution trends (especially fiscal-year-relative timing)
- Payment structure acceptance patterns
- Smokescreen detection rate and reasons
- Recent deal context (deal sizes, industries, buyer roles)

Example hypotheses this play might generate:
- "Navigation success rate dropped because `budget_exhausted` objections spiked — it's Q4 for 60% of our pipeline. Experiment: shift the default response for Q4 budget-exhausted objections from 'find remaining budget' to 'defer-and-lock for next fiscal year' with a pricing incentive for signing before year end."
- "Smokescreen rate increased from 15% to 32%. Discovery calls are not uncovering real objections. Experiment: add a mandatory budget qualification question to the discovery framework — 'Do you have budget allocated for solving this problem, and if so, roughly what range?' — before advancing any deal to the Proposed stage."
- "Payment structure 'ramp pricing' has a 78% acceptance rate but only 45% renewal rate at full price. Experiment: change the ramp from 60%/100%/120% to 80%/100%/110% to reduce year-2 sticker shock."

These hypotheses feed into the `autonomous-optimization` drill's experiment pipeline.

### 4. Build weekly budget intelligence report

Using `n8n-scheduling`, create a weekly cron workflow (Mondays at 9 AM):

1. Pull all budget objection data from the past week
2. Generate a report using Claude:

```json
{
  "report_sections": {
    "headline": "One sentence: best/worst budget metric this week",
    "navigation_success_rate": {"current": 0.57, "trend": "improving", "vs_target": "+7%"},
    "top_framework": {"name": "defer_and_lock", "resolve_rate": 0.72, "sample_size": 9},
    "worst_framework": {"name": "navigate_to_budget_owner", "resolve_rate": 0.25, "sample_size": 4},
    "root_cause_shift": "budget_exhausted surpassed competing_priorities as #1 root cause (Q4 effect)",
    "payment_structure_health": {"most_accepted": "quarterly_billing", "acceptance_rate": 0.65, "value_preserved": 0.94},
    "smokescreen_rate": 0.18,
    "deals_at_risk": [{"deal_name": "...", "risk_reason": "..."}],
    "budget_cycle_insight": "12 deals have fiscal year ending in 6 weeks — prioritize defer-and-lock conversations now",
    "recommended_actions": ["Action 1", "Action 2"],
    "active_experiments": [{"hypothesis": "...", "status": "running", "days_remaining": 4}]
  }
}
```

3. Post to Slack and store in Attio as a note on the "Budget Objection Handling" campaign record

### 5. Feed the optimization loop

The key output of this drill is structured metric data that `autonomous-optimization` can act on:

- Anomaly alerts trigger the optimization loop's Phase 2 (Diagnose)
- Domain-specific hypotheses feed into Phase 3 (Experiment)
- The weekly report provides Phase 5 (Report) content
- Framework effectiveness and payment structure data inform which variables to experiment on
- Budget cycle timing data enables seasonal optimization (different strategies for different fiscal periods)

Without this monitoring drill, `autonomous-optimization` would lack the budget-specific context needed to generate useful hypotheses.

## Output

- PostHog dashboard with 8 panels tracking all budget objection metrics
- Daily anomaly detection with automated alerts
- Domain-specific hypothesis generation for the optimization loop
- Weekly budget intelligence report
- Budget cycle timing intelligence (when are budget objections most common and most navigable)
- Structured data feed for the `autonomous-optimization` drill

## Triggers

- Dashboard: always available, refreshes on view
- Anomaly detection: daily cron via n8n (6 AM)
- Weekly report: Monday 9 AM cron via n8n
- Hypothesis generation: triggered by anomaly detection
