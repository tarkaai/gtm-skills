---
name: gamification-leaderboard-pipeline
description: Build, compute, and serve leaderboards with weekly resets, team scoping, and rank-change notifications
category: Enablement
tools:
  - PostHog
  - n8n
  - Intercom
fundamentals:
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-workflow-basics
  - intercom-in-app-messages
---

# Gamification Leaderboard Pipeline

This drill builds the backend pipeline that computes leaderboard rankings, serves them to the product, and triggers notifications on rank changes. Leaderboards drive competitive engagement but require careful design to avoid discouraging new or casual users.

## Input

- Gamification events flowing to PostHog (from `gamification-event-tracking` drill)
- Points system defined (from `gamification-system-design` drill)
- n8n instance for scheduled computation
- Product API or database endpoint for writing leaderboard data

## Steps

### 1. Design leaderboard scopes

Define which leaderboards to compute:

**Weekly Global:** All users, points earned this calendar week (Monday-Sunday). Resets weekly. Purpose: broad competition, fresh start every week.

**Weekly Team:** Points earned this week by users in the same team/organization. Purpose: intra-team motivation for multi-user products.

**Cohort:** Users who signed up in the same calendar month, all-time points. Purpose: fair comparison among peers who started at the same time.

**All-Time:** Cumulative points, no reset. Purpose: long-term recognition. Only show top 50 to prevent new users from feeling permanently behind.

Start with Weekly Global only. Add other scopes at Scalable level when you have enough users per scope (minimum 20 per leaderboard for meaningful competition).

### 2. Build the computation pipeline

Using `n8n-scheduling`, create an n8n workflow that runs every 4 hours:

**Step 1 -- Query points data:**
Query PostHog API for `gamification_points_earned` events within the current leaderboard period:
```
GET /api/projects/{id}/events?event=gamification_points_earned&after={period_start}
```
Aggregate total points per distinct_id.

**Step 2 -- Compute rankings:**
Sort users by total period points (descending). Assign rank 1, 2, 3, etc. Handle ties by giving equal rank and skipping the next (standard competition ranking: 1, 2, 2, 4).

**Step 3 -- Detect rank changes:**
Compare current rankings against the previous computation. Flag:
- Users who moved up 5+ positions (positive trigger)
- Users who entered the top 10 for the first time (positive trigger)
- Users who dropped out of the top 10 (at-risk trigger)

**Step 4 -- Write rankings:**
POST the computed leaderboard to your product API/database:
```json
{
  "scope": "weekly_global",
  "period_start": "2026-03-23",
  "period_end": "2026-03-29",
  "computed_at": "2026-03-29T12:00:00Z",
  "rankings": [
    {"user_id": "abc", "rank": 1, "points": 450, "rank_change": 2},
    {"user_id": "def", "rank": 2, "points": 430, "rank_change": -1}
  ]
}
```

**Step 5 -- Log computation:**
Track the computation event in PostHog:
```javascript
posthog.capture('leaderboard_computed', {
  scope: 'weekly_global',
  total_participants: participantCount,
  top_score: topScore,
  median_score: medianScore
});
```

### 3. Implement weekly reset

Using `n8n-scheduling`, create a workflow that runs every Monday at 00:01 UTC:

1. Archive the previous week's final leaderboard (store in your database for historical reference)
2. Optionally, send the final standings as a "Last week's winners" Intercom message or Loops email to the top 10
3. Clear the current period cache
4. The computation pipeline automatically starts fresh with the new period

### 4. Configure rank-change notifications

Using `intercom-in-app-messages`, trigger notifications on rank changes detected in Step 2:

**Entered Top 10:**
- Message: "You're #{rank} on this week's leaderboard. {points} points."
- CTA: "View leaderboard"

**Moved Up 5+ Positions:**
- Message: "You jumped {positions_gained} spots to #{rank}. Keep going."
- CTA: "View leaderboard"

**Weekly Winner (Rank 1 at period end):**
- Badge award: "Weekly Champion" badge via `gamification_badge_awarded` event
- Intercom message: "You won this week's leaderboard with {points} points."

Rate-limit: maximum 1 leaderboard notification per user per day.

### 5. Build the leaderboard dashboard panel

Using `posthog-dashboards`, add a leaderboard health panel to the Gamification Health dashboard:

| Metric | Purpose |
|--------|---------|
| Leaderboard participants (weekly trend) | Is competitive engagement growing? |
| Leaderboard views per active user | How many users actually look at the leaderboard? |
| Top score distribution (p50, p90, p99) | Is the top getting too far ahead? |
| Score gap: rank 1 vs rank 10 | Competitive health -- too big a gap discourages |
| New entrants to top 10 per week | Accessibility of the top -- should be 3+ new faces per week |

Alert: If top 10 is dominated by the same 7+ users for 3 consecutive weeks, consider adding handicap mechanics or cohort-scoped leaderboards to keep competition fresh.

### 6. Anti-gaming protections

Implement guards against point manipulation:

- **Daily point cap**: Maximum points earnable per day (e.g., 200 points/day). Prevents single-day grinding.
- **Action rate limiting**: Same action cannot earn points more than once per 5 minutes. Prevents rapid-fire spam.
- **Anomaly detection**: Flag users earning 3x the median daily points for manual review.
- Implement these as checks in the n8n pipeline before writing points.

## Output

- Leaderboard computation pipeline running every 4 hours via n8n
- Weekly reset workflow via n8n
- Rank-change notifications via Intercom
- Leaderboard health metrics on PostHog dashboard
- Anti-gaming protections in the computation pipeline

## Triggers

Computation runs every 4 hours via n8n cron. Weekly reset runs Monday at midnight UTC. Notifications fire on each computation when rank changes are detected. Re-run setup when adding new leaderboard scopes.
