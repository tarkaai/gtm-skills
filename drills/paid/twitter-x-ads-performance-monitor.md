---
name: twitter-x-ads-performance-monitor
description: Monitor Twitter/X ad campaign KPIs, detect creative fatigue and audience exhaustion, and generate optimization recommendations
category: Paid
tools:
  - Twitter/X Ads
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - twitter-x-ads-reporting
  - posthog-dashboards
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-workflow-basics
  - hypothesis-generation
---

# Twitter/X Ads Performance Monitor

Always-on monitoring workflow that tracks X Ads campaign performance, detects degradation patterns (creative fatigue, audience exhaustion, CPA spikes), and generates actionable optimization recommendations.

## Input

- Active X Ads campaign with at least 7 days of data
- PostHog dashboard with X Ads metrics synced (from `twitter-x-ads-campaign-build` drill)
- n8n instance for scheduling
- Anthropic API key for analysis

## Steps

### 1. Build the monitoring dashboard

Using `posthog-dashboards`, create a dedicated X Ads dashboard with these panels:
- **Daily impressions and clicks** — trend line, 30-day window
- **CTR by ad group** — grouped bar chart, weekly
- **CPC and CPA trends** — dual-axis line chart, daily
- **Conversion funnel** — funnel: ad click > landing page view > form submit > lead qualified
- **Creative performance table** — all promoted tweets ranked by CTR and CPA
- **Audience performance** — ad group comparison: keyword vs. follower-lookalike vs. interest

Set threshold alerts:
- CTR drops below 0.3% for any ad group for 3 consecutive days
- CPA exceeds 150% of target for 2 consecutive days
- Daily spend exceeds 120% of daily budget

### 2. Build the n8n monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow:

**Trigger**: Cron, daily at 8:00 AM

**Step 1 — Fetch data**: Pull yesterday's stats from X Ads API using `twitter-x-ads-reporting`. Also pull the last 14 days for trend context.

**Step 2 — Detect anomalies**: Using `posthog-anomaly-detection`, compare yesterday's metrics against the 14-day rolling average:
- CTR deviation >20% below average = **creative fatigue alert**
- CPC increase >30% above average = **auction pressure alert**
- Impressions drop >40% below average = **delivery issue alert**
- Conversion rate drop >25% below average = **landing page issue alert**

**Step 3 — Classify severity**:
- `normal`: All metrics within 20% of 14-day average. No action.
- `watch`: One metric deviating 20-30%. Log but no alert.
- `action_required`: Any metric deviating >30% or CPA above target for 2+ days.
- `critical`: Budget fully spent early, or zero conversions for 24+ hours.

**Step 4 — Generate recommendations** (for `action_required` and `critical`):
Using `hypothesis-generation`, pass the anomaly data to Claude:
```
Analyze this X Ads campaign performance data:
- Campaign: {name}
- Anomaly detected: {type} ({metric} deviated {%} from 14-day average)
- Current metrics: {impressions, clicks, CTR, CPC, CPA, conversions}
- 14-day trend: {daily metrics array}
- Active creative: {list of promoted tweets with individual CTR}
- Active audiences: {ad groups with individual performance}

Provide 3 ranked recommendations. Each must be:
1. A specific action an AI agent can execute (e.g., "pause promoted tweet {id}", "increase bid on ad group {id} by 15%")
2. Expected impact
3. Risk level (low/medium/high)
```

**Step 5 — Route output**:
- `normal` / `watch`: Log to Attio campaign notes
- `action_required`: Send Slack alert with recommendations. Auto-execute low-risk recommendations (e.g., pause underperforming creatives).
- `critical`: Send urgent Slack alert. Pause campaign if zero conversions for 24+ hours.

### 3. Creative fatigue detection

Creative fatigue follows a predictable pattern: CTR peaks in week 1, plateaus in week 2, declines in weeks 3-4.

Track per promoted tweet:
- Calculate 7-day rolling CTR
- If current week CTR is <70% of first-week CTR, flag as fatigued
- When >50% of active creatives are fatigued, trigger a creative refresh cycle (re-run `twitter-x-ads-creative` production steps from `twitter-x-ads-campaign-build`)

### 4. Audience exhaustion detection

Track per ad group:
- Frequency (impressions / unique reach). If frequency exceeds 3.0 in a 7-day window, the audience is seeing your ads too often.
- If impressions decline >20% week-over-week while budget is unchanged, the audience is exhausted.
- When exhaustion detected: expand targeting criteria or rotate to a new ad group.

## Output

- Daily monitoring alerts (Slack + Attio notes)
- Weekly performance summary with trend analysis
- Automatic creative fatigue and audience exhaustion detection
- Ranked optimization recommendations with risk levels
- Audit log of all automated actions taken

## Triggers

- Runs daily via n8n cron
- Manual trigger available for on-demand performance checks
