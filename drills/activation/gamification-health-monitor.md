---
name: gamification-health-monitor
description: Monitor gamification system health with anomaly detection, weekly reports, and intervention triggers for declining engagement
category: Enablement
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
---

# Gamification Health Monitor

This drill builds the always-on monitoring layer for the gamification system. It detects when gamification engagement declines, diagnoses the cause, and triggers automated interventions. This is the play-specific complement to the `autonomous-optimization` drill -- it handles gamification-specific signals that the generic optimization loop would miss.

## Input

- Gamification system running at Scalable level for at least 4 weeks
- PostHog dashboard from `gamification-event-tracking` drill
- n8n instance for scheduled monitoring
- Baseline metrics established (participation rate, streak survival, badge velocity)

## Steps

### 1. Define gamification health metrics

Establish the metrics this monitor tracks and their healthy ranges:

| Metric | Healthy Range | Warning | Critical |
|--------|--------------|---------|----------|
| Participation rate (% active users earning points/week) | >= 40% | 30-40% | < 30% |
| Streak survival (% of 3-day streaks reaching 7 days) | >= 50% | 35-50% | < 35% |
| Badge award velocity (badges awarded / active users / week) | >= 0.3 | 0.15-0.3 | < 0.15 |
| Leaderboard view rate (views / participants / week) | >= 1.5 | 0.8-1.5 | < 0.8 |
| Level-up rate (level ups / active gamified users / month) | >= 0.15 | 0.08-0.15 | < 0.08 |
| Gamified user retention (week-over-week) | >= 75% | 60-75% | < 60% |
| Streak break rate (streaks broken / active streaks / week) | <= 25% | 25-40% | > 40% |
| Challenge completion rate | 40-60% | 25-40% or 60-80% | < 25% or > 80% |

### 2. Build the daily health check

Using `n8n-scheduling`, create a workflow that runs daily at 6 AM:

1. Query PostHog for each health metric using the `posthog-anomaly-detection` fundamental
2. Compare each metric against its healthy range
3. Compare each metric against its 4-week rolling average (detect trends)
4. Classify each metric: **healthy**, **warning**, **critical**
5. If all healthy: log to PostHog and exit
6. If any warning or critical: trigger diagnostic phase

Log the daily health check:
```javascript
posthog.capture('gamification_health_check', {
  participation_rate: 0.42,
  streak_survival: 0.55,
  badge_velocity: 0.35,
  overall_status: 'healthy',  // healthy | warning | critical
  metrics_in_warning: [],
  metrics_in_critical: []
});
```

### 3. Implement diagnostic triggers

When a metric hits warning or critical, run targeted diagnostics:

**Participation rate declining:**
- Check: Are new users not starting gamification? (onboarding funnel drop-off)
- Check: Are existing gamified users stopping? (cohort retention breakdown)
- Check: Did a product change affect gamification visibility? (deploy correlation)

**Streak survival declining:**
- Check: Is a specific streak type breaking more? (daily vs weekly)
- Check: Is there a day-of-week pattern? (streaks break on weekends)
- Check: Are streak recovery mechanics being used? (if not, promote them)

**Badge velocity declining:**
- Check: Are users stuck at a specific badge? (threshold too high)
- Check: Have all easy badges been earned? (need new badges)
- Check: Are badge celebrations still showing? (Intercom delivery check)

**Challenge completion out of range:**
- Too low: challenges are too hard for the segment -- recalibrate difficulty
- Too high: challenges are too easy -- increase difficulty to maintain motivation

### 4. Configure automated interventions

For each diagnostic outcome, define automated responses:

**New users not discovering gamification:**
Using `intercom-in-app-messages`, send a targeted in-app message to users who signed up 3+ days ago with zero gamification events:
- "Did you know you can earn badges and climb the leaderboard? Complete your first [core action] to start."

**Streak holders at risk (active streak but declining daily points):**
Using `loops-transactional`, send a nudge email:
- "Your {streak_count}-day streak is going strong. Log in today to keep it alive."
- Timing: send at the user's typical login time (based on PostHog session data)

**Badge staleness (no new badges available for Level 3+ users):**
Flag for the product team: "Top users have earned all available badges. Add 3+ new badges targeting advanced features to maintain engagement."

**Leaderboard disengagement:**
Using `intercom-in-app-messages`, show a contextual nudge when a user who previously checked the leaderboard has not viewed it in 7+ days:
- "You're #{rank} this week. Check how you compare."

### 5. Build weekly gamification report

Using `n8n-scheduling`, create a weekly workflow that generates a gamification health report:

1. Aggregate all daily health checks for the week
2. Calculate week-over-week trends for each metric
3. Summarize interventions triggered and their outcomes
4. Highlight:
   - Best-performing gamification mechanic this week
   - Worst-performing mechanic (needs attention)
   - Cohort with highest/lowest gamification engagement
   - Notable user achievements (longest streak, most badges, leaderboard champion)
5. Generate the report and post to Slack
6. Store in PostHog as a custom event for historical tracking

### 6. Define escalation rules

Set escalation thresholds that require human attention:

- Any metric in **critical** for 3+ consecutive days -> Slack alert to product team
- Gamified user retention drops below 60% for 2 consecutive weeks -> flag for strategic review
- Participation rate below 30% for 1 week -> pause new gamification experiments, diagnose root cause
- Streak break rate above 40% for 1 week -> review streak difficulty and grace period settings

These escalations prevent the autonomous system from optimizing in the wrong direction when the problem is structural, not tactical.

## Output

- Daily health check workflow in n8n with metric classification
- Diagnostic triggers for each declining metric
- Automated interventions via Intercom and Loops for common issues
- Weekly gamification health report
- Escalation rules for human review

## Triggers

Daily health check runs at 6 AM via n8n cron. Weekly report generates Monday at 8 AM. Interventions fire in real-time when diagnostics detect issues. Escalation alerts fire immediately when thresholds are breached.
