---
name: holdout-integrity-monitor
description: Continuously validate that the holdout group is not contaminated by experiments, has stable size, and maintains demographic parity with the treatment group
category: Experimentation
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-holdout-group
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - n8n-triggers
  - attio-notes
---

# Holdout Integrity Monitor

A holdout group is only as valuable as its integrity. If holdout users are accidentally exposed to experiments, if the group size drifts, or if the holdout population becomes systematically different from the treatment population, the lift measurements become meaningless. This drill runs continuous validation checks.

## Input

- A provisioned holdout group (output of `holdout-group-setup`)
- PostHog project with both cohorts tracked
- n8n instance for automated scheduling
- Alert destination (Slack channel or email)

## Steps

### 1. Build the integrity check workflow in n8n

Using `n8n-scheduling`, create a weekly cron-triggered n8n workflow (every Monday at 08:00 UTC). The workflow runs four checks in sequence and reports a PASS/FAIL verdict.

### 2. Check 1 — Group size stability

Using `posthog-cohorts`, query the current holdout group size:

```sql
SELECT
  if(JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout', 'holdout', 'treatment') AS grp,
  uniqExact(distinct_id) AS user_count
FROM events
WHERE timestamp > now() - interval 7 day
GROUP BY grp
```

Compute `holdout_pct = holdout_count / (holdout_count + treatment_count) * 100`.

**PASS:** holdout_pct is within +/-2 percentage points of the target (e.g., for a 10% holdout, acceptable range is 8-12%).
**FAIL:** holdout_pct is outside the acceptable range. Causes: new users not being evaluated against the holdout flag, flag configuration changed, or a bulk user import bypassed PostHog identification.

### 3. Check 2 — Contamination detection

Using `posthog-holdout-group`, run the contamination query to find holdout users who were evaluated against experiment feature flags:

```sql
SELECT
  distinct_id,
  groupArray(DISTINCT properties.$feature_flag_response) AS experiment_flags_seen
FROM events
WHERE event = '$feature_flag_called'
  AND JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout'
  AND properties.$feature_flag NOT IN ('global-holdout')
  AND timestamp > now() - interval 7 day
GROUP BY distinct_id
```

**PASS:** Zero holdout users were evaluated against any experiment flag.
**FAIL:** One or more holdout users were exposed to experiments. For each contaminated user, log: `distinct_id`, which experiment flag they saw, and when. The offending experiment's filter conditions must be fixed immediately.

### 4. Check 3 — Demographic parity

Using `posthog-cohorts`, compare key properties between holdout and treatment populations to ensure the groups have not drifted apart:

```sql
SELECT
  if(JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout', 'holdout', 'treatment') AS grp,
  countIf(JSONExtractString(person_properties, 'plan') = 'free') / count() AS free_pct,
  countIf(JSONExtractString(person_properties, 'plan') = 'pro') / count() AS pro_pct,
  avg(toFloat(JSONExtractString(person_properties, 'days_since_signup'))) AS avg_tenure
FROM events
WHERE timestamp > now() - interval 7 day
  AND event = '$identify'
GROUP BY grp
```

**PASS:** No property distribution differs by more than 5 percentage points between groups.
**FAIL:** A property has drifted, meaning the groups are no longer comparable. Common cause: a specific acquisition channel routes all new users to treatment, skewing the treatment group toward newer users. Fix by ensuring the holdout flag evaluates before any other routing.

### 5. Check 4 — Baseline metric parity at holdout creation

Compare the holdout group's metrics in the first week after creation against the treatment group's metrics in the same period. This validates that the groups were equivalent at the start:

**PASS:** Primary metrics within +/-5% between groups during the first week.
**FAIL:** Groups were not equivalent from the start. The holdout may need to be dissolved and recreated with a larger sample or different randomization seed.

### 6. Generate integrity report

Using `n8n-workflow-basics`, compile the four check results into a structured report:

```json
{
  "report_date": "2026-03-30",
  "holdout_target_pct": 10,
  "checks": {
    "group_size": {"status": "PASS", "actual_pct": 10.2},
    "contamination": {"status": "PASS", "contaminated_users": 0},
    "demographic_parity": {"status": "PASS", "max_drift_pct": 2.1},
    "baseline_parity": {"status": "PASS", "initial_metric_diff_pct": 1.8}
  },
  "overall": "PASS",
  "holdout_valid": true
}
```

Store in Attio using `attio-notes`. Log to PostHog using `posthog-custom-events`:
- Event: `holdout_integrity_check`
- Properties: all check statuses, overall verdict, any failure details

### 7. Alert on failure

Using `n8n-triggers`, send an immediate alert if any check fails:

- **Group size failure:** "Holdout group has drifted to {actual_pct}% (target: {target_pct}%). Investigate new user flag evaluation."
- **Contamination failure:** "{N} holdout users were exposed to experiment {flag_name}. Fix experiment filter conditions immediately."
- **Demographic drift:** "Holdout and treatment groups have diverged on {property}: holdout={holdout_value}, treatment={treatment_value}."
- **Baseline parity failure:** "Holdout group was not equivalent at creation. Consider dissolving and recreating."

Route alerts to the person who owns the holdout program. Contamination alerts are urgent — they degrade every ongoing lift measurement.

## Output

- Weekly integrity report with 4 check results (PASS/FAIL)
- Attio notes with integrity history for audit trail
- PostHog events for longitudinal integrity tracking
- Immediate alerts on any integrity violation

## Triggers

At Baseline: run weekly via n8n cron. At Scalable+: run weekly with automated remediation (auto-fix experiment filters on contamination detection).
