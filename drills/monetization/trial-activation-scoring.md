---
name: trial-activation-scoring
description: Build a real-time trial health score combining activation milestones, feature usage, and engagement signals to prioritize interventions
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-funnels
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-crm-integration
  - attio-custom-attributes
  - attio-contacts
---

# Trial Activation Scoring

This drill builds a real-time scoring model that assigns each trial user a 0-100 health score based on activation milestone completion, feature usage depth, and engagement recency. The score drives intervention routing: high scores get upgrade nudges, medium scores get coaching, low scores get rescue campaigns.

## Prerequisites

- PostHog tracking trial events: `trial_started`, `activation_reached`, milestone events
- Attio configured with trial user records
- n8n instance for scheduled scoring runs

## Steps

### 1. Define scoring dimensions

Build a composite score from four weighted dimensions:

| Dimension | Weight | Signals | Score Range |
|-----------|--------|---------|-------------|
| Activation progress | 40% | Milestones completed out of total defined milestones | 0-100 |
| Feature usage depth | 25% | Unique features used / total available features explored | 0-100 |
| Engagement recency | 20% | Days since last session (inverse: 0 days = 100, 7+ days = 0) | 0-100 |
| Team signals | 15% | Teammates invited, shared artifacts, collaborative actions | 0-100 |

Final score = (activation * 0.4) + (usage * 0.25) + (recency * 0.2) + (team * 0.15)

### 2. Build the scoring query in PostHog

Using the `posthog-custom-events` fundamental, create a HogQL query that computes each dimension per trial user:

**Activation progress:**
```sql
SELECT
  distinct_id,
  countDistinctIf(event, event IN ('milestone_1_completed', 'milestone_2_completed', 'milestone_3_completed', 'activation_reached')) AS milestones_hit,
  (milestones_hit / {total_milestones}) * 100 AS activation_score
FROM events
WHERE properties.$group_0 = {trial_cohort}
  AND timestamp > now() - INTERVAL 30 DAY
GROUP BY distinct_id
```

**Feature usage depth:**
```sql
SELECT
  distinct_id,
  countDistinct(properties.feature_name) AS unique_features_used,
  (unique_features_used / {total_trackable_features}) * 100 AS usage_score
FROM events
WHERE event = 'feature_used'
  AND timestamp > now() - INTERVAL 30 DAY
GROUP BY distinct_id
```

**Engagement recency:**
```sql
SELECT
  distinct_id,
  dateDiff('day', max(timestamp), now()) AS days_since_last,
  greatest(0, 100 - (days_since_last * 15)) AS recency_score
FROM events
WHERE timestamp > now() - INTERVAL 30 DAY
GROUP BY distinct_id
```

**Team signals:**
```sql
SELECT
  distinct_id,
  countIf(event = 'teammate_invited') AS invites,
  countIf(event = 'artifact_shared') AS shares,
  least(100, (invites * 25) + (shares * 15)) AS team_score
FROM events
WHERE timestamp > now() - INTERVAL 30 DAY
GROUP BY distinct_id
```

### 3. Create scoring segments in PostHog

Using the `posthog-cohorts` fundamental, define three cohorts based on the composite score:

- **Hot (score >= 70):** High activation, recent usage, likely to convert. Route to upgrade prompt.
- **Warm (score 35-69):** Partial activation, some engagement. Route to coaching and milestone guidance.
- **Cold (score < 35):** Low activation, stalled or absent. Route to rescue campaign or let expire.

### 4. Build the daily scoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 07:00 UTC:

1. Query PostHog API for all active trial users with their event counts
2. Compute the composite score for each user
3. Classify into Hot / Warm / Cold segments
4. Using `n8n-crm-integration`, sync the score and segment to Attio using `attio-custom-attributes`:
   - `trial_health_score` (integer 0-100)
   - `trial_segment` (enum: Hot, Warm, Cold)
   - `trial_score_updated_at` (timestamp)
   - `days_remaining` (integer)
5. Detect segment transitions: if a user moved from Warm to Cold (or Cold to Warm), flag for intervention

### 5. Build the activation funnel

Using `posthog-funnels`, create a funnel that tracks milestone progression:

```
trial_started -> milestone_1 -> milestone_2 -> milestone_3 -> activation_reached -> upgrade_started -> payment_completed
```

Break down by `trial_segment` to validate that Hot users actually convert at higher rates. If Hot users do not convert at >= 2x the rate of Warm users, re-calibrate the scoring weights.

### 6. Sync scoring to intervention routing

The score feeds downstream systems:
- **Hot users (>= 70):** Trigger `upgrade-prompt` drill — show contextual upgrade messaging
- **Warm users (35-69):** Trigger coaching messages via Intercom — guide toward the next unfinished milestone
- **Cold users (< 35):** Trigger rescue email via Loops — personal outreach offering help or let the trial expire to conserve resources

Using `attio-contacts`, tag each trial user record with their current segment so sales reps and automation workflows can filter by trial health.

## Output

- Daily-refreshed trial health score (0-100) per user
- Three segments (Hot/Warm/Cold) synced to Attio and PostHog
- Activation funnel with segment breakdown
- Segment transition alerts for intervention routing

## Triggers

Runs daily at 07:00 UTC via n8n. Segment transitions trigger downstream intervention workflows immediately.
