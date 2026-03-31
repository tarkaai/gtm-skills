---
name: sdk-adoption-monitor
description: Continuous monitoring of SDK adoption metrics across registries with anomaly detection and competitive tracking
category: SDK
tools:
  - PostHog
  - n8n
  - Clay
  - Attio
fundamentals:
  - registry-download-tracking
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - clay-claygent
  - attio-reporting
---

# SDK Adoption Monitor

This drill builds the monitoring and reporting system for the SDK library development play at Durable level. It tracks downloads, conversion rates, developer activation, competitive positioning, and ecosystem changes across all package registries -- then surfaces anomalies and optimization opportunities in a weekly report.

## Input

- SDKs published across 4+ registries (output from `sdk-multi-language-scaling` drill)
- PostHog tracking configured for SDK-sourced traffic via UTM parameters
- n8n instance for scheduled data collection
- At least 8 weeks of SDK performance data (Scalable baseline established)

## Steps

### 1. Build the PostHog dashboard

Using `posthog-dashboards`, create an "SDK Adoption" dashboard:

**Panel 1 -- Aggregate Downloads:**
- Line chart: total weekly downloads across all registries (stacked by language)
- Counter: total downloads this month (all SDKs)
- Counter: month-over-month download growth rate

**Panel 2 -- Per-SDK Performance:**
- Table: `language`, `registry`, `downloads_7d`, `downloads_30d`, `readme_cta_clicks`, `signups`, `conversion_rate`
- Sorted by signups descending
- Color-code: green (growing >10% WoW), yellow (stable), red (declining >10% WoW)

**Panel 3 -- SDK-to-Revenue Funnel:**
- Funnel: `sdk_weekly_downloads` -> `sdk_readme_cta_clicked` -> `sdk_signup_completed` -> `sdk_api_key_created` -> `sdk_first_api_call`
- Break down by `language`

**Panel 4 -- Developer Activation:**
- Line chart: weekly `sdk_first_api_call` events by language
- Retention curve: of developers who made a first API call via SDK, what % are still active at 7d, 14d, 30d?
- Counter: SDK-sourced developers with >100 API calls in the last 30 days (power users)

**Panel 5 -- Competitive Landscape:**
- Table: `competitor_sdk`, `registry`, `their_downloads_30d`, `our_downloads_30d`, `our_rank_vs_theirs`
- Highlight rows where a competitor overtook our SDK in downloads

### 2. Configure anomaly detection

Using `posthog-anomaly-detection` and n8n:

**Anomaly thresholds:**
- **Download drop:** >25% decline in weekly downloads for any SDK vs 4-week rolling average
- **CTA conversion drop:** README CTA click-through rate drops >30% for any registry
- **Activation drop:** `sdk_first_api_call` count drops >20% week-over-week
- **New competitor:** A new SDK in your API category appears with >500 downloads in its first month
- **Staleness alert:** Any SDK repo has had no commits in >45 days
- **Breaking change signal:** A spike in GitHub issues mentioning "error", "broken", "upgrade" after a release

Route alerts to Slack with: the specific SDK, the metric, the deviation, and recommended investigation action.

### 3. Build competitive tracking

Using `clay-claygent`, monitor the competitive SDK landscape weekly:

**Claygent prompt:**
```
For the {api_category} API client/SDK category:
1. Search {registry} for packages matching: {keywords}
2. For the top 10 by downloads: extract name, downloads (last month), last updated date, GitHub stars
3. Compare to last week's snapshot: flag new entrants, rank changes, and abandoned SDKs (no update in 6+ months)
4. Search GitHub for new repos matching "{api_category} sdk" created in the last 7 days with >10 stars
Return as JSON array.
```

Run for each registry where you have an SDK published.

### 4. Track developer journey beyond signup

Using `posthog-custom-events`, instrument deeper activation signals:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `sdk_first_api_call` | First successful API call from SDK user-agent | `language`, `sdk_version`, `endpoint` |
| `sdk_error_encountered` | SDK-attributed error response | `language`, `sdk_version`, `error_type`, `endpoint` |
| `sdk_version_adoption` | API call from a specific SDK version | `language`, `sdk_version` |
| `sdk_user_upgraded` | SDK-sourced user upgrades to paid plan | `language`, `registry`, `plan` |

These events feed into the autonomous optimization loop to detect which SDKs produce the highest-quality (most activated, highest-LTV) developers.

### 5. Generate weekly SDK health report

The n8n workflow assembles:

```
SDK Health Report -- Week of {date}

DOWNLOADS:
  TypeScript (npm):   {count} ({change}% WoW) | {30d_count} 30d
  Python (PyPI):      {count} ({change}% WoW) | {30d_count} 30d
  Rust (crates.io):   {count} ({change}% WoW) | {30d_count} 30d
  Ruby (RubyGems):    {count} ({change}% WoW) | {30d_count} 30d
  Go (pkg.go.dev):    {count} ({change}% WoW) | {30d_count} 30d
  Java (Maven):       {count} ({change}% WoW) | {30d_count} 30d

CONVERSION:
  README CTA clicks:   {count} (best: {best_registry})
  Signups from SDKs:   {count}
  API keys created:    {count}
  First API calls:     {count}
  Paid conversions:    {count}

ANOMALIES:
  {list any triggered anomalies with context}

COMPETITIVE:
  {notable changes in competing SDKs}

RECOMMENDATIONS:
  {data-driven suggestions for next actions}
```

Post to Slack and store in Attio.

## Output

- PostHog dashboard with download trends, per-SDK performance, funnels, and competitive data
- Anomaly detection alerts for 6 key metric categories
- Weekly competitive landscape scan across all registries
- Developer activation tracking beyond signup
- Weekly SDK health report with recommendations
- Historical trend data feeding the autonomous optimization loop

## Triggers

- Data collection: weekly via n8n cron (Monday 7am)
- Anomaly alerts: continuous (checked during weekly collection; real-time for PostHog-tracked metrics)
- Competitive scan: weekly
- Dashboard: always-on, refreshes with live data
