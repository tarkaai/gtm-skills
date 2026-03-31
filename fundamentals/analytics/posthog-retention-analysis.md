---
name: posthog-retention-analysis
description: Query retention curves, cohort survival rates, and churn timing patterns from PostHog
tool: PostHog
difficulty: Advanced
---

# Retention Analysis in PostHog

Extract retention curves, cohort survival data, and churn timing patterns to feed into predictive churn models. This fundamental provides the raw behavioral data that churn scoring models consume.

## API Approach

### Cohort Retention Query

Use the PostHog REST API or MCP server to pull retention data grouped by signup cohort:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      dateTrunc('week', person.created_at) AS signup_week,
      dateDiff('week', person.created_at, timestamp) AS weeks_since_signup,
      uniqExact(distinct_id) AS active_users
    FROM events
    WHERE event IN ('$pageview', 'feature_used', 'action_completed')
      AND person.created_at > now() - interval 12 week
    GROUP BY signup_week, weeks_since_signup
    ORDER BY signup_week, weeks_since_signup"
  }
}
```

### Per-User Activity Decay Query

Pull per-user activity counts across rolling windows to detect declining engagement:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      distinct_id,
      countIf(timestamp > now() - interval 7 day) AS events_last_7d,
      countIf(timestamp > now() - interval 14 day AND timestamp <= now() - interval 7 day) AS events_prev_7d,
      countIf(timestamp > now() - interval 28 day AND timestamp <= now() - interval 14 day) AS events_prev_14_28d,
      dateDiff('day', max(timestamp), now()) AS days_since_last_event,
      uniqExact(event) AS distinct_event_types_30d
    FROM events
    WHERE timestamp > now() - interval 28 day
      AND event NOT IN ('$pageleave')
    GROUP BY distinct_id
    HAVING events_prev_7d > 0"
  }
}
```

This returns each user's activity trajectory: increasing, stable, declining, or dormant.

### Feature Abandonment Query

Identify users who stopped using features they previously relied on:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      distinct_id,
      event AS feature,
      countIf(timestamp > now() - interval 14 day) AS uses_last_14d,
      countIf(timestamp > now() - interval 42 day AND timestamp <= now() - interval 14 day) AS uses_prev_28d
    FROM events
    WHERE event IN ({feature_list})
      AND timestamp > now() - interval 42 day
    GROUP BY distinct_id, feature
    HAVING uses_prev_28d >= 3 AND uses_last_14d = 0"
  }
}
```

Replace `{feature_list}` with your product's core feature event names.

### MCP Approach

```
posthog.query_events({
  event: "$pageview",
  date_from: "-12w",
  breakdown: "week",
  math: "dau"
})
```

For per-user analysis, use the persons API:

```
posthog.get_persons({
  properties: [{"key": "last_seen", "value": "14", "operator": "gt", "type": "relative_date"}]
})
```

## Output Format

Return structured data suitable for churn scoring:

```json
{
  "user_id": "distinct_id",
  "activity_trend": "declining|stable|growing|dormant",
  "events_last_7d": 3,
  "events_prev_7d": 12,
  "decay_rate": -0.75,
  "days_since_last_event": 5,
  "abandoned_features": ["feature_a", "feature_b"],
  "distinct_event_types_30d": 2
}
```

## Error Handling

- If a user has fewer than 14 days of history, exclude from retention analysis (insufficient baseline)
- If PostHog returns timeout on large queries, add `LIMIT 10000` and paginate with `OFFSET`
- Rate limit: batch queries for up to 500 users per API call
