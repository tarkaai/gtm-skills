---
name: gamification-system-design
description: Design a gamification system with streaks, badges, points, and leaderboards mapped to retention-critical product actions
category: Enablement
tools:
  - PostHog
  - Intercom
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - intercom-checklists
---

# Gamification System Design

This drill produces the complete gamification blueprint: which mechanics to use, which product actions they reward, how progression works, and what the reward structure looks like. The output is a specification document an agent or engineer can implement directly.

## Input

- Product's core value actions (the behaviors that correlate with retention)
- PostHog with at least 14 days of usage data (to identify which actions power users perform)
- Target user segments (new, active, at-risk)

## Steps

### 1. Identify retention-critical actions

Query PostHog using `posthog-cohorts` to compare retained users (active 30+ days) against churned users (inactive 14+ days, previously active). Identify the 3-5 actions that most differentiate retained users from churned users. These are your gamification targets. Rank them by correlation strength.

Example output:
- Action A: "created_project" -- 87% of retained users did this 3+ times in first 14 days vs 23% of churned
- Action B: "invited_teammate" -- 72% of retained vs 11% of churned
- Action C: "used_advanced_feature_X" -- 65% of retained vs 8% of churned

### 2. Select gamification mechanics

Map mechanics to the behavioral goals:

**Streaks** -- for daily/weekly habitual actions. Best for actions users should repeat regularly (daily logins, weekly reports, content creation). Define:
- Streak unit: daily or weekly
- Minimum qualifying action per period (e.g., 1 project edit per day)
- Streak milestones: 3, 7, 14, 30, 60, 90 days
- Streak recovery: allow 1 grace period per 7-day window (prevents frustration from a single miss)

**Badges** -- for milestone achievements. Best for one-time or cumulative actions (first project, 10th collaboration, first API call). Define:
- Badge tiers: Bronze (easy, first week), Silver (moderate, first month), Gold (hard, power user)
- Each badge requires a specific, measurable action
- Maximum 15 badges at launch (too many dilutes motivation)

**Points** -- for quantifying overall engagement. Best for creating a single engagement score visible to the user. Define:
- Point values per action (weighted by retention importance)
- Point thresholds for levels (Level 1: 0-100, Level 2: 100-500, etc.)
- Points decay: optional weekly decay to encourage ongoing activity (e.g., 10% weekly decay on inactive weeks)

**Leaderboards** -- for competitive/social motivation. Best for team products or communities. Define:
- Scope: global, team, or cohort-based (users who signed up the same week)
- Time window: weekly resets (prevents permanent leaders from discouraging new users)
- Metric: points earned this period
- Visibility: top 10 + user's own rank

### 3. Design the progression system

Create a unified progression map:

```
Level 1 (Explorer): 0-100 points
  Unlock: Basic dashboard, streak counter visible
  Badges available: First Login, First [Core Action], 3-Day Streak

Level 2 (Builder): 100-500 points
  Unlock: Badge showcase on profile, weekly digest email
  Badges available: 7-Day Streak, 10x [Core Action], First Collaboration

Level 3 (Pro): 500-2000 points
  Unlock: Leaderboard access, custom avatar/theme
  Badges available: 30-Day Streak, Power User, Team Leader

Level 4 (Champion): 2000+ points
  Unlock: Beta features, community recognition
  Badges available: 90-Day Streak, 100x [Core Action], Mentor Badge
```

Ensure each level is achievable within a reasonable timeframe: Level 2 within 2 weeks of active use, Level 3 within 2 months, Level 4 within 6 months.

### 4. Define the event schema

Using `posthog-custom-events`, define the events the gamification system will fire:

```javascript
// Points earned
posthog.capture('gamification_points_earned', {
  action: 'created_project',
  points: 10,
  total_points: 450,
  level: 2
});

// Streak updated
posthog.capture('gamification_streak_updated', {
  streak_type: 'daily_login',
  streak_count: 7,
  is_milestone: true
});

// Badge awarded
posthog.capture('gamification_badge_awarded', {
  badge_id: 'first_collaboration',
  badge_tier: 'bronze',
  badges_total: 4
});

// Level up
posthog.capture('gamification_level_up', {
  new_level: 3,
  level_name: 'Pro',
  total_points: 510
});

// Leaderboard position
posthog.capture('gamification_leaderboard_viewed', {
  user_rank: 12,
  leaderboard_scope: 'weekly_global'
});
```

### 5. Map rewards to Intercom delivery

Using `intercom-checklists`, design the onboarding checklist that introduces gamification:

- Step 1: "Complete your first [core action]" -- auto-completes on `gamification_badge_awarded` where badge_id = first_core_action
- Step 2: "Start a streak -- come back tomorrow" -- auto-completes on `gamification_streak_updated` where streak_count >= 2
- Step 3: "Earn your first badge" -- auto-completes on `gamification_badge_awarded`

This checklist teaches users the gamification system through doing, not reading.

### 6. Document the specification

Produce a structured specification with:
- Complete list of badges (id, name, tier, trigger condition, PostHog event)
- Streak definitions (type, period, milestones, recovery rules)
- Point table (action, points, daily cap if any)
- Level thresholds and unlocks
- Leaderboard configuration (scope, reset period, metric)

This document is the input for the `gamification-event-tracking` and `gamification-reward-delivery` drills.

## Output

- Gamification specification document with all mechanics defined
- Event schema for PostHog instrumentation
- Progression map with levels, badges, streaks, and leaderboards
- Intercom onboarding checklist design for gamification introduction

## Triggers

Run this drill once at the start of the play. Re-run when adding new gamification mechanics or when retention data reveals new critical actions.
