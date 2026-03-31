---
name: win-loss-reporting
description: Aggregate win/loss insights into periodic reports with trend analysis and strategic recommendations
category: Research
tools:
  - Attio
  - Anthropic
  - PostHog
  - n8n
fundamentals:
  - attio-reporting
  - attio-deals
  - competitive-intel-aggregation
  - transcript-insight-extraction
  - posthog-dashboards
  - posthog-custom-events
  - anthropic-api-patterns
  - n8n-scheduling
---

# Win/Loss Reporting

This drill aggregates individual win/loss insights into periodic reports that surface patterns, track trends, and generate strategic recommendations. Individual interviews are data points; this drill turns them into intelligence.

## Prerequisites

- At least 10 completed win/loss analyses stored as "win-loss-insight" tagged notes in Attio
- Attio CRM with deal metadata populated (win/loss reason, competitors, sentiment)
- PostHog instance for trend dashboards
- Anthropic API key for synthesis
- n8n instance for scheduled report generation

## Input

- Date range for the report period (default: last 30 days)
- Minimum number of interviews to include (default: 5; below this, patterns are unreliable)

## Steps

### 1. Pull raw data from CRM

Using `attio-reporting` and `attio-deals`, query Attio for:
- All deals closed in the report period with "win-loss-insight" tagged notes
- For each deal: outcome, deal value, primary reason, competitors, sentiment score, all categorized insights
- Pipeline totals: total deals closed, win count, loss count, overall win rate

Build a data table with one row per deal and columns for each extracted field.

### 2. Calculate aggregate metrics

From the raw data, compute:
- **Win rate:** wins / (wins + losses) as a percentage
- **Win rate by segment:** break down by deal size (small/medium/large), by source, by competitor present
- **Top win reasons:** frequency count of primary reasons for won deals, ranked
- **Top loss reasons:** frequency count of primary reasons for lost deals, ranked
- **Average sentiment score:** mean across all interviews, and separately for won vs lost
- **Competitor frequency:** how often each competitor appeared, and win rate when they were in the deal
- **Insight category distribution:** count of insights by category (product-gap, pricing, sales-process, etc.)
- **Interview coverage:** percentage of closed deals that had a completed interview or survey

### 3. Identify patterns and trends

Using the `anthropic-api-patterns` fundamental, send the aggregate data to Claude for synthesis:

```
Analyze this win/loss data for the period {date_range}:

WIN RATE: {X}%
TOP WIN REASONS: {list with counts}
TOP LOSS REASONS: {list with counts}
COMPETITOR WIN RATES: {list}
ALL INSIGHTS BY CATEGORY: {full list}

Previous period win rate: {Y}% (for trend comparison)

Generate:
1. TOP 3 PATTERNS: What recurring themes emerge from the data?
2. BIGGEST RISK: What single factor is costing us the most deals?
3. BIGGEST OPPORTUNITY: What single change would improve win rate the most?
4. COMPETITIVE SHIFT: Are we gaining or losing ground against specific competitors? Which ones and why?
5. RECOMMENDED ACTIONS: 3 specific, concrete actions ranked by expected impact on win rate
```

### 4. Build the report

Assemble the report in this structure:

```markdown
# Win/Loss Report — {Period}

## Summary
- **Deals analyzed:** {N} ({X} won, {Y} lost)
- **Interview coverage:** {Z}% of closed deals
- **Win rate:** {rate}% (previous period: {prev_rate}%)
- **Average buyer sentiment:** {score}/10

## Why We Win
| Reason | Count | % of Wins |
|--------|-------|-----------|
| {reason} | {n} | {pct} |

## Why We Lose
| Reason | Count | % of Losses |
|--------|-------|-------------|
| {reason} | {n} | {pct} |

## Competitive Landscape
| Competitor | Deals Present | Our Win Rate | Trend |
|------------|---------------|--------------|-------|
| {name} | {n} | {rate}% | {up/down/flat} |

## Key Patterns
{AI-generated pattern analysis}

## Recommended Actions
1. {Action with expected impact}
2. {Action with expected impact}
3. {Action with expected impact}

## Raw Data
{Link to Attio filtered view with all analyzed deals}
```

### 5. Distribute the report

- Store the report as a note in Attio on a "Win/Loss Program" record
- Send via Slack to #sales and #product channels
- Push key metrics to PostHog as events using `posthog-custom-events`:
  - `winloss_report_generated` with properties: period, win_rate, deal_count, top_loss_reason, top_win_reason
  - This creates a time series for dashboards

### 6. Build the trend dashboard

Using `posthog-dashboards`, create a Win/Loss Intelligence dashboard with panels:
- Win rate trend (line chart, monthly)
- Top loss reasons over time (stacked bar, monthly)
- Competitor win rates over time (multi-line chart)
- Interview coverage rate (line chart)
- Average buyer sentiment (line chart)

Set alerts: if win rate drops more than 10 percentage points month-over-month, notify the sales leader.

### 7. Schedule automated reports (Scalable+ levels)

Using `n8n-scheduling`, create a workflow that generates this report automatically:
- **Trigger:** Cron — first Monday of each month at 9am
- **Steps:** Query data, compute aggregates, call Claude for synthesis, format report, post to Slack, push to PostHog
- **Fallback:** If fewer than 5 interviews were completed in the period, send an alert instead: "Win/loss interview coverage is too low for reliable reporting. Only {N} interviews completed."

## Output

- A formatted win/loss report covering the specified period
- Report stored in Attio and distributed via Slack
- Key metrics pushed to PostHog for trend tracking
- Dashboard updated with latest data points

## Triggers

- **Manual (Smoke/Baseline):** Run by the analyst after accumulating enough interviews
- **Automated (Scalable+):** Monthly via n8n cron job
