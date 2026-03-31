---
name: onboarding-health-monitor
description: Continuously monitor onboarding funnel health, detect degradation, and generate weekly activation reports
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-dashboards
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Onboarding Health Monitor

This drill creates an always-on monitoring system for onboarding funnel performance. It runs daily checks, detects degradation before it becomes a crisis, and generates weekly reports with actionable insights. This is the play-specific monitoring layer that feeds into the `autonomous-optimization` drill at the Durable level.

## Prerequisites

- PostHog tracking all onboarding events (from `posthog-gtm-events` drill)
- At least 4 weeks of onboarding data at Scalable level
- n8n instance with PostHog and Slack/email credentials
- Onboarding funnels defined in PostHog

## Steps

### 1. Define the health metrics

Track these metrics daily:

- **Overall activation rate**: Percentage of signups reaching activation within 7 days (trailing 7-day cohort)
- **Tour completion rate**: Percentage of users who start the tour and complete all steps
- **Time to activation**: Median time from signup to activation event (in hours)
- **Step drop-off rates**: Conversion rate between each onboarding funnel step
- **Per-persona activation rate**: Activation rate broken down by persona segment
- **Email sequence engagement**: Open rate and click rate for each onboarding email
- **Stalled user count**: Users who signed up 3+ days ago with no milestone progress

### 2. Build the monitoring dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "Onboarding Health" dashboard:

- **Row 1**: Activation rate trend (30-day line chart), tour completion rate trend, time-to-activation trend
- **Row 2**: Onboarding funnel (bar chart showing step-by-step conversion), per-persona activation comparison
- **Row 3**: Email sequence performance (open/click rates by email step), stalled user count trend

Set each metric's expected range based on the last 4 weeks of Scalable-level performance. Color-code: green = within 5% of baseline, yellow = 5-15% below baseline, red = more than 15% below baseline.

### 3. Build the daily health check workflow

Using the `n8n-scheduling` fundamental, create a workflow that runs daily at 09:00 UTC:

1. Query PostHog for yesterday's onboarding metrics using the API:
   - Activation rate for the 7-day cohort ending yesterday
   - Tour starts and completions in the last 24 hours
   - New signups vs activations ratio
   - Any step with conversion below 50% of its 4-week average

2. Run anomaly detection using `posthog-anomaly-detection`:
   - Compare each metric to its 4-week rolling average
   - Flag any metric that has declined for 3+ consecutive days
   - Flag any single-day drop exceeding 25%

3. If anomalies detected:
   - Send an immediate alert to Slack with: metric name, current value, baseline value, percentage change, and the number of consecutive days declining
   - Log the anomaly in Attio using `attio-notes` on the play's campaign record

4. If no anomalies: log a "healthy" entry. No alert needed.

### 4. Build the stalled-user intervention trigger

Using `n8n-workflow-basics`, create a workflow that runs daily:

1. Query PostHog using `posthog-cohorts` for users matching: `signup_date > 3 days ago AND activation_reached = false AND last_tour_step < total_tour_steps`
2. For each stalled user, determine where they are stuck (which milestone they last completed)
3. Group stalled users by stuck-point and persona
4. Output a daily stalled-user report: "12 users stalled at step 3 (mostly team_lead persona), 8 users stalled at step 1 (mostly solo_creator)"
5. Feed this data into the `autonomous-optimization` drill as a signal for hypothesis generation

### 5. Generate the weekly activation report

Using `n8n-scheduling`, create a workflow that runs every Monday at 10:00 UTC:

1. Pull 7-day metrics from PostHog:
   - Total signups, total activations, activation rate
   - Tour completion rate and average time-to-activation
   - Per-persona breakdown
   - Email sequence metrics (enrollments, opens, clicks, activations attributed to email)
   - Comparison to prior week and 4-week average

2. Generate the report using Claude (Anthropic API):
   - "Onboarding Health Report — Week of [date]"
   - Summary: 1-2 sentences on overall health
   - Key metrics table with week-over-week change
   - Top insight: the single most important finding this week
   - Recommended action: one specific thing to test or fix
   - Stalled user analysis: where users are getting stuck and any emerging patterns

3. Post the report to Slack and store in Attio

### 6. Set up guardrail alerts

Using `n8n-workflow-basics`, create always-on guardrails:

- **Activation crash**: If activation rate drops below 25% for any 48-hour period, send an urgent alert. This likely indicates a product bug, broken tour, or tracking failure.
- **Tour breakage**: If tour completion rate drops below 10%, the tour itself may be broken (e.g., targeting a DOM element that no longer exists after a product deploy). Alert immediately.
- **Email bounce spike**: If Loops reports bounce rate above 5%, the email sequence may be targeting invalid addresses. Pause new enrollments and investigate.

## Output

- Daily automated health checks with anomaly detection
- Weekly activation reports with insights and recommendations
- Stalled-user analysis feeding into the optimization loop
- Guardrail alerts for critical failures
- All data logged in Attio for audit trail
