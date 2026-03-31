---
name: deal-negotiation-intelligence-monitor
description: Continuous monitoring of multi-year deal negotiation health — dashboard, anomaly detection, weekly intelligence reports, and pattern analysis
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Deal Negotiation Intelligence Monitor

This drill builds the play-specific monitoring layer for multi-year deal negotiation at the Durable level. It creates the dashboards, anomaly detection rules, and weekly intelligence reports that feed the `autonomous-optimization` drill. While `autonomous-optimization` handles the generic experiment loop, this monitor provides the domain-specific context: what to watch, what anomalies mean, and what hypotheses to test.

## Input

- PostHog with at least 8 weeks of multi-year negotiation events (from `deal-negotiation-tracking`)
- Attio CRM with historical deal data
- n8n instance for scheduled monitoring
- Enough deal volume for meaningful trends (50+ proposals sent historically)

## Steps

### 1. Build the negotiation intelligence dashboard

Using `posthog-dashboards`, create a dashboard with 8 panels:

**Panel 1 — Multi-Year Close Rate (weekly trend line):**
Metric: `multiyear_deal_closed_won / multiyear_proposal_sent` per week. Show 12-week trend with 4-week rolling average overlay. This is the primary health metric.

**Panel 2 — Average TCV Trend (weekly):**
Metric: Average `final_tcv` from `multiyear_deal_closed_won` events per week. Tracks whether deal sizes are growing or shrinking.

**Panel 3 — Discount Distribution (histogram):**
Metric: Distribution of `final_discount_pct` across all closed-won multi-year deals. Highlights discount creep — if the distribution shifts right over time, sellers are giving away too much.

**Panel 4 — Negotiation Efficiency (scatter plot):**
Axes: `negotiation_rounds` (x) vs `anchor_to_close_ratio` (y). Each dot is a closed deal. Ideal: few rounds with high anchor-to-close ratio (close near the initial anchor). Cluster analysis reveals which deals close efficiently and which grind.

**Panel 5 — Loss Reason Breakdown (stacked bar, monthly):**
Metric: `lost_reason` from `multiyear_deal_closed_lost` events. Tracks: reverted_to_annual, competitor, no_decision, budget, timing. If one reason is growing, it signals a systematic issue.

**Panel 6 — Pipeline Conversion Funnel:**
Funnel: `multiyear_proposal_generated` -> `multiyear_proposal_sent` -> `multiyear_counter_received` -> `multiyear_deal_closed_won`. Shows where deals drop off.

**Panel 7 — Readiness Score vs Outcome:**
Metric: `multiyear_readiness_score` at time of proposal vs eventual outcome (won/lost/reverted). Validates whether the scoring model predicts correctly. If high-readiness deals are losing, the model needs recalibration.

**Panel 8 — Revenue Impact:**
Metric: Total committed TCV this month vs total annual ACV from non-multi-year deals. Shows the revenue leverage from multi-year deals.

### 2. Define anomaly detection rules

Using `posthog-anomaly-detection`, configure:

| Metric | Alert Condition | Severity | What It Means |
|--------|----------------|----------|---------------|
| Multi-year close rate | Drops >20% vs 4-week average | High | Proposals are failing — check pricing, competitive pressure, or proposal quality |
| Average discount | Increases >3pp vs 4-week average | High | Discount creep — sellers are conceding too quickly |
| Negotiation rounds | Average increases >50% | Medium | Deals are grinding — terms may be misaligned with buyer expectations |
| Revert-to-annual rate | Exceeds 40% of proposals | High | Multi-year proposition isn't compelling enough |
| Time to close | Average increases >5 business days | Medium | Decision process is slowing — may need to change delivery format or timing |
| Readiness score false positive rate | >30% of high-readiness deals lost | High | Scoring model needs recalibration |

### 3. Build the weekly intelligence report

Using `n8n-scheduling`, create a Monday-morning workflow:

1. Query PostHog for last 7 days of negotiation events
2. Compute key metrics: close rate, average TCV, average discount, negotiation rounds, pipeline volume
3. Compare to 4-week rolling averages
4. Check all anomaly rules
5. Generate the report via Claude:

```
## Multi-Year Deal Negotiation — Week of {date}

### Headline
{one sentence: best metric this week and biggest concern}

### Performance
- Proposals sent: {n} ({+/-X%} vs avg)
- Deals closed (multi-year): {n} at ${avg_tcv} avg TCV
- Close rate: {X}% ({+/-Y}pp vs avg)
- Average discount: {X}% ({+/-Y}pp vs avg)
- Average negotiation rounds: {n}

### Negotiation Quality
- Anchor-to-close ratio: {X} (target: >0.85)
- Concessions per deal: {X} (lower is better)
- Fastest close: {deal_name} in {X} days
- Longest negotiation: {deal_name} at {X} rounds

### Loss Analysis
- Deals lost to annual revert: {n}
- Deals lost to competitor: {n}
- Most common loss reason this week: {reason}

### Active Experiments
- {experiment_name}: {status}, {preliminary_results}

### Anomalies
{list of triggered alerts with context and recommended actions}

### Recommendation
{one actionable recommendation based on this week's data}
```

Post to Slack and store in Attio.

### 4. Build pattern analysis for hypothesis generation

Using `posthog-cohorts`, create behavioral cohorts:

- "Quick closers" — multi-year deals that closed in <7 days with <2 concessions
- "Grinders" — multi-year deals that took >21 days or >3 rounds
- "Discount seekers" — deals where final discount > proposed discount by >5pp
- "Anchor holders" — deals where anchor-to-close ratio > 0.9

Analyze what differentiates these cohorts:
- Company size and industry
- Champion seniority
- Delivery channel
- Term length proposed
- Time of year (fiscal year proximity)

This analysis feeds `hypothesis-generation` with domain-specific context. When the `autonomous-optimization` drill asks "what should we experiment on?", this monitor provides the evidence: "Quick closers are disproportionately mid-market companies with VP-level champions approached within 30 days of fiscal year end. Hypothesis: timing proposals to fiscal year proximity will increase close rate."

## Output

- 8-panel PostHog dashboard for negotiation health
- Anomaly detection rules with severity classification
- Weekly intelligence report (automated, Monday delivery)
- Behavioral cohort analysis feeding hypothesis generation
- Pattern library for the autonomous optimization loop

## Triggers

Dashboard updates in real-time. Anomaly detection runs daily via PostHog alerts. Intelligence report generates weekly via n8n cron. Cohort analysis refreshes monthly.
