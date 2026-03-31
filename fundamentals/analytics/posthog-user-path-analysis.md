---
name: posthog-user-path-analysis
description: Analyze user workflow sequences and navigation paths in PostHog to identify optimization opportunities
tool: PostHog
difficulty: Advanced
---

# Analyze User Paths in PostHog

Extract sequential user behavior patterns from PostHog to understand how users move through workflows, where they deviate from optimal paths, and which sequences correlate with retention or churn.

## API Approach

Use the PostHog REST API or MCP server to query user paths using HogQL.

### Sequential Event Path Query

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT
      person_id,
      groupArray(event) AS event_sequence,
      groupArray(timestamp) AS timestamps,
      dateDiff('second', min(timestamp), max(timestamp)) AS session_duration_seconds,
      length(groupArray(event)) AS event_count
    FROM events
    WHERE timestamp > now() - interval 30 day
      AND person_id != ''
      AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
    GROUP BY person_id
    ORDER BY event_count DESC
    LIMIT 500"
  }
}
```

### Workflow Step Transition Matrix

Identify which actions users take after a given action, and how frequently:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "WITH ordered_events AS (
      SELECT
        person_id,
        event,
        timestamp,
        leadInFrame(event, 1) OVER (PARTITION BY person_id ORDER BY timestamp) AS next_event
      FROM events
      WHERE timestamp > now() - interval 30 day
        AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
    )
    SELECT
      event AS from_event,
      next_event AS to_event,
      count() AS transition_count,
      count(DISTINCT person_id) AS unique_users
    FROM ordered_events
    WHERE next_event IS NOT NULL
    GROUP BY from_event, to_event
    ORDER BY transition_count DESC
    LIMIT 100"
  }
}
```

### Identify Inefficient Paths

Compare high-performing users (retained 30+ days) against churned users to find path differences:

```
POST /api/projects/{project_id}/query
{
  "query": {
    "kind": "HogQLQuery",
    "query": "WITH user_paths AS (
      SELECT
        person_id,
        groupArray(event) AS event_sequence,
        length(groupArray(event)) AS step_count,
        dateDiff('second', min(timestamp), max(timestamp)) AS total_time_seconds
      FROM events
      WHERE timestamp > now() - interval 60 day
        AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
      GROUP BY person_id
    )
    SELECT
      p.event_sequence,
      p.step_count,
      p.total_time_seconds,
      prs.properties.$retained_30d AS is_retained
    FROM user_paths p
    JOIN persons prs ON p.person_id = prs.id
    ORDER BY p.step_count DESC
    LIMIT 200"
  }
}
```

### MCP Approach

```
posthog.query_hogql({
  query: "SELECT event, leadInFrame(event, 1) OVER (PARTITION BY person_id ORDER BY timestamp) AS next_event, count() AS cnt FROM events WHERE timestamp > now() - interval 30 day GROUP BY event, next_event ORDER BY cnt DESC LIMIT 50"
})
```

## Output

Return a structured analysis:
- `transition_matrix`: array of `{from_event, to_event, count, unique_users}` — the most common workflow transitions
- `inefficient_paths`: array of `{person_id, step_count, total_time_seconds}` — users taking significantly more steps or time than the median to reach the same outcome
- `optimal_path`: the most common event sequence among retained/activated users
- `deviation_patterns`: sequences that diverge from the optimal path, ranked by frequency

## Error Handling

- If fewer than 50 unique users have path data, return `insufficient_data` — path analysis requires volume
- If HogQL window functions are unavailable (older PostHog versions), fall back to client-side sequencing: query raw events ordered by person_id and timestamp, then compute transitions in code
- Rate limit: max 2 path analysis queries per day (these are expensive queries)
