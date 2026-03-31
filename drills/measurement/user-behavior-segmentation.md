---
name: user-behavior-segmentation
description: Analyze product usage data to classify users into behavioral segments for personalized experiences
category: Experimentation
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-user-path-analysis
  - posthog-retention-analysis
  - attio-custom-attributes
  - attio-contacts
  - n8n-workflow-basics
  - n8n-scheduling
---

# User Behavior Segmentation

This drill builds a behavioral segmentation pipeline that classifies every active user into a behavior-based segment using product usage data. Unlike demographic or firmographic segmentation (role, company size), behavioral segmentation groups users by what they actually do in the product. The output feeds personalization engines, in-app messaging targeting, and retention interventions.

## Input

- PostHog tracking active with at least 21 days of per-user event data
- A defined set of core product events (feature usage, navigation, content creation, collaboration, settings changes)
- n8n instance for running the segmentation pipeline
- Attio CRM with contact records for segmented users

## Steps

### 1. Extract usage patterns from PostHog

Using `posthog-user-path-analysis`, pull the dominant user paths for your product over the last 30 days. Identify the 3-5 most common navigation sequences. These reveal how different users approach your product.

Using `posthog-custom-events`, query the following per-user behavioral dimensions:

**Primary workflow dimension:**

```sql
SELECT
  distinct_id,
  argMax(event, count) AS primary_workflow,
  count() AS primary_workflow_count,
  groupArray(DISTINCT event) AS all_workflows_used
FROM (
  SELECT distinct_id, event, count() AS count
  FROM events
  WHERE event IN ({core_feature_events})
    AND timestamp > now() - interval 21 day
  GROUP BY distinct_id, event
)
GROUP BY distinct_id
```

This identifies each user's most-used feature — their primary workflow.

**Session pattern dimension:**

```sql
SELECT
  distinct_id,
  uniq(toDate(timestamp)) AS active_days_21d,
  count() / greatest(uniq(toDate(timestamp)), 1) AS events_per_active_day,
  avg(session_duration_seconds) AS avg_session_minutes,
  countIf(toHour(timestamp) >= 6 AND toHour(timestamp) < 12) AS morning_events,
  countIf(toHour(timestamp) >= 12 AND toHour(timestamp) < 18) AS afternoon_events,
  countIf(toHour(timestamp) >= 18 OR toHour(timestamp) < 6) AS evening_events
FROM events
WHERE timestamp > now() - interval 21 day
GROUP BY distinct_id
```

This reveals usage cadence: daily vs weekly, power vs light, morning vs evening.

**Collaboration dimension:**

```sql
SELECT
  distinct_id,
  countIf(event IN ('invite_sent', 'comment_created', 'share_link_generated', 'mention_created')) AS collab_actions,
  uniqIf(properties.target_user_id, properties.target_user_id IS NOT NULL) AS unique_collaborators
FROM events
WHERE timestamp > now() - interval 21 day
GROUP BY distinct_id
```

This separates solo users from team collaborators.

### 2. Define behavioral segments

Based on the three dimensions (workflow, session pattern, collaboration), define 4-6 segments. More than 6 creates targeting complexity without proportional personalization lift. Example segments:

| Segment | Primary Workflow | Session Pattern | Collaboration | Description |
|---------|-----------------|-----------------|---------------|-------------|
| **Power Builder** | Core creation features | Daily, long sessions | High | Creates constantly, collaborates actively |
| **Efficient Executor** | Task/workflow features | Daily, short sessions | Medium | Gets in, does work, gets out |
| **Explorer** | Broad feature mix | Sporadic, medium sessions | Low | Tries many features, hasn't settled on a workflow |
| **Team Coordinator** | Admin/management features | Regular, medium sessions | High | Manages others' work more than creating their own |
| **Passive Consumer** | Read/view features | Sporadic, short sessions | Low | Consumes content but rarely creates |
| **New User** | Onboarding features | < 7 days active | Unknown | Still in first-week experience |

Adjust segments to match your product's actual behavior clusters. The HogQL queries above provide the raw data; map score ranges to segment membership.

### 3. Build the classification logic

For each user, compute segment membership using a rule-based classifier:

```
IF active_days < 7 → "New User"
ELIF primary_workflow IN (core_creation) AND active_days >= 15 AND collab_actions >= 10 → "Power Builder"
ELIF primary_workflow IN (task_features) AND events_per_active_day >= 5 AND avg_session_minutes < 10 → "Efficient Executor"
ELIF uniq(all_workflows_used) >= 4 AND active_days < 12 → "Explorer"
ELIF primary_workflow IN (admin_features) AND unique_collaborators >= 3 → "Team Coordinator"
ELIF primary_workflow IN (read_view) OR events_per_active_day < 3 → "Passive Consumer"
ELSE → "Efficient Executor" (default)
```

Store the classification rules in your n8n workflow so they can be updated without code deploys.

### 4. Build the daily segmentation pipeline in n8n

Using `n8n-scheduling`, create a workflow triggered daily at 06:00 UTC (before the engagement scoring pipeline):

1. **Pull active users:** Query PostHog for all users with at least 1 event in the last 30 days
2. **Run dimension queries:** Execute the three HogQL queries from Step 1 for all active users
3. **Apply classification rules:** Map each user to their segment using the logic from Step 3
4. **Detect segment changes:** Compare today's assignment to yesterday's. Flag users who shifted segments.
5. **Write to CRM:** Using `attio-custom-attributes` and `attio-contacts`, write:
   - `behavior_segment` (select: Power Builder / Efficient Executor / Explorer / Team Coordinator / Passive Consumer / New User)
   - `behavior_segment_updated_at` (date)
   - `behavior_segment_previous` (select: same options, for tracking transitions)
   - `primary_workflow` (text: the user's most-used feature)
   - `collaboration_level` (select: High / Medium / Low / None)
6. **Write to PostHog:** Fire `behavior_segment_assigned` event per user with `{segment, previous_segment, primary_workflow, collab_level}`
7. **Sync to PostHog person properties:** Set `behavior_segment` as a person property for feature flag and cohort targeting

### 5. Create PostHog cohorts per segment

Using `posthog-cohorts`, create dynamic cohorts:

- `behavior-power-builders`
- `behavior-efficient-executors`
- `behavior-explorers`
- `behavior-team-coordinators`
- `behavior-passive-consumers`
- `behavior-new-users`

These cohorts feed personalization rule engines, in-app message targeting, and experiment segmentation.

### 6. Validate segment stability

After 14 days of segmentation, assess:

1. **Distribution check:** No single segment should contain more than 40% of users (if it does, split it) or fewer than 5% (if so, merge it with a neighbor)
2. **Stability check:** Fewer than 15% of users should change segments week-over-week. High churn between segments means the classification rules are too sensitive — widen the thresholds.
3. **Predictive check:** Using `posthog-retention-analysis`, compare 30-day retention rates across segments. If segments do not show meaningfully different retention rates (within 5pp of each other), the segmentation is not capturing real behavioral differences — revisit the dimension definitions.

## Output

- Daily per-user behavioral segment assignments stored in Attio and PostHog
- 4-6 PostHog cohorts for segment-based targeting
- Person properties in PostHog for feature flag and experiment targeting
- Segment transition events for detecting behavior changes
- Validation metrics confirming segment quality

## Triggers

- Daily pipeline: n8n cron, 06:00 UTC
- Segment rule recalibration: monthly (adjust thresholds based on distribution and stability)
- Full revalidation: quarterly (re-derive segments from fresh clustering analysis)
