---
name: deprecation-health-monitor
description: Continuous monitoring of deprecation migration health across all active sunsets, with automated alerting and trend analysis for long-running optimization
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
  - attio-custom-attributes
---

# Deprecation Health Monitor

This drill provides the always-on monitoring layer for feature deprecations running at Durable level. It tracks migration health across all active sunsets, detects when migration velocity stalls, identifies users who are at risk of being stranded at sunset, and feeds data into the autonomous optimization loop. This is the deprecation-specific monitoring that complements the generic `autonomous-optimization` drill.

## Input

- One or more active feature deprecations with migration tracking in place
- PostHog events and cohorts from the deprecation migration tracker
- At least 4 weeks of migration data (needed for trend analysis)
- Attio records tagged with migration scores and tiers

## Steps

### 1. Build the deprecation health dashboard

Using `posthog-dashboards`, create a master dashboard that aggregates across all active deprecations:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Active deprecations overview | Table | Feature, sunset date, days remaining, migration %, risk level |
| Migration velocity trend | Multi-line chart | Weekly migration completion rate per active deprecation |
| Stranded user forecast | Area chart | Projected unmigrated users at sunset, updated daily |
| Stall rate by route | Grouped bar | Which migration paths have the highest stall rates |
| Communication effectiveness | Funnel | Notice shown -> clicked -> migration started -> completed |
| Revenue at risk | Single number | MRR of users projected to be unmigrated at sunset |
| Intervention save rate | Percentage | Users who were stalled but completed migration after intervention |

### 2. Configure anomaly detection

Using `posthog-anomaly-detection`, set up monitoring for:

- **Migration velocity drop:** If weekly migration completions drop 30%+ from the rolling 4-week average, something broke. Common causes: communication fatigue, replacement feature regression, new user cohort with different needs.
- **Stall rate spike:** If the percentage of stalled users increases 20%+ week-over-week, the migration path has a new blocker.
- **Regression surge:** If regressed users (tried replacement, went back) increase 50%+ in a week, the replacement feature may have a bug or usability issue.

### 3. Build automated alerting workflow

Using `n8n-scheduling`, create a workflow that runs daily at 09:00 UTC:

1. Query PostHog for current migration metrics across all active deprecations
2. Compare against baselines from the anomaly detection rules
3. For each anomaly detected:
   - Classify severity: warning (trend concerning) vs. critical (immediate risk to sunset deadline)
   - Generate a brief: what changed, when it started, which users/segments are affected, potential causes
   - Store the alert in Attio using `attio-notes`
   - For critical alerts: send a webhook to trigger human review

4. Even when no anomalies are detected, log a daily health check event:

```javascript
posthog.capture('deprecation_health_check', {
  feature_slug: '{feature_slug}',
  migration_pct: currentMigrationPercent,
  stall_rate: currentStallRate,
  days_to_sunset: daysRemaining,
  projected_completion_pct: projectedCompletion,
  status: 'healthy' // or 'warning' or 'critical'
});
```

### 4. Track deprecation lifecycle metrics

Using `posthog-custom-events`, maintain a running record of each deprecation's lifecycle:

- **Time to 50% migration:** How many days from announcement to half the affected users being migrated. Benchmark for future deprecations.
- **Communication touchpoints per migration:** How many notices/emails it took before the average user completed migration. Lower is better.
- **Intervention efficiency:** For each intervention type (self-serve, guided, high-touch, rescue), track cost (staff hours + tool costs) and success rate. Build a cost-per-migration metric.
- **Post-sunset orphan rate:** After the feature is actually removed, how many users experienced errors or filed support tickets because they were not migrated. This is the ultimate failure metric.

### 5. Generate weekly deprecation health reports

Using `n8n-scheduling`, run a weekly workflow (Monday 08:00 UTC) that:

1. Aggregates all daily health check data for the week
2. Computes: migration progress delta, stall rate trend, intervention effectiveness, projected completion
3. Generates a structured report:
   - **Status:** On track / At risk / Critical
   - **Progress:** X% migrated (up/down Y% from last week)
   - **Velocity:** Z users/week completing migration (accelerating/decelerating)
   - **Risk:** N users projected unmigrated at sunset, representing $X MRR
   - **Interventions:** A sent, B converted, C% save rate
   - **Recommendations:** What the autonomous optimization loop should test next
4. Store the report in Attio using `attio-notes`

### 6. Feed data into autonomous optimization

The health monitor produces the metrics that the `autonomous-optimization` drill consumes. Specifically:

- **Primary KPI for optimization:** migration completion rate
- **Secondary KPIs:** stall rate, communication engagement rate, intervention save rate
- **Anomaly triggers:** any anomaly detected by this monitor becomes an input to the optimization loop's diagnosis phase
- **Experiment evaluation data:** when the optimization loop runs A/B tests on migration messaging or routing, this monitor provides the outcome data

Ensure the health monitor's PostHog events use consistent property names so the autonomous optimization drill can query them without custom mapping.

## Output

- Master deprecation health dashboard in PostHog
- Daily anomaly detection with automated alerting
- Daily health check events logged to PostHog
- Weekly deprecation health reports in Attio
- Lifecycle metrics (time to 50%, touchpoints per migration, cost per migration, orphan rate)
- Clean data feed for the autonomous optimization drill

## Triggers

Daily health check runs at 09:00 UTC via n8n cron. Weekly report runs Monday 08:00 UTC. Anomaly alerts fire in real-time when thresholds are breached. Continue running until 30 days after the last active deprecation's sunset date.
