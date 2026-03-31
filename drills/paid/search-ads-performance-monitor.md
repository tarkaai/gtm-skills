---
name: search-ads-performance-monitor
description: Continuously monitor search ad campaign KPIs, detect anomalies, and generate optimization recommendations
category: Paid
tools:
  - Google Ads
  - Microsoft Advertising
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - google-ads-search-query-mining
  - google-ads-bidding-strategy
  - google-ads-search-campaigns
  - posthog-anomaly-detection
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
  - hypothesis-generation
---

# Search Ads Performance Monitor

This drill creates an always-on monitoring system for search ad campaigns. It detects performance anomalies, identifies optimization opportunities, and generates agent-executable recommendations. This is the play-specific monitoring layer that feeds into the `autonomous-optimization` drill at Durable level.

## Prerequisites

- Active search campaigns on Google Ads and/or Microsoft Advertising with at least 14 days of data
- PostHog tracking configured with search ad events (from `search-keyword-campaign-build`)
- n8n instance for scheduling automated checks
- Anthropic API key for analysis and recommendation generation

## Input

- Campaign IDs for Google and Microsoft Ads
- Target CPA and target ROAS thresholds
- PostHog dashboard URL for the search ads play
- Slack webhook URL or notification channel for alerts

## Steps

### 1. Build the daily metrics collection workflow

Create an n8n workflow using `n8n-scheduling` that runs daily at 9am:

**Google Ads data pull:**
- Query the Google Ads API for the last 7 days, segmented by day:
  ```
  SELECT campaign.name, ad_group.name, metrics.impressions, metrics.clicks,
         metrics.conversions, metrics.cost_micros, metrics.click_through_rate,
         metrics.average_cpc, metrics.search_impression_share
  FROM campaign
  WHERE segments.date DURING LAST_7_DAYS
    AND campaign.advertising_channel_type = 'SEARCH'
  ```
- Calculate rolling 7-day averages for: CTR, CPC, CPA, conversion rate, impression share

**Microsoft Ads data pull (if active):**
- Query the Microsoft Advertising Reporting API for matching metrics
- Normalize to the same format as Google data for unified analysis

**PostHog data pull:**
- Query PostHog for landing page metrics: `search_ad_form_view` to `search_ad_form_submit` conversion rate, bounce rate by source

**Store in PostHog:**
- Send daily summary metrics as custom events using `posthog-custom-events`: `search_ads_daily_summary` with properties for each metric

### 2. Configure anomaly detection rules

Using `posthog-anomaly-detection`, set up alerts for:

- **CPA spike**: CPA exceeds 150% of 14-day rolling average for 2 consecutive days
- **CTR drop**: CTR falls below 70% of 14-day average (signals ad fatigue or competitor pressure)
- **Conversion rate drop**: Landing page conversion rate drops below 50% of baseline (signals landing page or tracking issue)
- **Budget depletion**: Daily spend consistently hits budget cap before 3pm (signals underfunding of profitable campaigns)
- **Impression share loss**: Search impression share drops below 50% (signals bid pressure from competitors)
- **Quality score degradation**: Average quality score drops below 6 (signals relevance issues)

### 3. Build the weekly search query mining workflow

Create an n8n workflow that runs weekly using `n8n-scheduling`:

1. Run `google-ads-search-query-mining` to extract the last 7 days of search terms
2. Classify each query as: **converting** (has conversions), **promising** (clicks but no conversions yet, CPC below target), **wasteful** (clicks, no conversions, CPC above target), or **irrelevant** (clearly off-topic)
3. Auto-add wasteful and irrelevant queries as negative keywords via the API
4. Flag converting queries that are not yet exact-match keywords for human review
5. Post a weekly search terms digest to Slack: new negatives added, new keyword candidates, total wasted spend recovered

### 4. Build the creative fatigue detector

Create an n8n workflow that checks weekly:

1. Pull ad-level performance data for the last 30 days
2. For each ad, calculate CTR trend: compare last 7 days CTR to the first 7 days after launch
3. Flag ads where CTR has declined >30% from their initial performance as "fatigued"
4. Use `hypothesis-generation` to draft 3 new headline variations based on what worked in the high-performing period
5. Post fatigued ad alerts and new headline suggestions to Slack for human review (or auto-implement at Durable level)

### 5. Generate weekly performance report

Using `posthog-dashboards`, build a weekly report workflow:

```markdown
# Search Ads Weekly Report — Week of {date}

## Performance Summary
| Metric | This Week | Last Week | Change | Target |
|--------|-----------|-----------|--------|--------|
| Spend | ${X} | ${Y} | {%} | ${budget} |
| Clicks | {X} | {Y} | {%} | — |
| Conversions | {X} | {Y} | {%} | — |
| CPA | ${X} | ${Y} | {%} | ${target} |
| CTR | {X}% | {Y}% | {%} | >2% |
| Conv. Rate | {X}% | {Y}% | {%} | >3% |

## Anomalies Detected
{List of any triggered anomaly alerts this week}

## Actions Taken
- Negative keywords added: {count} (est. ${savings}/mo recovered)
- Ads flagged for fatigue: {count}
- Keywords paused: {count}

## Recommendations
1. {Agent-generated recommendation with data}
2. {Agent-generated recommendation with data}
```

Post to Slack and store in Attio as a note on the campaign record.

## Output

- Daily automated metrics collection and anomaly detection
- Weekly search query mining with auto-negative keyword management
- Weekly creative fatigue detection with headline suggestions
- Weekly performance report with agent-generated recommendations
- All data centralized in PostHog for cross-play analysis

## Triggers

- Daily: metrics collection and anomaly checks
- Weekly: search query mining, creative fatigue check, performance report
- On anomaly: immediate Slack alert with diagnosis and recommended action
