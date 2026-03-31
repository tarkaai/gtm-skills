---
name: meddic-qualification-reporting
description: Build MEDDIC qualification dashboards and weekly reports tracking scoring accuracy, element completion rates, and pipeline health
category: Sales
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
---

# MEDDIC Qualification Reporting

This drill builds the measurement layer for your MEDDIC qualification play. It creates dashboards that track qualification funnel health, per-element completion rates, scoring accuracy, and pipeline velocity — so you can see whether your MEDDIC process is actually producing qualified deals that close.

## Input

- PostHog project with MEDDIC events being tracked (from `meddic-scorecard-setup`)
- Attio CRM with deals flowing through MEDDIC pipeline stages
- At least 2 weeks of qualification data for meaningful analysis

## Steps

### 1. Build the MEDDIC qualification funnel dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "MEDDIC Qualification Funnel" with these panels:

**Panel 1 — Qualification volume (bar chart, weekly):**
- Count of `meddic_score_created` events per week
- Breakdown by `verdict` (Qualified / Needs Work / Disqualified)
- Shows total throughput and qualification rate trend

**Panel 2 — Composite score distribution (histogram):**
- Distribution of `meddic_composite_score` values across all scored deals
- Helps identify if your scoring model clusters too tightly (needs recalibration) or spreads well

**Panel 3 — Element completion heatmap (table):**
- For each MEDDIC element, show the percentage of active deals where that element is above 50 (sufficiently assessed)
- Identify which elements are consistently incomplete across the pipeline
- Example: if Champion is above 50 in only 30% of deals, champion identification is a systemic gap

**Panel 4 — Element-by-element trend (line chart, weekly):**
- Average scores for Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion per week
- Identifies which element is consistently weakest across your pipeline

**Panel 5 — Pre-score vs. post-call accuracy (line chart):**
- Compare `meddic_composite_score` at `meddic_assessment_source = "Pre-call Enrichment"` vs. `meddic_assessment_source = "Discovery Call"` for the same deals
- The gap between these lines measures enrichment accuracy. Closer = better pre-qualification.
- Break down by individual elements to see which elements enrichment predicts well vs. poorly

**Panel 6 — Deal health distribution (pie chart):**
- Count of deals in each health tier: Healthy, At Risk, Critical
- From `meddic-deal-health-monitor` drill data

### 2. Build the pipeline velocity funnel

Using the `posthog-funnels` fundamental, create a funnel:

```
meddic_score_created → meddic_qualification_passed → meddic_champion_identified → meddic_economic_buyer_engaged → proposal_sent → deal_closed_won
```

Measure:
- Conversion rate at each step
- Median time between steps
- Drop-off points (where deals stall)

Break down by `meddic_verdict` to compare: do deals that scored "Qualified" on first assessment actually convert better than "Needs Work" deals that were later promoted?

Also create element-specific funnels:
- **Champion funnel:** No Champion → Potential Champion → Active Champion → Deal Won
- **Economic Buyer funnel:** Unknown → Identified Not Engaged → Identified and Engaged → Deal Won

### 3. Build scoring accuracy cohorts

Using the `posthog-cohorts` fundamental, create cohorts:

- **True Positives:** Deals scored Qualified that eventually closed won
- **False Positives:** Deals scored Qualified that closed lost or stalled 60+ days
- **True Negatives:** Deals scored Disqualified that never converted
- **False Negatives:** Deals scored Disqualified that later came back and closed
- **Element Accuracy:** For each MEDDIC element, track whether high element scores correlated with won deals

Track these cohorts over time. The goal is to maximize True Positives + True Negatives and minimize False Positives + False Negatives.

Calculate:
- `Scoring Accuracy = (True Positives + True Negatives) / Total Scored Deals`
- `Element Predictive Power = correlation(element_score, deal_won)` for each of the 6 elements

### 4. Set up weekly automated report via n8n

Using the `n8n-scheduling` fundamental, create a workflow that runs every Monday at 8am:

1. Query PostHog for last week's MEDDIC metrics:
   - Total deals scored
   - Qualification rate (% scored Qualified)
   - Average composite score
   - Top-scoring deals (list top 5 by composite score)
   - Weakest element (lowest average across all deals)
   - Element completion rates (% of deals with each element above 50)
2. Query Attio for pipeline health:
   - Deals in each MEDDIC stage (count + total value)
   - Deals that moved forward this week
   - Deals that stalled (no activity for 7+ days)
   - Deals where champion was identified this week
   - Deals where economic buyer meeting occurred this week
3. Generate a text report summarizing the data:
   ```
   ## MEDDIC Weekly Report — {week}

   ### Qualification Summary
   - {X} deals scored this week. {Y}% qualified on first assessment.
   - Average composite: {score}. Last week: {prev_score} ({change}).

   ### Element Health
   | Element | Avg Score | % Complete (>50) | Change |
   |---------|-----------|-------------------|--------|
   | Metrics | {score} | {pct}% | {change} |
   | Economic Buyer | {score} | {pct}% | {change} |
   | Decision Criteria | {score} | {pct}% | {change} |
   | Decision Process | {score} | {pct}% | {change} |
   | Identify Pain | {score} | {pct}% | {change} |
   | Champion | {score} | {pct}% | {change} |

   ### Pipeline Movement
   - {X} deals moved forward. {Y} deals stalled.
   - Champions identified: {count}
   - Economic buyer meetings: {count}

   ### Top Deals This Week
   {list of top 5 deals by composite score with key details}

   ### Action Items
   {auto-generated recommendations based on the data}
   ```
4. Post to Slack and store in Attio as a note on the "MEDDIC Qualification" campaign record

### 5. Set up anomaly alerts

Configure PostHog alerts (or n8n monitors) for:

- **Qualification rate drops below 20%:** May indicate ICP drift or list quality degradation
- **Average composite score drops below 45:** Enrichment data may be stale or scoring formula needs recalibration
- **Champion completion rate drops below 25%:** You are not doing enough champion development work
- **Economic Buyer completion rate drops below 30%:** Deals are progressing without budget holder engagement (risk)
- **False positive rate exceeds 30%:** Scoring model is too generous — tighten thresholds
- **Zero deals scored for 3+ days:** Pipeline has dried up — check lead source health

Each alert triggers a Slack notification with the metric value and recommended diagnostic action.

### 6. Monthly calibration review

At the end of each month, run a calibration analysis:

1. Pull all deals closed this month (won and lost) from Attio
2. Compare their MEDDIC scores at qualification time vs. their actual outcome
3. Calculate per-element predictive accuracy: which element best predicts closed-won?
4. Check if any element is over-weighted (high score but deals still lose) or under-weighted (low score but deals still win)
5. Adjust scoring weights if data shows a different weighting would improve accuracy
6. Check enrichment accuracy: for each element, how close was the pre-call score to the post-call score?
7. Document the calibration change and rationale in an Attio note
8. Update `meddic-scorecard-setup` if weights change

## Output

- PostHog dashboard with 6+ panels tracking MEDDIC qualification funnel health
- Pipeline velocity funnel showing conversion rates at each MEDDIC milestone
- Element-specific funnels (Champion progression, Economic Buyer engagement)
- Scoring accuracy cohorts tracking true/false positive/negative rates
- Per-element predictive power analysis
- Weekly automated Slack report on qualification metrics
- Anomaly alerts for key metric degradations
- Monthly calibration review process

## Triggers

- Dashboard and funnel: set up once, viewed continuously
- Weekly report: runs every Monday via n8n cron
- Anomaly alerts: always-on monitoring
- Monthly calibration: manual trigger at month end
