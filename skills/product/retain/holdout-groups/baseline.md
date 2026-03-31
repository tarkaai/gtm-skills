---
name: holdout-groups-baseline
description: >
  Holdout Group Analysis — Baseline Run. Run the holdout measurement system always-on
  with weekly automated lift calculations, integrity monitoring, and a dedicated
  PostHog dashboard comparing holdout vs treatment populations.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 4 weeks"
outcome: ">=10% confirmed cumulative lift (treatment vs holdout) at 95% confidence"
kpis: ["Cumulative lift %", "Lift statistical significance", "Holdout integrity score", "Experiment count since holdout creation"]
slug: "holdout-groups"
install: "npx gtm-skills add product/retain/holdout-groups"
drills:
  - holdout-lift-measurement
  - holdout-integrity-monitor
  - posthog-gtm-events
---

# Holdout Group Analysis — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Weekly automated measurement of cumulative lift between holdout and treatment populations. A PostHog dashboard shows the lift trend over time. Holdout integrity is validated weekly with automated checks. At least 3 experiments have been shipped to the treatment group while the holdout remains clean. Cumulative lift reaches >=10% on the primary metric with 95% statistical confidence.

## Leading Indicators

- Weekly lift measurements running via n8n automation
- Holdout integrity checks passing every week (no contamination, stable size, demographic parity)
- Lift trend line is positive and increasing week over week
- Treatment group shows improving metrics while holdout group remains stable

## Instructions

### 1. Configure holdout-specific event tracking

Run the `posthog-gtm-events` drill to add holdout-specific events to your taxonomy:
- `holdout_lift_measured` — fired weekly with properties: `metric_name`, `holdout_value`, `treatment_value`, `lift_pct`, `p_value`, `significant`
- `holdout_integrity_check` — fired weekly with properties: `group_size_status`, `contamination_status`, `parity_status`, `overall_verdict`
- `holdout_experiment_shipped` — fired when a new experiment launches, confirming holdout exclusion filter is present

### 2. Launch weekly lift measurement

Run the `holdout-lift-measurement` drill to set up automated weekly measurement. This creates an n8n workflow that:
- Queries PostHog for holdout vs treatment metrics every Monday
- Computes cumulative lift percentage for each primary metric
- Assesses statistical significance (p-value)
- Builds the lift trend over time (week-over-week change)
- Stores results in Attio and logs to PostHog

Configure the measurement for your primary metrics:
- Retention rate (Week 4 retention for users in each group)
- Engagement frequency (average actions per user per week)
- Conversion rate (if applicable — e.g., free-to-paid, feature adoption)

### 3. Launch weekly integrity monitoring

Run the `holdout-integrity-monitor` drill to set up automated weekly validation. This creates an n8n workflow that runs four checks:
- Group size stability (holdout % within +/-2% of target)
- Contamination detection (zero holdout users exposed to experiments)
- Demographic parity (no property differs >5% between groups)
- Baseline parity confirmation (groups were equivalent at creation)

Configure alerts: any FAIL result triggers an immediate notification to the holdout program owner.

### 4. Ship experiments to the treatment group

Continue running your product optimization experiments (A/B tests, feature rollouts, onboarding improvements). For every experiment:
- Verify the holdout exclusion filter is present in the experiment's feature flag
- Log the experiment in the holdout tracking system: experiment name, start date, hypothesis, primary metric
- After each experiment concludes, record its individual result alongside the cumulative holdout lift

Aim for at least 3 experiments shipped during the 4-week Baseline window. More experiments = faster cumulative lift growth.

### 5. Evaluate against threshold

After 4 weeks, review the cumulative lift data:
- Primary metric lift must be >=10% (treatment outperforms holdout by 10%+)
- Statistical significance must be p < 0.05 (95% confidence)
- Holdout integrity must have been PASS on every weekly check

If PASS, proceed to Scalable. If FAIL:
- If lift is positive but below 10%: ship more impactful experiments. Extend the measurement window by 2 weeks.
- If lift is not statistically significant: extend the measurement window (more data = more power). Or increase holdout size if feasible.
- If integrity failed: fix the contamination or drift issue, then restart the measurement clock.

## Time Estimate

- 4 hours: configure event tracking and set up automated workflows
- 2 hours: build the holdout dashboard in PostHog
- 8 hours: ship and monitor 3+ experiments over 4 weeks (2-3 hours per experiment)
- 2 hours: weekly review of lift and integrity reports (30 min/week x 4)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, dashboards, event tracking | Free up to 1M flag requests/mo; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Weekly cron workflows for lift measurement and integrity checks | Starter: ~$24/mo for 2,500 executions ([n8n.io/pricing](https://n8n.io/pricing)) |

## Drills Referenced

- `holdout-lift-measurement` — weekly automated comparison of holdout vs treatment metrics with statistical significance
- `holdout-integrity-monitor` — weekly validation of group size, contamination, and demographic parity
- `posthog-gtm-events` — holdout-specific event taxonomy setup
