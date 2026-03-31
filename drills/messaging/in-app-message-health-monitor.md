---
name: in-app-message-health-monitor
description: Monitor in-app message fatigue, delivery rates, engagement decay, and trigger rotation to maintain campaign health
category: Messaging
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-user-properties
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# In-App Message Health Monitor

This drill builds a monitoring layer that detects when in-app messaging campaigns degrade: engagement rates decay, users develop message fatigue, delivery rates drop, or specific segments stop responding. It triggers alerts and automated corrective actions before campaign performance collapses.

## Input

- Intercom in-app messaging configured with behavioral triggers
- PostHog tracking message impressions, clicks, dismissals, and downstream conversions
- n8n instance for scheduled monitoring workflows
- At least 14 days of message performance data

## Steps

### 1. Define message health metrics

Using the `posthog-custom-events` fundamental, ensure these events are tracked for every in-app message:

- `in_app_message_delivered` — message was rendered in the UI
- `in_app_message_seen` — message was visible in viewport for 2+ seconds
- `in_app_message_clicked` — user clicked the CTA
- `in_app_message_dismissed` — user explicitly closed the message
- `in_app_message_ignored` — message was delivered but neither clicked nor dismissed within the session
- `in_app_message_converted` — user completed the desired action within 24 hours of clicking

Properties on each event: `message_id`, `campaign_slug`, `segment`, `message_variant`, `trigger_type` (behavioral, time-based, threshold).

Calculate derived health metrics:
- **Delivery rate**: delivered / eligible users (target: >90%, below 80% indicates targeting issues)
- **Visibility rate**: seen / delivered (target: >70%, below 50% indicates placement problems)
- **Engagement rate**: clicked / seen (target: >15%, below 8% indicates copy or relevance issues)
- **Dismissal rate**: dismissed / seen (target: <30%, above 50% indicates fatigue)
- **Conversion rate**: converted / clicked (target: >25%, below 10% indicates broken flow)
- **Fatigue index**: dismissals per user over trailing 14 days (target: <3, above 5 means throttle)

### 2. Build the message health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Engagement rate by campaign (7-day trend) | Line chart | Spot engagement decay early |
| Dismissal rate by campaign (7-day trend) | Line chart | Detect rising fatigue |
| Conversion rate by campaign | Bar chart | Which campaigns actually drive action |
| Fatigue index distribution | Histogram | How many users are over-messaged |
| Delivery rate by segment | Table | Which segments have delivery problems |
| Message performance heatmap | Heatmap (day x campaign) | Cross-campaign view of daily health |
| Engagement by trigger type | Bar chart | Which trigger types produce the best results |

### 3. Create fatigue detection and throttling

Using `posthog-cohorts`, build a "fatigued users" cohort: users who dismissed 3+ in-app messages in the last 14 days OR who have not clicked any in-app message in 30+ days despite receiving 5+.

Using `intercom-user-properties`, sync the fatigue flag to Intercom so fatigued users are automatically excluded from non-critical messages. Only high-priority messages (account health alerts, critical product changes) should reach fatigued users.

Using `n8n-triggers`, build a workflow that runs daily:
1. Query PostHog for the fatigued users cohort
2. Update Intercom user property `message_fatigue = true` for fatigued users
3. Clear the flag for users whose fatigue index drops below 2 (they re-engaged)
4. Log the fatigue cohort size trend in Attio using `attio-notes`

### 4. Build engagement decay alerting

Using `n8n-scheduling`, create a workflow that runs every 3 days:

1. For each active campaign, pull the last 14 days of engagement data from PostHog
2. Compare week-over-week engagement rate:
   - **Stable** (within ±5%): no action
   - **Declining** (>10% drop for 2 consecutive checks): alert via Slack, suggest copy refresh or segment review
   - **Collapsing** (>25% drop or engagement below 8%): pause the campaign automatically via Intercom API, create an Attio task for campaign review
3. For new campaigns (< 14 days old), compare against the portfolio average engagement rate instead of historical self

### 5. Implement message rotation logic

When a campaign's engagement decays past the alert threshold, the agent should:

1. Check if alternate message variants exist for this campaign
2. If variants exist: rotate to the next variant via `intercom-in-app-messages` and reset the decay tracking window
3. If no variants exist: flag for new copy creation and reduce message frequency by 50% in the interim
4. Track how many rotations each campaign has been through — if 3+ variants all decay, the campaign concept is exhausted and should be retired

### 6. Generate weekly message health reports

Using the `n8n-scheduling` fundamental, schedule a weekly report that aggregates:

- Total messages delivered, seen, clicked, and converted this week
- Top 3 performing campaigns by conversion rate
- Bottom 3 campaigns by engagement (candidates for refresh or retirement)
- Fatigue cohort trend (growing or shrinking)
- Recommendations: which campaigns to refresh, which to retire, which segments to exclude
- Estimated revenue or retention impact of messaging (conversion rate x average account value)

Store in Attio and deliver via Slack.

## Output

- Message health dashboard in PostHog with 7 panels
- Fatigue detection and Intercom throttling workflow in n8n (daily)
- Engagement decay alerting workflow in n8n (every 3 days)
- Message rotation logic for decaying campaigns
- Weekly message health report

## Triggers

- Fatigue detection: daily via n8n cron
- Engagement decay check: every 3 days via n8n cron
- Weekly health report: Monday 9am via n8n cron
- Re-run full setup when adding new campaign types or changing message placement strategy
