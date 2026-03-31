---
name: gamification-reward-delivery
description: Deliver gamification rewards and celebrations via Intercom in-app messages and Loops email notifications
category: Product
tools:
  - Intercom
  - Loops
  - n8n
  - PostHog
fundamentals:
  - intercom-in-app-messages
  - intercom-checklists
  - loops-transactional
  - n8n-triggers
  - posthog-custom-events
---

# Gamification Reward Delivery

This drill builds the notification and celebration layer for your gamification system. When a user earns a badge, levels up, hits a streak milestone, or climbs the leaderboard, they need to know immediately and feel rewarded. This drill connects gamification events to delivery channels.

## Input

- Gamification system designed (from `gamification-system-design` drill)
- Gamification events instrumented in PostHog (from `gamification-event-tracking` drill)
- Intercom configured with Messenger on your product
- Loops configured for transactional email
- n8n instance for orchestration

## Steps

### 1. Configure real-time in-app celebrations

Using `intercom-in-app-messages`, create messages triggered by gamification events. For each reward type:

**Badge Earned:**
Create an Intercom post (banner-style) triggered when `gamification_badge_awarded` fires:
- Title: "Badge Unlocked: {badge_name}"
- Body: "{badge_description}. You've earned {badges_total} badges so far."
- CTA: "View your badges" -> deep link to profile/badges page
- Display: show_once per badge, dismiss after 10 seconds
- Audience: user where badge_id = {specific badge} AND badge_celebrated != true

**Streak Milestone:**
Create an Intercom tooltip or post triggered on `gamification_streak_updated` where is_milestone = true:
- 3-day streak: "3 days in a row. Keep it going!"
- 7-day streak: "A full week. You're building a habit."
- 14-day streak: "Two weeks strong. Only 2% of users reach this."
- 30-day streak: "30-day streak. You're in the top 1%."
- Display: show_once per milestone

**Level Up:**
Create an Intercom post triggered on `gamification_level_up`:
- Title: "Level Up: {level_name}"
- Body: "You unlocked {unlock_description}. Your next milestone is {next_level_points - current_points} points away."
- CTA: "See what's new" -> deep link to unlocked feature or rewards page
- Display: show_once per level

**Leaderboard Climb:**
Using `n8n-triggers`, detect when a user's rank improves by 5+ positions and trigger an Intercom message:
- Body: "You moved up to #{new_rank} on the leaderboard this week."
- CTA: "View leaderboard"

### 2. Configure email reward notifications

Using `loops-transactional`, set up email notifications for high-value gamification moments:

**Weekly Streak Summary (for active streak holders):**
Trigger: weekly on Monday via n8n for users with gamification_current_streak >= 3
- Subject: "Your {streak_count}-day streak is alive"
- Body: Points earned this week, badges close to earning, streak milestone approaching, leaderboard position
- CTA: "Keep your streak" -> deep link to the product action that extends the streak

**Badge Earned Email:**
Trigger: on `gamification_badge_awarded` for silver and gold tier badges (skip bronze to avoid email fatigue)
- Subject: "You earned the {badge_name} badge"
- Body: What the badge means, how many users have it, what badge to aim for next
- CTA: "See your collection"

**Streak Recovery Nudge:**
Trigger: on `gamification_streak_broken` where streak_count_at_break >= 7 (only nudge for meaningful streaks)
- Subject: "Your {streak_count}-day streak ended yesterday"
- Body: Acknowledge the achievement (not the failure), mention streak recovery if available, show how close they are to their next milestone
- CTA: "Start a new streak today"
- Send timing: 24 hours after the break (gives time for organic return)

**Monthly Progress Digest:**
Trigger: first of month via n8n
- Subject: "Your {month_name} progress: {points_earned} points, {badges_earned} badges"
- Body: Monthly stats, level progression, best streak, leaderboard highlights, comparison to previous month
- CTA: "See your full profile"

### 3. Build the orchestration workflow

Using `n8n-triggers`, create an n8n workflow that listens for PostHog gamification events via webhook and routes them to the appropriate delivery channel:

1. **Webhook trigger**: PostHog sends events via webhook to n8n
2. **Event router**: Switch node based on event name
3. **Deduplication**: Check if this reward was already delivered (query Intercom user attributes)
4. **Channel selection**: In-app for all events; email only for high-value events (silver/gold badges, streak milestones >= 7, level ups)
5. **Delivery**: Send Intercom message via API, send Loops email via API
6. **Logging**: Track delivery in PostHog via `posthog-custom-events`:

```javascript
posthog.capture('gamification_reward_delivered', {
  reward_type: 'badge_earned',
  channel: 'intercom_in_app',
  badge_id: 'first_collaboration',
  delivered_at: timestamp
});
```

### 4. Implement progressive notification rules

Prevent notification fatigue with these rules:

- Maximum 3 gamification notifications per user per day (in-app)
- Maximum 2 gamification emails per user per week
- If a user earns multiple badges in one session, batch them into a single "You earned 3 badges today" message
- Streak notifications only at milestones (3, 7, 14, 30, 60, 90), not every day
- Suppress gamification emails for users who have not opened the last 3 gamification emails (use Loops engagement data)

### 5. Track delivery effectiveness

Using `posthog-custom-events`, measure the impact of each notification:

- **Click-through rate**: % of notifications where the user clicked the CTA
- **Return rate**: % of streak recovery nudges that resulted in a new streak starting within 48 hours
- **Engagement lift**: Compare weekly active days for users who received notifications vs those who did not
- **Unsubscribe rate**: Monitor Loops unsubscribe events for gamification emails -- if above 1% per send, reduce frequency

## Output

- In-app celebration messages for badges, streaks, levels, and leaderboard moves via Intercom
- Email notifications for weekly summaries, high-value badges, streak recovery, and monthly digests via Loops
- n8n orchestration workflow routing gamification events to delivery channels
- Notification fatigue prevention rules
- Delivery effectiveness tracking in PostHog

## Triggers

The n8n orchestration workflow runs continuously, triggered by PostHog webhook events. Weekly streak summaries fire Monday mornings. Monthly digests fire on the 1st. Re-run the full drill setup when adding new gamification mechanics or notification channels.
