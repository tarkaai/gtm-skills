---
name: behavior-cluster-computation
description: Use Claude to cluster users into behavioral segments from feature-usage vectors and session patterns
tool: Anthropic
difficulty: Advanced
---

# Compute Behavioral Clusters

Given a set of user behavior vectors (feature usage frequencies, session patterns, workflow sequences), use Claude to assign each user to a behavioral cluster. This replaces traditional k-means or DBSCAN with an LLM-based approach that produces human-interpretable segment labels, descriptions, and recommended personalization actions for each cluster.

## API Call — Cluster Discovery

Run this first to identify the natural segments in your user base. Provide behavior data for 50-200 representative users.

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "You are a user segmentation agent. Analyze these user behavior vectors and identify natural behavioral clusters.\n\nProduct context:\n- Product type: {product_type}\n- Core features: {feature_list}\n- Key retention drivers: {retention_drivers}\n- Typical user lifecycle: {lifecycle_description}\n\nUser behavior data (sample of {n} users):\n{behavior_vectors_json}\n\nEach vector contains:\n- feature_usage: map of feature_name -> usage_count_30d\n- session_frequency: sessions_per_week\n- session_depth: avg_events_per_session\n- primary_workflow: most_common_event_sequence\n- account_age_days: number\n- collaboration_score: 0-100 (team activity level)\n- time_of_day_pattern: morning|afternoon|evening|mixed\n\nIdentify 4-8 natural behavioral clusters. For each cluster:\n1. A short label (2-4 words, e.g., 'Power Collaborator', 'Solo Explorer')\n2. A one-sentence description of this user archetype\n3. The defining behavioral signals (what makes them different from other clusters)\n4. Estimated churn risk for this cluster (low/medium/high)\n5. Recommended personalization strategy (what product experience to optimize for this segment)\n6. Estimated percentage of users in this cluster\n\nRespond in JSON:\n{\n  \"clusters\": [\n    {\n      \"id\": \"cluster_01\",\n      \"label\": \"\",\n      \"description\": \"\",\n      \"defining_signals\": [\"\"],\n      \"churn_risk\": \"low|medium|high\",\n      \"personalization_strategy\": \"\",\n      \"estimated_pct\": 0.0,\n      \"centroid\": {\"session_frequency\": 0, \"session_depth\": 0, \"feature_breadth\": 0, \"collaboration\": 0}\n    }\n  ],\n  \"total_users_analyzed\": 0,\n  \"cluster_quality_notes\": \"\"\n}"
  }]
}
```

## API Call — User Assignment

After discovering clusters, assign individual users (batch up to 30 per call):

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "messages": [{
    "role": "user",
    "content": "You are a user segmentation agent. Assign each user to the closest behavioral cluster.\n\nCluster definitions:\n{clusters_json}\n\nUsers to assign:\n{users_json}\n\nFor each user, return the best-fit cluster and a confidence score (0.0-1.0). If a user does not fit any cluster well (confidence < 0.5), label them 'unclassified'.\n\nRespond in JSON:\n{\n  \"assignments\": [\n    {\n      \"user_id\": \"\",\n      \"cluster_id\": \"\",\n      \"cluster_label\": \"\",\n      \"confidence\": 0.0,\n      \"reasoning\": \"brief explanation\"\n    }\n  ]\n}"
  }]
}
```

## Cluster Refresh

Re-run cluster discovery monthly or when >15% of users fall into "unclassified." Pass the previous cluster definitions as context so the model can evolve clusters incrementally rather than creating an entirely new taxonomy:

```
"Previous cluster definitions (from last month):\n{previous_clusters_json}\n\nUpdated user behavior data:\n{new_vectors_json}\n\nRefine or update the cluster definitions based on the new data. Preserve cluster IDs where the segment still exists. Add new clusters if a distinct new pattern emerges. Retire clusters if fewer than 5% of users belong to them."
```

## Output

- `clusters`: Array of cluster definitions with labels, descriptions, signals, risk levels, and personalization strategies
- `assignments`: Per-user cluster assignment with confidence scores
- Store cluster ID and label as PostHog person properties (`behavior_segment_id`, `behavior_segment_label`) and Attio custom attributes

## Error Handling

- If fewer than 30 users in the sample, return `insufficient_data` — clustering requires volume
- If the API returns fewer than 3 clusters, the user base may be too homogeneous — reduce feature dimensions and retry
- If >25% of users are "unclassified" after assignment, the cluster definitions need refinement — re-run discovery with a larger sample
- Rate limit: max 1 cluster discovery per week, max 500 user assignments per day
- Cost estimate: ~$0.10 per discovery run, ~$0.02 per 30-user assignment batch
