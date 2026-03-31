---
name: engagement-score-computation
description: Build and run a per-user engagement scoring pipeline that computes composite scores from usage frequency, feature breadth, session depth, and recency signals
category: Product
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-retention-analysis
  - attio-custom-attributes
  - attio-contacts
  - attio-lists
  - n8n-workflow-basics
  - n8n-scheduling
---

# Engagement Score Computation

This drill builds the core pipeline that computes a per-user engagement score. Unlike account-level health scores (see `health-score-model-design`), this operates at the individual user level -- scoring every active user on a 0-100 scale based on their actual product behavior. The output feeds churn prediction, re-engagement campaigns, and upsell targeting.

## Input

- PostHog tracking active with at least 14 days of per-user event data
- A defined set of "core engagement events" for your product (feature usage, content creation, collaboration, exports, etc.)
- n8n instance for running the daily scoring pipeline
- Attio CRM with contact records for scored users

## Steps

### 1. Define the engagement event taxonomy

Using `posthog-custom-events`, identify the 5-10 events that best represent meaningful engagement. Good engagement signals have two properties: they require intentional effort, and they correlate with retention.

**Strong signals (high weight):**
- Core feature usage: the 3-5 actions that deliver your product's primary value
- Content creation: users generating data, documents, projects, or artifacts
- Collaboration: sharing, inviting teammates, commenting, assigning tasks
- Integration usage: connecting external tools, using API

**Moderate signals (medium weight):**
- Navigation depth: visiting 3+ distinct product areas per session
- Return visits: logging in on 4+ distinct days in 14-day window
- Settings configuration: customizing the product (signals investment)
- Help/docs access: learning the product (early-stage engagement)

**Weak signals (low weight or exclude):**
- Page views alone (passive)
- Single-page sessions (bounces)
- Logins with no subsequent action

Define your event list and document it. Every event must already be tracked in PostHog or you must instrument it before proceeding.

### 2. Build the scoring model

Compute four dimensions, each on a 0-100 scale:

**Frequency dimension (weight: 30%)**

Query PostHog using `posthog-retention-analysis` for per-user activity:

```sql
SELECT
  distinct_id,
  uniq(toDate(timestamp)) AS active_days_14d,
  count() AS total_events_14d,
  total_events_14d / greatest(active_days_14d, 1) AS events_per_active_day
FROM events
WHERE event IN ({core_events})
  AND timestamp > now() - interval 14 day
GROUP BY distinct_id
```

Score: `min((active_days_14d / 10) * 100, 100)` -- a user active 10+ of the last 14 days scores 100.

**Breadth dimension (weight: 25%)**

Using `posthog-cohorts`, measure feature diversity:

```sql
SELECT
  distinct_id,
  uniq(event) AS distinct_features_14d,
  groupArray(DISTINCT event) AS features_used
FROM events
WHERE event IN ({all_feature_events})
  AND timestamp > now() - interval 14 day
GROUP BY distinct_id
```

Score: `min((distinct_features_14d / total_trackable_features) * 100, 100)` -- using all tracked features scores 100.

**Depth dimension (weight: 25%)**

Measure intensity per session:

```sql
SELECT
  distinct_id,
  count() / greatest(uniq(properties.$session_id), 1) AS events_per_session,
  avg(session_duration_seconds) AS avg_session_duration
FROM events
WHERE event IN ({core_events})
  AND timestamp > now() - interval 14 day
GROUP BY distinct_id
```

Score: `min((events_per_session / target_events_per_session) * 60, 60) + min((avg_session_duration / target_session_duration) * 40, 40)` -- hitting target actions and duration scores 100.

**Recency dimension (weight: 20%)**

Using `posthog-custom-events`, compute days since last meaningful action:

```sql
SELECT
  distinct_id,
  dateDiff('day', max(timestamp), now()) AS days_since_last_action
FROM events
WHERE event IN ({core_events})
GROUP BY distinct_id
```

Score: `max(100 - (days_since_last_action * 10), 0)` -- active today scores 100; 10+ days ago scores 0.

**Composite score:**

```
engagement_score = (
  frequency_score * 0.30 +
  breadth_score * 0.25 +
  depth_score * 0.25 +
  recency_score * 0.20
)
```

Round to integer. Range: 0-100.

### 3. Classify engagement tiers

Map the composite score to tiers:

| Score Range | Tier | Description | Action |
|------------|------|-------------|--------|
| 80-100 | Power User | Deep, frequent, broad usage | Expansion/advocacy candidate |
| 60-79 | Engaged | Consistent, meaningful usage | Monitor for growth |
| 40-59 | Casual | Sporadic or narrow usage | Nudge toward deeper adoption |
| 20-39 | At Risk | Declining or minimal usage | Re-engagement intervention |
| 0-19 | Dormant | Near-zero recent activity | Win-back campaign |

### 4. Compute score trend

Compare the current 14-day score to the previous 14-day score:

- **Rising:** Score increased by 10+ points
- **Stable:** Score changed by less than 10 points
- **Declining:** Score decreased by 10+ points

A "Declining" trend on a "Casual" user is more urgent than a stable "At Risk" user. Declining signals active disengagement vs passive inactivity.

### 5. Build the daily scoring pipeline in n8n

Using `n8n-scheduling`, create a workflow triggered daily at 07:00 UTC:

1. **Pull active users:** Query PostHog for all users with at least 1 event in the last 30 days
2. **Compute dimension scores:** Run the four HogQL queries from step 2 for each user
3. **Calculate composite score:** Apply the weighted formula
4. **Classify tier and trend:** Map score to tier, compare to previous day
5. **Write to CRM:** Using `attio-custom-attributes` and `attio-contacts`, write:
   - `engagement_score` (number, 0-100)
   - `engagement_tier` (select: Power User / Engaged / Casual / At Risk / Dormant)
   - `engagement_trend` (select: Rising / Stable / Declining)
   - `engagement_score_updated_at` (date)
   - `engagement_frequency_score` (number)
   - `engagement_breadth_score` (number)
   - `engagement_depth_score` (number)
   - `engagement_recency_score` (number)
6. **Log to PostHog:** Fire `engagement_score_computed` event per user with all scores as properties
7. **Detect tier changes:** Flag users who moved tiers since yesterday. Fire `engagement_tier_changed` event with old_tier and new_tier.

### 6. Create PostHog cohorts for each tier

Using `posthog-cohorts`, create dynamic cohorts:

- `engagement-power-users` (score >= 80)
- `engagement-engaged` (score 60-79)
- `engagement-casual` (score 40-59)
- `engagement-at-risk` (score 20-39)
- `engagement-dormant` (score < 20)

These cohorts feed downstream targeting: in-app messages, emails, and feature flags.

### 7. Sync scored users to CRM lists

Using `attio-lists`, maintain lists:

- "Engagement: Power Users" -- expansion and advocacy candidates
- "Engagement: At Risk" -- needs re-engagement intervention
- "Engagement: Declining" -- users whose trend is Declining regardless of current tier

These lists feed the `engagement-alert-routing` and `health-score-alerting` drills.

### 8. Validate the model

After 30 days of scoring, back-test against known outcomes:

1. Pull users who churned in the last 60 days from Attio
2. Check what their engagement scores were 14 days before churn
3. Target: 70%+ of churners should have been scored At Risk or Dormant 14 days pre-churn
4. If the model misses too many churners, adjust dimension weights or add new signals
5. If the model flags too many false positives (At Risk users who did not churn), tighten the thresholds

## Output

- Daily per-user engagement scores (0-100) computed and stored in Attio
- Five PostHog cohorts for tier-based targeting
- CRM lists for Power Users, At Risk, and Declining users
- Score trend tracking for trajectory-based interventions
- PostHog events logging every score computation for model evaluation
- Back-test validation results confirming predictive accuracy

## Triggers

- Daily pipeline: n8n cron, 07:00 UTC
- Model recalibration: monthly (adjust weights based on churn prediction accuracy)
- Full revalidation: quarterly (back-test against 90 days of churn data)
