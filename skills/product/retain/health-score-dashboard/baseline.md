---
name: health-score-dashboard-baseline
description: >
  Account Health Scoring — Baseline Run. Automate daily health score computation for all accounts
  via n8n, sync scores to Attio, and build a PostHog dashboard. First always-on automation.
  Validate that the model maintains >=80% accuracy over 2 weeks.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=80% churn prediction accuracy maintained for 2 consecutive weeks with daily automated scoring"
kpis: ["Churn prediction accuracy", "Score refresh reliability (daily uptime)", "Risk level distribution stability", "Dimension signal coverage"]
slug: "health-score-dashboard"
install: "npx gtm-skills add product/retain/health-score-dashboard"
drills:
  - health-score-model-design
  - posthog-gtm-events
  - dashboard-builder
  - threshold-engine
---
# Account Health Scoring — Baseline Run

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Take the manually validated health score model from Smoke and automate it. Build a daily n8n pipeline that scores all customer accounts, syncs results to Attio, and populates a PostHog dashboard with health trends. Prove the automated scoring maintains >=80% accuracy over 2 weeks of continuous operation.

**Pass threshold:** >=80% churn prediction accuracy maintained for 2 consecutive weeks with daily automated scoring running without manual intervention.

## Leading Indicators

- Daily scoring pipeline completes within 15 minutes and covers 100% of active accounts
- Health score distribution is stable day-over-day (no wild swings caused by data issues)
- PostHog dashboard shows meaningful score trends across the account base
- At least 2 accounts that move from Monitor to At Risk are confirmed as genuinely struggling (not false positives)
- Score refresh runs daily without errors for 14 consecutive days

## Instructions

### 1. Automate the scoring pipeline

Run the `health-score-model-design` drill's step 6 (build the scoring pipeline in n8n) to create the daily automated workflow:

1. Create an n8n workflow triggered by a daily cron at 06:00 UTC
2. Query Attio for all active customer company records
3. For each account, query PostHog for the 4 dimension signals:
   - Usage: weekly active users, session frequency, usage trend, login gap
   - Engagement: feature breadth, events per session, active user count, content consumption
   - Support: ticket volume and sentiment (query Intercom or your support tool API)
   - Adoption: core feature coverage, integration status, team penetration, milestone completion
4. Compute dimension scores using percentile ranking against the full customer base
5. Compute composite score with the weights validated at Smoke level
6. Classify risk level (Healthy/Monitor/At Risk/Critical) and trend (Improving/Stable/Declining)
7. Write all scores to Attio using `attio-health-score-sync`
8. Log each computation as a PostHog event (`health_score_computed`) for trend analysis

Test the pipeline end-to-end by running it manually once. Verify scores match your Smoke-level manual calculations for 5 accounts (tolerance: +/- 5 points).

### 2. Set up the health score event tracking layer

Run the `posthog-gtm-events` drill to formalize the event taxonomy for health scoring:

- `health_score_computed` — fired daily per account, properties: company_id, health_score, risk_level, usage_score, engagement_score, support_score, adoption_score, trend
- `health_risk_level_changed` — fired when an account moves between risk tiers, properties: company_id, old_level, new_level, old_score, new_score, primary_dimension_change
- `health_score_pipeline_completed` — fired once per daily run, properties: accounts_scored, average_score, risk_distribution, errors

These events power the dashboard and enable longitudinal analysis.

### 3. Build the health score dashboard

Run the `dashboard-builder` drill to create a "Customer Health" PostHog dashboard with these panels:

1. **Overall health distribution:** Pie chart showing percentage of accounts in each risk tier (Healthy/Monitor/At Risk/Critical). Updated daily.
2. **Health score trend:** Line chart showing average health score across all accounts over the last 8 weeks. Add threshold lines at 80 (Healthy) and 40 (Critical).
3. **Risk tier migration:** Stacked area chart showing how many accounts are in each risk tier over time. Healthy accounts should grow, Critical should shrink.
4. **Dimension breakdown:** Bar chart comparing average scores across the 4 dimensions. Reveals which dimension is weakest across the base.
5. **At-risk account table:** Table listing all accounts currently At Risk or Critical, sorted by score ascending, showing: company name, score, risk level, worst dimension, trend, days at current risk level.
6. **Score change leaderboard:** Table showing the 10 accounts with the biggest score changes (up or down) in the last 7 days.

### 4. Validate automated accuracy

After 1 week of automated scoring, validate:

1. Pull the list of accounts that churned, downgraded, or had support escalations in the past week
2. Check whether the health score model flagged them as At Risk or Critical before the event occurred
3. Calculate accuracy: (correctly flagged) / (total negative events) * 100
4. Target: >=80% of accounts that experienced negative outcomes were scored At Risk or Critical before the event

Also check for false positives: pull all accounts scored At Risk or Critical that did NOT experience any negative outcomes. If false positive rate exceeds 30%, the model is too aggressive — adjust the scoring thresholds or dimension weights.

### 5. Monitor pipeline reliability

Over 2 weeks, track:
- Did the pipeline run every day? (target: 14/14 days)
- Did it complete without errors? (target: >=12/14 days with no errors)
- Did it cover all accounts? (target: 100% of active accounts scored daily)
- Is the score distribution stable? (no day-to-day swings >10 points in the average)

### 6. Evaluate against threshold

Run the `threshold-engine` drill: did the automated scoring achieve >=80% churn prediction accuracy for 2 consecutive weeks?

If PASS: Proceed to Scalable. Document the production model weights, scoring functions, and any adjustments made. The health score system is now an always-on, validated tool.

If FAIL: Diagnose — is the issue accuracy (model needs better signals or weight tuning), reliability (pipeline errors or data gaps), or coverage (some accounts missing data)? Fix and re-run for another 2-week evaluation period.

## Time Estimate

- 6 hours: Build and test the n8n scoring pipeline
- 4 hours: Set up PostHog events and build the dashboard
- 2 hours: Run initial validation against known outcomes
- 4 hours: Monitor over 2 weeks, fix pipeline errors, tune thresholds
- 2 hours: Run accuracy validation and evaluate threshold
- 2 hours: Document model and prepare for Scalable

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data, dashboards, event logging | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Account records, score storage | Free tier or existing plan — [attio.com/pricing](https://attio.com/pricing) |
| n8n | Daily scoring pipeline automation | Self-hosted free or Cloud from EUR 20/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** Free (using free tiers and self-hosted n8n) to ~$20/mo (n8n cloud)

## Drills Referenced

- `health-score-model-design` — Automates the scoring pipeline that was manually validated at Smoke
- `posthog-gtm-events` — Formalizes the health score event taxonomy in PostHog
- `dashboard-builder` — Creates the Customer Health PostHog dashboard
- `threshold-engine` — Evaluates accuracy against the pass threshold
