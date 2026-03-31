---
name: support-churn-correlation
description: Correlate support ticket patterns with actual churn events to validate and tune churn prediction from support data
category: Product
tools:
  - PostHog
  - Anthropic
  - Attio
  - n8n
fundamentals:
  - ticket-churn-signal-scoring
  - posthog-cohorts
  - posthog-funnels
  - attio-deals
  - n8n-triggers
---

# Support-Churn Correlation

This drill connects support ticket patterns with actual churn outcomes to validate which ticket signals genuinely predict churn and to score accounts for churn risk based on their support history.

## Input

- Classified ticket data from `support-ticket-analysis` drill
- At least 30 days of ticket data (90 days preferred for statistical validity)
- Churn events in PostHog or Attio (subscription_cancelled, account_churned, downgrade_completed)
- n8n instance for scheduling

## Steps

### 1. Build the churned-vs-retained dataset

Use the `posthog-cohorts` fundamental to create two cohorts:

- **Churned cohort**: Users/accounts that cancelled or downgraded in the analysis period. Pull from PostHog events (`subscription_cancelled`) or Attio deal stage changes.
- **Retained cohort**: Users/accounts active throughout the same period who did NOT cancel.

For each cohort member, attach their ticket summary from the `support-ticket-analysis` drill output: ticket count, categories, severities, CSAT, repeat issues, sentiment trend.

### 2. Compare ticket patterns between cohorts

Analyze the differences:

- **Volume**: Do churned accounts file more tickets? Calculate median tickets/month for churned vs retained.
- **Category mix**: Which categories are over-represented in churned accounts? (e.g., if 60% of churned accounts had billing tickets vs 15% of retained, billing tickets are a strong signal)
- **Severity**: Are churned accounts filing more critical/high tickets?
- **Resolution time**: Did churned accounts wait longer for resolution?
- **CSAT**: What is the average CSAT for churned vs retained?
- **Repeat issues**: Do churned accounts have more repeat issues?
- **Trajectory**: Did churned accounts show increasing ticket volume before cancellation?

### 3. Identify the strongest churn predictors

Rank ticket signals by predictive power. Calculate for each signal:
- **Lift**: How much more likely is churn when this signal is present vs absent?
- **Coverage**: What % of churned accounts exhibited this signal?
- **False positive rate**: What % of retained accounts also exhibited this signal?

A strong predictor has high lift (>2x), decent coverage (>30% of churned accounts), and low false positive rate (<15% of retained accounts).

Use `posthog-funnels` to visualize: accounts with signal X -> churn rate vs accounts without signal X -> churn rate.

### 4. Score active accounts

Use the `ticket-churn-signal-scoring` fundamental to score every active account based on their current ticket history. The scoring model uses the validated signals from Step 3 to weight different ticket patterns.

Run scoring weekly for all accounts with any ticket activity in the last 30 days. Store scores in Attio using `attio-deals` so CS reps see risk levels on their dashboards.

### 5. Set up alert routing

Use `n8n-triggers` to build automated routing:

- **High risk (score 51-75)**: Create a task in Attio for the account's CS owner. Include: risk score, top signals, recommended talking points, ticket history link.
- **Critical risk (score 76+)**: Send immediate Slack alert to CS lead AND create urgent Attio task. Include all context needed for a same-day intervention call.
- **Medium risk (score 26-50)**: Add to weekly CS review list. No immediate action but tracked.

### 6. Track intervention outcomes

When CS acts on an alert (makes a call, sends a message, offers a concession), log the intervention and outcome:
- Intervention type (call, email, in-app message, offer)
- Result (re-engaged, requested help, gave feedback, continued declining, churned anyway)
- Score at time of intervention
- Time from alert to intervention

Feed outcomes back to improve the scoring model: if accounts at score 65 that received intervention churn at 10% vs 45% without intervention, the intervention threshold is validated.

## Output

- Validated churn signal weights (which ticket patterns actually predict churn)
- Churn risk scores for all active accounts, updated weekly
- Automated CS alert routing for high/critical risk accounts
- Intervention outcome tracking for model improvement

## Triggers

- **Validation analysis**: Run monthly to recalibrate signal weights against actual churn data
- **Account scoring**: Run weekly via n8n cron
- **Alert routing**: Runs immediately after scoring completes
