---
name: referral-segment-scaling
description: Scale the referral program across user segments with personalized incentives, localized prompts, and cohort-specific optimization
category: Product
tools:
  - PostHog
  - Loops
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-experiments
  - posthog-custom-events
  - intercom-in-app-messages
  - loops-sequences
  - loops-ab-testing
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-lists
---

# Referral Segment Scaling

This drill takes a referral program that works for a single user segment and scales it across all segments. Different user types refer differently: power users respond to status rewards, price-sensitive users respond to credits, team leads respond to team benefits. This drill builds the segmentation, personalization, and testing infrastructure to find the optimal referral strategy per segment.

## Prerequisites

- Referral program running at Baseline level with proven referral rate (>=12%)
- PostHog tracking all referral funnel events
- At least 500 eligible users across multiple segments
- Baseline referral incentive validated

## Steps

### 1. Define referral segments

Using `posthog-cohorts`, create segments based on referral propensity signals:

| Segment | Definition | Expected Referral Behavior |
|---------|-----------|---------------------------|
| Power Users | Top 20% by usage frequency + feature breadth | Refer for status and recognition. Respond to exclusive rewards and leaderboards. |
| Price Sensitive | Users on free plan or who downgraded | Refer for credits and discounts. Respond to monetary incentives. |
| Team Leads | Users who invited 2+ team members | Refer other team leads at different companies. Respond to team-level benefits. |
| New Enthusiasts | Users in first 30 days with above-median activation speed | Refer while excitement is high. Respond to "share the discovery" framing. |
| Long-tenured Quiet | Active 6+ months, moderate usage, never referred | Have not been asked effectively. Respond to personalized asks tied to their specific use case. |

Create each segment as a PostHog cohort with clear, queryable criteria. Store segment assignments in Attio as a custom attribute using `attio-lists`.

### 2. Design segment-specific incentive variants

For each segment, configure a variant of the referral incentive:

**Power Users:** "Refer 3 friends and unlock [exclusive feature/early access]. Your referrals get 1 month free." Surface referral progress toward the goal.

**Price Sensitive:** "Give a friend 1 month free, get $X credit for each friend who joins." Emphasize the monetary value.

**Team Leads:** "Refer a team lead at another company. They get a team trial, you get [team-level benefit]." Frame as professional networking.

**New Enthusiasts:** "Loving [product]? Your friends get [reward] when they join through your link, and so do you." Strike while enthusiasm is fresh.

**Long-tenured Quiet:** "You've been using [specific feature] for [X months]. Know someone who'd benefit from the same?" Personalize to their actual usage pattern.

### 3. Implement segment-specific delivery

Using `posthog-feature-flags`, create a feature flag `referral-incentive-variant` that returns the segment-appropriate incentive for each user. The flag evaluates against the PostHog cohort memberships.

Using `intercom-in-app-messages`, create 5 variant in-app referral prompts, each targeted to its segment cohort. Trigger timing differs by segment:

- Power Users: after completing an advanced workflow
- Price Sensitive: when approaching plan limits
- Team Leads: after adding a new team member
- New Enthusiasts: after their first "aha moment" event
- Long-tenured Quiet: on their product anniversary or after a milestone

Using `loops-sequences`, create 5 variant email sequences, each with segment-appropriate copy and incentive framing. Use Loops audience segments synced from PostHog cohorts.

### 4. Run segment A/B tests

Using `posthog-experiments`, test each segment's variant against the baseline (generic) incentive:

For each segment:
1. Create an experiment: control = baseline incentive, treatment = segment-specific incentive
2. Allocate 50/50 within the segment
3. Primary metric: `referral_link_shared` rate
4. Secondary metrics: `referral_signup` conversion, `referral_activated` conversion, reward cost per acquisition
5. Run until 100+ users per variant per segment (use `n8n-scheduling` to check sample sizes daily)

Using `loops-ab-testing`, run parallel tests on the email sequence variants to determine which copy and framing resonates per segment.

### 5. Scale winning variants

Using `n8n-workflow-basics`, build an automation that:

1. At the end of each segment experiment, queries PostHog for results
2. If the segment variant wins (statistically significant at 95%, practical improvement >= 2pp in referral rate): roll out to 100% of that segment
3. If no significant difference: keep the simpler (baseline) variant for that segment
4. If the segment variant loses: log the result, test a different variant hypothesis for that segment
5. Update Attio with the winning variant per segment

### 6. Monitor cross-segment performance

Using `n8n-scheduling`, create a weekly report that:

1. Queries PostHog for referral funnel metrics broken down by segment
2. Calculates: referral rate, conversion rate, reward cost per acquisition, and viral coefficient per segment
3. Compares each segment against its pre-scaling baseline
4. Flags segments where performance dropped after scaling (possible cannibalization or audience fatigue)
5. Stores the report in Attio as a note on the referral program record

Track the aggregate viral coefficient:

```javascript
posthog.capture('referral_segment_report', {
  segment: 'power_users',
  referral_rate: 0.18,
  conversion_rate: 0.42,
  reward_cost_per_acquisition: 12.50,
  viral_coefficient: 0.31,
  total_referred_this_week: 23,
  variant: 'exclusive_feature_unlock'
});
```

## Output

- 5 user segments with distinct referral propensity profiles
- Segment-specific incentive variants with personalized copy
- Feature flag routing users to the right incentive
- A/B tests validating each segment variant against baseline
- Automated rollout of winning variants
- Weekly cross-segment performance report

## Triggers

Segment experiments run continuously until reaching sample size. Weekly performance reports fire via n8n cron. Re-run the segmentation step when user base composition changes significantly (new pricing tier, new product vertical, geographic expansion).
