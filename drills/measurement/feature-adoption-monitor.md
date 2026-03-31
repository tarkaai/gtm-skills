---
name: feature-adoption-monitor
description: Track progressive feature discovery rates, tier transition velocity, and identify stalled users for intervention
category: Experimentation
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
---

# Feature Adoption Monitor

This drill builds the measurement and intervention layer for progressive feature reveal. It tracks how users move through feature tiers, identifies where they stall, and triggers automated nudges to keep them progressing. Without this drill, you have gating but no visibility into whether it is working.

## Input

- Feature readiness gating already configured (feature tiers, PostHog events, cohorts, and flags from the `feature-readiness-gating` drill)
- PostHog with at least 7 days of tier transition data
- n8n instance for scheduled monitoring
- Intercom and Loops configured for nudge delivery

## Steps

### 1. Build the feature adoption funnel

Using the `posthog-funnels` fundamental, create a funnel that tracks the progression path:

```
signup_completed
  -> core_action_completed (3+ times)
    -> feature_tier_unlocked (tier=intermediate)
      -> intermediate_feature_first_used
        -> feature_tier_unlocked (tier=advanced)
          -> advanced_feature_first_used
            -> feature_tier_unlocked (tier=power)
```

Break this funnel down by:
- Signup source (organic, paid, referral)
- Plan type (free, trial, paid)
- Signup week (cohort analysis)

Identify the largest drop-off point. This is where your optimization effort should focus.

### 2. Create tier transition velocity metrics

Using `posthog-custom-events`, calculate how long users take to move between tiers. Create PostHog insights for:

- **Median time: Signup to Intermediate unlock** (target: under 3 days)
- **Median time: Intermediate to Advanced unlock** (target: under 14 days)
- **Median time: Advanced to Power unlock** (target: under 30 days)
- **Overall: Signup to full unlock** (target: under 45 days)

Track these as weekly trends. Acceleration means your reveal strategy is working. Deceleration means friction is building.

### 3. Build the stalled-user detection workflow

Using `n8n-scheduling`, create a daily workflow that queries PostHog for stalled users:

- **Stalled at Core**: Signed up 7+ days ago, completed fewer than 3 Core actions. This user is confused or disengaged.
- **Stalled at Intermediate**: Unlocked Intermediate 14+ days ago, has not used any Intermediate features. The unlock message did not convert.
- **Stalled at Advanced**: Unlocked Advanced 21+ days ago, has not used any Advanced features. The user may not see value in the advanced tier.

For each stalled segment, the workflow triggers a different intervention.

### 4. Configure stalled-user interventions

For **Stalled at Core** users, use `intercom-in-app-messages` to show a contextual help widget the next time they log in: "Need help getting started? Here's the fastest way to [achieve first value]." Link to a specific action, not a help center.

For **Stalled at Intermediate** users, use `loops-transactional` to send an email showcasing the top Intermediate feature with a concrete use case: "You unlocked Templates last week. Here's how [similar company] saved 4 hours/week using them." Include a deep link to the feature.

For **Stalled at Advanced** users, use `intercom-in-app-messages` to show a tooltip on the Advanced feature they are most likely to use (based on their Intermediate usage patterns): "Ready to automate this? Click here to set up your first rule."

### 5. Build the feature adoption dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Tier distribution (current) | Pie chart | What percentage of active users are at each tier right now |
| Tier transitions this week | Bar chart | How many users unlocked each tier this week |
| Adoption funnel | Funnel chart | Drop-off between tiers |
| Time to unlock by tier | Line chart (trend) | Is progression speeding up or slowing down |
| Stalled users by segment | Table | How many users are stalled at each tier |
| Feature usage by tier | Heatmap | Which unlocked features are actually being used |
| Intervention effectiveness | Bar chart | Nudge sent vs. feature adopted within 7 days |

Set alerts for:
- Tier distribution shifting toward Core (users are not progressing)
- Stalled user count exceeding 20% of active users at any tier
- Time-to-unlock increasing for 2+ consecutive weeks

### 6. Track intervention effectiveness

Using `posthog-custom-events`, measure each intervention's impact:

```javascript
posthog.capture('stall_nudge_shown', {
  tier: 'intermediate',
  nudge_type: 'email',
  template_id: 'intermediate-stall-v1'
});

posthog.capture('stall_nudge_converted', {
  tier: 'intermediate',
  nudge_type: 'email',
  template_id: 'intermediate-stall-v1',
  days_to_convert: daysSinceNudge
});
```

Calculate: nudge conversion rate (users who engaged with the feature within 7 days of the nudge divided by users who received the nudge). Target 15%+ for in-app nudges, 8%+ for email nudges. If a nudge underperforms, test a different message or feature highlight.

## Output

- Feature adoption funnel in PostHog
- Tier transition velocity metrics tracked weekly
- Daily stalled-user detection workflow in n8n
- Automated interventions for each stall type via Intercom and Loops
- Feature adoption dashboard with 7 panels and threshold alerts
- Intervention effectiveness tracking

## Triggers

The stalled-user detection runs daily via n8n cron. The dashboard and velocity metrics are reviewed weekly. Re-run the full drill setup when adding new feature tiers or changing readiness criteria.
