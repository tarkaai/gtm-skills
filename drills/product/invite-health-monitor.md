---
name: invite-health-monitor
description: Continuous monitoring of invite funnel health, acceptance rates, viral coefficient trends, and anomaly detection for the team invite system
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Invite Health Monitor

This drill creates the always-on monitoring layer for the invite mechanism. It detects when invite funnel metrics degrade, identifies the cause, and generates alerts for the `autonomous-optimization` drill to act on. Without this monitor, invite performance can silently decay as product changes, user mix shifts, or email deliverability fluctuates.

## Input

- Invite mechanism running at Scalable level with 500+ total invitations sent
- PostHog tracking the full invite funnel (all events from `invite-flow-setup`)
- Viral coefficient tracking (from `invite-viral-loop`)
- n8n instance for scheduled monitoring
- Attio for alert logging

## Steps

### 1. Build the invite health dashboard

Using `posthog-dashboards`, create a dashboard called "Invite Mechanism — Health" with these panels:

**Top-level metrics (large number tiles):**
- Current invite rate (% of active users who sent an invite in last 30 days)
- Current acceptance rate (invites accepted / invites sent, last 30 days)
- Viral coefficient (k) for the last 30 days
- Viral cycle time (median days from user signup to their invite being accepted)

**Trend charts (line charts, 12-week history):**
- Weekly invite rate with 4-week moving average
- Weekly acceptance rate with 4-week moving average
- Weekly viral coefficient with 4-week moving average
- Invites sent per week (volume)
- Unique inviters per week (breadth)

**Funnel breakdown (funnel chart):**
- invite_form_opened -> invite_sent -> invite_email_delivered -> invite_link_clicked -> invite_accepted -> invited_user_first_action
- Show conversion percentage at each step

**Segment comparison (bar charts):**
- Invite rate by plan tier (free, starter, pro, enterprise)
- Acceptance rate by entry point (team_settings, share_button, onboarding_checklist, etc.)
- Invited user retention (30-day retention of invited users vs organic users)

### 2. Define health thresholds

Set thresholds for each metric based on Scalable-level performance:

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Invite rate | >40% | 30-40% | <30% |
| Acceptance rate | >55% | 45-55% | <45% |
| Viral coefficient (k) | >0.25 | 0.15-0.25 | <0.15 |
| Email deliverability | >95% | 90-95% | <90% |
| Invite-to-click rate | >45% | 35-45% | <35% |
| Signup completion rate | >60% | 50-60% | <50% |
| Invited user activation | >65% | 55-65% | <55% |

These thresholds should be calibrated based on your actual Scalable-level baselines. Use the 4-week average from the end of Scalable as the starting "healthy" threshold.

### 3. Build the anomaly detection workflow

Using `n8n-scheduling`, create a workflow that runs every 6 hours:

1. Query PostHog for the last 7 days of invite funnel data using the `posthog-anomaly-detection` fundamental
2. Compare each metric against its 4-week rolling average
3. Classify each metric: **healthy** (within ±10% of average), **warning** (10-25% below average), **critical** (>25% below average or below the critical threshold)
4. For any metric in warning or critical state:
   a. Pull the breakdown by segment (plan tier, entry point, device, acquisition source)
   b. Identify which segment is driving the decline
   c. Check if a product deploy happened in the last 48 hours (common cause of invite funnel breaks)
   d. Check email deliverability metrics from Loops (common cause of acceptance rate drops)
5. Generate an alert payload:
   ```json
   {
     "metric": "acceptance_rate",
     "status": "critical",
     "current_value": 0.38,
     "baseline_value": 0.58,
     "decline_pct": 34.5,
     "worst_segment": "entry_point:share_button",
     "possible_cause": "email_deliverability_drop",
     "detected_at": "2025-03-15T09:00:00Z"
   }
   ```
6. Post alert to Slack and store in Attio as a note on the invite-mechanism campaign record

### 4. Build the invited-user retention monitor

Invited users should retain better than organic users (they have social proof and team context). If they do not, the acceptance flow is broken.

Using `posthog-cohorts`, create:
- Cohort: "Invited users — signed up last 30 days" (property: `was_invited = true`)
- Cohort: "Organic users — signed up last 30 days" (property: `was_invited = false`)

Using `posthog-custom-events`, compare 7-day and 30-day retention between the two cohorts. Track weekly:

```javascript
posthog.capture('invite_health_check', {
  check_type: 'retention_comparison',
  invited_user_7d_retention: 0.72,
  organic_user_7d_retention: 0.58,
  retention_lift: 0.14,  // invited users retain 14 percentage points better
  invited_user_30d_retention: 0.55,
  organic_user_30d_retention: 0.42,
  check_date: '2025-03-15'
});
```

Alert if invited user retention drops below organic user retention — this means the invite experience is actively harming the user journey.

### 5. Monitor viral chain depth

Track multi-generational invite chains. Using `posthog-custom-events`, aggregate:

- Generation 0: organic signups
- Generation 1: users invited by organic users
- Generation 2: users invited by Generation 1 users
- Generation 3+: deeper chains

Healthy viral loops show some generation 2+ activity. If all chains terminate at generation 1, the invited-user-invites-others loop is not working. Feed this signal to the `autonomous-optimization` drill as a specific experiment target: "Improve generation 2+ chain rate from {{current}}% to {{target}}%."

### 6. Build the weekly health report

Using `n8n-scheduling`, create a weekly report (Mondays 9 AM):

1. Pull all invite health metrics for the week
2. Compare to prior week and to 4-week average
3. Generate a structured report:
   - **Status:** HEALTHY / WARNING / CRITICAL
   - **Key metrics:** invite rate, acceptance rate, k-value, each with trend arrows
   - **Anomalies detected this week:** list with causes
   - **Experiments in flight:** any active A/B tests on the invite flow
   - **Recommended actions:** based on the worst-performing metric
4. Store in Attio and post to Slack

This report is the input for the `autonomous-optimization` drill's weekly review cycle.

## Output

- PostHog dashboard with 4 panel groups covering top-level metrics, trends, funnel, and segments
- Anomaly detection running every 6 hours via n8n
- Invited-user retention comparison (invited vs organic)
- Viral chain depth tracking
- Weekly health report posted to Slack and stored in Attio

## Triggers

Runs continuously at Durable level. Anomaly detection every 6 hours. Full health report weekly. Recalibrate thresholds quarterly based on actual performance data.
