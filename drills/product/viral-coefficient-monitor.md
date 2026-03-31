---
name: viral-coefficient-monitor
description: Continuous health monitor for viral loop metrics — tracks K-factor trends, channel-level performance, and loop decay signals
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-cohorts
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Viral Coefficient Monitor

This drill creates an always-on monitoring system that tracks the health of viral loops and generates alerts when metrics shift. It is the play-specific companion to `autonomous-optimization` — while autonomous-optimization handles the experiment loop, this monitor provides the viral-specific signal detection and reporting that feeds it.

## Input

- Viral loop running at Scalable level for at least 4 weeks (sufficient data for trend detection)
- PostHog tracking all viral events (output of `viral-loop-instrumentation` drill)
- Viral Metrics Dashboard configured in PostHog
- n8n instance for scheduling

## Steps

### 1. Define viral health signals

Configure `posthog-anomaly-detection` to monitor these viral-specific metrics:

**Primary metrics** (checked daily):
- Viral coefficient (K): rolling 7-day calculation
- Invite volume: total `viral_share_initiated` events per day
- Invite-to-signup conversion rate: `viral_signup_completed` / `viral_landing_viewed`
- Referee activation rate: `viral_referee_activated` / `viral_signup_completed`

**Secondary metrics** (checked weekly):
- Channel-level K: K-factor broken down by `share_channel`
- Loop depth: average `generation` value from `viral_loop_closed`
- Time-to-share: median days from user signup to first `viral_share_initiated`
- Referrer concentration: top 10% of referrers as a percentage of total referrals (Gini coefficient proxy)

**Decay signals** (trigger immediate investigation):
- K drops below target threshold for 7 consecutive days
- Invite-to-signup conversion drops >25% week-over-week
- Active referrer count drops >30% month-over-month
- Zero loop-close events for 14 consecutive days

### 2. Build the monitoring workflow

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for yesterday's viral metrics using the viral dashboard's saved insights
2. Compare against 4-week rolling average
3. Classify each metric: **healthy** (within +/-10% of average), **warning** (deviation 10-25%), **critical** (deviation >25% or below absolute threshold)
4. If any metric is critical, fire an alert to Slack with: metric name, current value, average value, deviation percentage, and a link to the PostHog dashboard
5. Log all daily readings to Attio using `attio-notes` on the play's campaign record

### 3. Build the weekly viral health report

Using `n8n-scheduling`, create a weekly cron workflow:

1. Pull 7-day viral metrics from PostHog
2. Calculate week-over-week changes for all primary and secondary metrics
3. Generate a structured report:

```
VIRAL HEALTH REPORT — Week of [date]
===================================
K-Factor: [value] ([change]% WoW) [status emoji: healthy/warning/critical]
Invite Volume: [count] ([change]% WoW)
Invite→Signup: [rate]% ([change]pp WoW)
Referee Activation: [rate]% ([change]pp WoW)
Loop Depth (avg): [value] generations

TOP CHANNELS:
1. [channel]: K=[value], [volume] invites
2. [channel]: K=[value], [volume] invites

SIGNALS:
- [list of warnings or critical signals, or "All metrics healthy"]

RECOMMENDATION:
- [auto-generated: "No action needed" / "Investigate [metric] decline" / "Optimize [channel] conversion"]
```

4. Post to Slack and store in Attio

### 4. Build channel decay detection

Using `posthog-cohorts`, create weekly snapshots of channel performance. The workflow detects when a specific sharing channel's conversion rate degrades while others remain stable. This isolates channel-specific problems (e.g., email deliverability issues, social platform algorithm changes) from product-wide viral decay.

Compare each channel's current 2-week conversion rate against its own 8-week rolling average. Flag any channel with >20% decline. The flag includes the channel name, decline magnitude, and the specific funnel step where conversion dropped.

### 5. Monitor referrer health

Using `posthog-cohorts` and `n8n-workflow-basics`, build a referrer activity tracker:

- Count of users who referred at least once this month vs. last month
- New referrers this month (first `viral_share_initiated` ever)
- Lapsed referrers (referred previously, not this month, still active in product)
- Referrer churn (referred previously, now inactive in product entirely)

If new referrers cannot replace lapsed + churned referrers, the viral loop will decay even if per-referrer performance holds. Flag when new referrer growth rate falls below replacement rate for 2 consecutive weeks.

## Output

- Daily automated health checks on primary viral metrics
- Weekly viral health report posted to Slack and stored in Attio
- Channel-level decay detection isolating platform-specific problems
- Referrer pipeline health tracking (new vs. lapsed vs. churned)
- Alert system for critical metric deviations

## Triggers

Runs continuously from Durable level onward. Daily checks run via n8n cron. Weekly reports run every Monday. Channel and referrer health checks run weekly.
