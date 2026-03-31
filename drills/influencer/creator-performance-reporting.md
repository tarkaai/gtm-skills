---
name: creator-performance-reporting
description: Aggregate creator campaign metrics, compare creator performance, and generate optimization reports
category: Influencer
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
---

# Creator Performance Reporting

This drill builds the reporting layer for micro-influencer campaigns. It answers: which creators drive real leads, what is the true cost per lead across creators, and where should the next dollar go?

## Input

- PostHog with `influencer_lead_captured` and `influencer_meeting_booked` events flowing (from `creator-campaign-execution` drill)
- Attio with creator records tagged with campaign data
- At least 2 completed creator posts with 7+ days of data

## Steps

### 1. Build the PostHog creator performance dashboard

Using the `posthog-dashboards` fundamental, create a "Creator Campaign Performance" dashboard:

**Panel 1 — Campaign Overview:**
- Total UTM-tagged page views where `$utm_medium = influencer` (trend, last 30 days)
- Total `influencer_lead_captured` events (trend, last 30 days)
- Total `influencer_meeting_booked` events (trend, last 30 days)
- Overall funnel: page_view to lead to meeting (conversion rates)

**Panel 2 — Creator Comparison:**
- Bar chart: leads captured per creator (breakdown by `$utm_source`)
- Bar chart: page views per creator (breakdown by `$utm_source`)
- Table: creator handle, page views, leads, conversion rate, CPL (requires manual CPL input or Attio sync)

**Panel 3 — Content Format Analysis:**
- Bar chart: leads by `$utm_content` (linkedin-post, newsletter, youtube, twitter)
- Conversion rate by format
- This tells you which format (not just which creator) drives the best results

**Panel 4 — Time Analysis:**
- Trend: page views per day for the last 30 days, broken down by creator
- Identify how long a creator post drives traffic (most B2B creator posts peak in 24-48 hours on social, but newsletters and YouTube have longer tails)

### 2. Build Attio creator scorecard views

Using the `attio-reporting` fundamental:

**"Creator Scorecard" view:**
- Filter: `creator_status = completed`
- Columns: creator_name, platform, follower_count, post_cost, leads_generated, cpl, conversion_rate, engagement_rate, creator_score
- Sort by: CPL ascending (best value first)

**"Active Campaigns" view:**
- Filter: `creator_status IN (briefed, posted)`
- Columns: creator_name, platform, post_date, days_since_post, leads_so_far

**"Creator Pipeline" view:**
- Filter: `creator_status IN (prospect, outreach_sent, negotiating)`
- Columns: creator_name, platform, creator_tier, estimated_cost, outreach_date, last_activity

### 3. Calculate derived metrics

For each completed creator, compute and store in Attio:

- **CPL (Cost per Lead):** creator_fee / leads_generated
- **CPC (Cost per Click):** creator_fee / total_clicks
- **ROAS estimate:** (leads * average_deal_value * close_rate) / creator_fee
- **Engagement quality score:** (comments + shares) / (likes + views) — higher ratio means more genuine engagement
- **Audience-to-lead ratio:** leads / (creator_follower_count / 1000) — normalizes for audience size

### 4. Automate weekly reporting

Using the `n8n-scheduling` fundamental, build a workflow:

1. **Trigger:** Weekly cron every Monday at 9am
2. **Pull PostHog data:** Query the creator dashboard API for last 7 days
3. **Pull Attio data:** Aggregate creator statuses, new bookings, completed posts, total spend
4. **Compute week-over-week changes:** leads this week vs last week, spend this week vs last week, CPL trend
5. **Generate report:**
   - Top performing creator this week (by CPL)
   - Total leads from creator channel this week
   - CPL vs target (are we above or below the acceptable CPL?)
   - Recommendations: which creators to rebook, which to drop, which new creators to try
6. **Deliver:** Post to Slack and store in Attio as a campaign note

### 5. Set alert thresholds

Configure n8n alerts for:
- **Zero leads from a completed post:** if a post has been live 7+ days and generated 0 leads, flag it. Diagnose: was the tracking link used? Was the post actually published?
- **CPL spike:** if any creator's CPL is >3x the campaign average, flag for review
- **Budget pacing:** if total spend exceeds monthly budget by >10%, pause new bookings

## Output

- Real-time PostHog dashboard comparing creator performance
- Attio scorecard views for creator management
- Weekly automated performance report
- Alert system for anomalies

## Triggers

Dashboard refreshes in real-time. Weekly report fires every Monday. Alerts fire daily when thresholds are breached.
