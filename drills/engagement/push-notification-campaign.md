---
name: push-notification-campaign
description: Design, schedule, and send targeted push notification campaigns based on user behavior and engagement patterns
category: Messaging
tools:
  - OneSignal
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - onesignal-send-notification
  - onesignal-segment-management
  - posthog-cohorts
  - posthog-custom-events
  - n8n-triggers
  - n8n-scheduling
---

# Push Notification Campaign

This drill covers the end-to-end process of designing, targeting, scheduling, and sending push notification campaigns that drive engagement and retention. Each campaign should have a clear behavioral trigger and measurable outcome.

## Prerequisites

- Push notification infrastructure set up (run `push-notification-setup` drill first)
- PostHog tracking active with at least 14 days of user behavior data
- OneSignal (or chosen provider) with active subscribers
- n8n instance for scheduling and triggers

## Steps

### 1. Define Campaign Types

Build a library of push notification campaigns, each tied to a specific user behavior:

**Habit Reinforcement:**
- Streak maintenance: "You're on a 5-day streak! Open the app to keep it going"
- Session reminder: Sent at the user's peak-activity time when they haven't opened today
- Weekly milestone: "You completed 12 tasks this week — 3 more than last week"

**Time-Sensitive Engagement:**
- Teammate activity: "Sarah commented on your project" (real-time)
- Expiring content: "Your trial ends in 48 hours — activate now"
- Limited availability: "Live webinar starting in 30 minutes"

**Re-engagement:**
- Dormancy nudge: "We saved your progress — pick up where you left off" (sent after 3+ days inactive)
- New feature: "We shipped the export feature you requested" (sent to users who asked for it)
- Social proof: "Your team has been active — see what they accomplished"

**Value Delivery:**
- Report ready: "Your weekly analytics report is ready to view"
- Goal achieved: "You hit your monthly target! Here's your summary"
- Personalized insight: "Your most-used feature this week was [X] — try [Y] next"

### 2. Build Behavioral Segments

Using `onesignal-segment-management` and `posthog-cohorts`, create the targeting segments for each campaign:

For each campaign, define the entry criteria:
- **Who**: Which users should receive this push? (e.g., "active in last 7 days AND has not opened today")
- **When**: What triggers the send? (e.g., "3 PM in user's local timezone" or "immediately when teammate posts")
- **Frequency cap**: Maximum pushes per user per day (recommended: 2-3 max)
- **Exclusions**: Who should NOT receive this push? (e.g., "users who already performed the target action today")

Set up OneSignal tags from PostHog data via n8n to keep segments fresh. Run the sync hourly using `n8n-scheduling`.

### 3. Write Push Copy

Push notification copy must be scannable in under 2 seconds:

- **Title**: 5-8 words maximum. Lead with the action or value, not your brand name.
- **Body**: 15-25 words. Specific > generic. Use numbers. Include the user's context when possible.
- **Deep link**: Always link to the specific content or action, never the home screen.

Bad: "Check out what's new in the app!" (vague, no value)
Good: "3 items need your review — Sarah and Jake posted updates" (specific, social, actionable)

Bad: "Don't forget about us!" (guilt-trip, no value)
Good: "Your weekly report is ready: revenue up 12% vs last week" (delivers value in the notification itself)

### 4. Configure Send Automation

Using `n8n-triggers` and `onesignal-send-notification`, build automation workflows:

**Event-triggered pushes** (real-time):
1. PostHog webhook fires when a tracked event occurs (e.g., `comment_posted`)
2. n8n receives the webhook, resolves the target user(s)
3. n8n calls OneSignal API to send the push to the recipient
4. n8n logs `push_sent` event back to PostHog with campaign metadata

**Scheduled pushes** (recurring):
1. n8n cron triggers at the configured time (e.g., daily at 9 AM)
2. n8n queries PostHog for the cohort (e.g., "users with streak > 3 who haven't opened today")
3. For each matched user, n8n calls OneSignal to send with timezone delivery
4. n8n logs all sends to PostHog

**Lifecycle pushes** (one-time triggers):
1. n8n monitors PostHog for lifecycle events (e.g., `trial_started`, `day_3_reached`)
2. When triggered, send the appropriate lifecycle push
3. Mark the user so they don't receive the same lifecycle push again

### 5. Set Frequency Caps and Quiet Hours

Implement sending limits to avoid notification fatigue:

- **Per-user daily cap**: Maximum 3 pushes per user per day. If a user would receive a 4th, skip the lowest-priority one.
- **Quiet hours**: Do not send between 9 PM and 8 AM in the user's local timezone. Queue pushes for the next morning.
- **Cooldown**: After a user clicks a push, wait at least 2 hours before sending another (unless it's a real-time trigger like teammate activity).
- **Unsubscribe signal**: If a user dismisses 5 consecutive pushes without clicking, reduce their frequency by 50% for 7 days.

### 6. Measure Campaign Performance

Using `posthog-custom-events`, track per-campaign:

- **Delivery rate**: `push_delivered / push_sent` (target: >95%)
- **CTR**: `push_clicked / push_delivered` (target: >25% for Smoke, >35% for Baseline)
- **Downstream action**: Did the user perform the intended action within 30 minutes of clicking? (target: >50% of clickers)
- **Opt-out rate**: `push_unsubscribed` events per week (alarm if >2% weekly)

Build a PostHog dashboard showing these metrics per campaign type, per segment, and trending over time.

## Output

- Library of 4+ push notification campaigns with behavioral triggers
- Automated send workflows in n8n for event-triggered, scheduled, and lifecycle pushes
- Frequency capping and quiet hours enforced
- PostHog dashboard tracking delivery, CTR, downstream action, and opt-out per campaign
