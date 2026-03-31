---
name: expansion-scoring-pipeline
description: Automated scoring pipeline that combines usage proximity, growth velocity, engagement depth, and firmographics to rank expansion opportunities for sales prioritization
category: Deal Management
tools:
  - PostHog
  - Attio
  - Clay
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-anomaly-detection
  - attio-custom-attributes
  - attio-lists
  - attio-deals
  - clay-company-search
  - clay-scoring
  - n8n-scheduling
  - n8n-workflow-basics
  - n8n-triggers
---

# Expansion Scoring Pipeline

This drill builds an automated scoring system that continuously ranks accounts by expansion readiness. It replaces the manual qualification from Smoke with a pipeline that runs daily, combines four signal categories, and surfaces a prioritized expansion queue for the sales team.

## Input

- PostHog tracking usage events per account (metered resources, feature adoption, engagement)
- Attio CRM with account records
- Clay workspace for firmographic enrichment
- n8n instance for scheduled pipeline runs

## Steps

### 1. Define the four signal categories

The expansion score is a weighted composite of four categories:

**Category 1: Usage Proximity (40% weight)**
How close is the account to plan limits?

| Signal | Score |
|--------|-------|
| Any resource at 95%+ of limit | 40 |
| Any resource at 85-94% | 30 |
| Any resource at 70-84% | 15 |
| Multiple resources at 70%+ | +10 per additional resource |
| Consumption velocity increasing (rate grew 20%+ in 30 days) | +10 |
| Projected to hit limit within current billing period | +15 |

Query via PostHog using `posthog-custom-events`:

```sql
SELECT
  properties.account_id AS account_id,
  max(properties.current_count / properties.plan_limit * 100) AS max_pct_used,
  count(DISTINCT properties.resource_type) AS resources_near_limit,
  -- velocity: compare last 7 days consumption rate vs prior 7 days
  sum(CASE WHEN timestamp > now() - interval 7 day THEN 1 ELSE 0 END) /
    greatest(sum(CASE WHEN timestamp BETWEEN now() - interval 14 day AND now() - interval 7 day THEN 1 ELSE 0 END), 1) AS velocity_ratio
FROM events
WHERE event = 'resource_consumed'
  AND timestamp > now() - interval 14 day
  AND properties.plan_limit > 0
  AND properties.current_count / properties.plan_limit >= 0.7
GROUP BY account_id
```

**Category 2: Growth Velocity (30% weight)**
Is the account's usage trajectory trending up?

| Signal | Score |
|--------|-------|
| Weekly active users grew 25%+ in last 30 days | 30 |
| New seats added in last 30 days | 20 |
| New projects or workspaces created in last 14 days | 15 |
| API key created (new integration) | 10 |
| Admin visited billing page in last 14 days | 25 |
| Admin visited pricing comparison page | 20 |

Query via PostHog. Create a growth velocity score per account by counting qualifying events with decay weighting.

**Category 3: Engagement Depth (20% weight)**
Is the account deeply embedded in the product?

| Signal | Score |
|--------|-------|
| Daily active usage (used product 5+ of last 7 days) | 25 |
| Using advanced features (API, integrations, automations) | 20 |
| Multiple active users (3+ users active in last 7 days) | 15 |
| Feature adoption breadth (using 60%+ of available features) | 15 |
| Time in product trending up (session duration grew 20%+ in 30 days) | 10 |

Deep engagement signals that the account relies on the product and will be receptive to expansion rather than cancellation.

**Category 4: Firmographic Fit (10% weight)**
Does the account match your expansion ICP?

| Signal | Score |
|--------|-------|
| Company headcount 50+ employees | 15 |
| Recent funding round (last 12 months) | 15 |
| Industry vertical match (top-performing expansion verticals) | 10 |
| Tech stack signals (using complementary tools) | 10 |
| Company headcount growing (10%+ in last 6 months) | 10 |

Pull via Clay using `clay-company-search` and `clay-scoring`. Cache firmographic data in Attio — refresh monthly, not daily.

### 2. Compute the composite expansion score

Build the scoring computation in n8n using `n8n-workflow-basics`:

```
expansion_score = (
  usage_proximity_score * 0.40 +
  growth_velocity_score * 0.30 +
  engagement_depth_score * 0.20 +
  firmographic_fit_score * 0.10
)
```

Normalize each category to 0-100 before applying weights. The composite score ranges from 0-100.

### 3. Classify into expansion tiers

Using `posthog-cohorts`, create three dynamic cohorts:

- **Tier 1 — Sales-ready (score >= 65):** Immediate outreach. Create expansion deal if one does not exist. These accounts have strong usage signals, are growing, and match the expansion ICP.
- **Tier 2 — Watch (score 40-64):** Monitor weekly. Add to expansion nurture list in Attio. Send a single warm touch if usage hits 85%+.
- **Tier 3 — Self-serve (score < 40):** Route to automated upgrade prompts. Do not involve sales.

### 4. Store scores and trigger outreach

Using `attio-custom-attributes`, store per-account:

- `expansion_score`: the composite 0-100 score
- `expansion_tier`: tier_1 | tier_2 | tier_3
- `expansion_score_updated`: timestamp of last computation
- `expansion_top_signal`: the highest-weight signal driving the score
- `expansion_projected_value`: estimated expansion ARR

Using `attio-lists`, maintain:
- "Expansion — Sales Ready" (Tier 1 accounts)
- "Expansion — Watch List" (Tier 2 accounts)

Using `attio-deals`, automatically create expansion deals for Tier 1 accounts that do not already have one. Include the score breakdown and top signals in the deal notes.

Using `n8n-triggers`, fire a webhook to the `expansion-outreach-sequence` drill when a new Tier 1 account is identified or when a Tier 2 account crosses into Tier 1.

### 5. Build the scheduled pipeline

Using `n8n-scheduling`, create a workflow that runs daily at 07:00 UTC:

1. Query PostHog for usage proximity scores (Category 1)
2. Query PostHog for growth velocity scores (Category 2)
3. Query PostHog for engagement depth scores (Category 3)
4. Query Attio for cached firmographic scores (Category 4, refreshed monthly via Clay)
5. Compute composite scores
6. Update Attio records
7. Identify tier transitions (accounts that moved up or down)
8. For new Tier 1 accounts: create deals and fire outreach webhook
9. For accounts that dropped from Tier 1 to Tier 2: flag for review (usage may have decreased — do not continue outreach)
10. Log the pipeline run metrics: total accounts scored, tier distribution, new Tier 1 count

### 6. Track scoring accuracy

Using `posthog-custom-events`, log every scoring event:

```javascript
posthog.capture('expansion_score_computed', {
  account_id: accountId,
  expansion_score: 78,
  tier: 'tier_1',
  usage_proximity_score: 85,
  growth_velocity_score: 70,
  engagement_depth_score: 65,
  firmographic_fit_score: 50,
  top_signal: 'api_calls_at_92_pct'
});
```

After 60 days, measure: of Tier 1 accounts, what percentage resulted in a closed expansion deal within 30 days? Target: 35%+ close rate. If below 25%, the scoring weights need recalibration. Run a correlation analysis between individual signals and actual expansion outcomes to find the highest-predictive signals.

## Output

- Daily automated expansion scoring pipeline running in n8n
- Three PostHog cohorts (Tier 1, Tier 2, Tier 3) updated daily
- Attio records enriched with composite expansion scores and tier assignments
- Automatic deal creation and outreach triggering for Tier 1 accounts
- Scoring accuracy tracking for ongoing calibration

## Triggers

Runs daily at 07:00 UTC via n8n cron. Firmographic data refreshed monthly via Clay. Scoring weights recalibrated quarterly based on actual conversion data. On-demand rescoring available via webhook for individual accounts.
