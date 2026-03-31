---
name: posthog-holdout-group
description: Create and manage a persistent holdout group in PostHog that is excluded from all experiments
tool: PostHog
product: PostHog
difficulty: Advanced
---

# Create a Persistent Holdout Group in PostHog

A holdout group is a randomly selected subset of users who are permanently excluded from all experiments and feature changes. By comparing the holdout group against the rest of the population over time, you measure the cumulative lift of all optimizations combined — not just individual experiments in isolation.

## Prerequisites

- PostHog project with identified users (distinct_id set on every event)
- At least 500 active users (to support a statistically meaningful holdout)
- PostHog feature flags enabled

## Create the Holdout Feature Flag

Use the PostHog API to create a persistent feature flag that assigns users to the holdout group:

```
POST /api/projects/{project_id}/feature_flags/
{
  "key": "global-holdout",
  "name": "Global Holdout Group",
  "filters": {
    "groups": [{
      "rollout_percentage": 10,
      "variant": "holdout"
    }]
  },
  "ensure_experience_continuity": true,
  "active": true
}
```

Key parameters:

- `rollout_percentage`: Set to 10% for most products. Use 5% if you have 5,000+ active users (smaller holdout still yields statistical power with less lost opportunity). Use 15-20% only if your user base is under 1,000.
- `ensure_experience_continuity`: MUST be `true`. This pins each user to their assigned group permanently via PostHog's consistent hashing on distinct_id. Without this, users could drift between holdout and treatment across sessions.

## Verify Assignment Consistency

After creating the flag, verify that a user always resolves to the same group:

```
POST /api/projects/{project_id}/feature_flags/{flag_id}/evaluation
{
  "distinct_id": "test-user-123"
}
```

Call this 5 times with the same distinct_id. The result must be identical every time. If it varies, check that `ensure_experience_continuity` is enabled.

## Query Holdout vs Treatment Populations

To compare metrics between holdout and treatment groups, use HogQL:

```sql
SELECT
  if(
    JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout',
    'holdout',
    'treatment'
  ) AS group_assignment,
  count(DISTINCT distinct_id) AS users,
  countIf(event = '{target_event}') AS target_events,
  countIf(event = '{target_event}') / count(DISTINCT distinct_id) AS rate_per_user
FROM events
WHERE timestamp > now() - interval {window} day
  AND event IN ('{target_event}', '$identify')
GROUP BY group_assignment
```

Replace `{target_event}` with the event you are measuring (e.g., `feature_used`, `subscription_renewed`, `upgrade_completed`) and `{window}` with the measurement period in days.

## Exclude Holdout from All Experiments

When creating any new PostHog experiment or feature flag, add a filter condition that excludes holdout users:

```json
{
  "filters": {
    "groups": [{
      "properties": [{
        "key": "$feature/global-holdout",
        "value": "holdout",
        "operator": "is_not"
      }],
      "rollout_percentage": 50
    }]
  }
}
```

This ensures holdout users never see experimental variants. They remain on the default product experience as of the holdout creation date.

## Validate Holdout Integrity

Run a weekly integrity check to verify the holdout group is not contaminated:

```sql
SELECT
  distinct_id,
  JSONExtractString(person_properties, '$feature/global-holdout') AS holdout_status,
  groupArray(DISTINCT JSONExtractString(properties, '$feature_flag')) AS flags_evaluated
FROM events
WHERE timestamp > now() - interval 7 day
  AND event = '$feature_flag_called'
  AND JSONExtractString(person_properties, '$feature/global-holdout') = 'holdout'
GROUP BY distinct_id, holdout_status
HAVING length(flags_evaluated) > 1
```

If any holdout user has been evaluated against experiment flags (beyond the holdout flag itself), there is contamination. Investigate and fix the experiment's filter conditions.

## Error Handling

- If the feature flag API returns 429 (rate limit), retry with exponential backoff (1s, 2s, 4s)
- If a user has no `$feature/global-holdout` property, they were created after the holdout flag but before their first flag evaluation. Force evaluation by calling the decide endpoint for that user
- If holdout group size drifts beyond +/-2% of target (e.g., 10% target but measured at 13%), check for new user onboarding flows that bypass flag evaluation
- Maximum holdout size: 20%. Larger holdouts sacrifice too much optimization surface area
- Minimum holdout size: 5%. Smaller holdouts require impractically long measurement windows for statistical power
