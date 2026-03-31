---
name: need-assessment-reporting
description: Build need assessment dashboards and weekly reports tracking need scoring accuracy, pattern analysis, and pipeline health
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

# Need Assessment Reporting

This drill builds the measurement layer for your need assessment play. It creates dashboards that track need scoring accuracy, need pattern distribution, hypothesis-to-discovery calibration, and pipeline health — so you can see whether your need assessment process is producing qualified deals that close.

## Input

- PostHog project with need assessment events being tracked (from `need-scorecard-setup`)
- Attio CRM with deals flowing through need assessment pipeline stages
- At least 2 weeks of need assessment data for meaningful analysis

## Steps

### 1. Build the need assessment funnel dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Need Assessment Funnel" with these panels:

**Panel 1 — Assessment volume (bar chart, weekly):**
- Count of `need_assessment_completed` events per week
- Breakdown by `need_tier` (High Need / Medium Need / Low Need)
- Shows throughput and qualification rate trend

**Panel 2 — Need category heatmap (table):**
- Average severity score per need category across all assessed deals
- Breakdown by ICP segment
- Identifies which needs resonate most by segment and which categories rarely surface

**Panel 3 — Score distribution (histogram):**
- Distribution of `need_total_score` values across all assessed deals
- Helps identify if scoring clusters too tightly (needs recalibration) or spreads well

**Panel 4 — Hypothesis accuracy (line chart):**
- Compare `need_total_score` at `need_assessment_source = "Pre-call Hypothesis"` vs. `need_assessment_source = "Discovery Call"` for the same deals
- The gap between these lines measures how well enrichment-based hypotheses predict actual needs
- Trend this weekly to track whether hypothesis accuracy improves over time

**Panel 5 — Critical need identification rate (line chart):**
- Percentage of assessed deals with >=2 Critical needs per week
- This is your primary signal for whether you are targeting the right prospects

### 2. Build the pipeline velocity funnel

Using the `posthog-funnels` fundamental, create a funnel:

```
need_hypothesis_generated → need_assessment_completed → need_qualified → demo_booked → proposal_sent → deal_closed_won
```

Measure:
- Conversion rate at each step
- Median time between steps
- Drop-off points (where deals stall)

Break down by `need_tier` to compare: do High Need deals convert better than Medium Need deals that were nurtured up?

### 3. Build need scoring accuracy cohorts

Using the `posthog-cohorts` fundamental, create cohorts:

- **True Positives:** Deals scored High Need that eventually closed won
- **False Positives:** Deals scored High Need that closed lost or stalled
- **True Negatives:** Deals scored Low Need that never converted
- **False Negatives:** Deals scored Low Need that later came back and closed

Track these cohorts over time. Calculate:
`Scoring Accuracy = (True Positives + True Negatives) / Total Assessed Deals`

### 4. Build need pattern analysis

Create a PostHog insight that shows:
- **Winning need combinations:** Which 2-3 need categories, when all scored Critical, produce the highest win rate?
- **Deal size correlation:** Do deals with more Critical needs close at higher ACV?
- **Speed correlation:** Do High Need deals close faster than Medium Need deals?

This analysis feeds back into the scoring model — if certain need combinations are stronger predictors than raw total score, adjust qualification criteria accordingly.

### 5. Set up weekly automated report via n8n

Using the `n8n-scheduling` fundamental, create a workflow that runs every Monday at 8am:

1. Query PostHog for last week's need assessment metrics:
   - Total deals assessed
   - Qualification rate (% meeting minimum threshold)
   - Average total need score
   - Top-scoring deals (top 5 by need score)
   - Most common Critical need category
   - Least common need category (potential discovery gap)
2. Query Attio for pipeline health:
   - Deals in each need assessment stage (count + total value)
   - Deals that moved forward this week
   - Deals stalled in "Need Assessed" for 7+ days without next step
3. Query hypothesis accuracy:
   - Average delta between hypothesis score and post-call score
   - Which need categories have the biggest hypothesis error
4. Generate a text report summarizing the data
5. Post to Slack and store in Attio as a note on the "Need Assessment" campaign record

### 6. Set up anomaly alerts

Configure PostHog alerts (or n8n monitors) for:

- **Qualification rate drops below 40%:** May indicate ICP drift or targeting wrong prospects
- **Average need score drops below 10:** Prospects are not experiencing the problems you solve at meaningful severity
- **Hypothesis accuracy degrades (delta > 5 points):** Enrichment signals may be stale or need category definitions need updating
- **Zero assessments for 3+ days:** Pipeline has dried up — check lead source health
- **Critical need concentration:** If >80% of Critical needs cluster in one category, you may be over-indexing on one value prop

Each alert triggers a Slack notification with the metric value and recommended diagnostic action.

### 7. Monthly calibration review

At the end of each month:

1. Pull all deals closed this month (won and lost) from Attio
2. Compare their need scores at assessment time vs. actual outcome
3. Calculate: which need categories best predict closed-won? Which are noise?
4. Adjust need category weights or definitions if data shows certain needs are stronger predictors
5. Update qualification thresholds if the data warrants it
6. Document the calibration change and rationale in an Attio note

## Output

- PostHog dashboard with 5+ panels tracking need assessment funnel health
- Pipeline velocity funnel showing conversion rates at each stage
- Scoring accuracy cohorts tracking true/false positive/negative rates
- Need pattern analysis identifying winning need combinations
- Weekly automated Slack report on need assessment metrics
- Anomaly alerts for key metric degradations
- Monthly calibration review process

## Triggers

- Dashboard and funnel: set up once, viewed continuously
- Weekly report: runs every Monday via n8n cron
- Anomaly alerts: always-on monitoring
- Monthly calibration: manual trigger at month end
