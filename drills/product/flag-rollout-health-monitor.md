---
name: flag-rollout-health-monitor
description: Monitor feature flag rollout success rates, rollback frequency, flag hygiene, and system-wide flag health
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-feature-flags
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - posthog-cohorts
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Flag Rollout Health Monitor

This drill builds the observability layer for your feature flag system. It tracks whether flags are being rolled out successfully, how often rollbacks occur, whether stale flags are accumulating, and whether the flag system is making your product more stable or less stable over time. This is the measurement companion to the `flag-lifecycle-automation` drill.

## Input

- Feature flag lifecycle automation already running (from `flag-lifecycle-automation` drill)
- PostHog tracking flag lifecycle events (`flag_created`, `flag_rollout_advanced`, `flag_rollout_blocked`, `flag_cleanup_recommended`)
- At least 4 weeks of flag lifecycle data for meaningful trends
- n8n instance for scheduled health checks

## Steps

### 1. Define flag health KPIs

Track these metrics, computed weekly:

| KPI | Calculation | Target |
|-----|------------|--------|
| Rollout success rate | Flags reaching 100% without rollback / total flags created | >=90% |
| Mean time to full rollout | Average days from flag creation to 100% | Low risk: <=7d, Medium: <=14d, High: <=28d |
| Rollback rate | Flags rolled back / total flags created | <=10% |
| Mean time to detect regression | Hours from rollout advance to regression gate blocking | <=24h |
| Stale flag count | Flags at 100% for >14 days not archived | <=5 |
| Active flag count | Total active flags at any given time | <=20 |
| Flag debt ratio | Stale flags / total active flags | <=25% |
| Blocked flag count | Flags with rollout currently blocked by regression | <=3 |

### 2. Build the flag health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard with these panels:

| Panel | Visualization | Data Source |
|-------|--------------|-------------|
| Rollout success rate (weekly trend) | Line chart | `flag_created` vs `flag_rollout_completed` events |
| Active flags by rollout stage | Stacked bar | Current flag states: canary, partial, full, stale |
| Rollback timeline | Event timeline | `flag_rollout_blocked` events with regression details |
| Mean time to full rollout | Line chart (trend) | `flag_created` to `flag_rollout_completed` duration |
| Stale flag inventory | Table | Flags at 100% for >14d, sorted by days stale |
| Flag debt ratio (weekly trend) | Line chart | Stale / active ratio over time |
| Per-flag impact on product metrics | Table | For each active flag: error rate delta, conversion delta |

### 3. Build the weekly health check workflow

Using `n8n-scheduling`, create a workflow that runs every Monday:

1. Query PostHog for all flag lifecycle events from the past 7 days
2. Compute each KPI from Step 1
3. Compare against targets — classify each as GREEN (on target), YELLOW (within 20% of target), RED (exceeds target)
4. Generate a structured health report:
   ```
   Flag System Health — Week of {date}

   Rollout Success Rate: {value} [{GREEN|YELLOW|RED}]
   Mean Time to Full Rollout: {value} [{GREEN|YELLOW|RED}]
   Rollback Rate: {value} [{GREEN|YELLOW|RED}]
   Active Flags: {count} [{GREEN|YELLOW|RED}]
   Stale Flags: {count} [{GREEN|YELLOW|RED}]
   Flag Debt Ratio: {value} [{GREEN|YELLOW|RED}]

   Flags Rolled Back This Week:
   - {flag-key}: {regression reason}, rolled back at {percentage}%

   Flags Ready for Cleanup:
   - {flag-key}: at 100% for {days} days, owner: {owner}

   Recommended Actions:
   - {action 1}
   - {action 2}
   ```
5. Log the report as an Attio note using `attio-notes`
6. Post to the team channel

### 4. Set up anomaly alerts

Using `posthog-anomaly-detection`, configure alerts for:

- **Rollout success rate drops below 80%** for 2 consecutive weeks: something is wrong with release quality or flag configuration. Investigate recent failed rollouts for common patterns.
- **Active flag count exceeds 25**: flag debt is accumulating faster than cleanup. Trigger a flag cleanup sprint.
- **Rollback rate exceeds 20%**: either regression gates are too sensitive (false positives) or release quality has degraded. Review the last 5 rollbacks to distinguish.
- **Mean time to full rollout increases by >50%** vs 4-week average: rollouts are getting slower. Check if regression gates are blocking too frequently or if the team is not advancing flags on schedule.

Each alert triggers an n8n workflow that creates a triage task with the specific data needed to diagnose the issue.

### 5. Track per-flag product impact

For each active feature flag, maintain a running comparison between the treatment and control groups using `posthog-cohorts`:

1. Create dynamic cohorts: `flag-{key}-treatment` (users seeing the feature) and `flag-{key}-control` (users not seeing it)
2. Weekly, compare key product metrics between groups: session frequency, feature engagement, error rates, conversion rates
3. Store the comparison in PostHog as a saved insight: "{flag-key} Impact Analysis"
4. If any flag shows a statistically significant negative impact on a key metric after 7+ days, alert the owner even if the regression gate did not catch it (the gate checks 48-hour windows; this checks longer-term trends)

### 6. Generate monthly flag system report

On the first Monday of each month, generate a comprehensive report:

- Total flags created, completed (100%), rolled back, and archived this month
- Month-over-month trend for each KPI
- Top 3 most impactful flags (largest positive product metric delta)
- Top 3 most problematic flags (triggered regressions, took longest to roll out)
- Flag debt status and cleanup recommendations
- Recommendations for adjusting rollout schedules or regression gate thresholds based on the month's data

## Output

- Flag health dashboard in PostHog with 7 panels
- Weekly automated health check with KPI scoring
- Anomaly alerts for 4 critical flag health metrics
- Per-flag product impact tracking via cohort comparison
- Monthly comprehensive flag system report

## Triggers

Weekly health check runs every Monday via n8n cron. Per-flag impact tracking runs daily. Monthly report runs on the first Monday of each month. Re-run setup when adding new KPIs or changing target thresholds.
