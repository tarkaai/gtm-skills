---
name: bant-qualification-reporting
description: Build qualification funnel dashboards and weekly reports tracking BANT scoring accuracy and pipeline health
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

# BANT Qualification Reporting

This drill builds the measurement layer for your BANT qualification play. It creates dashboards that track qualification funnel health, scoring accuracy, and pipeline velocity — so you can see whether your BANT process is actually producing qualified deals that close.

## Input

- PostHog project with BANT events being tracked (from `bant-scorecard-setup`)
- Attio CRM with deals flowing through BANT pipeline stages
- At least 2 weeks of qualification data for meaningful analysis

## Steps

### 1. Build the qualification funnel dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "BANT Qualification Funnel" with these panels:

**Panel 1 — Qualification volume (bar chart, weekly):**
- Count of `bant_score_created` events per week
- Breakdown by `verdict` (Qualified / Needs Work / Disqualified)
- Shows total throughput and qualification rate trend

**Panel 2 — Score distribution (histogram):**
- Distribution of `bant_composite_score` values across all scored deals
- Helps identify if your scoring model clusters too tightly (needs recalibration) or spreads well

**Panel 3 — Dimension breakdown (stacked bar):**
- Average scores for Budget, Authority, Need, Timeline per week
- Identifies which BANT dimension is consistently weakest across your pipeline

**Panel 4 — Pre-score vs. post-call accuracy (line chart):**
- Compare `bant_composite_score` at `bant_assessment_source = "Pre-call Enrichment"` vs. `bant_assessment_source = "Discovery Call"` for the same deals
- The gap between these lines measures enrichment accuracy. Closer = better pre-qualification.

### 2. Build the pipeline velocity funnel

Using the `posthog-funnels` fundamental, create a funnel:

```
bant_score_created → bant_qualification_passed → meeting_booked → proposal_sent → deal_closed_won
```

Measure:
- Conversion rate at each step
- Median time between steps
- Drop-off points (where deals stall)

Break down by `bant_verdict` to compare: do deals that scored "Qualified" actually convert better than "Needs Work" deals that were manually promoted?

### 3. Build scoring accuracy cohorts

Using the `posthog-cohorts` fundamental, create cohorts:

- **True Positives:** Deals scored Qualified that eventually closed won
- **False Positives:** Deals scored Qualified that closed lost or stalled
- **True Negatives:** Deals scored Disqualified that never converted
- **False Negatives:** Deals scored Disqualified that later came back and closed (through re-engagement or inbound)

Track these cohorts over time. The goal is to maximize True Positives + True Negatives and minimize False Positives + False Negatives.

Calculate: `Scoring Accuracy = (True Positives + True Negatives) / Total Scored Deals`

### 4. Set up weekly automated report via n8n

Using the `n8n-scheduling` fundamental, create a workflow that runs every Monday at 8am:

1. Query PostHog for last week's BANT metrics:
   - Total deals scored
   - Qualification rate (% scored Qualified)
   - Average composite score
   - Top-scoring deals (list top 5 by composite score)
   - Weakest dimension (lowest average across all deals)
2. Query Attio for pipeline health:
   - Deals in each BANT stage (count + total value)
   - Deals that moved forward this week
   - Deals that stalled (no activity for 7+ days)
3. Generate a text report summarizing the data
4. Post to Slack and store in Attio as a note on the "BANT Qualification" campaign record

### 5. Set up anomaly alerts

Configure PostHog alerts (or n8n monitors) for:

- **Qualification rate drops below 25%:** May indicate ICP drift or list quality degradation
- **Average composite score drops below 50:** Enrichment data may be stale or scoring formula needs recalibration
- **False positive rate exceeds 30%:** Scoring model is too generous — tighten thresholds
- **Zero deals scored for 3+ days:** Pipeline has dried up — check lead source health

Each alert triggers a Slack notification with the metric value and recommended diagnostic action.

### 6. Monthly calibration review

At the end of each month, run a calibration analysis:

1. Pull all deals closed this month (won and lost) from Attio
2. Compare their BANT scores at qualification time vs. their actual outcome
3. Calculate per-dimension accuracy: which dimension best predicts closed-won?
4. Adjust scoring weights if data shows a different weighting would improve accuracy
5. Document the calibration change and rationale in an Attio note

## Output

- PostHog dashboard with 4+ panels tracking qualification funnel health
- Pipeline velocity funnel showing conversion rates at each stage
- Scoring accuracy cohorts tracking true/false positive/negative rates
- Weekly automated Slack report on qualification metrics
- Anomaly alerts for key metric degradations
- Monthly calibration review process

## Triggers

- Dashboard and funnel: set up once, viewed continuously
- Weekly report: runs every Monday via n8n cron
- Anomaly alerts: always-on monitoring
- Monthly calibration: manual trigger at month end
