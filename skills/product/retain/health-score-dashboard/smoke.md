---
name: health-score-dashboard-smoke
description: >
  Account Health Scoring — Smoke Test. Manually build a health score model for your top 20 accounts
  using PostHog usage data and Attio records. Validate that the composite score correlates with
  known healthy and at-risk accounts before automating.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: "Score 20+ accounts and >=70% of known at-risk accounts correctly classified"
kpis: ["Score accuracy vs known outcomes", "Dimension signal quality", "Back-test churn correlation"]
slug: "health-score-dashboard"
install: "npx gtm-skills add product/retain/health-score-dashboard"
drills:
  - health-score-model-design
  - posthog-gtm-events
  - threshold-engine
---
# Account Health Scoring — Smoke Test

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Prove that a composite health score built from usage, engagement, support, and adoption signals actually predicts which accounts are healthy and which are at risk. At this level, you manually design the model, compute scores for your top 20 accounts, and validate against known outcomes (accounts you already know are thriving or struggling). No automation, no dashboards. Just proof that the signal exists.

**Pass threshold:** Score 20+ accounts AND >=70% of known at-risk accounts correctly classified as "At Risk" or "Critical" by the model.

## Leading Indicators

- Dimension signals load successfully from PostHog (usage data exists for all 20 accounts)
- Score distribution shows meaningful spread (not all accounts clustered at the same score)
- Known healthy accounts score above 70 and known struggling accounts score below 50
- At least 3 of the 4 dimensions contribute useful signal (one dimension being noisy is acceptable at Smoke)

## Instructions

### 1. Verify usage data exists in PostHog

Run the `posthog-gtm-events` drill to confirm your product is tracking the events needed for health scoring: session starts, feature usage events, key workflow completions, and user identification with company grouping. If PostHog Group Analytics is not enabled, enable it and pass `company_id` as a group property on all events.

Query PostHog to verify at least 30 days of account-level data exists:

```sql
SELECT properties.$group_0 AS company_id, count() AS total_events
FROM events
WHERE timestamp > now() - interval 30 day
  AND properties.$group_0 IS NOT NULL
GROUP BY company_id
ORDER BY total_events DESC
LIMIT 30
```

If fewer than 20 accounts have meaningful data, wait until you have enough history before proceeding.

### 2. Select your scoring cohort

Pull your top 20 accounts from Attio: active paying customers with at least 30 days of history. Intentionally include a mix: 5-6 accounts you know are thriving, 5-6 you know are struggling or at churn risk, and 8-10 you are uncertain about. The known accounts are your validation set.

**Human action required:** Review the 20 accounts and label each as "Known Healthy," "Known At-Risk," or "Unknown." Write these labels down before computing any scores. This prevents bias.

### 3. Design the health score model

Run the `health-score-model-design` drill, but execute it manually for these 20 accounts. For each account, compute:

**Usage dimension (weight 35%):** Query PostHog for weekly active users, session frequency, usage trend (last 2 weeks vs prior 2 weeks), and days since last login. Rank each account against the cohort on each signal. Average the percentile ranks. Multiply by 100 for a 0-100 dimension score.

**Engagement dimension (weight 25%):** Query PostHog for distinct features used in the last 30 days (breadth), average events per session (depth), number of distinct active users (collaboration), and help/docs page views (learning). Same percentile ranking approach.

**Support dimension (weight 20%):** Pull support ticket data from Intercom or your support tool. Count tickets, categorize as complaints vs feature requests, check resolution satisfaction. If you do not have structured support data yet, use a simplified version: ticket count only, where fewer tickets = healthier (score = 100 - percentile_rank(ticket_count) * 100).

**Adoption dimension (weight 20%):** Query PostHog for: has the account used each of your core features in the last 30 days? Has the account connected an integration? What percentage of invited users are active? Score each signal 0-100 and average.

Compute the composite: `health_score = usage * 0.35 + engagement * 0.25 + support * 0.20 + adoption * 0.20`

### 4. Validate against known outcomes

Compare computed scores to your pre-labeled accounts:

- Do all "Known Healthy" accounts score above 70?
- Do all "Known At-Risk" accounts score below 50?
- What percentage of your labeled accounts were correctly classified?

Target: >=70% of known at-risk accounts should land in the "At Risk" (40-59) or "Critical" (0-39) tiers.

If accuracy is below 70%, diagnose:
- Which dimension is producing the most noise? (Healthy accounts scoring low on it, or at-risk accounts scoring high)
- Are the weights wrong? Try adjusting: if usage is the strongest predictor, increase its weight to 40-45% and reduce others
- Are signals missing? If engagement scores are all similar, add more granular feature tracking

Iterate on weights and signals until accuracy reaches 70%.

### 5. Evaluate against threshold

Run the `threshold-engine` drill: did you score 20+ accounts AND achieve >=70% classification accuracy on known outcomes?

If PASS: Proceed to Baseline. You have validated that composite health scoring produces actionable signal. Document the final dimension weights, signals, and scoring functions.

If FAIL: Diagnose whether the issue is data quality (not enough events in PostHog), model design (wrong signals or weights), or sample bias (your "known" labels were inaccurate). Adjust and re-run.

## Time Estimate

- 2 hours: Verify PostHog data, select accounts, label known outcomes
- 3 hours: Query PostHog for each dimension, compute scores manually
- 1 hour: Validate against known outcomes, iterate on weights
- 1 hour: Document model design, evaluate threshold, prepare for Baseline
- 1 hour: Buffer for PostHog query troubleshooting

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage and engagement data queries | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Account records, labeling, score storage | Free tier or existing plan — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost:** Free

## Drills Referenced

- `health-score-model-design` — Defines the 4-dimension scoring model and scoring functions
- `posthog-gtm-events` — Verifies event tracking is in place for health score signals
- `threshold-engine` — Evaluates results against the pass threshold
