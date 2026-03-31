---
name: holdout-group-setup
description: Design and provision a persistent holdout group using PostHog feature flags, defining the control population that measures cumulative experiment impact
category: Measurement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-holdout-group
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-cohorts
  - n8n-workflow-basics
  - attio-notes
---

# Holdout Group Setup

This drill provisions a persistent holdout group — a randomly selected subset of users who are permanently excluded from all experiments. The holdout group acts as a long-running control, letting you measure the cumulative impact of every optimization you ship, not just individual A/B test results.

## Input

- PostHog project with identified users and at least 4 weeks of event history
- Target holdout percentage (default: 10%)
- Primary retention/engagement metric to track (e.g., `subscription_renewed`, `weekly_active`, `feature_used`)
- n8n instance for automation (Baseline+ levels)

## Steps

### 1. Determine holdout size

Calculate the appropriate holdout percentage based on your active user count:

| Active Monthly Users | Recommended Holdout % | Reason |
|---|---|---|
| < 500 | Skip holdout | Insufficient sample size for any meaningful measurement |
| 500-2,000 | 15-20% | Larger holdout needed for statistical power |
| 2,000-10,000 | 10% | Standard size balances measurement power vs. optimization reach |
| 10,000+ | 5% | Smaller holdout still yields strong statistics |

The holdout percentage is a permanent tradeoff: larger holdouts give you more statistical confidence but exclude more users from benefiting from your optimizations.

### 2. Create the holdout feature flag

Use the `posthog-holdout-group` fundamental to create the `global-holdout` feature flag. Set `ensure_experience_continuity: true` to guarantee stable user assignment.

Log the holdout creation in PostHog using `posthog-custom-events`:
- Event: `holdout_group_created`
- Properties: `holdout_percentage`, `total_users_at_creation`, `holdout_user_count`, `primary_metric`

### 3. Create PostHog cohorts for each group

Using the `posthog-cohorts` fundamental, create two cohorts:

**Holdout cohort:**
```json
{
  "name": "Holdout Group",
  "groups": [{
    "properties": [{
      "key": "$feature/global-holdout",
      "value": "holdout",
      "operator": "exact"
    }]
  }]
}
```

**Treatment cohort:**
```json
{
  "name": "Treatment Group (Non-Holdout)",
  "groups": [{
    "properties": [{
      "key": "$feature/global-holdout",
      "value": "holdout",
      "operator": "is_not"
    }]
  }]
}
```

These cohorts enable quick filtering in any PostHog insight, funnel, or retention analysis.

### 4. Baseline both groups

Before running any new experiments, capture the current state of both groups using `posthog-custom-events`. For your primary metric, query the last 4 weeks of data split by holdout vs treatment:

- Retention rate (Week 1, Week 2, Week 4)
- Primary metric value (e.g., subscription renewal rate, feature usage frequency)
- Engagement score (if using engagement scoring)

Store this baseline in Attio using `attio-notes` on the holdout campaign record. This baseline is critical — all future lift measurements compare against it.

### 5. Enforce holdout exclusion in all experiments

Using `posthog-feature-flags`, update your experiment creation workflow to always include the holdout exclusion filter. Every new feature flag or experiment must include:

```json
{
  "properties": [{
    "key": "$feature/global-holdout",
    "value": "holdout",
    "operator": "is_not"
  }]
}
```

**Human action required:** Communicate the holdout policy to anyone creating PostHog experiments. If your team uses a shared experiment creation template or n8n workflow, add the holdout filter to the template so it is included by default.

### 6. Set up automated holdout validation

Using `n8n-workflow-basics`, create a weekly n8n workflow that:

1. Queries PostHog for holdout group size (should match target percentage within +/-2%)
2. Checks for contamination (holdout users exposed to experiment flags)
3. Verifies both groups have comparable baseline demographics (no drift)
4. Sends an alert if any check fails

This validation runs automatically at Baseline+ levels.

## Output

- A `global-holdout` PostHog feature flag with stable user assignment
- Two PostHog cohorts (Holdout Group, Treatment Group)
- Baseline metric snapshot for both groups stored in Attio
- Weekly validation workflow (Baseline+ levels)
- All existing and future experiments configured to exclude holdout users

## Triggers

At Smoke level: run once manually. At Baseline+: the validation workflow runs weekly via n8n cron.
