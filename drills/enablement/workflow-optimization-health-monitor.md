---
name: workflow-optimization-health-monitor
description: Continuous monitoring of workflow suggestion system health, user efficiency trends, and optimization ROI
category: Enablement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
  - attio-reporting
---

# Workflow Optimization Health Monitor

This drill provides continuous visibility into whether the workflow optimization suggestion system is actually making users more efficient and retained. It tracks system health (are suggestions being generated and delivered?), user impact (are users adopting suggestions and becoming more efficient?), and business outcomes (is efficiency improvement correlated with retention and expansion?).

## Input

- `workflow-behavior-analysis`, `workflow-suggestion-delivery`, and `workflow-suggestion-personalization` drills all operational
- At least 12 weeks of suggestion delivery data in PostHog
- n8n instance for scheduled monitoring
- Attio for logging reports and alerts

## Steps

### 1. Build the workflow optimization dashboard

Using `posthog-dashboards`, create a dedicated dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Suggestion pipeline health | Number tiles | Suggestions generated, delivered, viewed, adopted this week |
| Acceptance rate trend | Line chart (12-week) | Overall suggestion adoption rate over time |
| Acceptance by category | Bar chart | Efficiency vs. discovery vs. automation adoption rates |
| Acceptance by segment | Heatmap | Maturity x pattern segment adoption rates |
| User efficiency trend | Line chart (12-week) | Median workflow completion time across all users |
| Feature discovery rate | Line chart (12-week) | % of available features used by median user |
| Suggestion-to-retention correlation | Scatter plot | Users who adopted suggestions vs. 30-day retention |
| Suggestion fatigue indicator | Line chart | Dismissal rate trend — rising dismissals signal fatigue |

### 2. Configure threshold alerts

Using `posthog-anomaly-detection` and `n8n-triggers`, set alerts for:

- **Acceptance rate drops below 15%** for 2 consecutive weeks: Suggestions may be irrelevant or delivery timing is wrong. Trigger: review suggestion quality and regenerate.
- **Dismissal rate exceeds 40%**: Users are fatigued. Trigger: reduce delivery frequency by 50% and increase confidence threshold.
- **Pipeline stall**: Zero suggestions generated for 3+ days. Trigger: check behavior analysis pipeline health and PostHog event flow.
- **Efficiency regression**: Median workflow time increases 10%+ for 2 consecutive weeks. Trigger: investigate whether a product change, user mix shift, or suggestion misfire caused it.
- **Segment imbalance**: One segment receives 3x more suggestions than others. Trigger: review segmentation pipeline for classification bias.

Route all alerts to the responsible team member. Alerts without owners get ignored.

### 3. Build the weekly optimization brief

Using `n8n-scheduling`, create a workflow that runs every Monday:

1. Query PostHog for the past week's suggestion metrics: generated, delivered, viewed, clicked, adopted, dismissed
2. Query efficiency metrics: median workflow time change, feature discovery rate change, power user cohort growth
3. Query retention correlation: 30-day retention rate for users who adopted 1+ suggestions vs. users who received but did not adopt
4. Calculate ROI: estimated time saved (sum of adopted suggestion benefits x user count) and retention lift
5. Generate the brief using Claude:
   - This week's key numbers (3-5 bullets)
   - What worked (top-performing suggestion and segment)
   - What did not (worst-performing suggestion and why)
   - Recommendation for next week (1 specific action)
6. Post the brief to Slack and log in Attio using `attio-notes`

### 4. Track long-term efficiency curves

Using `posthog-cohorts`, build monthly cohort analysis:

- For each monthly signup cohort, track: median workflow time at day 7, 30, 60, 90
- Compare cohorts that received workflow suggestions vs. those that did not (using the original feature flag control group)
- Measure: do suggestion-receiving cohorts reach power-user efficiency levels faster?

The target: users receiving suggestions should reach the power user efficiency benchmark 30% faster than users who do not.

### 5. Monitor suggestion quality decay

Suggestions generated from stale behavior analysis become irrelevant. Track:

- Average age of the behavior data used to generate each suggestion
- Correlation between data freshness and adoption rate
- Whether product changes (new features, UI updates) have invalidated existing suggestion templates

If adoption rate correlates negatively with data age (suggestions from older analysis perform worse), tighten the analysis refresh cadence.

### 6. Generate monthly executive report

Using `n8n-scheduling`, create a monthly workflow that compiles:

- Total users receiving suggestions, total suggestions delivered
- Aggregate adoption rate and trend
- Estimated efficiency improvement (hours saved per user per month)
- Retention impact (retention rate for adopters vs. non-adopters)
- Cost of the system (Claude API, Intercom messages, n8n compute)
- ROI: efficiency gain + retention value vs. system cost

Log the report in Attio using `attio-reporting` and distribute via email.

## Output

- Workflow optimization dashboard in PostHog (8 panels)
- 5 threshold alerts configured in n8n
- Weekly optimization brief (automated via n8n + Claude)
- Monthly cohort efficiency analysis
- Monthly executive ROI report

## Triggers

Dashboard is live and updated in real-time. Alerts fire continuously. Weekly brief generated every Monday via n8n cron. Monthly report generated on the 1st of each month.
