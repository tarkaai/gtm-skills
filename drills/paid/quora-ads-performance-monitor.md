---
name: quora-ads-performance-monitor
description: Continuous monitoring, reporting, and anomaly detection for Quora Ads campaigns with question-level and topic-level analysis
category: Paid
tools:
  - Quora Ads
  - PostHog
  - n8n
  - Attio
fundamentals:
  - quora-ads-reporting
  - quora-ads-question-targeting
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-deals
---

# Quora Ads Performance Monitor

This drill builds the monitoring, reporting, and anomaly detection layer for Quora Ads campaigns. It tracks question-level and topic-level performance, detects creative fatigue and targeting saturation, and generates actionable reports. This is the data substrate that the `autonomous-optimization` drill reads from at the Durable level.

## Input

- Active Quora Ads campaigns with conversion tracking configured
- PostHog receiving `quora_ads_page_view`, `quora_ads_lead_captured`, and `quora_ads_lead_qualified` events
- Attio configured with Quora-sourced leads and campaign records
- n8n instance for scheduled workflows

## Steps

### 1. Build the PostHog Dashboard

Using `posthog-dashboards`, create a Quora Ads dashboard with 8 panels:

| Panel | Metric | Visualization |
|-------|--------|--------------|
| 1. Spend & Reach | Daily impressions and spend (from Quora export or connector) | Line chart, dual axis |
| 2. Click Performance | CTR and CPC by ad set (topic vs question vs keyword) | Bar chart, grouped |
| 3. Conversion Funnel | `quora_ads_page_view` > `quora_ads_lead_captured` > `quora_ads_lead_qualified` | Funnel |
| 4. CPA Trend | Cost per qualified lead over time | Line chart with target line |
| 5. Creative Performance | CTR and conversion rate by ad variant (utm_content breakdown) | Table, sortable |
| 6. Targeting Comparison | CPA by targeting type (topic vs question vs keyword ad sets) | Bar chart |
| 7. Lead Quality | % of leads scoring 70+ on ICP scoring, by ad set | Stacked bar |
| 8. Full-Funnel Attribution | Quora click > page view > lead > qualified > meeting > deal | Funnel |

### 2. Build Attio Saved Views

Create Attio views for Quora campaign management:

- **Quora-sourced contacts**: Filter contacts where `source = quora-ads`. Sort by lead score descending.
- **Quora pipeline**: Filter deals where `source = quora-ads`. Track stage progression and time in stage.
- **Quora ROI by targeting type**: Group deals by `utm_campaign` and `ad_set_targeting_type`. Calculate revenue per dollar spent.

### 3. Deploy Weekly Automated Report

Build an n8n workflow using `n8n-scheduling` (trigger: every Monday 8 AM):

1. **Gather Quora data**: Pull the latest CSV export from Google Drive or query via Supermetrics/Improvado connector
2. **Gather PostHog data**: Query PostHog API for `quora_ads_*` events from last 7 days
3. **Gather Attio data**: Query Attio API for Quora-sourced leads and deals created last 7 days
4. **Calculate metrics**:
   - Weekly: impressions, clicks, CTR, CPC, conversions, CPA, spend vs budget
   - Week-over-week change for each metric
   - Best and worst performing ad sets and ad variants
   - Lead quality score (% qualified)
5. **Generate report**: Format as a structured message with key metrics, changes, and recommendations
6. **Post to Slack**: Send the weekly summary
7. **Log in Attio**: Store as a note on the campaign record

### 4. Configure Real-Time Anomaly Alerts

Build 5 n8n workflows using `n8n-workflow-basics`, each triggered by PostHog webhook or scheduled check:

**Alert 1 — CPC Spike:**
- Check: If average CPC over last 3 days exceeds 150% of 14-day rolling average
- Action: Slack alert with recommendation to check targeting breadth or creative freshness

**Alert 2 — Conversion Rate Drop:**
- Check: If landing page conversion rate (form submits / page views) drops below 2% for 48+ hours
- Action: Slack alert with recommendation to diagnose landing page or ad-to-page message match

**Alert 3 — Zero Conversions:**
- Check: If a campaign has 200+ clicks in the last 7 days but zero `quora_ads_lead_captured` events
- Action: Urgent Slack alert — likely a tracking issue (pixel not firing, form broken, or CAPI misconfigured)

**Alert 4 — Budget Runaway:**
- Check: If daily spend exceeds 120% of daily budget target
- Action: Slack alert with recommendation to pause or reduce bids

**Alert 5 — Creative Fatigue:**
- Check: If any ad variant's CTR has declined for 5 consecutive days
- Action: Slack alert recommending ad rotation — flag the fatigued variant for replacement

### 5. Implement Question/Topic Performance Tracking

This is Quora-specific: track which questions and topics drive the best results.

Using Quora Ads Manager export data (or connector):

1. Export performance data broken down by ad set
2. Map ad set names to their targeting configurations (topics, questions, keywords)
3. Calculate CPA at the ad-set level to determine which targeting clusters perform best
4. Maintain a running log: `topic_name -> CPA, conversion_rate, total_spend`
5. Flag topics/questions with CPA >150% of average for removal
6. Flag topics/questions with CPA <75% of average for budget increase

Store this targeting effectiveness data in Attio as structured notes. Feed it back into targeting optimization at Scalable and Durable levels.

### 6. Monthly Full-Funnel Attribution Report

Build a monthly report (runs first Monday of each month):

1. Pull all Quora-sourced deals from Attio for the month
2. Calculate:
   - Total Quora ad spend for the month
   - Total pipeline generated (sum of deal values)
   - Total revenue closed (won deals)
   - ROAS: revenue / spend
   - Full-funnel CPA: spend / deals created
   - Average deal cycle time for Quora-sourced deals
3. Compare to other paid channels (LinkedIn, Google, Reddit) if data is available
4. Generate a narrative summary of Quora's contribution to the pipeline
5. Post to Slack and store in Attio

## Output

- PostHog dashboard with 8 panels tracking Quora Ads performance
- Attio saved views for Quora leads, pipeline, and ROI
- Weekly automated performance report via n8n
- 5 real-time anomaly alerts
- Question/topic performance tracking log
- Monthly full-funnel attribution report
