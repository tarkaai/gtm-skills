---
name: display-performance-reporting
description: Comprehensive reporting on display advertising effectiveness — placement quality, creative health, audience performance, and pipeline attribution
category: Paid
tools:
  - PostHog
  - Google Ads
  - Meta Ads
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - google-ads-display-campaign
  - meta-ads-campaign-setup
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-reporting
  - hypothesis-generation
---

# Display Performance Reporting

This drill builds the reporting infrastructure for display advertising campaigns. It provides the data layer that the `autonomous-optimization` drill reads from at Durable level. Without accurate, granular reporting, the optimization loop cannot generate meaningful hypotheses.

## Prerequisites

- Display campaigns running on GDN and/or Meta Audience Network for at least 4 weeks
- PostHog receiving display ad events with properties: `platform`, `campaign_id`, `ad_group`, `creative_id`, `placement`, `pain_point`
- n8n instance for automated report generation
- Attio CRM with display-sourced leads tagged

## Steps

### 1. Build the PostHog display dashboard

Using `posthog-dashboards`, create a dashboard with 8 panels:

**Panel 1 -- Spend and reach trends (line chart, 90 days)**
- Y-axes: daily spend (left), daily impressions (right), grouped by platform
- Shows budget utilization and reach trajectory

**Panel 2 -- Placement quality matrix (table, 30 days)**
- Columns: placement_domain, impressions, clicks, CTR, conversions, CPA
- Sorted by CPA ascending
- Highlight: placements with CPA below target (green), above 150% target (red)
- Used for weekly placement exclusion decisions

**Panel 3 -- Creative performance (bar chart, 30 days)**
- X-axis: creative_id grouped by pain_point
- Y-axis: CTR and conversion rate side by side
- Color code by creative age (days since launch)
- Used for creative fatigue detection and rotation decisions

**Panel 4 -- Audience segment comparison (bar chart, 30 days)**
- X-axis: audience segment (managed placements, custom intent, retargeting, lookalike, interest)
- Y-axis: CPA and lead quality score side by side
- Used for budget reallocation decisions

**Panel 5 -- Conversion funnel (funnel, 30 days)**
- Steps: display_click > page_view > scroll_50 > form_focus > form_submit > demo_booked
- Filter by platform
- Shows where prospects drop off between ad click and conversion

**Panel 6 -- Lead quality trend (line chart, 90 days)**
- Y-axis: percentage of display leads scoring 70+ in Attio (from Clay ICP scoring)
- Alert threshold: quality drops below 40%
- Correlate with audience segment to identify which segments produce quality leads

**Panel 7 -- Cross-platform CPA trend (line chart, 90 days)**
- Y-axis: cost per qualified lead, grouped by platform
- Includes the 4-week rolling average as a reference line
- Alert threshold: CPA exceeds 150% of rolling average

**Panel 8 -- Pipeline attribution (table, 90 days)**
- Columns: month, display_leads, qualified_leads, meetings_booked, deals_created, pipeline_value
- Shows full-funnel attribution from display ad click to pipeline
- Calculates: ROAS = pipeline_value / ad_spend

### 2. Build Attio saved views

Create 3 saved views in Attio:

1. **Display-sourced contacts:** Filter contacts where `source = display-ads`. Columns: name, company, lead_score, platform, campaign, created_date, current_stage
2. **Display pipeline:** Filter deals where `source = display-ads`. Columns: deal_name, company, value, stage, created_date, days_in_stage
3. **Display ROI by campaign:** Group deals by `campaign` tag. Show: deal count, total pipeline value, average deal value, win rate

### 3. Deploy the weekly automated report

Build an n8n workflow triggered every Monday at 08:00 UTC:

1. Pull 7-day performance data from PostHog across all display campaigns
2. Pull lead and deal data from Attio for the same period
3. Generate the weekly brief using Claude via `hypothesis-generation`:

```
Display Advertising Weekly Brief - Week of {date}

PERFORMANCE SUMMARY:
- Total spend: ${spend} ({change}% vs previous week)
- Impressions: {impressions} ({change}%)
- Clicks: {clicks}, CTR: {ctr}%
- Conversions: {conversions}, CPA: ${cpa} (target: ${target_cpa})
- Qualified leads: {qualified} ({quality_rate}% quality rate)

PLACEMENT HEALTH:
- Top 3 placements by CPA: {list}
- Placements excluded this week: {count}
- New placements discovered: {list}

CREATIVE HEALTH:
- Active creatives: {count}
- Fatigued creatives paused: {count}
- New creatives launched: {count}
- Top performer: {creative_id} — {pain_point} — CTR {ctr}%

AUDIENCE HEALTH:
- Best segment: {segment} — CPA ${cpa}
- Worst segment: {segment} — CPA ${cpa}
- Budget reallocation recommendation: {recommendation}

PIPELINE IMPACT:
- Meetings booked from display leads: {count}
- Pipeline created: ${value}
- Display share of total pipeline: {percentage}%

RECOMMENDED ACTIONS:
{ai_generated_recommendations}
```

4. Post to Slack channel
5. Store in Attio as a note on the display advertising campaign record

### 4. Deploy the monthly ROI report

Build an n8n workflow triggered on the first Monday of each month:

1. Pull 30-day data from PostHog and Attio
2. Calculate:
   - Total display ad spend
   - Total qualified leads generated
   - Cost per qualified lead
   - Meetings booked from display leads
   - Deals created and pipeline value
   - ROAS: pipeline value / ad spend
   - Comparison to other paid channels (if data available)
3. Generate a monthly executive summary via Claude
4. Post to Slack and store in Attio

### 5. Configure real-time anomaly alerts

Using `posthog-anomaly-detection`, set up 5 alerts:

1. **CPA spike:** CPA exceeds 200% of 4-week average for any campaign -> Slack alert + auto-pause if CPA exceeds 300%
2. **CTR collapse:** Campaign-level CTR drops below 0.05% for 3 consecutive days -> Slack alert (possible placement quality issue)
3. **Zero conversions:** Any campaign with $100+ daily spend produces zero conversions for 2 consecutive days -> Slack alert
4. **Budget runaway:** Any campaign spending more than 120% of daily budget -> auto-alert and budget cap enforcement
5. **Lead quality drop:** Percentage of display leads scoring 70+ drops below 30% for a week -> Slack alert to review targeting

## Output

- PostHog dashboard with 8 panels covering spend, placement quality, creative health, audience performance, funnel, lead quality, CPA trends, and pipeline attribution
- 3 Attio saved views for display-sourced contacts, pipeline, and ROI
- Weekly automated report posted to Slack
- Monthly ROI report
- 5 real-time anomaly alerts

## Triggers

- Weekly report: Monday 08:00 UTC
- Monthly ROI report: first Monday of month, 08:00 UTC
- Anomaly alerts: real-time (PostHog webhooks via n8n)
