---
name: push-notification-segmentation
description: Build and maintain behavioral user segments for personalized push notification targeting at scale
category: Messaging
tools:
  - OneSignal
  - PostHog
  - n8n
  - Clay
fundamentals:
  - onesignal-segment-management
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - clay-scoring
---

# Push Notification Segmentation

This drill builds the behavioral segmentation layer that powers personalized push notifications at scale. Instead of blasting the same message to all subscribers, segment users by engagement level, feature usage, lifecycle stage, and predicted intent so each push is relevant to the recipient.

## Prerequisites

- Push notification setup complete (run `push-notification-setup` drill first)
- PostHog with at least 30 days of tracked user behavior
- OneSignal with active subscribers
- n8n instance for scheduled sync workflows

## Steps

### 1. Define the Segmentation Matrix

Build segments across two dimensions: engagement level and lifecycle stage.

**Engagement levels** (derived from PostHog session data):

| Segment | Definition | Push Strategy |
|---------|------------|---------------|
| Power users | 5+ sessions/week, use 3+ features | Low frequency, feature-depth content |
| Regular users | 2-4 sessions/week | Habit reinforcement, streak nudges |
| Casual users | 1 session/week or less | Value highlights, "here's what you missed" |
| At-risk | Was regular, dropped to 0 sessions in 7+ days | Re-engagement with specific value prop |
| Dormant | No session in 21+ days | Win-back with product update summary |

**Lifecycle stages** (derived from account events):

| Stage | Definition | Push Strategy |
|-------|------------|---------------|
| Onboarding | Account < 14 days, setup incomplete | Guide to next setup step |
| Activated | Completed core value action | Feature discovery |
| Retained | Active 30+ days | Milestone celebrations, depth |
| Expanding | Using advanced features or adding team | Team-focused notifications |
| Churning | Usage declining week-over-week | Intervention, support offer |

### 2. Build PostHog Cohorts

Using `posthog-cohorts`, create a cohort for each cell in the segmentation matrix:

Example cohort definitions:
- **Power + Retained**: `session_count_7d >= 5 AND account_age >= 30 AND feature_count >= 3`
- **At-risk + Activated**: `session_count_7d == 0 AND previous_session_count_7d >= 2 AND has_completed_activation`
- **Casual + Onboarding**: `session_count_7d <= 1 AND account_age < 14`

Create at least 8 cohorts covering the highest-impact combinations. You do not need every matrix cell — focus on segments where push can change behavior.

### 3. Sync Segments to OneSignal

Using `n8n-scheduling` and `n8n-workflow-basics`, build a sync workflow that runs every 4 hours:

1. Query PostHog API for each cohort's current members
2. For each user in the cohort, update their OneSignal tags via `onesignal-segment-management`:
   - `engagement_level`: "power", "regular", "casual", "at_risk", "dormant"
   - `lifecycle_stage`: "onboarding", "activated", "retained", "expanding", "churning"
   - `last_active_days_ago`: integer
   - `top_feature`: the feature they use most
   - `session_count_7d`: integer
3. Remove tags from users who left a cohort (e.g., an at-risk user who returned)
4. Log sync results to PostHog: users updated, segment sizes, errors

### 4. Build Feature-Usage Segments

Beyond engagement and lifecycle, segment by which features users actually use:

Using `posthog-custom-events`, identify the top 5 features by usage volume. For each feature:
- Create a "uses X" segment (used feature in last 14 days)
- Create a "never tried X" segment (has never fired the feature event, account > 7 days)
- Create a "stopped using X" segment (used feature before, not in last 14 days)

These segments power feature discovery pushes: "You haven't tried [Export] yet — it saves 20 minutes/week."

### 5. Add Enrichment Signals

Using `clay-scoring`, add external context to push targeting:

- Company size (from enrichment): solo users get individual tips, team users get collaboration nudges
- Industry: tailor examples and use cases in push copy to match the user's industry
- Plan tier: free users get upgrade nudges at usage limits, paid users get depth content

Sync enrichment data as OneSignal tags alongside behavioral data.

### 6. Validate Segment Quality

After building segments, validate they produce meaningful targeting:

- **Size check**: Each segment should contain at least 50 users. Segments smaller than 50 cannot produce statistically meaningful push performance data.
- **Overlap check**: Verify engagement segments are mutually exclusive (a user is in exactly one engagement level). Lifecycle stages may overlap for transition periods.
- **Freshness check**: After 1 week of sync, verify segment sizes are changing (users are moving between segments, not stuck).
- **Push relevance check**: For each segment, write the push copy you would send. If you cannot write a push that is different from the default, the segment is not adding value.

## Output

- Segmentation matrix with engagement levels and lifecycle stages defined
- PostHog cohorts created for at least 8 high-impact segments
- n8n workflow syncing segment data to OneSignal every 4 hours
- Feature-usage segments for top 5 features
- Enrichment data integrated into push targeting
- Validation report confirming segment sizes, exclusivity, and freshness
