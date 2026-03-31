---
name: freemium-conversion-health-report
description: Weekly report on freemium-to-paid conversion funnel covering prompt-to-upgrade rates, cohort progression, revenue attribution, and prompt fatigue signals
category: Conversion
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
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
---

# Freemium Conversion Health Report

This drill generates a weekly structured report on how the freemium-to-paid conversion pipeline is performing. It tracks the full free-user-to-paid funnel across all upgrade surfaces (in-app prompts, limit alerts, feature gates, emails), detects prompt fatigue, measures cohort progression velocity, and attributes revenue to specific conversion triggers. The report feeds directly into the autonomous optimization loop at Durable level.

## Input

- PostHog tracking configured with conversion events: `upgrade_prompt_shown`, `upgrade_prompt_clicked`, `upgrade_started`, `upgrade_completed`, `upgrade_prompt_dismissed`, `usage_limit_hit`, `feature_gate_hit`
- At least 14 days of free-to-paid conversion data
- Attio with upgrade deals tagged by conversion source
- n8n instance for scheduling the report

## Steps

### 1. Build the freemium conversion funnel dashboard

Using the `posthog-dashboards` fundamental, create a dashboard called "Freemium Conversion — Health":

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Free-to-paid funnel (overall) | Funnel chart | `signup_completed` -> `upgrade_prompt_shown` -> `upgrade_prompt_clicked` -> `upgrade_started` -> `upgrade_completed` |
| Conversion by trigger type | Bar chart | Upgrade rate per trigger: limit_proximity, feature_gate, time_based, growth_signal |
| Cohort progression | Line chart (weekly signup cohorts) | Days from signup to paid conversion, are newer cohorts converting faster |
| Revenue from free-to-paid | Trend line | MRR from new conversions per week, broken down by trigger type |
| Prompt fatigue index | Line chart | Ratio of `upgrade_prompt_dismissed` to `upgrade_prompt_shown` over 4-week rolling window |
| Free user activation funnel | Funnel chart | `signup_completed` -> `first_value_action` -> `habit_formed` (3+ sessions in 7 days) -> `upgrade_prompt_eligible` |
| Surface comparison | Bar chart | Conversion rate by prompt surface: in-app modal, banner, tooltip, email, limit-alert, feature-gate |
| Free user pool health | Area chart | Total free users, active free users (7-day), prompt-eligible free users, prompt-fatigued free users |

Set dashboard subscription to deliver Monday 09:00 to the growth team.

### 2. Define the free-user health metric

A freemium conversion play lives or dies on the quality of the free user pool. Using `posthog-custom-events`, compute per free user:

- **Activation state**: inactive (no value action), activated (1+ value action), habitual (3+ sessions in 7 days), power-free (using advanced free features)
- **Prompt history**: prompts seen, prompts clicked, prompts dismissed, days since last prompt
- **Conversion probability score**: based on activation state + engagement velocity + feature usage breadth. Compute this as a PostHog calculated property or via a daily n8n sync.

Using `posthog-cohorts`, create dynamic cohorts:
- **free-activated**: Free users who completed the first value action but have not upgraded
- **free-upgrade-ready**: Free users hitting 80%+ of a plan limit or repeatedly encountering feature gates
- **free-prompt-fatigued**: Free users who dismissed 3+ prompts in 14 days. Suppress further in-app prompts; email only.
- **free-at-risk**: Free users whose 7-day session count dropped by 50%+ vs prior 7 days. They are disengaging before converting.

### 3. Schedule the weekly report workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 8:00 AM:

1. Query PostHog for last 7 days of free-to-paid funnel data using `posthog-funnels`
2. Pull per-trigger breakdown from PostHog
3. Pull upgrade revenue data from Attio using `attio-deals` (filter by deals with stage = "Free to Paid" or source containing "freemium")
4. Run `posthog-anomaly-detection` to check week-over-week changes in: free-to-paid rate, prompt CTR per trigger type, free user pool size, prompt fatigue rate
5. Generate the report using Claude:
   - **Conversion table**: trigger type, prompts shown, prompts clicked, upgrades started, upgrades completed, conversion rate, MRR attributed, trend vs. 4-week average
   - **Cohort analysis**: this week's signup cohort conversion velocity vs. prior 4 cohorts. Are newer users converting faster?
   - **Free user pool health**: total free users, active %, activated %, upgrade-ready %, prompt-fatigued %. Trend each metric.
   - **Top converter**: which trigger type drove the most upgrades this week and the conversion path that worked
   - **Underperformer**: which trigger type has the worst funnel conversion and where the specific drop-off occurs
   - **Fatigue alerts**: trigger types where prompt fatigue exceeds 15% of exposed users, with suppression counts
   - **Revenue attribution**: total free-to-paid MRR this month, average revenue per conversion, highest-value trigger source
   - **Recommended action**: one specific experiment to run next week, with hypothesis and expected impact
6. Post to Slack and store in Attio as a note on the freemium-feature-upsell campaign record

### 4. Track free user lifecycle transitions

Using `posthog-custom-events`, log every meaningful transition in the free user lifecycle:

```javascript
posthog.capture('free_user_transition', {
  from_state: 'inactive',      // inactive, activated, habitual, power-free, upgraded, churned
  to_state: 'activated',
  trigger: 'first_project_created',
  days_since_signup: daysSinceSignup,
  account_id: accountId
});
```

Build a PostHog insight showing the weekly flow: how many free users move between states each week. A healthy funnel shows steady flow from inactive -> activated -> habitual -> upgraded. Bottlenecks (large pools stuck in one state) indicate where the conversion pipeline is broken.

### 5. Measure revenue attribution per conversion path

Using `attio-deals`, tag every upgrade deal with the conversion path:
- `conversion_trigger`: which specific trigger fired (limit_proximity, feature_gate, time_based, growth_signal, email_nudge)
- `conversion_surface`: where the upgrade happened (in-app modal, pricing page, email link, Stripe checkout)
- `prompts_before_conversion`: how many upgrade prompts the user saw before converting
- `days_signup_to_conversion`: total time from free signup to paid conversion
- `free_tier_usage`: what the user accomplished on the free tier (projects created, features used, team members invited)

Aggregate monthly: total MRR from free-to-paid conversions, average deal value by conversion trigger, average days to convert, fastest-converting trigger paths.

### 6. Build the degradation detection layer

Using `posthog-anomaly-detection` and `n8n-scheduling`, create a daily check at 08:00 UTC:

1. Query PostHog for each trigger type's conversion rate over the last 7 days
2. Compare against the 4-week rolling average
3. Flag any trigger where conversion rate dropped more than 20% from its rolling average
4. Flag if the free-at-risk cohort grew more than 20% week-over-week
5. Flag if the prompt-fatigued cohort exceeds 15% of active free users

When a flag fires:
- Create a note on the Attio campaign record using `attio-reporting`
- Send a Slack notification: "Freemium conversion: [trigger_type] conversion dropped [X]% vs 4-week avg. At-risk free users: [count]. Fatigued: [count]."
- If prompt-fatigued exceeds 15%, recommend pausing in-app prompts for fatigued segment and switching to email-only nudges with different messaging

## Output

- Weekly health report covering the full freemium-to-paid pipeline
- Free user lifecycle tracking with state transition monitoring
- 4 dynamic cohorts for segmentation and suppression
- Daily degradation detection with Slack + Attio alerting
- Revenue attribution linking upgrades to specific conversion triggers and paths
- Recommended action feeding into the autonomous optimization loop

## Triggers

Dashboard reviewed weekly. Degradation detection runs daily via n8n cron at 08:00 UTC. Revenue attribution insight updated continuously via PostHog. Re-run full setup when adding new upgrade trigger types or prompt surfaces.
