---
name: competitive-win-loss-reporting
description: Generate periodic competitive win/loss reports from deal data, track competitive positioning effectiveness, and surface actionable patterns by competitor
category: Sales
tools:
  - Attio
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - attio-deals
  - attio-reporting
  - attio-notes
  - posthog-dashboards
  - posthog-custom-events
  - competitive-intel-aggregation
  - hypothesis-generation
  - n8n-workflow-basics
  - n8n-scheduling
---

# Competitive Win/Loss Reporting

This drill generates structured competitive win/loss reports that identify which competitors you beat, which beat you, why, and what patterns predict competitive outcomes. Unlike generic pipeline reporting, this drill focuses exclusively on the competitive dimension: positioning effectiveness, battlecard usage impact, competitor strategy shifts, and emerging competitive threats.

## Input

- Attio CRM with deal records tagged with `competitors_evaluated`, `competitive_risk`, and win/loss outcomes
- At least 20 closed deals (won or lost) with competitive situation data
- PostHog events: `competitive_situation_identified`, `competitor_named`, `battlecard_delivered`, `competitive_positioning_generated`
- n8n instance for automated report generation

## Steps

### 1. Aggregate competitive deal outcomes from Attio

Query Attio for all deals closed in the reporting period (default: last 30 days) where `competitors_evaluated` is not empty. For each deal, extract:

```json
{
  "deal_id": "...",
  "outcome": "won|lost",
  "competitors_evaluated": ["Competitor A", "Competitor B"],
  "primary_competitor": "Competitor A",
  "competitive_risk_at_close": "low|medium|high|critical",
  "deal_value": 50000,
  "industry": "...",
  "company_size": "...",
  "decision_criteria_top3": ["criterion_1", "criterion_2", "criterion_3"],
  "evaluation_method": "formal_rfp|informal_comparison|...",
  "battlecard_delivered": true|false,
  "positioning_generated": true|false,
  "loss_reason": "null or reason if lost",
  "days_in_pipeline": 45
}
```

### 2. Calculate per-competitor metrics

For each competitor with 3+ deal appearances in the period:

| Metric | Formula | Purpose |
|--------|---------|---------|
| Win rate against | Wins / (Wins + Losses) * 100 | Core competitive health |
| Deal count | Total deals where mentioned | Frequency of competitive encounters |
| Average competitive deal value | Mean deal value in competitive deals | Revenue at stake |
| Competitive deal velocity | Average days in pipeline for competitive deals | Do they slow us down |
| Battlecard usage rate | Deals with battlecard / Total competitive deals | Intel adoption |
| Win rate with battlecard | Wins with battlecard / Total with battlecard | Intel effectiveness |
| Win rate without battlecard | Wins without / Total without | Controlled comparison |
| Battlecard lift | Win rate with - Win rate without | Marginal impact of competitive intel |

### 3. Run pattern analysis with Claude

Use the `hypothesis-generation` fundamental to identify competitive patterns:

```json
{
  "prompt": "Analyze these competitive deal outcomes and identify patterns that predict wins and losses against each competitor.\n\nDeal data:\n{deals_json}\n\nFor each competitor with 5+ deals, identify:\n1. WINNING_PATTERN: What deal characteristics (industry, size, criteria, evaluation method) correlate with wins\n2. LOSING_PATTERN: What deal characteristics correlate with losses\n3. POSITIONING_EFFECTIVENESS: Which positioning frameworks (from competitive_positioning_generated data) had highest win rates\n4. EMERGING_THREATS: Competitors whose mention frequency or win rate is trending in their favor\n5. ACTIONABLE_RECOMMENDATIONS: 3 specific changes to make this month based on the data\n\nReturn as structured JSON."
}
```

### 4. Generate the competitive report

Build a structured report combining quantitative metrics and qualitative analysis:

```markdown
## Competitive Win/Loss Report — {period}

### Executive Summary
- **Deals with competitors:** {n} of {total} closed deals ({pct}%)
- **Overall competitive win rate:** {rate}%
- **Battlecard usage rate:** {rate}%
- **Battlecard lift on win rate:** +{lift}%

### Competitor Scorecard
| Competitor | Deals | Win Rate | Avg Deal Value | Velocity (days) | Battlecard Lift | Trend |
|-----------|-------|----------|----------------|-----------------|-----------------|-------|
| {name}    | {n}   | {rate}%  | ${value}        | {days}           | +{lift}%         | {arrow} |

### Winning Patterns
{Per-competitor: when we win, what's true about the deal}

### Losing Patterns
{Per-competitor: when we lose, what's true about the deal}

### Positioning Effectiveness
{Which positioning frameworks have highest win rates by competitor}

### Emerging Threats
{Competitors with increasing frequency or improving win rate against us}

### Recommendations
1. {Specific action based on data}
2. {Specific action based on data}
3. {Specific action based on data}
```

### 5. Store and distribute the report

1. **Store in Attio:** Create a note on a "Competitive Intelligence" campaign record with the full report
2. **Post to Slack:** Send the executive summary + competitor scorecard table to the sales channel
3. **Fire PostHog event:** `competitive_report_generated` with properties: period, total_deals, overall_win_rate, top_threat_competitor
4. **Update Competitor records:** For each competitor in the report, update their win rate, loss rate, and mention count in Attio

### 6. Track report-over-report trends

Compare this period's metrics against the previous period:
- Win rate delta per competitor (improving or degrading?)
- Battlecard usage trend (adoption increasing?)
- Battlecard lift trend (effectiveness holding?)
- New competitors appearing that were not in previous report

Log period-over-period changes as PostHog events: `competitive_trend_updated` with delta values.

## Output

- Structured competitive win/loss report with per-competitor scorecards
- Pattern analysis identifying why we win or lose against each competitor
- Positioning effectiveness rankings
- Emerging threat identification
- Actionable recommendations grounded in data

## Triggers

- **Monthly report:** Cron via n8n, first Monday of each month at 8 AM
- **Quarterly deep dive:** Cron via n8n, first Monday of each quarter with 90-day lookback
- **Ad hoc:** Triggered manually when competitive strategy review is needed
