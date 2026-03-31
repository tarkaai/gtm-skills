---
name: email-subject-performance-monitor
description: Track email subject-line test results over time, detect declining open rates, and surface winning patterns
category: Product
tools:
  - PostHog
  - Loops
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - loops-audience
  - n8n-scheduling
  - n8n-workflow-basics
---

# Email Subject Performance Monitor

This drill builds always-on monitoring for email subject-line performance across all lifecycle campaigns. It detects open-rate declines, surfaces winning subject-line patterns, and generates weekly performance reports.

## Input

- PostHog tracking configured for email subject tests (events: `email_subject_test_sent`, `email_subject_test_opened`, etc.)
- At least 4 weeks of subject-line test history
- Active Loops sequences and broadcasts

## Steps

### 1. Build the email subject performance dashboard

Using the `posthog-dashboards` fundamental, create a dedicated dashboard with these panels:

- **Open rate trend (8 weeks):** Line chart showing weekly average open rate across all retention emails. Add a threshold line at your target open rate.
- **Open rate by email type:** Bar chart breaking down open rate by email category (re-engagement, feature announcement, renewal, usage update, etc.)
- **Test velocity:** Count of subject-line tests completed per week
- **Winning patterns log:** Table of the last 10 test results showing control subject, variant subject, winner, and lift

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set up checks on the aggregate open rate:

- **Drop alert:** Open rate falls >15% below the 4-week rolling average for 2 consecutive sends
- **Fatigue signal:** Open rate declines 3+ weeks in a row, even if each decline is <5%
- **Deliverability flag:** Open rate drops below 15% on any single send (likely a deliverability issue, not a subject-line issue)

### 3. Build automated monitoring workflow

Using the `n8n-scheduling` fundamental, create a weekly cron workflow (Monday 9am):

1. Query PostHog for all email sends from the past 7 days using `posthog-custom-events`
2. Compute: open rate per email, open rate per sequence, aggregate open rate
3. Compare each to the 4-week rolling average
4. Flag any email with open rate >10% below its historical average
5. Compile findings into a structured report

### 4. Generate the weekly subject-line brief

The n8n workflow produces a weekly report:

```
Subject-Line Performance Brief — Week of {date}
- Emails sent: {count}
- Aggregate open rate: {rate}% (vs {rolling_avg}% 4-week avg)
- Tests completed: {count}
- Tests won (variant beat control): {count}
- Best performing subject: "{subject}" — {open_rate}% open rate
- Worst performing subject: "{subject}" — {open_rate}% open rate
- Pattern insights: {top patterns that consistently win}
- Flagged emails: {list of emails with declining opens}
```

Post to Slack and store in Attio as a note on the email-subject-testing campaign record.

### 5. Maintain the subject-line pattern library

After each test, log the result in a structured format:

- Test date
- Email type (re-engagement, feature, renewal, usage)
- Control subject
- Variant subject
- Variant framing category (personalization, curiosity, social proof, value, urgency)
- Open rate: control vs. variant
- Winner
- Lift (percentage points)

Query this library monthly to identify durable patterns: which framing categories consistently win for which email types. Feed these patterns back into `email-subject-test-pipeline` to generate higher-quality variants.

## Output

- PostHog dashboard tracking open rates across all retention emails
- Weekly automated performance brief
- Subject-line pattern library with proven winners by email type
- Anomaly alerts for open-rate drops

## Triggers

Runs weekly via n8n cron at Baseline level. At Scalable, increase to twice-weekly checks. At Durable, the `autonomous-optimization` drill subsumes this monitoring into its daily loop.
