---
name: funnel-optimization-health-monitor
description: Continuous monitoring of all key funnel metrics with automated alerting, regression detection, and weekly health reports
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Funnel Optimization Health Monitor

This drill creates an always-on monitoring system for all key funnels (signup, activation, upgrade). It detects regressions before they compound, tracks the cumulative impact of optimizations, and produces weekly health reports that feed into the `autonomous-optimization` drill at Durable level.

## Input

- PostHog funnels configured for each key conversion flow (signup, activation, upgrade)
- Baseline conversion rates for each funnel step (from `signup-funnel-audit` or equivalent)
- n8n instance for scheduled monitoring workflows
- Attio for logging health state and alerts

## Steps

### 1. Define the funnel health model

For each monitored funnel, define:

| Funnel | Steps | Primary Metric | Healthy Range | Warning | Critical |
|--------|-------|---------------|---------------|---------|----------|
| Signup | page_viewed > form_started > completed | End-to-end CVR | >=baseline | 10-20% below baseline | >20% below baseline |
| Activation | signup > aha_moment > activated | Activation rate | >=baseline | 10-15% below baseline | >15% below baseline |
| Upgrade | feature_gate_hit > pricing_viewed > checkout_started > payment_completed | Upgrade CVR | >=baseline | 15-25% below baseline | >25% below baseline |

Store these thresholds in the n8n workflow as variables so they can be updated as baselines improve.

### 2. Build the daily monitoring workflow

Using `n8n-scheduling`, create a workflow triggered at 08:00 UTC daily:

**Step 1 — Pull funnel metrics.** For each monitored funnel, query the PostHog API using `posthog-funnels`:

```
POST /api/projects/<id>/insights/funnel/
{
  "filters": {
    "insight": "FUNNELS",
    "events": [{funnel_events}],
    "date_from": "-7d",
    "funnel_window_days": 7
  }
}
```

Pull both the 7-day window and the 28-day rolling average for comparison.

**Step 2 — Compute health status.** For each funnel step:
- Calculate: `step_cvr_7d` and `step_cvr_28d`
- Compute: `change_pct = (step_cvr_7d - step_cvr_28d) / step_cvr_28d * 100`
- Classify: "healthy" if within range, "warning" if degraded, "critical" if severely degraded

**Step 3 — Detect step-level regressions.** A regression is when a previously improving step reverses direction for 3+ consecutive daily checks. Track the trend direction per step. If a step that was improving starts declining for 3 days, flag it even if still within healthy range.

**Step 4 — Emit health events.** Using `posthog-custom-events`:

```javascript
posthog.capture('funnel_health_check', {
  funnel: '{funnel_name}',
  step: '{step_name}',
  cvr_7d: {value},
  cvr_28d: {value},
  change_pct: {value},
  status: 'healthy|warning|critical',
  trend: 'improving|stable|declining',
  check_date: '{ISO date}'
});
```

**Step 5 — Route alerts.** Using `n8n-workflow-basics`:
- Warning: Post to Slack #product-metrics channel
- Critical: Post to Slack #product-metrics AND create an Attio task for the product owner using `attio-notes`
- Regression detected: Post to Slack with the specific step, direction, and duration

### 3. Build the funnel health dashboard

Using `posthog-dashboards`, create a dashboard with:

- **Row 1:** End-to-end conversion rate for each funnel (signup, activation, upgrade) as trend lines with 28-day window
- **Row 2:** Per-step conversion rates for the primary funnel (the one with most traffic), with threshold lines overlaid
- **Row 3:** Segment breakdown for any funnel currently in warning/critical state
- **Row 4:** Experiment impact tracker — a table showing active and completed experiments with before/after conversion rates

Configure dashboard auto-refresh at 1-hour intervals.

### 4. Generate weekly health reports

Using `n8n-scheduling`, create a Monday 09:00 UTC workflow that:

1. Queries all funnel health check events from the past 7 days
2. Computes: which funnels improved, which degraded, which were stable
3. Lists any active experiments and their interim results
4. Calculates cumulative optimization impact: `(current_cvr - original_baseline_cvr) / original_baseline_cvr * 100`
5. Identifies the current primary bottleneck (the step with the largest absolute drop-off across all funnels)

Format as:

```
## Weekly Funnel Health Report — {week}

### Summary
- Signup funnel: {status} — {cvr}% (trend: {direction}, {change}% vs last week)
- Activation funnel: {status} — {cvr}% (trend: {direction}, {change}% vs last week)
- Upgrade funnel: {status} — {cvr}% (trend: {direction}, {change}% vs last week)

### Current Bottleneck
{step_name} in {funnel_name}: {cvr}% conversion, {absolute_drop} users lost per week

### Active Experiments
| Experiment | Funnel | Step | Started | Interim Result |
|-----------|--------|------|---------|----------------|

### Cumulative Optimization Impact
- Signup: {lift}% above original baseline
- Activation: {lift}% above original baseline
- Upgrade: {lift}% above original baseline

### Recommended Actions
1. {action based on current data}
2. {action based on current data}
```

Post to Slack and store in Attio.

### 5. Track optimization velocity

Monitor how fast the team is finding and shipping improvements:

- **Experiment velocity:** Number of experiments started per month
- **Win rate:** Percentage of experiments that beat control
- **Time to implement:** Days from experiment win to full rollout
- **Baseline drift:** How much the baseline has moved since the play started

Emit `funnel_optimization_velocity` events weekly to PostHog for long-term tracking.

## Output

- Daily automated health checks for all monitored funnels
- Real-time alerting for warnings, critical regressions, and trend reversals
- PostHog dashboard with funnel health, experiments, and cumulative impact
- Weekly health report posted to Slack and stored in Attio
- Optimization velocity metrics for meta-analysis

## Triggers

Runs continuously once configured. Daily health checks at 08:00 UTC. Weekly report at Monday 09:00 UTC.
