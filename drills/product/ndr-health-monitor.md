---
name: ndr-health-monitor
description: Continuous NDR health monitoring that feeds the autonomous optimization loop — tracks intervention effectiveness, component drift, and convergence signals
category: Product
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-cohorts
  - attio-notes
  - attio-custom-attributes
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# NDR Health Monitor

This drill is the Durable-level monitoring layer for net dollar retention. It operates alongside the `autonomous-optimization` drill, feeding it the signals it needs to detect when NDR components drift and generating the context for hypothesis generation. While `autonomous-optimization` runs the experiment loop, this drill owns the NDR-specific intelligence: which component is degrading, which segments are affected, and what interventions have worked historically.

## Prerequisites

- `ndr-cohort-tracking` drill running at Scalable level for at least 4 weeks (baseline data required)
- `autonomous-optimization` drill configured for this play
- PostHog with billing events and NDR tracking events flowing
- Attio with historical NDR data and intervention logs
- Anthropic API key for Claude (diagnostic analysis)

## Steps

### 1. Build the NDR signal pipeline

Using `n8n-scheduling`, create a daily workflow (runs 07:00 UTC) that computes real-time NDR health signals:

1. Query PostHog for trailing 7-day billing events
2. Compute rolling NDR components:
   - 7-day churned MRR rate (annualized)
   - 7-day contraction MRR rate (annualized)
   - 7-day expansion MRR rate (annualized)
   - 7-day logo churn rate (annualized)
3. Compare each component against its 30-day rolling average
4. Using `posthog-anomaly-detection`, classify each component:
   - **Normal:** Within one standard deviation of 30-day average
   - **Watch:** Between one and two standard deviations
   - **Alert:** Beyond two standard deviations
5. Using `posthog-custom-events`, emit a daily `ndr_health_signal` event:

```javascript
posthog.capture('ndr_health_signal', {
  date: '2026-03-30',
  ndr_7d_annualized: 112.4,
  churn_component_status: 'normal',
  contraction_component_status: 'watch',
  expansion_component_status: 'normal',
  logo_churn_status: 'normal',
  churned_mrr_7d: 1200,
  contraction_mrr_7d: 450,
  expansion_mrr_7d: 2800,
  churn_deviation_sigma: 0.4,
  contraction_deviation_sigma: 1.3,
  expansion_deviation_sigma: -0.2,
  accounts_at_risk_count: 7,
  accounts_expanding_count: 12
});
```

### 2. Track intervention effectiveness over time

Using `posthog-cohorts`, create cohorts for accounts that received each type of retention/expansion intervention:

- **Churn prevention intervention cohort:** Accounts that received churn-prevention outreach (from the `churn-prevention` drill)
- **Upgrade prompt cohort:** Accounts that received expansion prompts (from the `upgrade-prompt` drill)
- **Health score alert cohort:** Accounts that received health-based interventions (from the `health-score-alerting` drill)

For each cohort, track outcomes 30 and 90 days after intervention:

```sql
SELECT
  properties.intervention_type AS intervention,
  count() AS total_interventions,
  countIf(properties.outcome = 'retained') AS retained,
  countIf(properties.outcome = 'expanded') AS expanded,
  countIf(properties.outcome = 'churned') AS churned,
  countIf(properties.outcome = 'retained') / count() * 100 AS save_rate,
  countIf(properties.outcome = 'expanded') / count() * 100 AS expansion_rate
FROM events
WHERE event = 'intervention_outcome_30d'
  AND timestamp > now() - interval 90 day
GROUP BY intervention
```

Store these effectiveness metrics in Attio using `attio-custom-attributes` on an "NDR Optimization" record.

### 3. Build the component drift detector

Using `n8n-workflow-basics`, extend the daily workflow to detect multi-day trends:

1. Pull the last 14 daily `ndr_health_signal` events from PostHog
2. Compute trend direction for each NDR component:
   - **Improving:** 3+ consecutive days of improvement or return from Alert to Normal
   - **Stable:** Fluctuating within Normal range
   - **Degrading:** 3+ consecutive days of worsening or any component in Alert for 2+ days
3. When a component enters "Degrading" status, generate an NDR-specific context package for the `autonomous-optimization` drill:

```json
{
  "play": "net-retention-optimization",
  "degrading_component": "contraction",
  "current_value": 8.2,
  "baseline_value": 5.1,
  "deviation_sigma": 2.1,
  "affected_segments": ["mid-lifecycle", "starter-plan"],
  "recent_interventions": [
    {"type": "churn-prevention", "count": 12, "save_rate": 0.42},
    {"type": "upgrade-prompt", "count": 28, "save_rate": 0.08}
  ],
  "historical_experiments": [
    {"hypothesis": "Earlier churn detection threshold", "result": "adopted", "impact": "+3% save rate"},
    {"hypothesis": "Personalized downgrade alternatives", "result": "reverted", "impact": "no effect"}
  ]
}
```

This context package is what the `autonomous-optimization` drill's `hypothesis-generation` fundamental uses to generate targeted improvement hypotheses.

### 4. Detect convergence

The optimization loop should not run forever at full intensity. Using `posthog-custom-events`, track the impact of each adopted experiment on NDR:

1. After each experiment the `autonomous-optimization` drill adopts, log an `ndr_experiment_impact` event with the measured NDR change
2. Maintain a rolling window of the last 6 adopted experiments
3. Compute the average impact of recent experiments
4. If the average impact of the last 3 consecutive experiments is <2% improvement on the targeted NDR component, the play has reached its local maximum for that component

When convergence is detected:
- Log a `ndr_convergence_reached` event in PostHog with the converged component and its final value
- Reduce the monitoring frequency for that component from daily to weekly
- Using `attio-notes`, log the convergence milestone on the play record
- The `autonomous-optimization` drill should shift focus to the next-lowest-performing NDR component

### 5. Generate the weekly NDR optimization brief

Using the `hypothesis-generation` fundamental (Claude), synthesize the week's NDR health data into an executive brief:

```
# NDR Optimization Brief — Week of [date]

## Current NDR: [X%] (target: [Y%])
## Trend: [Improving / Stable / Degrading] for [N] consecutive weeks

## Component Health
| Component | Status | Value | vs. Baseline | Trend |
|-----------|--------|-------|-------------|-------|
| Churn | [Normal/Watch/Alert] | [X%] | [+/-Y%] | [arrow] |
| Contraction | [Normal/Watch/Alert] | [X%] | [+/-Y%] | [arrow] |
| Expansion | [Normal/Watch/Alert] | [X%] | [+/-Y%] | [arrow] |

## Experiments This Week
- Active: [description, variant performance so far]
- Completed: [description, result, impact]
- Queued: [next hypothesis to test]

## Intervention Effectiveness (trailing 30 days)
| Intervention | Volume | Save Rate | Expansion Rate |
|-------------|--------|-----------|---------------|
| Churn prevention | [N] | [X%] | — |
| Upgrade prompt | [N] | — | [X%] |
| Health-based alert | [N] | [X%] | [X%] |

## Convergence Status
- Churn component: [Optimizing / Converged at X%]
- Contraction component: [Optimizing / Converged at X%]
- Expansion component: [Optimizing / Converged at X%]

## Recommended Focus
[AI-generated recommendation based on which component has the most room for improvement]
```

Post to Slack and store in Attio.

## Output

- Daily NDR health signals emitted to PostHog with per-component status
- Intervention effectiveness tracking across all retention/expansion drills
- Component drift detection that feeds the `autonomous-optimization` drill with targeted context
- Convergence detection that reduces optimization intensity when local maximum is reached
- Weekly NDR optimization brief synthesized by Claude

## Triggers

- Daily health signal computation: cron, 07:00 UTC
- Component drift detection: piggybacks on daily signal computation
- Convergence check: runs after each experiment is adopted (triggered by `autonomous-optimization`)
- Weekly brief: cron, Monday 09:00 UTC
