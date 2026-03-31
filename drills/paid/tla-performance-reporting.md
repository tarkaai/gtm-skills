---
name: tla-performance-reporting
description: Build dashboards and automated reports tracking Thought Leader Ad performance across content, audience, and pipeline metrics
category: Paid
tools:
  - PostHog
  - LinkedIn Ads
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-custom-events
  - linkedin-ads-measurement
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# TLA Performance Reporting

This drill builds the reporting infrastructure that feeds the `autonomous-optimization` drill for Thought Leader Ads at the Durable level. It tracks three layers: content performance (which posts and formats work), audience performance (which segments convert), and pipeline performance (which TLA touches drive revenue).

## Prerequisites

- TLA campaigns running at Scalable level for at least 4 weeks
- PostHog tracking TLA events (`tla_click`, `tla_engagement`, `tla_conversion`)
- Attio CRM with TLA-sourced contacts and deals
- n8n instance for automated report generation

## Input

- 4+ weeks of TLA campaign data from LinkedIn Campaign Manager
- PostHog event data for TLA-attributed website traffic
- Attio deal data for TLA-sourced pipeline

## Steps

### 1. Build the PostHog TLA Dashboard

Using `posthog-dashboards`, create a dashboard with 8 panels:

**Panel 1 -- TLA Spend & Reach (weekly trend):**
- Metrics: weekly ad spend, impressions, unique reach
- Source: LinkedIn Marketing API data synced via n8n
- Purpose: track spend efficiency over time

**Panel 2 -- Engagement by Post (last 30 days):**
- Metrics: per-post engagement rate, likes, comments, shares
- Breakdown: by post_id and thought_leader
- Purpose: identify which posts and thought leaders drive engagement

**Panel 3 -- CPC Trend (weekly):**
- Metrics: average CPC, CPC by audience segment
- Benchmarks: overlay target CPC line ($2-5 range)
- Purpose: detect cost creep or efficiency gains

**Panel 4 -- Audience Segment Comparison:**
- Metrics: CTR, CPC, conversions by audience segment
- Breakdown: Core ICP vs Adjacent ICP vs Retargeting
- Purpose: inform budget reallocation across segments

**Panel 5 -- Content Format Performance:**
- Metrics: engagement rate and CPC by post format (text, image, video, carousel)
- Purpose: guide content production toward highest-performing formats

**Panel 6 -- Hook Type Analysis:**
- Metrics: engagement rate by hook type (question, stat, story, contrarian)
- Source: `hook_type` property on `tla_engagement` events
- Purpose: inform the content production templates

**Panel 7 -- Conversion Funnel:**
Using `posthog-funnels`, build:
`tla_impression` > `tla_click` > `page_view` > `form_submit` > `demo_booked`
- Breakdown: by audience segment and thought leader
- Purpose: identify where prospects drop off

**Panel 8 -- Pipeline Attribution:**
- Metrics: TLA-sourced contacts, deals created, pipeline value, deals won
- Source: Attio CRM data synced via n8n
- Purpose: connect ad spend to revenue

### 2. Build Attio Saved Views

Using `attio-reporting`, create saved views:

**View 1 -- TLA-Sourced Contacts:**
- Filter: `source = tla`
- Columns: name, company, title, lead_score, thought_leader, post_id, created_date
- Sort: created_date descending

**View 2 -- TLA Pipeline:**
- Filter: deals where contact source = tla
- Columns: deal name, company, stage, value, days_in_stage, thought_leader
- Sort: created_date descending

**View 3 -- TLA ROI by Thought Leader:**
- Group by: thought_leader
- Metrics: contacts created, deals created, pipeline value, deals won, revenue

### 3. Build the Weekly Automated Report

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs every Monday at 8am:

1. **Pull LinkedIn Ads data** via Marketing API: spend, impressions, clicks, engagement actions for the last 7 days
2. **Pull PostHog data** via API: TLA funnel conversion rates, per-post engagement, audience segment performance
3. **Pull Attio data** via API: new TLA-sourced contacts, deals created, pipeline changes
4. **Calculate derived metrics:**
   - Cost per engagement (spend / total social actions)
   - Cost per qualified lead (spend / leads with score >= 70)
   - Content velocity (posts promoted this week vs last week)
   - Audience fatigue index (average frequency across segments)
   - Blended CPA (spend / total conversions)
5. **Generate report** using Claude:
   ```
   Summarize this week's TLA performance in 5 bullet points:
   - Overall: spend, reach, CPC trend (up/down/stable vs last week)
   - Best performer: which post and why
   - Audience insight: which segment is winning and losing
   - Pipeline: new contacts, deals, revenue attributed
   - Action items: what to change next week based on data
   ```
6. **Post to Slack** and **store in Attio** as a note on the TLA campaign record

### 4. Build the Monthly ROI Report

Using `n8n-scheduling`, create a monthly workflow:

1. Aggregate 4 weeks of weekly data
2. Calculate:
   - Total TLA spend
   - Total pipeline generated (TLA-sourced deal value)
   - TLA-influenced pipeline (deals where TLA was a touchpoint but not first touch)
   - ROAS: pipeline / spend (target: 5x+ for B2B)
   - Revenue closed from TLA-sourced deals
   - Customer acquisition cost from TLA channel
3. Compare to other paid channels (if running Google, Meta, etc.)
4. Trend analysis: is TLA ROAS improving, stable, or declining month-over-month?
5. Generate a monthly executive summary and post to Slack

### 5. Set Up Anomaly Alerts

Using `posthog-custom-events` and `n8n-workflow-basics`, configure real-time alerts:

- **CPC spike:** If daily CPC exceeds 2x the 14-day average, alert via Slack
- **Engagement drop:** If weekly engagement rate drops below 1% (TLA benchmark is 1.5-3%), alert
- **Zero conversions:** If 3+ consecutive days with spend but zero conversions, alert
- **Budget runaway:** If daily spend exceeds 150% of the daily budget setting, alert
- **Audience fatigue:** If average frequency for any segment exceeds 5 per week, alert

These alerts serve as the monitoring substrate for the `autonomous-optimization` drill at the Durable level.

## Output

- PostHog dashboard with 8 panels covering content, audience, and pipeline performance
- 3 Attio saved views for TLA contact and pipeline management
- Weekly automated report delivered to Slack every Monday
- Monthly ROI report with cross-channel comparison
- 5 real-time anomaly alerts configured in n8n

## Triggers

- Dashboard: refreshes automatically in PostHog
- Weekly report: every Monday at 8am via n8n
- Monthly report: first Monday of each month via n8n
- Anomaly alerts: real-time via n8n
