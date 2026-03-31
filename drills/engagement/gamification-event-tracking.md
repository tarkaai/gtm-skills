---
name: gamification-event-tracking
description: Instrument all gamification events in PostHog and build funnels, cohorts, and dashboards for gamification measurement
category: Enablement
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - n8n-workflow-basics
---

# Gamification Event Tracking

This drill implements the event schema from the `gamification-system-design` drill in PostHog and builds the measurement layer: funnels, cohorts, and dashboards that track gamification health.

## Input

- Gamification specification from the `gamification-system-design` drill
- PostHog project with SDK installed
- Product codebase with gamification logic implemented (or ready for instrumentation)

## Steps

### 1. Implement core gamification events

Using `posthog-custom-events`, instrument these events at the points where gamification state changes occur in your product:

**Points events:**
```javascript
posthog.capture('gamification_points_earned', {
  action: actionName,        // which product action earned points
  points: pointsAwarded,     // points from this action
  total_points: userTotal,   // cumulative total
  level: currentLevel,       // user's current level
  source: 'organic'          // organic | bonus | streak_multiplier
});
```

**Streak events:**
```javascript
posthog.capture('gamification_streak_updated', {
  streak_type: streakType,   // daily_login | weekly_active | etc.
  streak_count: count,       // current consecutive count
  is_milestone: isMilestone, // true at 3, 7, 14, 30, 60, 90
  streak_best: personalBest  // user's all-time best for this streak
});

posthog.capture('gamification_streak_broken', {
  streak_type: streakType,
  streak_count_at_break: lastCount,
  days_since_last_activity: daysMissed,
  grace_period_used: usedGrace  // true if recovery was available but not used
});
```

**Badge events:**
```javascript
posthog.capture('gamification_badge_awarded', {
  badge_id: badgeId,
  badge_name: badgeName,
  badge_tier: tier,          // bronze | silver | gold
  badges_total: totalCount,
  time_to_earn_days: daysFromSignup
});
```

**Level events:**
```javascript
posthog.capture('gamification_level_up', {
  previous_level: prevLevel,
  new_level: newLevel,
  level_name: levelName,
  total_points: totalPoints,
  days_since_signup: daysSinceSignup
});
```

**Leaderboard events:**
```javascript
posthog.capture('gamification_leaderboard_viewed', {
  user_rank: rank,
  leaderboard_scope: scope,  // weekly_global | weekly_team | cohort
  total_participants: count
});
```

### 2. Set person properties for gamification state

Update PostHog person properties on each gamification state change:

```javascript
posthog.people.set({
  gamification_level: currentLevel,
  gamification_total_points: totalPoints,
  gamification_badges_count: badgeCount,
  gamification_longest_streak: longestStreak,
  gamification_current_streak: currentStreak,
  gamification_joined_date: joinDate
});
```

These properties enable cohort creation and segmentation.

### 3. Build gamification funnels

Using `posthog-funnels`, create funnels that measure gamification adoption and progression:

**Gamification Onboarding Funnel:**
```
signup_completed
  -> gamification_points_earned (first ever)
    -> gamification_badge_awarded (first badge)
      -> gamification_streak_updated (streak >= 3)
        -> gamification_level_up (level 2+)
```

**Streak Retention Funnel:**
```
gamification_streak_updated (streak = 3)
  -> gamification_streak_updated (streak = 7)
    -> gamification_streak_updated (streak = 14)
      -> gamification_streak_updated (streak = 30)
```

Break both funnels down by signup cohort (week), acquisition channel, and plan type.

### 4. Create gamification cohorts

Using `posthog-cohorts`, create cohorts for targeting and analysis:

- **Gamification Active**: earned points in last 7 days
- **Gamification Dormant**: has gamification_level >= 1 but no points earned in 14+ days
- **Streak Holders**: gamification_current_streak >= 3
- **Streak Broken**: gamification_streak_broken event in last 7 days AND gamification_current_streak = 0
- **Badge Collectors**: gamification_badges_count >= 5
- **Leaderboard Engaged**: gamification_leaderboard_viewed 3+ times in last 14 days
- **Level Stalled**: same gamification_level for 21+ days with declining weekly points

### 5. Build the gamification dashboard

Using `posthog-dashboards`, create a "Gamification Health" dashboard:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Participation rate | Trend line | % of active users earning points this week |
| Points earned (weekly) | Bar chart | Total points earned across all users, by week |
| Streak distribution | Histogram | How many users at each streak length |
| Active streaks trend | Trend line | Count of users with active streak >= 3, by week |
| Badge award velocity | Bar chart | Badges awarded per week, by badge tier |
| Level distribution | Pie chart | % of gamification users at each level |
| Gamification onboarding funnel | Funnel | Drop-off from first points to level 2 |
| Streak survival curve | Retention | % of users maintaining streak at day 3, 7, 14, 30 |
| Leaderboard engagement | Trend line | Leaderboard views per week |
| Gamified vs non-gamified retention | Comparison | Week-over-week retention for gamification participants vs non-participants |

Set alerts:
- Participation rate drops below 30% of active users
- Active streaks count declines 20%+ week-over-week
- Gamification onboarding funnel conversion drops below 40%

### 6. Set up data pipeline for leaderboards

Using `n8n-workflow-basics`, build an n8n workflow that:

1. Runs daily via cron
2. Queries PostHog for points earned in the current leaderboard period (weekly)
3. Computes rankings (global, per-team if applicable)
4. Writes rankings to your product database or API
5. Detects rank changes and flags users who moved up 5+ positions (for notification triggers)

## Output

- All gamification events instrumented in PostHog
- Person properties tracking gamification state
- 3 funnels measuring gamification adoption and streak retention
- 7 cohorts for targeting interventions
- 10-panel gamification health dashboard with alerts
- Daily leaderboard computation pipeline in n8n

## Triggers

Run this drill once during initial setup. Re-run the dashboard and cohort definitions when adding new gamification mechanics. The leaderboard pipeline runs daily on n8n cron.
