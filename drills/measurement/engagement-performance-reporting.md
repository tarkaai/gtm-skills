---
name: engagement-performance-reporting
description: Generate weekly and monthly reports on comment-to-DM play performance with content-to-pipeline attribution
category: Measurement
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

# Engagement Performance Reporting

This drill builds the reporting system for the comment-to-DM play, tracking the full funnel from comments through DMs to meetings booked. It answers: which prospects are moving through the cadence, what comment strategies work best, and is the play producing pipeline?

## Input

- PostHog with comment-to-DM events flowing (from `posthog-gtm-events` drill)
- Attio with prospect records tracking cadence stages (from `comment-to-dm-cadence` drill)
- At least 2 weeks of activity data

## Steps

### 1. Define the report structure

**Weekly Report (generated every Monday):**
- Comments posted this week (count, by prospect tier)
- Author replies received (count, reply rate)
- Prospects advanced to DM-ready stage
- DMs sent and DM reply rate
- Meetings booked from DMs
- Pipeline created from comment-to-DM activity

**Monthly Report (generated first Monday of each month):**
- Full funnel conversion: comments -> author replies -> DM-ready -> DM sent -> DM reply -> meeting -> deal
- Average touches to DM-ready (by prospect tier)
- Average days from first comment to meeting booked
- Best-performing comment strategies (which strategy type produces the most author replies)
- Best-performing post topics (which topics lead to the most DM conversions)
- Prospect tier analysis: which tier converts best and at what cost (time per meeting)

### 2. Build the PostHog dashboard

Using the `posthog-dashboards` fundamental, create a "Comment-to-DM Performance" dashboard:

**Panel 1 -- Weekly Activity:**
- Trend: comments_posted per week
- Trend: author_replies_received per week
- Trend: dms_sent per week

**Panel 2 -- Conversion Funnel:**
- Funnel: comment_posted -> author_reply_received -> dm_sent -> dm_reply_received -> meeting_booked
- Break down by prospect_tier (Tier 1, 2, 3)

**Panel 3 -- Comment Strategy Analysis:**
- Bar chart: author_reply_rate by comment_strategy (add_value, counterpoint, sharp_question, personal_story)
- Bar chart: dm_conversion_rate by comment_strategy

**Panel 4 -- Pipeline Attribution:**
- Number: total meetings booked this month from comment-to-DM
- Number: total pipeline value attributed to comment-to-DM
- Trend: meetings booked per week (4-week rolling)

### 3. Build the Attio report queries

Using the `attio-reporting` fundamental, create saved views in Attio:

**"Active Comment-to-DM Prospects" view:**
- Filter: comment_dm_stage IN (warming, warm, dm-ready, dm_sent, conversation)
- Columns: name, company, tier, stage, touch_count, last_comment_date, days_in_stage

**"Comment-to-DM Pipeline" view:**
- Filter: lead_source = "comment-to-dm" AND deal_stage != "lost"
- Columns: contact_name, company, deal_value, days_from_first_comment, current_deal_stage

**"Stalled Prospects" view:**
- Filter: comment_dm_stage IN (warming, warm) AND last_comment_date > 14 days ago
- This surfaces prospects you have not engaged with recently

### 4. Automate report generation

Using the `n8n-scheduling` fundamental, build an n8n workflow:

1. **Trigger**: Weekly cron every Monday at 9am
2. **Pull PostHog data**: Query the dashboard API for last 7 days of metrics
3. **Pull Attio data**: Query prospect counts by stage, new meetings booked, pipeline created
4. **Calculate derived metrics**: reply rate, conversion rate, average touches to DM-ready
5. **Generate report text**: Format as a concise summary with key numbers, trends (up/down vs last week), and recommended actions
6. **Deliver**: Post to Slack channel and/or send via email

### 5. Define alert thresholds

Set alerts that fire when metrics deviate from expectations:

- **Comment volume drops**: If fewer than 15 comments posted in a week (engagement cadence breaking down)
- **Reply rate drops**: If author reply rate falls below 10% for 2 consecutive weeks (comment quality issue)
- **DM reply rate drops**: If DM reply rate falls below 30% for 2 consecutive weeks (timing or messaging issue)
- **Pipeline stall**: If zero meetings booked in 2 consecutive weeks (cadence or volume problem)

Route alerts to Slack with recommended diagnostic actions.

## Output

- Weekly performance report delivered every Monday
- Monthly deep-dive report delivered first Monday of each month
- Real-time PostHog dashboard for on-demand monitoring
- Automated alerts when metrics breach thresholds
- Attio saved views for prospect pipeline management

## Triggers

Weekly reports fire automatically via n8n cron. Monthly reports fire on the first Monday of each month. Dashboard is always-on and refreshes with live data. Alert thresholds are checked daily via n8n.
