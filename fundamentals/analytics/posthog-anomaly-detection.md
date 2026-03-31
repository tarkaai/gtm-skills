---
name: posthog-anomaly-detection
description: Detect metric anomalies and trend shifts in PostHog using HogQL queries
tool: PostHog
product: PostHog
difficulty: Advanced
---

# Detect Metric Anomalies in PostHog

Monitor play metrics for statistically significant changes — drops, plateaus, or unexpected spikes — that signal the need for intervention.

## API Approach

Use the PostHog MCP server or REST API to run HogQL queries that compare recent performance windows.

### Rolling Average Comparison

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      dateTrunc('week', timestamp) AS week,
      count() AS events,
      avg(toFloat(properties.$value)) AS avg_value,
      -- Compare to 4-week rolling average
      avg(avg_value) OVER (ORDER BY week ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING) AS rolling_avg,
      -- Percent change from rolling average
      (avg_value - rolling_avg) / rolling_avg * 100 AS pct_change
    FROM events
    WHERE event = '{event_name}'
      AND timestamp > now() - interval 8 week
    GROUP BY week
    ORDER BY week DESC
    LIMIT 4"
  }
}
```

### Anomaly Criteria

Flag a metric as anomalous when:
- **Drop:** pct_change < -20% for 2+ consecutive periods
- **Plateau:** pct_change between -2% and +2% for 4+ consecutive periods (optimization has stalled)
- **Spike:** pct_change > +50% (investigate — could be a bug or a real win)

### MCP Approach

```
posthog.query_events({
  event: "gtm_play_completed",
  properties: { play_slug: "{slug}" },
  date_from: "-8w",
  breakdown: "week"
})
```

Compare the last 2 weeks against the 4-week rolling average. Return: metric name, current value, rolling average, pct_change, anomaly_type (drop/plateau/spike/normal).

## Error Handling

- If insufficient data (< 4 weeks), return "insufficient_data" — cannot detect anomalies yet
- If PostHog returns empty results, verify the event name and property filters
- Rate limit: max 1 anomaly check per play per day
