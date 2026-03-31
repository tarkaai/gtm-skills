---
name: social-content-performance-monitor
description: Continuous monitoring and reporting system for founder social content performance with anomaly detection and content-to-pipeline attribution
category: Analytics
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - linkedin-organic-analytics
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Social Content Performance Monitor

This drill builds the always-on monitoring and reporting system specific to founder social content plays. It tracks the full funnel from post published to pipeline created, detects anomalies in content performance, and generates weekly reports that feed into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog with social content events flowing (from `posthog-gtm-events` drill)
- Attio with lead records attributed to social content
- At least 4 weeks of Scalable-level content data (baseline for anomaly detection)
- n8n instance for automated monitoring

## Steps

### 1. Build the Founder Content Performance Dashboard

Using the `posthog-dashboards` fundamental, create a "Founder Social Content" dashboard:

**Panel 1 -- Publishing Cadence:**
- Trend: posts published per week by platform (LinkedIn, Twitter/X)
- Trend: posts published by content pillar
- Target overlay: minimum 7 posts/week across platforms

**Panel 2 -- Engagement Health:**
- Trend: average engagement rate per post (4-week rolling, by platform)
- Trend: average impressions per post (4-week rolling)
- Trend: follower growth rate (weekly net new followers)
- Bar chart: engagement rate by content pillar (which topics resonate)
- Bar chart: engagement rate by format (list, story, contrarian, how-to)

**Panel 3 -- Lead Generation Funnel:**
- Funnel: post_published -> engagement_received -> profile_visit -> dm_received -> lead_captured -> meeting_booked
- Trend: leads generated per week from social content
- Trend: meetings booked per week from social content
- Conversion rate: engagements to leads (weekly)

**Panel 4 -- Content-to-Pipeline Attribution:**
- Number: total pipeline value attributed to social content this month
- Trend: pipeline value attributed per week (8-week rolling)
- Table: top 10 posts by leads generated (post URL, pillar, format, leads, meetings)

**Panel 5 -- Efficiency:**
- Number: founder time spent on content this week (logged manually or via time tracking)
- Calculated: leads per hour of founder time
- Calculated: pipeline value per hour of founder time

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set up monitoring for these signals:

**Engagement anomalies (check daily):**
- Average engagement rate drops >25% vs 4-week rolling average -> trigger: "engagement-decline"
- Average impressions per post drops >30% vs 4-week rolling average -> trigger: "reach-decline"
- Zero DMs received in 7 days (when baseline is 2+/week) -> trigger: "dm-drought"

**Lead anomalies (check daily):**
- Zero leads captured in 7 days (when baseline is 3+/week) -> trigger: "lead-drought"
- Lead-to-meeting conversion drops below 20% for 2 consecutive weeks -> trigger: "conversion-decline"

**Growth anomalies (check weekly):**
- Follower growth rate drops to zero or negative -> trigger: "growth-stall"
- Follower unfollows spike >3x average -> trigger: "audience-churn"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 3. Build the content attribution system

Track the complete journey from content to revenue:

Using `posthog-custom-events` and `posthog-funnels`, implement these attribution events:

1. `social_post_published` — properties: platform, pillar, format, hook_type, post_url, scheduled_time
2. `social_post_engagement` — properties: platform, post_url, likes, comments, shares, impressions (collected 48h after publish)
3. `social_profile_visit` — properties: platform, visitor_title, visitor_company (from Taplio/Shield)
4. `social_dm_received` — properties: platform, sender_title, sender_company, buying_signal (true/false)
5. `social_lead_captured` — properties: platform, source_post_url, lead_title, lead_company, signal_type
6. `social_meeting_booked` — properties: lead_name, source_post_url, days_from_engagement_to_meeting
7. `social_deal_created` — properties: lead_name, deal_value, source_post_url, days_from_first_touch

Build a PostHog funnel from events 1-7 to visualize full-funnel conversion. Break down by content pillar to answer: "Which topics produce the most revenue, not just the most likes?"

### 4. Automate weekly performance reports

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly report workflow:

**Trigger:** Monday at 9am

**Data collection:**
1. Pull last 7 days of social content events from PostHog API
2. Pull lead and meeting data from Attio using `attio-reporting`
3. Pull engagement metrics from Taplio/Shield using `linkedin-organic-analytics`

**Report generation:**
Use Claude API to generate a narrative report from the data:

```
Prompt: "You are analyzing a founder's social content performance for the past week. Here is the data: {DATA}. Compare to the 4-week rolling average: {BASELINE}. Generate a report with:
1. Executive summary (2 sentences: what's working, what's not)
2. Key metrics table (this week vs last week vs 4-week avg)
3. Top performing posts (top 3 by engagement, top 3 by leads)
4. Underperforming areas (anything trending down for 2+ weeks)
5. Recommended experiments (1-2 specific tests to run next week)
Keep it under 500 words. Use specific numbers, not vague language."
```

**Delivery:**
- Post to Slack channel
- Store in Attio as a note on the social content campaign record
- If any anomaly was detected this week, add a section: "ANOMALY DETECTED: {type} — recommended action: {action}"

### 5. Build monthly deep-dive reports

Using the same n8n infrastructure, build a monthly report that runs on the first Monday:

**Additional monthly metrics:**
- Content pillar performance ranking (which pillars to keep, which to retire)
- Format performance ranking (which formats to double down on)
- Audience evolution: are follower demographics shifting toward or away from ICP?
- Content-to-pipeline: total pipeline value attributed to social content this month
- Efficiency trend: leads per hour of founder time vs previous months
- Experiment results: which optimization experiments ran, what was learned

### 6. Set up alert routing

Build n8n alert workflows for critical events:

- **Immediate Slack alert**: When a post exceeds 3x average engagement (opportunity to ride the wave with engagement and DM follow-ups)
- **Daily digest**: Summary of leads captured and meetings booked from social content
- **Weekly flag**: If no experiments are running for 2+ weeks (optimization stall — the `autonomous-optimization` drill should always have something in flight)

## Output

- Real-time PostHog dashboard with 5 panels covering publishing, engagement, leads, pipeline, and efficiency
- Anomaly detection feeding into autonomous optimization loop
- Full content-to-pipeline attribution tracking
- Automated weekly and monthly performance reports
- Alert routing for opportunities and issues

## Triggers

Dashboard is always-on. Anomaly detection runs daily via n8n. Weekly reports fire every Monday at 9am. Monthly reports fire first Monday of each month. Alerts fire in real-time via webhooks and daily digests.
