---
name: quora-ads-reporting
description: Pull Quora Ads performance data for campaign analysis, budget decisions, and optimization
tool: Quora Ads
difficulty: Config
---

# Quora Ads — Reporting

Pull performance data from Quora Ads Manager for campaign analysis, budget reallocation, and optimization decisions. Quora provides native reporting in Ads Manager plus data export. For automated pipelines, use Supermetrics, Improvado, or Funnel.io connectors.

## Native Reporting (Ads Manager)

### Dashboard Metrics

In Ads Manager, navigate to the campaign, ad set, or ad level to view:

| Metric | Description |
|--------|-------------|
| Impressions | Number of times ad was shown |
| Clicks | Number of clicks on ad |
| CTR | Click-through rate (clicks / impressions) |
| CPC | Average cost per click |
| CPM | Cost per 1,000 impressions |
| Spend | Total amount spent |
| Conversions | Number of tracked conversion events |
| Cost per Conversion | Spend / conversions |
| Conversion Rate | Conversions / clicks |

### Breakdowns

Quora Ads Manager supports breakdowns by:
- **Time**: daily, weekly, monthly
- **Placement**: feed, question page, digest email
- **Device**: desktop, mobile, tablet
- **Geography**: country, region
- **Ad Set / Ad**: per-targeting-group and per-creative performance

### Data Export

1. In Ads Manager, select the campaigns/ad sets/ads to export
2. Click **Export** > **CSV** or **Excel**
3. Select date range and metrics
4. Download the file

For scheduled exports, use third-party connectors (below).

## Automated Reporting via Third-Party Connectors

### Supermetrics

Connect Quora Ads as a data source in Supermetrics to pull data into Google Sheets, Looker Studio, or a data warehouse.

1. In Supermetrics, add **Quora Ads** as a source
2. Authenticate with your Quora Ads account
3. Select metrics: impressions, clicks, CTR, CPC, conversions, cost per conversion
4. Select dimensions: campaign name, ad set name, ad name, date, device, geo
5. Schedule daily or weekly refresh

### Improvado

For enterprise-grade ETL:

1. Connect Quora Ads in Improvado dashboard
2. Configure data sync schedule (daily recommended)
3. Map Quora metrics to your unified marketing data model
4. Join with PostHog, Attio, and other source data for cross-channel attribution

### n8n Workflow (Manual Export Processing)

For simpler setups, build an n8n workflow that:

1. **Trigger**: Weekly cron (every Monday 8 AM)
2. **Step 1**: Send Slack reminder to download Quora Ads CSV export for last week
3. **Step 2**: Watch a Google Drive folder for the uploaded CSV
4. **Step 3**: Parse CSV, extract key metrics (impressions, clicks, CPC, conversions, CPA)
5. **Step 4**: Compare to previous week and threshold targets
6. **Step 5**: Generate a performance summary and post to Slack
7. **Step 6**: Log metrics in Attio as a note on the campaign record

## Key Reports to Build

### 1. Weekly Performance Summary

Pull weekly: impressions, clicks, CTR, CPC, conversions, CPA, spend vs budget.
Compare week-over-week. Flag: CPA increase >20%, CTR decline >30%, budget underspend >40%.

### 2. Targeting Effectiveness Report

Compare performance by targeting type:
- Topic targeting ad sets vs question targeting ad sets vs keyword targeting ad sets
- Identify which topics/questions/keywords drive the lowest CPA
- Shift budget toward best performers

### 3. Creative Performance Report

Compare performance by ad variant:
- CTR by hook type (data, question, outcome, social proof)
- CPC by creative format (image vs text)
- Conversion rate by headline theme
- Identify creative fatigue: CTR declining over 5+ consecutive days

### 4. Funnel Attribution Report (PostHog)

Cross-reference Quora data with PostHog:
- Quora ad click > landing page view > form submit > lead qualified > meeting booked > deal created
- Calculate full-funnel CPA (not just cost per click or cost per form submit)
- Compare Quora full-funnel CPA to other paid channels

## Metric Formulas

```
CTR = Clicks / Impressions
CPC = Spend / Clicks
CPM = (Spend / Impressions) * 1000
Conversion Rate = Conversions / Clicks
CPA = Spend / Conversions
ROAS = Revenue Attributed / Spend
Blended CPA = Total Paid Spend / Total Conversions (across all channels)
```

## Reporting Cadence

| Report | Frequency | Audience |
|--------|-----------|----------|
| Performance snapshot | Daily (during Smoke/Baseline) | Agent + marketer |
| Weekly summary | Weekly | Marketing team |
| Targeting effectiveness | Bi-weekly | Agent (for optimization) |
| Creative performance | Weekly | Agent (for creative rotation) |
| Full-funnel attribution | Monthly | Leadership |
