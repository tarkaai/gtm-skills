---
name: churn-prediction-model-smoke
description: >
  AI Churn Prediction — Smoke Test. Extract behavioral signals from PostHog usage data, score
  churn risk with an LLM, and validate that the model identifies the top 20% at-risk users.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Predict top 20% at risk"
kpis: ["Prediction accuracy", "Churn rate", "Intervention success"]
slug: "churn-prediction-model"
install: "npx gtm-skills add product/retain/churn-prediction-model"
drills:
  - churn-signal-extraction
  - threshold-engine
---

# AI Churn Prediction — Smoke Test

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Prove the concept: can you extract behavioral signals from PostHog and score churn risk accurately enough to identify the top 20% most at-risk users? No automation, no always-on. Just a single agent run that produces a ranked list of at-risk users and validates against known churn outcomes.

## Leading Indicators

- Signal extraction query returns data for 80%+ of active users (data coverage)
- Risk scores distribute across all 4 tiers (not clustered in one tier)
- At least 3 of the top 10 scored users match known recent churners or users with open cancellation requests

## Instructions

### 1. Verify PostHog data readiness

Confirm your PostHog project has at least 30 days of tracked user events. Check that the following event types exist:
- Core feature usage events (whatever actions indicate healthy engagement in your product)
- Login/session events
- Support ticket or help article view events (if instrumented)
- Billing/pricing page view events

Run this verification query via PostHog API or MCP:
```
SELECT event, count() FROM events WHERE timestamp > now() - interval 30 day GROUP BY event ORDER BY count() DESC LIMIT 20
```

If fewer than 3 meaningful event types exist, instrument tracking first using the `posthog-custom-events` fundamental before proceeding.

### 2. Define your healthy usage baseline

Before scoring risk, define what "healthy" looks like. Query your retained users (active for 60+ days, still active in the last 7 days):
- Average events per week
- Average distinct feature types used per month
- Typical login frequency

Document these numbers. They become the reference point for the scoring model.

### 3. Extract churn signals

Run the `churn-signal-extraction` drill in manual mode. This extracts per-user behavioral signals from PostHog: activity decay rate, feature abandonment, login gaps, engagement breadth, and more. The drill outputs a signal vector per user.

**Human action required:** Review the signal vectors for 10 users you know well. Do the signals match your intuition about those users' engagement levels? If the data looks wrong, fix the extraction queries before proceeding.

### 4. Score churn risk

The `churn-signal-extraction` drill passes each user's signal vector to the `churn-score-computation` fundamental, which uses Claude to produce a risk score (0-100) with a risk tier, primary signal, and reasoning.

Review the scored output. Check:
- Do the scores distribute reasonably? (Not all users in one tier)
- Do the explanations make sense? (The "primary_signal" and "reasoning" fields should be coherent)
- Are there obvious false positives? (Healthy users scored high-risk)

### 5. Validate against known outcomes

Compare the model's predictions against reality. Pull a list of users who actually churned in the last 30 days. Check how many of them the model would have flagged as high-risk or critical-risk.

Run the `threshold-engine` drill to evaluate: did the model correctly identify the top 20% most at-risk users? The pass threshold is that at least 60% of actual churners appear in the model's top 20% risk tier.

### 6. Document and decide

Record:
- Total users scored
- Distribution across risk tiers
- Validation accuracy (% of actual churners caught in top 20%)
- False positive rate (% of top 20% who did not actually churn)
- Top 3 most predictive signals for your product

If PASS (top 20% catches 60%+ of churners), proceed to Baseline. If FAIL, examine which churners were missed, identify which signals were absent for them, and re-run with adjusted signal definitions.

## Time Estimate

- 1 hour: verify PostHog data and define healthy usage baseline
- 1.5 hours: run signal extraction and review output
- 1 hour: score users and review risk distributions
- 1 hour: validate against known churn outcomes
- 0.5 hours: document findings and decide next steps

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data extraction, cohort analysis | Free tier up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Churn risk scoring | ~$0.01-0.03/user scored ($3/$15 per 1M input/output tokens) — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated cost for Smoke: Free** (PostHog free tier + <$5 in API calls for a single scoring run)

## Drills Referenced

- `churn-signal-extraction` — extracts behavioral signals from PostHog and scores each user's churn risk
- `threshold-engine` — evaluates whether the prediction accuracy meets the pass threshold
