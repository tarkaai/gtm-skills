---
name: behavior-segmentation-pipeline
description: Extract user behavior vectors from PostHog, cluster users into behavioral segments via LLM, and sync segment assignments to CRM and analytics
category: Product
tools:
  - PostHog
  - Anthropic
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-retention-analysis
  - posthog-user-path-analysis
  - behavior-cluster-computation
  - attio-custom-attributes
  - attio-contacts
  - attio-lists
  - n8n-workflow-basics
  - n8n-scheduling
---

# Behavior Segmentation Pipeline

This drill builds the end-to-end pipeline that turns raw product usage data into AI-generated behavioral segments. It extracts per-user behavior vectors from PostHog, feeds them to an LLM-based clustering model, writes segment assignments back to PostHog and Attio, and creates dynamic cohorts per segment. The output drives personalized in-app experiences, targeted emails, and churn interventions.

## Input

- PostHog project with at least 14 days of per-user event data (30+ days recommended for accuracy)
- A defined list of core product features (event names representing meaningful usage)
- n8n instance for scheduling the segmentation pipeline
- Anthropic API key for Claude (cluster discovery and user assignment)
- Attio CRM with person records for segmented users

## Steps

### 1. Extract behavior vectors from PostHog

Using `posthog-custom-events` and `posthog-retention-analysis`, build the per-user behavior vector. Each vector captures what the user does, how often, how deeply, and in what patterns.

Query via PostHog API or HogQL:

```sql
SELECT
  person_id,
  -- Feature usage map
  countIf(event = 'feature_a_used') AS feature_a_count,
  countIf(event = 'feature_b_used') AS feature_b_count,
  countIf(event = 'feature_c_used') AS feature_c_count,
  -- (add one column per core feature)

  -- Session patterns
  uniq(toDate(timestamp)) AS active_days_30d,
  count() / greatest(uniq(properties.$session_id), 1) AS avg_events_per_session,
  uniq(properties.$session_id) / 4.3 AS sessions_per_week,

  -- Feature breadth
  uniq(event) AS distinct_features_used,

  -- Collaboration signals
  countIf(event IN ('team_invite_sent', 'shared_with_teammate', 'comment_created')) AS collab_actions,

  -- Temporal pattern
  multiIf(
    avg(toHour(timestamp)) < 12, 'morning',
    avg(toHour(timestamp)) < 17, 'afternoon',
    'evening'
  ) AS time_of_day_pattern,

  -- Account age
  dateDiff('day', min(timestamp), now()) AS account_age_days
FROM events
WHERE timestamp > now() - interval 30 day
  AND person_id != ''
  AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
GROUP BY person_id
HAVING active_days_30d >= 2
```

Replace `feature_a_used`, `feature_b_used`, etc. with your actual tracked feature events. The `HAVING active_days_30d >= 2` filter excludes single-visit bounces.

### 2. Compute a collaboration score

Normalize the collaboration signals into a 0-100 score:

```
collab_score = min((collab_actions / target_collab_actions) * 100, 100)
```

Where `target_collab_actions` is the 90th percentile of collaboration actions across all active users. A solo user scores 0-10; a heavy collaborator scores 80-100.

### 3. Identify workflow sequences

Using `posthog-user-path-analysis`, extract each user's most common event sequence (their "primary workflow"). Query the top-3 most frequent 3-event sequences per user:

```sql
WITH ordered AS (
  SELECT
    person_id,
    event,
    leadInFrame(event, 1) OVER (PARTITION BY person_id ORDER BY timestamp) AS next_1,
    leadInFrame(event, 2) OVER (PARTITION BY person_id ORDER BY timestamp) AS next_2
  FROM events
  WHERE timestamp > now() - interval 30 day
    AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
)
SELECT
  person_id,
  concat(event, ' -> ', next_1, ' -> ', next_2) AS workflow,
  count() AS frequency
FROM ordered
WHERE next_1 IS NOT NULL AND next_2 IS NOT NULL
GROUP BY person_id, workflow
ORDER BY person_id, frequency DESC
```

Take the top workflow per user as their `primary_workflow` field.

### 4. Run cluster discovery

Assemble the behavior vectors into JSON. Sample 100-200 users (stratified: include users from each engagement tier if available, otherwise random sample of active users). Pass to the `behavior-cluster-computation` fundamental's cluster discovery call.

Review the output: expect 4-8 clusters. Common patterns include:
- **Power Users:** High frequency, high breadth, deep sessions
- **Focused Specialists:** High depth in 1-2 features, low breadth
- **Casual Browsers:** Low frequency, low depth, broad but shallow
- **Team Drivers:** High collaboration, moderate individual usage
- **New Explorers:** Low account age, high breadth (trying everything), uncertain depth

Store the cluster definitions JSON. This is the reference taxonomy for all subsequent assignments.

### 5. Assign all active users to clusters

Batch all active users (from step 1) through the `behavior-cluster-computation` fundamental's assignment call. Process in batches of 30 users. For each user, receive: `cluster_id`, `cluster_label`, `confidence`.

Flag users with confidence < 0.5 as `unclassified`. If >15% are unclassified, re-run cluster discovery with a larger sample or more behavior dimensions.

### 6. Write segment assignments to PostHog

Using `posthog-custom-events`, set person properties for each user:

- `behavior_segment_id`: cluster ID (e.g., `cluster_01`)
- `behavior_segment_label`: human-readable label (e.g., `Power Collaborator`)
- `behavior_segment_confidence`: assignment confidence (0.0-1.0)
- `behavior_segment_updated_at`: ISO timestamp

Fire a `behavior_segment_assigned` event per user with properties: `segment_id`, `segment_label`, `confidence`, `previous_segment_id` (if re-segmenting).

### 7. Create PostHog cohorts per segment

Using `posthog-cohorts`, create a dynamic cohort for each cluster:

- `segment-{cluster_label_slugified}` (e.g., `segment-power-collaborator`)

These cohorts feed downstream targeting: Intercom in-app messages, Loops email campaigns, PostHog feature flags.

Also create cross-cutting cohorts:
- `segment-high-confidence` (confidence >= 0.8)
- `segment-unclassified` (confidence < 0.5 or no assignment)
- `segment-recently-changed` (segment changed in last 7 days)

### 8. Sync to Attio CRM

Using `attio-custom-attributes` and `attio-contacts`, write to each person record:
- `behavior_segment`: segment label
- `behavior_segment_confidence`: confidence score
- `behavior_segment_date`: date of assignment

Using `attio-lists`, maintain lists:
- "Segment: {Label}" for each cluster -- enables sales/CS to filter by segment
- "Segment: Unclassified" -- users needing manual review or more data

### 9. Build the recurring segmentation pipeline

Using `n8n-scheduling`, create a workflow triggered weekly (Sunday 06:00 UTC):

1. Extract fresh behavior vectors (step 1)
2. Assign all active users to current cluster definitions (step 5)
3. Detect segment changes: compare new assignment to previous `behavior_segment_id`
4. Fire `behavior_segment_changed` events for users who moved segments
5. Update PostHog person properties and Attio records
6. Log pipeline run: users processed, segment distribution, unclassified count, segment migration counts

Monthly (1st of month), also re-run cluster discovery (step 4) to check whether segments need updating.

### 10. Validate segment quality

After 30 days, measure segment quality:

- **Segment stability:** What percentage of users stayed in the same segment week-over-week? Target: >75%. Unstable segments indicate noisy clustering.
- **Retention divergence:** Do segments have meaningfully different retention rates? If all segments retain at ~40%, the segmentation is not capturing retention-relevant behavior. Target: >15pp spread between highest and lowest segment retention rates.
- **Churn prediction:** Of users who churned, what segment were they in? The highest-churn segment should have 2x+ the churn rate of the lowest.
- **Personalization lift:** Are segments responding differently to in-app messages and emails? If response rates are uniform across segments, the personalization is not leveraging the segments effectively.

Log validation metrics as a PostHog event: `segmentation_model_validated` with properties for each metric.

## Output

- Per-user behavioral segment assignments stored in PostHog and Attio
- Dynamic PostHog cohorts for each segment
- Attio lists for segment-based filtering by sales/CS
- Weekly automated re-assignment pipeline in n8n
- Monthly cluster refresh check
- Validation metrics for segment quality

## Triggers

- **Smoke:** Run once manually to validate that clustering produces distinct, stable segments
- **Baseline:** Weekly pipeline via n8n cron. Monthly cluster refresh.
- **Scalable/Durable:** Weekly pipeline with automated quality validation and cluster evolution
