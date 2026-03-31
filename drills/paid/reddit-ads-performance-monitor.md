---
name: reddit-ads-performance-monitor
description: Monitor Reddit Ads campaign performance, detect issues, and trigger optimization actions
category: Paid
tools:
  - Reddit Ads API
  - PostHog
  - n8n
  - Attio
fundamentals:
  - reddit-ads-reporting
  - posthog-custom-events
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Reddit Ads Performance Monitor

This drill builds an always-on monitoring system for Reddit Ads campaigns. It pulls performance data daily, detects anomalies and optimization opportunities, and triggers automated responses or human alerts.

## Input

- Active Reddit Ads campaign IDs
- Target KPIs: target CPC, target CPA, target CTR, target conversion rate
- Budget constraints: maximum daily spend, maximum CPA
- PostHog project with Reddit ad events flowing

## Steps

### 1. Build the daily reporting workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create an n8n workflow triggered by a daily cron at 09:00 UTC:

**Node chain:**
1. **HTTP Request**: Pull campaign report from Reddit Ads API using `reddit-ads-reporting` fundamental. Group by DATE + ADGROUP.
2. **Function**: Convert microdollar values to dollars. Calculate derived metrics: CPA (spend / conversions), ROAS (estimated revenue / spend), budget utilization (spend / budget).
3. **HTTP Request**: Pull PostHog events for the same period. Compare PostHog lead counts vs. Reddit-reported conversions (discrepancy check).
4. **Set**: Merge Reddit metrics + PostHog metrics into a unified daily report object.
5. **Branch**: Route based on health checks (see step 2).

### 2. Define health checks and alert thresholds

Configure IF nodes in the n8n workflow for each check:

| Check | Condition | Action |
|---|---|---|
| CPA spike | CPA > 150% of target for 3+ consecutive days | Alert: reduce bid or pause underperforming ad groups |
| CTR decay | CTR dropped >30% from first-week average | Alert: creative fatigue, refresh ad variants |
| Budget underspend | Spend < 50% of daily budget | Alert: targeting too narrow or bids too low |
| Budget overspend | Spend > 110% of daily budget | Alert: check daily caps |
| Conversion tracking gap | PostHog leads > 2x Reddit-reported conversions | Alert: CAPI may not be firing, fix tracking |
| Zero conversions | 0 conversions for 3+ days with >100 clicks | Alert: landing page or tracking issue |
| Subreddit underperformer | Ad group CTR < 50% of campaign average | Flag for budget reallocation |

### 3. Build the PostHog dashboard

Using `posthog-dashboards`, create a "Reddit Ads Performance" dashboard with these panels:

- **Spend vs. Leads** (trend, last 30 days): daily spend line overlaid with daily lead count
- **CPA trend** (trend, last 30 days): cost per acquisition over time
- **CTR by ad group** (bar chart): compare subreddit cluster performance
- **Conversion funnel**: `paid_reddit_ads_page_view` -> form focus -> `paid_reddit_ads_lead_captured`
- **Lead quality** (table): leads from Reddit ads with their Attio deal stage and qualification status
- **Ad variant performance** (table): CTR, conversion rate, and CPA per ad variant

Using `posthog-custom-events`, ensure all events carry the `utm_content` property (ad variant ID) and `utm_term` property (subreddit cluster) for proper breakdown.

### 4. Set up CRM logging

Using `attio-notes`, log weekly performance summaries to the campaign record in Attio:

```
Week of {date}: Reddit Ads
- Spend: ${spend} | Budget utilization: {pct}%
- Impressions: {impressions} | Clicks: {clicks} | CTR: {ctr}%
- Leads: {leads} | CPA: ${cpa}
- Top subreddit: r/{subreddit} (CTR: {ctr}%, CPA: ${cpa})
- Worst subreddit: r/{subreddit} (CTR: {ctr}%, CPA: ${cpa})
- Action taken: {action or "none needed"}
```

### 5. Weekly optimization cadence

Every Monday, the monitoring workflow generates an optimization report:

1. **Pull 7-day Reddit Ads report** grouped by ADGROUP and AD
2. **Rank ad groups** by CPA (ascending = best)
3. **Rank ad variants** by CTR (descending = best)
4. **Generate recommendations:**
   - If an ad group's CPA is >2x the best ad group: recommend pausing or reallocating budget
   - If an ad variant's CTR is <50% of the best variant: recommend replacing
   - If overall CPA is within target: recommend increasing budget 20%
   - If overall CPA is above target: recommend tightening targeting or refreshing creative
5. **Post to Slack** and log in Attio

### 6. Monthly subreddit refresh

Every 30 days, trigger a re-evaluation:

1. Pull subreddit-level performance (group by SUBREDDIT)
2. Identify exhausted subreddits (declining CTR over 4 weeks)
3. Flag for the `reddit-ads-subreddit-targeting` drill to find replacements
4. Update the targeting clusters

## Output

- Daily automated health checks with alerts for anomalies
- PostHog dashboard with real-time Reddit Ads performance visibility
- Weekly optimization reports with specific recommendations
- Monthly subreddit refresh triggers
- CRM audit trail of all performance data and actions taken

## Triggers

- Daily at 09:00 UTC (automated health checks)
- Weekly on Monday (optimization report)
- Monthly on 1st (subreddit refresh evaluation)
- On-demand when manually triggered for investigation
