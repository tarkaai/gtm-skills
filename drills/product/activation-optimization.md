---
name: activation-optimization
description: Identify and improve the activation metric that predicts long-term retention
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-funnel-tracking
  - posthog-cohort-analysis
  - posthog-event-tracking
  - intercom-product-tours
  - n8n-trigger-setup
---

# Activation Optimization

This drill helps you find your product's true activation metric, measure it accurately, and systematically improve the percentage of new users who reach it. Activation is the single most leveraged metric in your growth model — improving it lifts retention, revenue, and referrals simultaneously.

## Prerequisites

- PostHog tracking installed with comprehensive event coverage
- At least 60 days of signup and usage data
- Intercom configured for in-app guidance
- A hypothesis about what "activated" means for your product

## Steps

### 1. Find your activation metric

Using the `posthog-cohort-analysis` fundamental, compare retained users (active at Day 30) to churned users (inactive by Day 30). Look for the actions that most clearly separate the two groups. Common activation metrics:

- Created their first [core object] within 48 hours
- Completed a specific workflow end-to-end
- Invited at least one teammate
- Connected an integration or data source
- Reached a usage threshold (e.g., sent 10 messages, processed 100 records)

The best activation metric has the highest correlation with 30-day retention and is something the user can complete within their first few sessions.

### 2. Measure your current activation rate

Using `posthog-funnel-tracking`, build a funnel from signup to activation. Break it down by: signup source, plan type, user role, and cohort week. Your activation rate is the percentage of signups that reach the activation metric within your time window (typically 7-14 days). Identify the biggest drop-off steps in the funnel.

### 3. Remove friction at drop-off points

For each major drop-off step, diagnose the friction:

- **Confusion**: Users do not know what to do next. Fix with product tours using `intercom-product-tours`.
- **Effort**: The step requires too much work upfront. Simplify the flow, offer templates, or pre-fill data.
- **Value unclear**: Users do not see why this step matters. Add context, show examples, or display progress toward the outcome.
- **Technical blockers**: Errors, slow loading, or broken flows. Fix the bugs.

### 4. Build activation nudges

Using the `n8n-trigger-setup` fundamental, create workflows that nudge inactive users toward activation. If a user signs up but has not completed Step 2 of the funnel after 24 hours, trigger a help message via Intercom. If they completed Step 2 but stalled at Step 3, send a contextual email with a tutorial for that specific step.

### 5. Run activation experiments

Change one thing at a time and measure the impact on activation rate. Use PostHog feature flags to A/B test: different onboarding flows, simplified signup forms, guided vs. self-serve setup, different first-time user experiences. Track each variant's activation rate over 14 days with sufficient sample size before declaring a winner.

### 6. Monitor activation continuously

Track activation rate weekly as a leading indicator. Set up a PostHog dashboard showing: overall activation rate, activation rate by cohort, time-to-activation distribution, and drop-off by funnel step. A declining activation rate is an urgent signal — investigate immediately.
