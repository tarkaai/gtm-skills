---
name: free-to-paid-funnel-health-monitor
description: Weekly report on the free-to-paid conversion funnel covering signup-to-upgrade rates, activation progression, upgrade surface performance, and prompt fatigue signals
category: Product
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
  - Stripe
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - attio-deals
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
  - billing-event-streaming
---

# Free-to-Paid Funnel Health Monitor

This drill generates a weekly structured report on how the free-to-paid conversion funnel is performing end-to-end. It tracks every stage from free signup through activation to paid conversion, measures upgrade surface effectiveness (in-app prompts, feature gates, email nudges, limit alerts), detects prompt fatigue and activation stalls, and attributes new MRR to specific conversion paths. The report feeds directly into the `autonomous-optimization` drill at Durable level.

## Input

- PostHog tracking configured with funnel events: `signup_completed`, `activation_milestone_reached`, `upgrade_prompt_shown`, `upgrade_prompt_clicked`, `upgrade_started`, `upgrade_completed`, `upgrade_prompt_dismissed`, `feature_gate_hit`, `usage_limit_hit`
- Stripe billing event streaming configured via `billing-event-streaming` for real-time subscription data
- At least 14 days of free-to-paid conversion data
- Attio with upgrade deals tagged by conversion source
- n8n instance for scheduling the report

## Steps

### 1. Build the free-to-paid funnel dashboard

Using the `posthog-dashboards` fundamental, create a dashboard called "Free-to-Paid Funnel — Health":

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Full funnel (overall) | Funnel chart | `signup_completed` -> `activation_milestone_reached` -> `upgrade_prompt_shown` -> `upgrade_prompt_clicked` -> `upgrade_started` -> `upgrade_completed` |
| Conversion by upgrade surface | Bar chart | Upgrade rate per surface: in-app modal, feature gate, limit alert, email nudge, pricing page |
| Cohort progression velocity | Line chart (weekly signup cohorts) | Median days from signup to paid conversion per cohort — are newer cohorts converting faster |
| New MRR from conversions | Trend line | Weekly MRR from free-to-paid upgrades, broken down by trigger surface |
| Prompt fatigue index | Line chart | Ratio of `upgrade_prompt_dismissed` to `upgrade_prompt_shown` over 4-week rolling window, per surface type |
| Free user activation funnel | Funnel chart | `signup_completed` -> `first_value_action` -> `habit_formed` (3+ sessions in 7 days) -> `upgrade_prompt_eligible` |
| Upgrade surface comparison | Bar chart | Conversion rate by prompt surface: in-app modal, banner, tooltip, email, limit-alert, feature-gate |
| Free user pool health | Area chart | Total free users, active free users (7-day), activated free users, upgrade-ready free users, prompt-fatigued free users |

Set dashboard subscription to deliver Monday 09:00 to the growth team.

### 2. Define free user lifecycle segments

Using `posthog-cohorts`, create dynamic cohorts that segment the free user pool:

- **free-inactive**: Signed up but never completed the first value action. These users need onboarding nudges, not upgrade prompts.
- **free-activated**: Completed the first value action but usage is sporadic (fewer than 3 sessions in 7 days). They see value but have not formed a habit.
- **free-habitual**: 3+ sessions in 7 days and regularly using core features. These are the highest-probability conversion candidates.
- **free-upgrade-ready**: Habitual users who are at 80%+ of a plan limit OR have hit a feature gate 2+ times in 7 days. Show upgrade prompts to this cohort.
- **free-prompt-fatigued**: Users who dismissed 3+ upgrade prompts in 14 days. Suppress in-app prompts; switch to email-only at reduced frequency.
- **free-at-risk**: Users whose 7-day session count dropped by 50%+ vs prior 7 days. They are disengaging before converting.

Using `posthog-custom-events`, log every lifecycle transition:

```javascript
posthog.capture('free_user_lifecycle_transition', {
  from_state: 'inactive',
  to_state: 'activated',
  trigger: 'first_project_created',
  days_since_signup: daysSinceSignup,
  account_id: accountId
});
```

### 3. Schedule the weekly report workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 08:00 UTC:

1. Query PostHog for last 7 days of funnel data using `posthog-funnels`
2. Pull per-surface breakdown: in-app modal, feature gate, limit alert, email nudge, pricing page
3. Pull upgrade revenue data from Attio using `attio-deals` (filter by deals with source containing "free-to-paid") and cross-reference with Stripe subscription data via `billing-event-streaming`
4. Run `posthog-anomaly-detection` to check week-over-week changes in: overall conversion rate, per-surface CTR, free user pool size, prompt fatigue rate, activation rate
5. Generate the report using Claude:
   - **Conversion table**: surface type | prompts shown | prompts clicked | upgrades started | upgrades completed | conversion rate | MRR attributed | trend vs. 4-week average
   - **Cohort velocity**: this week's signup cohort conversion velocity vs. prior 4 cohorts. Median days to paid conversion. Are newer users converting faster?
   - **Free user pool health**: total free users | active % | activated % | habitual % | upgrade-ready % | prompt-fatigued % | at-risk %. Trend each metric week-over-week.
   - **Top performer**: which upgrade surface drove the most conversions this week, with the specific conversion path
   - **Underperformer**: which surface has the worst funnel conversion, with the specific step where users drop off
   - **Fatigue alerts**: surfaces where prompt fatigue exceeds 15% of exposed users, with current suppression counts
   - **Revenue attribution**: total free-to-paid MRR this week, month-to-date, average revenue per conversion, highest-value surface
   - **Recommended action**: one specific experiment to run next week, with hypothesis and expected impact on conversion rate
6. Post the report to Slack and store in Attio as a note on the free-to-paid-conversion-funnel campaign record

### 4. Build the daily degradation detection layer

Using `posthog-anomaly-detection` and `n8n-scheduling`, create a daily check at 08:00 UTC:

1. Query PostHog for each upgrade surface's conversion rate over the last 7 days
2. Compare against the 4-week rolling average for that surface
3. Flag triggers:
   - Any surface where conversion rate dropped more than 20% from its rolling average
   - Free-at-risk cohort grew more than 20% week-over-week
   - Prompt-fatigued cohort exceeds 15% of active free users
   - Overall activation rate (signup to first value action) dropped more than 15%
   - Median days-to-conversion increased more than 25% vs. 30-day average

When a flag fires:
- Create a note on the Attio campaign record using `attio-reporting`
- Send a Slack alert: "Free-to-paid funnel: [metric] degraded [X]% vs 4-week avg. At-risk free users: [count]. Fatigued: [count]."
- If activation rate drops, recommend pausing upgrade prompts and focusing on onboarding fixes
- If prompt fatigue exceeds threshold, recommend suppressing in-app prompts for the fatigued segment and switching to email-only nudges

### 5. Track revenue attribution per conversion path

Using `attio-deals` and `billing-event-streaming`, tag every upgrade deal with:
- `conversion_surface`: which upgrade surface the user interacted with last (in-app modal, feature gate, limit alert, email nudge, pricing page)
- `conversion_trigger`: the specific trigger that fired (limit_proximity, feature_gate_hit, time_based, growth_signal, email_nudge)
- `prompts_before_conversion`: total upgrade prompts the user saw before converting
- `days_signup_to_conversion`: total time from free signup to paid subscription
- `activation_milestone_days`: days from signup to activation milestone
- `plan_selected`: which paid plan the user chose
- `initial_mrr`: first month's revenue from this conversion

Aggregate monthly: total free-to-paid MRR, average deal value by surface, average days to convert, fastest-converting paths, highest-LTV conversion sources.

## Output

- Weekly health report covering the full free-to-paid funnel
- Free user lifecycle tracking with 6 dynamic cohorts and state transition monitoring
- Daily degradation detection with Slack + Attio alerting
- Revenue attribution linking every upgrade to its conversion surface and trigger path
- Recommended action feeding directly into the `autonomous-optimization` drill

## Triggers

Dashboard reviewed weekly. Degradation detection runs daily via n8n cron at 08:00 UTC. Revenue attribution updated continuously via PostHog and Stripe webhooks. Re-run full setup when adding new upgrade surfaces or changing plan structure.
