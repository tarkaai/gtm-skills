---
name: push-notification-health-monitor
description: Continuously monitor push notification performance metrics and alert on anomalies in delivery, CTR, opt-out, and downstream engagement
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Push Notification Health Monitor

This drill builds the always-on monitoring system for push notification performance. It detects problems (delivery drops, CTR decline, opt-out spikes) before they compound, and tracks the impact of push on downstream engagement metrics (DAU, session depth, retention).

## Prerequisites

- Push notifications sending for at least 14 days (baseline data required)
- PostHog tracking push lifecycle events (`push_sent`, `push_delivered`, `push_clicked`, `push_unsubscribed`)
- n8n instance for scheduling automated checks
- Attio for logging health reports

## Steps

### 1. Build the Push Performance Dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

**Delivery Health:**
- Delivery rate trend (daily): `push_delivered / push_sent` — target >95%
- Failed deliveries by error type (expired tokens, invalid tokens, rate limited)
- Subscriber count trend (net new subscriptions minus unsubscribes)

**Engagement:**
- CTR trend (daily): `push_clicked / push_delivered` — track by campaign type
- CTR by segment: power users vs regular vs casual vs at-risk
- CTR by notification type: habit, time-sensitive, re-engagement, value delivery
- CTR by time of day: heatmap showing which send times perform best

**Downstream Impact:**
- DAU lift: compare DAU on push-send days vs non-send days
- Session depth after push click: average pages/actions in the session triggered by push
- Retention correlation: 7-day retention rate for push subscribers vs non-subscribers
- Feature adoption from push: users who adopted a feature within 24 hours of a push promoting it

**Health Signals:**
- Opt-out rate trend (weekly): `push_unsubscribed` events — alarm if >2% of subscribers in a week
- Permission denial rate: `push_permission_denied / push_prompt_shown` — alarm if >70%
- Notification fatigue index: ratio of `push_dismissed / push_delivered` trending upward over 4 weeks

### 2. Configure Anomaly Detection

Using `posthog-anomaly-detection`, set up automated checks that run daily via `n8n-scheduling`:

| Metric | Normal Range | Alert Threshold | Action |
|--------|-------------|-----------------|--------|
| Delivery rate | >95% | Drops below 90% | Check push provider status, audit expired tokens |
| Overall CTR | Baseline ±5pp | Drops >10pp from 4-week average | Audit recent push copy, check segment drift |
| Opt-out rate | <0.5%/week | Exceeds 2%/week | Immediately reduce send frequency, audit copy |
| Permission grant rate | >40% | Drops below 25% | Audit prompt timing and copy |
| Subscriber count | Growing | Declines for 2+ weeks | Audit opt-in prompt visibility and value prop |

### 3. Build the Alerting Workflow

Using `n8n-triggers` and `n8n-scheduling`, create an n8n workflow:

1. **Daily check (8 AM)**: Query PostHog for yesterday's push metrics. Compare against thresholds.
2. **If anomaly detected**: Post a Slack alert with the specific metric, current value, threshold, and recommended action.
3. **If critical anomaly** (opt-out spike >3%/week or delivery rate <80%): Automatically pause all non-essential push campaigns via OneSignal API. Post urgent Slack alert.
4. **Weekly summary (Monday 9 AM)**: Generate a digest of the past week's push performance. Include trend direction for each metric and highlight the best and worst performing campaigns.

### 4. Track Push Impact on Retention

Build a PostHog insight specifically measuring push's contribution to retention:

1. Create two cohorts: `push_subscriber` and `non_push_subscriber` (matched by signup date and initial engagement)
2. Compare 7-day, 14-day, and 30-day retention between cohorts
3. Calculate the **push lift**: the percentage point improvement in retention attributable to push
4. Track this lift over time — if it's declining, push content needs refreshing

This metric is the primary justification for the push program. If push subscribers do not retain better than non-subscribers, the push strategy needs fundamental rethinking.

### 5. Log Health Reports

Using `attio-notes`, log each weekly health report as a note on the push notification campaign record in Attio. Include:

- Week-over-week metric changes
- Anomalies detected and actions taken
- Top-performing and worst-performing campaigns
- Subscriber growth/decline
- Recommended actions for the coming week

This creates an audit trail that the `autonomous-optimization` drill can use when diagnosing what to experiment on.

## Output

- PostHog dashboard with delivery, engagement, downstream impact, and health signal panels
- Daily automated anomaly detection with Slack alerts
- Critical anomaly auto-pause for push campaigns
- Weekly health digest with trend analysis
- Push lift measurement comparing subscriber vs non-subscriber retention
- Health reports logged in Attio for historical reference
