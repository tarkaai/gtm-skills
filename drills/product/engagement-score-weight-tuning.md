---
name: engagement-score-weight-tuning
description: Automatically recalibrate engagement score dimension weights by measuring prediction accuracy against actual churn and expansion outcomes
category: Product
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-custom-events
  - posthog-retention-analysis
  - posthog-dashboards
  - attio-custom-attributes
  - attio-contacts
  - n8n-workflow-basics
  - n8n-scheduling
  - hypothesis-generation
---

# Engagement Score Weight Tuning

This drill automates the process of recalibrating engagement score dimension weights. Instead of manually reviewing and adjusting weights quarterly, an agent runs a monthly back-test loop: compare predicted engagement tiers to actual outcomes (churn, expansion, status quo), compute the accuracy of each dimension's contribution, and adjust weights to maximize predictive power.

This is a play-specific companion to `autonomous-optimization`. While `autonomous-optimization` runs the broad detect-hypothesize-experiment-evaluate loop across all play KPIs, this drill focuses narrowly on keeping the scoring model itself accurate as user behavior evolves.

## Input

- At least 60 days of engagement scores computed and stored (from `engagement-score-computation`)
- Attio records with churn dates and expansion dates for outcome labeling
- PostHog with `engagement_score_computed` events containing dimension breakdowns
- n8n for scheduling the recalibration pipeline
- Anthropic API key for hypothesis generation when weights plateau

## Steps

### 1. Build the outcome-labeled dataset

Using `posthog-custom-events` and `attio-contacts`, create a labeled dataset of user outcomes:

For each user who was scored 60+ days ago, label their outcome as of today:

- **Churned:** User has no events in the last 30 days AND was active 60 days ago
- **Expanded:** User upgraded plan, added teammates, or increased usage volume by 50%+
- **Retained:** User is still active at similar or stable engagement levels
- **Declined:** User's engagement score dropped 20+ points but has not churned yet

Query PostHog for the engagement scores from 60 days ago and join with current status from Attio.

### 2. Measure dimension accuracy

For each of the four dimensions (frequency, breadth, depth, recency), measure how well it predicted outcomes:

```
For each dimension:
  1. Rank all users by that dimension's score 60 days ago
  2. Split into quartiles (top 25%, upper-mid, lower-mid, bottom 25%)
  3. Compute churn rate per quartile
  4. Compute a "separation score": churn_rate_bottom_quartile - churn_rate_top_quartile
  5. Higher separation = the dimension is more predictive of churn
```

A dimension with a separation score of 40% (bottom quartile churns at 50%, top at 10%) is highly predictive. A dimension with separation of 5% adds noise.

### 3. Compute optimal weights

Allocate weight proportional to each dimension's predictive power:

```
raw_weight[dim] = separation_score[dim]
total = sum(raw_weight for all dims)
new_weight[dim] = raw_weight[dim] / total
```

Apply constraints:
- No single dimension gets more than 40% weight
- No dimension drops below 10% weight
- Weights must sum to 1.0

Compare new weights to current weights. If the change is less than 3% on every dimension, the model is stable -- no update needed.

### 4. Simulate the new weights

Before deploying new weights, back-test them:

1. Recompute engagement scores for all users using the new weights applied to historical dimension scores
2. Measure: would the new weights have correctly identified more churners as At Risk or Dormant?
3. If new-weight accuracy > current-weight accuracy by 5%+ points, adopt the new weights
4. If improvement is less than 5%, keep current weights (avoid unnecessary model churn)

### 5. Deploy updated weights

If the new weights pass simulation:

1. Update the weight configuration in the `engagement-score-computation` n8n workflow
2. Log the change in Attio as a note on a "Scoring Model" record:
   - Previous weights
   - New weights
   - Separation scores per dimension
   - Accuracy improvement (old vs new)
   - Date of change
3. Fire a PostHog event `engagement_score_weights_updated` with the old and new weights

### 6. Handle edge cases with AI hypothesis generation

When the model plateaus (no weight adjustment improves accuracy for 2 consecutive months), use `hypothesis-generation` to diagnose:

- Are there new user behaviors not captured by the current 4 dimensions?
- Has the product changed in a way that invalidates existing signals?
- Is the user base composition shifting (more enterprise, more self-serve)?

The agent generates 3 hypotheses for why the model stopped improving, each with a concrete action: add a new dimension, change the event taxonomy, or segment the model by user type.

### 7. Build the recalibration dashboard

Using `posthog-dashboards`, add panels to the engagement scoring dashboard:

- **Weight history:** Line chart showing dimension weights over time (should converge)
- **Prediction accuracy:** Monthly accuracy rate (% of At Risk/Dormant users who actually churned within 60 days)
- **False positive rate:** % of At Risk/Dormant users who did NOT churn (lower is better)
- **Dimension separation scores:** Bar chart of current separation scores per dimension

## Output

- Monthly automated weight recalibration pipeline in n8n
- Back-test simulation before deploying weight changes
- Audit trail of every weight change with accuracy metrics
- AI-powered hypothesis generation when the model plateaus
- Dashboard panels tracking model health over time

## Triggers

- Monthly recalibration: n8n cron, 1st of each month at 06:00 UTC
- On-demand recalibration: webhook trigger for manual runs
- Plateau detection: after 2 consecutive months with no improvement, escalate to hypothesis generation
