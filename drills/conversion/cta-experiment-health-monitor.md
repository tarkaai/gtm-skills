---
name: cta-experiment-health-monitor
description: Track CTA experiment velocity, cumulative lift, and surface coverage to ensure continuous optimization health
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-experiments
  - posthog-custom-events
  - n8n-scheduling
  - attio-reporting
---

# CTA Experiment Health Monitor

This drill builds an always-on monitoring system that tracks the health of CTA optimization across all surfaces. It answers: are we testing fast enough, are our tests producing lift, and are any surfaces being neglected? Designed to run alongside `autonomous-optimization` at the Durable level.

## Input

- PostHog with experiment data from at least 4 completed CTA tests
- Attio experiment log with historical test results
- n8n instance for scheduled health checks
- All CTA surfaces instrumented with `cta_impression`, `cta_clicked`, and conversion events

## Steps

### 1. Build the CTA optimization dashboard

Using `posthog-dashboards`, create a dashboard named "CTA Optimization Health" with these panels:

| Panel | Visualization | Data Source |
|-------|--------------|-------------|
| Cumulative CTR lift (all time) | Line chart | Running total of lift from all shipped variants |
| Active experiments | Table | Currently running experiments with start date, days elapsed, sample size |
| Experiment velocity | Bar chart | Tests completed per month (target: 2-4/month) |
| Win rate | Trend line | Percentage of experiments that produced a statistically significant winner |
| Surface coverage | Heatmap | Which CTA surfaces have been tested recently vs neglected |
| Top-performing CTAs | Table | Current best variant per surface with CTR and conversion rate |
| Diminishing returns tracker | Line chart | Lift from each successive experiment (detect convergence) |

### 2. Build the experiment velocity monitor

Using `n8n-scheduling`, create a weekly cron workflow that:

1. Queries PostHog for all experiments tagged with `cta-variant-*`
2. Counts experiments completed in the last 30 days
3. Compares to target velocity (2-4 experiments/month)
4. If below target: alerts that optimization is stalling. Diagnose: are experiments running too long (insufficient traffic), or are new experiments not being queued?
5. If above target: verify experiments are not being stopped prematurely (minimum 7 days or 200 samples per variant)

### 3. Build the surface neglect detector

Using `posthog-custom-events`, query all unique `page` + `surface_type` combinations from `cta_impression` events in the last 90 days. For each surface:

- Check when it was last included in an experiment
- If never tested: flag as "untested surface"
- If last tested > 60 days ago and CTR is below the cross-surface median: flag as "stale -- due for retesting"
- If last tested > 60 days ago but CTR is above median: flag as "performing -- low priority"

Output a ranked list of surfaces by optimization priority (untested first, then stale underperformers, then stale performers).

### 4. Track diminishing returns

For each CTA surface, plot the lift from each successive experiment in chronological order. Using `posthog-experiments` data:

- If the last 3 experiments on a surface all produced < 2% lift: the surface has converged. Report: "Surface {X} has reached its local maximum at {CTR}%. Further CTA optimization will not produce meaningful gains. Consider testing the entire page layout, value proposition, or traffic source instead."
- If lift is still > 5% per experiment: the surface has room for optimization. Keep testing.

### 5. Generate weekly optimization brief

Using `n8n-scheduling`, create a weekly cron workflow that assembles:

1. **Experiments this week:** which experiments started, which completed, which decisions were made
2. **Cumulative lift:** total CTR improvement across all surfaces since optimization began
3. **Revenue impact estimate:** if CTA optimization feeds a conversion funnel, estimate the revenue impact of the cumulative lift (e.g., "+12% CTR on pricing page CTA -> estimated +X signups/month")
4. **Next actions:** which surfaces to test next, which hypotheses are queued
5. **Convergence status:** which surfaces are converged, which still have headroom

Post the brief to Slack and store in Attio as a campaign note.

### 6. Set guardrail alerts

Configure alerts that fire immediately (not weekly) when:

- Any CTA surface CTR drops > 25% vs its 4-week average (possible technical break or traffic change)
- An experiment's variant is performing > 30% worse than control after 3+ days with 100+ samples (auto-revert candidate)
- Total CTA impressions across all surfaces drops > 40% (traffic problem, not a CTA problem)

Route alerts to the optimization owner via Slack and Attio.

## Output

- CTA Optimization Health dashboard in PostHog (7 panels)
- Weekly experiment velocity check with alerts
- Surface neglect detection and prioritization
- Diminishing returns / convergence tracking per surface
- Weekly optimization brief with cumulative lift and next actions
- Real-time guardrail alerts for CTR drops and experiment failures

## Triggers

- Weekly health check: runs every Monday at 9 AM via n8n cron
- Weekly optimization brief: runs every Friday at 4 PM via n8n cron
- Guardrail alerts: event-triggered via n8n, fires within minutes of threshold breach
