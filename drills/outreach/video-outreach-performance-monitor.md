---
name: video-outreach-performance-monitor
description: Monitor and report on personalized video outreach performance with video-specific metrics and funnel analysis
category: Outreach
tools:
  - PostHog
  - Attio
  - Loom
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - posthog-funnels
  - attio-reporting
  - loom-analytics
  - n8n-scheduling
  - n8n-workflow-basics
---

# Video Outreach Performance Monitor

This drill builds the monitoring, reporting, and alerting layer for personalized video outreach plays. It tracks video-specific metrics (watch rate, completion rate, CTA clicks) alongside standard outreach metrics (reply rate, meeting rate) to give a complete picture of the video outreach funnel. This is the primary data input for the `autonomous-optimization` drill at Durable level.

## Input

- Active video outreach campaigns (from `video-prospecting-outreach` drill)
- PostHog tracking configured with video events (from `posthog-gtm-events` drill)
- Attio with deal pipeline tracking
- Loom Business account with analytics
- At least 2 weeks of video outreach data

## Steps

### 1. Define the video outreach event taxonomy

Using `posthog-custom-events`, verify these events are firing correctly:

**Video-specific events:**
- `video_email_sent` -- properties: campaign_id, prospect_tier, loom_video_id, personalization_level (full/segment/generic)
- `video_email_opened` -- properties: campaign_id, open_count
- `video_thumbnail_clicked` -- properties: campaign_id, prospect_email, time_since_send
- `video_viewed` -- properties: campaign_id, prospect_email, loom_video_id, watch_percentage, cta_clicked
- `video_cta_clicked` -- properties: campaign_id, prospect_email, cta_type (book_meeting/learn_more)

**Outreach events:**
- `video_email_replied` -- properties: campaign_id, sentiment, sequence_step
- `video_meeting_booked` -- properties: campaign_id, source (cta_click/email_reply/direct), prospect_tier
- `video_deal_created` -- properties: campaign_id, deal_value, prospect_tier

### 2. Build the video outreach dashboard

Using the `posthog-dashboards` fundamental, create a dashboard named "Video Outreach -- Performance" with these panels:

**Row 1 -- Volume & Reach:**
- Videos recorded this week (count of `video_email_sent` events)
- Video emails delivered (sent minus bounced)
- Open rate trend (weekly line chart)

**Row 2 -- Video Engagement Funnel:**
- Full funnel: email_sent -> email_opened -> thumbnail_clicked -> video_viewed -> cta_clicked -> meeting_booked
- Conversion rate at each step with week-over-week comparison
- Average watch percentage distribution (histogram: 0-25%, 25-50%, 50-75%, 75-100%)

**Row 3 -- Video vs Text Comparison (if running both):**
- Reply rate: video emails vs text-only emails
- Meeting rate: video path vs text path
- Time to meeting: video vs text
- Cost per meeting: video vs text

**Row 4 -- Engagement Quality:**
- Watch rate by prospect tier (do high-priority prospects watch more?)
- Watch rate by ICP segment (which segments respond to video?)
- Watch rate by day of week and time of send
- CTA click rate by video length bucket

**Row 5 -- Pipeline Impact:**
- Total meetings booked from video outreach this month
- Pipeline value created from video outreach
- Video cost per meeting (Loom subscription / meetings booked)
- Average deal size from video-sourced vs text-sourced deals

Add threshold indicators: green if meeting rate >=10% of videos sent, yellow if 5-10%, red if <5%.

### 3. Configure anomaly detection

Using `posthog-anomaly-detection`, set alerts for:

- Video completion rate drops below 10% for 5 consecutive days (videos are not engaging)
- Thumbnail click rate drops below 5% for 1 week (email copy or thumbnail not compelling)
- Meeting booking rate drops to 0 for 7+ days
- Email bounce rate exceeds 3% (domain health issue)
- Negative reply rate exceeds 5% (messaging or targeting problem)
- Video view count drops 50%+ week over week (deliverability issue or audience fatigue)

Route all alerts to Slack and log as Attio campaign notes.

### 4. Build the weekly video outreach brief

Using `n8n-scheduling`, create a workflow that runs every Monday at 8am:

1. Pull last 7 days of video outreach events from PostHog
2. Pull Loom analytics using `loom-analytics` for video-level engagement data
3. Pull Attio deal data using `attio-reporting` for pipeline from video outreach
4. Calculate video-specific metrics:
   - Videos sent, videos watched, completion rate, CTA click rate
   - Watch-to-reply ratio (do watched videos lead to replies?)
   - Watch-to-meeting ratio (the core conversion metric)
   - Average recording time per video (efficiency metric)
5. Calculate effectiveness metrics:
   - Best-performing video scripts (which opening hooks get highest completion?)
   - Best-performing ICP segments for video (which personas respond?)
   - Optimal video length (what duration maximizes meetings?)
   - Best send time for video emails
6. Compare this week vs 4-week rolling average
7. Generate the weekly brief:
   - Video funnel metrics with week-over-week delta
   - Top 3 best-performing videos this week (by meeting conversion)
   - Script pattern analysis (what do winning videos have in common?)
   - Recommendations: adjust video length, change opening hook, shift ICP focus
8. Post to Slack and store in Attio

### 5. Build the A/B test results tracker

Track ongoing experiments specific to video outreach:

- Subject line variants (e.g., "Quick video for you" vs "{first_name}, 60 seconds for you")
- Video length variants (60s vs 90s vs 120s)
- GIF thumbnail vs static image thumbnail
- Camera + screen vs camera only
- CTA placement (end only vs mid + end)

For each active experiment, display current results on the dashboard: variant, sample size, conversion rate, confidence level, estimated days to significance.

### 6. Feed data to the optimization loop

Ensure all metrics, anomalies, and weekly summaries fire structured PostHog events:

- `video_outreach_weekly_summary` -- properties: all computed metrics as key-value pairs
- `video_outreach_anomaly` -- properties: anomaly_type, metric_value, threshold_value, severity
- `video_outreach_experiment_result` -- properties: experiment_id, winner, confidence, effect_size

These events are consumed by the `autonomous-optimization` drill to generate hypotheses and design experiments.

## Output

- Live PostHog dashboard with real-time video outreach funnel metrics
- Weekly automated briefs with video-specific performance analysis
- Anomaly alerts catching engagement degradation early
- A/B test tracking for continuous video optimization
- Structured data feed for the autonomous optimization loop

## Triggers

Dashboard refreshes with live data. Weekly briefs fire every Monday. Anomaly checks run daily. Experiment tracking updates with each new data point.
