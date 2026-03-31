---
name: engagement-scoring-baseline
description: >
  User Engagement Scoring — Baseline Run. Deploy the engagement scoring pipeline as a daily
  automated workflow. Scores compute continuously, sync to CRM, and feed PostHog cohorts.
  First always-on scoring system running for 2+ weeks with stable accuracy.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=75% churn prediction accuracy: 75%+ of users who churn within 60 days were scored At Risk or Dormant 14 days prior"
kpis: ["Churn prediction accuracy (% of churners correctly flagged)", "Score stability (day-over-day variance < 15 points for stable users)", "CRM sync completion rate (100% of scored users written to Attio daily)"]
slug: "engagement-scoring"
install: "npx gtm-skills add product/retain/engagement-scoring"
drills:
  - engagement-score-computation
  - usage-drop-detection
  - dashboard-builder
---

# User Engagement Scoring — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Deploy the engagement scoring model from Smoke as a daily automated pipeline. Every morning, the n8n workflow computes engagement scores for all active users, writes them to Attio, updates PostHog cohorts, and detects tier changes. After 2 weeks of continuous operation, the system achieves 75%+ churn prediction accuracy: at least 75% of users who churn within 60 days were scored At Risk or Dormant 14 days before they left.

This is the first always-on automation. The agent builds and monitors the pipeline. Scoring runs daily without manual intervention.

## Leading Indicators

- The n8n scoring workflow executes successfully every day for 14+ consecutive days with zero failures
- Attio records update within 2 hours of the daily cron trigger
- PostHog `engagement_score_computed` events fire for every active user each day
- Score distributions remain stable day-over-day (no sudden shifts suggesting data pipeline issues)
- At least 3 of 5 tiers have users in them consistently
- Tier change events (`engagement_tier_changed`) fire when users move between tiers

## Instructions

### 1. Build the daily scoring automation

Run the `engagement-score-computation` drill step 5 to build the n8n workflow:

1. Create an n8n workflow triggered by a daily cron at 07:00 UTC
2. The workflow queries PostHog for all users with events in the last 30 days
3. For each user, compute the 4 dimension scores using the HogQL queries validated in Smoke
4. Calculate the composite engagement score and classify into tiers
5. Compare today's score to yesterday's stored score to compute trend (Rising / Stable / Declining)
6. Write all scores, tiers, and trends to Attio contact records using the `attio-custom-attributes` fundamental
7. Fire `engagement_score_computed` and `engagement_tier_changed` events to PostHog
8. Update the 5 dynamic PostHog cohorts (one per tier)

Test the workflow end-to-end: trigger manually, verify Attio records update, verify PostHog events fire, verify cohorts populate.

### 2. Set up usage drop detection

Run the `usage-drop-detection` drill to build the per-user engagement drop detector:

1. Configure the daily detection query that compares each user's last-7-day activity to their personal 30-day baseline
2. Classify drops into Watch (-30% to -50%), Alert (-50% to -80%), and Critical (below -80% or zero activity) tiers
3. Store risk data in Attio: `engagement_risk_tier`, `engagement_pct_change`, `engagement_alert_count`
4. Create PostHog cohorts for each risk tier: `usage-drop-watch`, `usage-drop-alert`, `usage-drop-critical`

This runs alongside the engagement score pipeline -- the score gives the absolute position, the drop detection gives the velocity of change.

### 3. Build the engagement scoring dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard with:

- **Score distribution:** Histogram of engagement scores across all active users
- **Tier breakdown:** Count and percentage of users in each tier, updated daily
- **Tier migration:** Sankey or table showing how many users moved between tiers this week
- **Dimension heatmap:** Average score per dimension, broken down by tier (shows which dimensions differentiate tiers)
- **Score trend:** 14-day moving average of the population mean engagement score
- **Drop detection:** Count of users in Watch, Alert, and Critical drop tiers this week

### 4. Monitor pipeline health for 2 weeks

For 14 consecutive days, verify:

- The n8n workflow completes without errors each morning
- The number of scored users matches the number of active users in PostHog (within 5%)
- Score distributions are stable (no sudden jumps suggesting query bugs)
- CRM sync is complete (spot-check 10 random Attio records against PostHog data)

If the workflow fails on any day, diagnose and fix before the next run. The 2-week clock restarts after any pipeline failure that causes missed or incorrect scores.

### 5. Evaluate against threshold

After 2 weeks of stable operation, run the back-test from `engagement-score-computation` step 8:

1. Pull users who churned in the last 60 days
2. Check their engagement scores from 14 days before churn
3. Calculate accuracy: (churners scored At Risk or Dormant) / (total churners)
4. Target: >= 75%

If PASS, the scoring model is accurate enough to drive automated interventions. Proceed to Scalable.

If FAIL, diagnose:
- Are the dimension weights wrong? (Re-run Smoke step 4 with fresh data)
- Are engagement events missing? (Audit PostHog instrumentation)
- Is the 14-day lookback too short? (Try 21-day or 30-day windows)

Iterate and re-run the 2-week baseline period.

## Time Estimate

- 4 hours: Build and test the n8n scoring workflow (step 1)
- 3 hours: Set up usage drop detection (step 2)
- 2 hours: Build the dashboard (step 3)
- 5 hours: Monitor and debug over 2 weeks (step 4)
- 2 hours: Run back-test and evaluate (step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event queries, cohorts, dashboard | Free tier: 1M events/mo. https://posthog.com/pricing |
| n8n | Daily scoring workflow automation | Free (self-hosted) or $20/mo (cloud). https://n8n.io/pricing |
| Attio | CRM storage for scores and tiers | Free tier: 3 users. https://attio.com/pricing |

## Drills Referenced

- `engagement-score-computation` -- the core scoring pipeline: daily computation, CRM sync, cohort updates
- `usage-drop-detection` -- per-user engagement drop detection with risk tier classification
- `dashboard-builder` -- PostHog dashboard construction for monitoring scoring health
