---
name: engagement-scoring-smoke
description: >
  User Engagement Scoring — Smoke Test. Define the engagement event taxonomy, build the scoring
  model, and compute scores for all active users in a single manual run to validate the model
  produces meaningful tier separations before investing in automation.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Score all active users with tier separation: top-quartile churn rate < 10%, bottom-quartile churn rate > 30%"
kpis: ["Score distribution across 5 tiers", "Tier-churn correlation (top vs bottom quartile)", "Dimension coverage (all 4 dimensions producing non-zero scores)"]
slug: "engagement-scoring"
install: "npx gtm-skills add product/retain/engagement-scoring"
drills:
  - engagement-score-computation
  - posthog-gtm-events
---

# User Engagement Scoring — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Score every active user (anyone with at least 1 event in the last 30 days) on a 0-100 composite engagement scale. Validate that the scoring model separates users meaningfully: users in the top engagement quartile should have a churn rate under 10% while users in the bottom quartile should have a churn rate above 30% when back-tested against the last 60 days of churn data.

This is a one-time manual run. No automation, no always-on pipelines. The agent computes scores locally and validates the model has predictive signal before investing in infrastructure.

## Leading Indicators

- All 4 dimension scores (frequency, breadth, depth, recency) produce a non-degenerate distribution (not all zeros, not all 100s)
- The 5-tier classification (Power User / Engaged / Casual / At Risk / Dormant) has users in at least 3 tiers
- Spot-checking the top 10 and bottom 10 scored users matches intuition about who is engaged vs disengaged
- At least 50% of known recent churners (if any) would have scored in the At Risk or Dormant tier 14 days before they left

## Instructions

### 1. Verify event tracking coverage

Run the `posthog-gtm-events` drill to audit your current PostHog event instrumentation. Identify the 5-10 events that represent intentional, value-creating user behavior in your product. Document them in a `engagement_events.json` file:

```json
{
  "core_events": ["feature_used", "content_created", "report_exported", "teammate_invited", "integration_connected"],
  "moderate_events": ["settings_configured", "docs_viewed", "dashboard_visited"],
  "total_trackable_features": 8
}
```

If critical engagement events are not yet tracked in PostHog, instrument them now using the `posthog-custom-events` fundamental. Do not proceed until the events are firing correctly -- verify by triggering each event manually and confirming it appears in PostHog's live events stream.

**Human action required:** Review the event list. Confirm these are the actions that genuinely indicate a user is getting value from the product. Remove vanity metrics (page views, passive logins).

### 2. Compute engagement scores for all users

Run the `engagement-score-computation` drill steps 1-4 manually. Execute the four HogQL queries against PostHog to compute dimension scores for every active user:

- **Frequency (30%):** Active days in the last 14 days, normalized against a 10-day target
- **Breadth (25%):** Distinct feature events used, normalized against total trackable features
- **Depth (25%):** Events per session and average session duration, normalized against target thresholds
- **Recency (20%):** Days since last core action, decaying from 100 (today) to 0 (10+ days)

Compute the composite score: `frequency * 0.30 + breadth * 0.25 + depth * 0.25 + recency * 0.20`

Classify each user into a tier: Power User (80-100), Engaged (60-79), Casual (40-59), At Risk (20-39), Dormant (0-19).

### 3. Validate the score distribution

Check the output for quality signals:

- **Distribution shape:** Plot or summarize the histogram. A healthy model produces a roughly normal or bimodal distribution. If 90%+ of users cluster in one tier, the thresholds or weights need adjustment.
- **Dimension independence:** Check that the four dimension scores are not perfectly correlated. If frequency and recency produce identical rankings, one of them is redundant -- consider replacing it with a different signal.
- **Face validity:** Pull the top 10 scored users and the bottom 10. Do the top 10 look like your most engaged power users? Do the bottom 10 look like users who are drifting away? If not, adjust dimension weights.

### 4. Back-test against churn data

If you have users who churned in the last 60 days:

1. Pull their engagement dimension data from 14 days before churn
2. Compute what their engagement score would have been
3. Check: would 50%+ of them have been classified as At Risk or Dormant?
4. If yes, the model has baseline predictive value -- PASS
5. If no, the model needs iteration: try different event weights, add or remove events, adjust tier thresholds

If you do not have churn data yet, validate using the score distribution and face validity checks from step 3. The back-test becomes mandatory at Baseline level once you have 60+ days of scoring history.

**Human action required:** Review the back-test results. Decide whether the score separations are strong enough to act on. If the model correctly identifies at-risk users, approve proceeding to Baseline.

## Time Estimate

- 1 hour: Audit and document engagement events (step 1)
- 2 hours: Run HogQL queries and compute scores (step 2)
- 1 hour: Validate distribution and face validity (step 3)
- 1 hour: Back-test against churn data and iterate weights (step 4)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, HogQL queries, user data | Free tier: 1M events/mo. https://posthog.com/pricing |

## Drills Referenced

- `engagement-score-computation` -- defines the scoring model, dimension queries, and tier classification
- `posthog-gtm-events` -- audits and configures PostHog event tracking for the engagement taxonomy
