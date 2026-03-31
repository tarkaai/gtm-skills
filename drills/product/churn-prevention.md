---
name: churn-prevention
description: Detect churn signals from usage data and trigger interventions to retain at-risk customers
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-cohort-analysis
  - posthog-event-tracking
  - intercom-in-app-messages
  - loops-transactional-emails
  - n8n-trigger-setup
  - attio-deal-tracking
---

# Churn Prevention

This drill builds a system that detects early churn signals from product usage data and triggers targeted interventions before a customer actually cancels. Prevention is cheaper than winback.

## Prerequisites

- PostHog tracking active with at least 30 days of usage data
- Intercom configured for in-app messaging
- Loops configured for triggered emails
- n8n instance for workflow automation
- Understanding of what "healthy usage" looks like for your product

## Steps

### 1. Define your churn signals

Using the `posthog-cohort-analysis` fundamental, analyze churned customers to find common pre-churn patterns. Typical signals:

- **Usage decline**: 50%+ drop in weekly active sessions compared to their average
- **Feature abandonment**: Stopped using a core feature they previously used regularly
- **Support increase**: Filed 3+ support tickets in a week (frustration signal)
- **Login gap**: No login for 7+ days when they previously logged in daily
- **Team shrinkage**: Removed team members from the account
- **Billing page visits**: Visited pricing or cancellation pages

Combine signals into a churn risk score: each signal adds points, and a threshold triggers intervention.

### 2. Build the detection workflow

Using the `n8n-trigger-setup` fundamental, create a workflow that runs daily. It queries PostHog for users matching churn signal criteria, scores them, and routes at-risk accounts to the appropriate intervention. Store risk scores in Attio using the `attio-deal-tracking` fundamental so your team has visibility.

### 3. Design tiered interventions

Match intervention intensity to risk level:

- **Low risk (score 20-40)**: In-app message offering help or highlighting an unused feature they might benefit from. Use the `intercom-in-app-messages` fundamental.
- **Medium risk (score 40-70)**: Triggered email from the `loops-transactional-emails` fundamental. Personalize around the specific signal: "We noticed you haven't used [feature] lately — here's what's new." Include a help link and a calendar booking link.
- **High risk (score 70+)**: Personal outreach from a team member. Create a task in Attio for the account owner. Include the user's usage data and specific risk signals so the conversation is informed, not generic.

### 4. Implement feedback loops

When a high-risk user responds to intervention, log the outcome: re-engaged, requested help, gave feedback, or continued declining. Feed this data back into your churn scoring model. Some signals may be false positives (users on vacation, seasonal businesses) — track and exclude these patterns.

### 5. Track intervention effectiveness

Using `posthog-event-tracking`, measure: how many at-risk users were identified, how many received intervention, how many re-engaged within 14 days, and how many ultimately churned despite intervention. Calculate your save rate (interventions that prevented churn divided by total interventions) and optimize the signals and responses that produce the highest save rates.
