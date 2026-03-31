---
name: flag-lifecycle-automation
description: Automate feature flag creation, progressive rollout schedules, and stale flag cleanup via PostHog API and n8n
category: Experimentation
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-cohorts
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - n8n-error-handling
  - attio-notes
---

# Flag Lifecycle Automation

This drill builds the automation layer for managing feature flags from creation through full rollout to retirement. Instead of manually creating flags and adjusting rollout percentages, the agent operates a structured lifecycle: create flag with metadata, execute a progressive rollout schedule, monitor for regressions at each stage, and clean up stale flags that have reached 100% and stabilized.

## Input

- PostHog project with feature flags enabled and SDK installed in the product
- n8n instance for scheduling rollout steps and cleanup jobs
- A list of features planned for flagged rollout (name, description, target audience, risk level)
- Attio configured for logging flag lifecycle events

## Steps

### 1. Standardize flag creation

Build an n8n workflow triggered by webhook (called when engineering marks a feature as ready-to-flag). The workflow uses the `posthog-feature-flags` fundamental to create the flag via API:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "{feature-slug}",
  "name": "{Feature Name}",
  "filters": {
    "groups": [{
      "rollout_percentage": 0,
      "properties": []
    }]
  },
  "active": true
}
```

Attach metadata as flag properties:
- `owner`: the team or person responsible for this flag
- `created_date`: ISO timestamp
- `risk_level`: low | medium | high
- `expected_full_rollout_date`: calculated from risk level (low=7d, medium=14d, high=28d)
- `rollout_schedule`: the specific percentage stages this flag will follow

Use `posthog-custom-events` to log `flag_created` with the flag key, owner, and risk level.

### 2. Define progressive rollout schedules

Based on risk level, assign a rollout schedule:

**Low risk** (UI tweaks, copy changes):
- Day 0: 5% (canary)
- Day 1: 25%
- Day 3: 50%
- Day 5: 100%

**Medium risk** (new features, workflow changes):
- Day 0: 2% (canary)
- Day 2: 10%
- Day 5: 25%
- Day 7: 50%
- Day 10: 75%
- Day 14: 100%

**High risk** (pricing changes, core flow changes):
- Day 0: 1% (canary, internal users only via cohort)
- Day 3: 5%
- Day 7: 10%
- Day 14: 25%
- Day 21: 50%
- Day 28: 100%

Store the schedule in the n8n workflow context so the agent knows what comes next.

### 3. Build the rollout progression workflow

Create an n8n cron workflow that runs daily and checks all active flags against their rollout schedule:

1. Query PostHog API for all active feature flags: `GET /api/projects/<id>/feature_flags/?active=true`
2. For each flag, compare current rollout percentage against the schedule
3. If the flag is due for a percentage increase:
   a. Check the regression gate (Step 4) before proceeding
   b. If gate passes: `PATCH /api/projects/<id>/feature_flags/<flag-id>/` to update rollout_percentage
   c. Log `flag_rollout_advanced` event with flag key, old percentage, new percentage
   d. Create an Attio note using `attio-notes`: "Flag {key} advanced from {old}% to {new}%"
4. If the flag is overdue (missed its scheduled advance by 2+ days), alert the owner

Use `n8n-error-handling` to handle API failures gracefully — a failed rollout advance should retry once, then alert rather than silently skip.

### 4. Implement regression gates

Before each rollout percentage increase, the workflow checks for regressions:

1. Query PostHog for error rates and key metrics for users in the flag's treatment group vs control group over the last 48 hours
2. Compare: if treatment group shows >10% higher error rate OR >15% lower conversion on any tracked metric, BLOCK the rollout advance
3. Log `flag_rollout_blocked` event with the regression details
4. Send alert to the flag owner with specific metrics that failed the gate
5. The flag stays at its current percentage until the owner manually unblocks (via webhook to n8n) or the regression resolves in the next daily check

Using `posthog-cohorts`, create dynamic cohorts for each flag's treatment and control groups to enable this comparison.

### 5. Build the stale flag cleanup workflow

Create an n8n weekly cron workflow that identifies flags ready for cleanup:

1. Query all feature flags at 100% rollout
2. For each, check: has it been at 100% for 14+ days with no regressions?
3. If yes, mark the flag as `cleanup_ready` by adding a tag via the PostHog API
4. Generate a cleanup report: flag key, owner, days at 100%, recommendation (archive)
5. Log `flag_cleanup_recommended` event
6. Post the report to the team (Slack or email via n8n)

The agent does NOT delete flags automatically — it recommends cleanup and the engineering team removes the flag from code, then archives via API: `PATCH /api/projects/<id>/feature_flags/<flag-id>/ {"deleted": true}`

### 6. Track flag inventory health

Using `posthog-custom-events`, maintain running metrics:
- `flags_active_count`: total active flags (alert if >20 — flag debt is accumulating)
- `flags_stale_count`: flags at 100% for >14 days not yet archived
- `flags_blocked_count`: flags with rollout blocked by regression
- `avg_rollout_duration_days`: mean time from flag creation to 100% rollout

These metrics feed into the flag rollout health monitor at higher play levels.

## Output

- Standardized flag creation workflow triggered by webhook
- Progressive rollout schedules for 3 risk levels
- Daily rollout progression workflow with regression gates
- Weekly stale flag cleanup report
- Flag inventory health metrics in PostHog

## Triggers

The rollout progression workflow runs daily via n8n cron. The cleanup workflow runs weekly. Flag creation runs on-demand via webhook. Re-run setup when changing rollout schedule policies or regression gate thresholds.
