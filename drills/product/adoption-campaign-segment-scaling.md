---
name: adoption-campaign-segment-scaling
description: Scale adoption campaigns across multiple user segments with per-segment messaging, channels, and success criteria
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - intercom-in-app-messages
  - loops-sequences
  - n8n-workflow-basics
  - n8n-scheduling
---

# Adoption Campaign Segment Scaling

This drill takes an adoption campaign that works for one user segment and expands it to cover all meaningful segments. Each segment gets tailored messaging, channel priority, and success thresholds. The goal is to drive feature adoption across your entire active user base without sending irrelevant messages to users who do not need the feature.

## Input

- A working adoption campaign (proven at Baseline level) with a known success rate for one segment
- PostHog tracking the campaign's core events: `campaign_impression`, `campaign_engaged`, `campaign_converted`, `feature_first_used`, `feature_retained_7d`
- Intercom and Loops configured for multi-segment campaigns
- n8n instance for orchestrating segment-specific workflows

## Steps

### 1. Define adoption segments

Using the `posthog-cohorts` fundamental, create cohorts based on who needs this feature and why:

| Segment | Definition | Messaging Angle |
|---------|-----------|-----------------|
| Power users, never tried | Top 20% by usage volume, `feature_first_used` is null | "You're already doing X manually — this feature automates it" |
| Active users, tried once | Used feature 1 time, not returned in 14+ days | "Here's what you missed — 3 use cases for [feature]" |
| New signups (last 30 days) | Signup in last 30 days, completed onboarding | "Now that you're set up, try [feature] to [benefit]" |
| Churning users | Usage down 50%+ in last 2 weeks, feature not adopted | "Stuck? [Feature] solves [their likely pain point]" |
| Team admins | Admin role, team size 3+, feature not enabled for team | "Enable [feature] for your team — here's the impact" |

Adjust segments based on your product. The key principle: each segment hears a different reason to adopt, delivered through the channel they respond to best.

### 2. Build per-segment campaign variants

For each segment, configure a separate campaign variant:

Using `intercom-in-app-messages`, create targeted messages for segments best reached in-app (power users, active users). Use feature-specific tooltips, banners, or modals depending on the segment's expected receptivity. Power users get a subtle tooltip; churning users get a more prominent banner.

Using `loops-sequences`, create email sequences for segments best reached via email (new signups, churning users). Each sequence should be 3 emails maximum:
1. Feature introduction with the segment-specific angle
2. Use case walkthrough with a concrete example
3. Social proof from similar users who adopted the feature

### 3. Configure feature flags per segment

Using `posthog-feature-flags`, create a flag per segment campaign variant. This lets you:
- Launch segments one at a time (not all at once)
- Easily pause a segment that is underperforming without affecting others
- Run A/B tests within each segment (control receives no campaign, treatment receives the campaign)
- Measure per-segment adoption lift cleanly

### 4. Build the orchestration workflow

Using `n8n-workflow-basics` and `n8n-scheduling`, create a workflow that:

1. Runs daily to check which users have entered each segment cohort
2. For users entering a segment for the first time: trigger the appropriate campaign variant
3. For users who converted (adopted the feature): remove them from the campaign cohort and log the conversion
4. For users who completed all campaign touches without converting: mark them as "campaign exhausted" and do not re-target for 30 days
5. Generate a daily summary: new users entered each segment, conversions per segment, exhaustion rates

### 5. Track per-segment performance

Using `posthog-custom-events`, tag all campaign events with the segment identifier:

```javascript
posthog.capture('campaign_impression', {
  campaign: 'feature-adoption',
  segment: 'power-users-never-tried',
  variant: 'tooltip-v1',
  channel: 'in-app'
});
```

Build a PostHog insight comparing adoption rates across segments. Identify which segments respond best and which need different messaging or channels.

### 6. Iterate per segment

After 2 weeks of running each segment:
- Segments converting above target: reduce campaign frequency (the message is working, do not over-deliver)
- Segments converting below target: test a different messaging angle or channel
- Segments with high dismissal rates: the feature may not be relevant — stop campaigning and investigate whether the segment definition is wrong

## Output

- PostHog cohorts for each adoption segment
- Per-segment campaign variants in Intercom and Loops
- Feature flags controlling per-segment rollout
- n8n orchestration workflow managing segment lifecycle
- Per-segment performance tracking and comparison

## Triggers

Run once during Scalable level setup. The n8n workflow runs daily. Review segment performance weekly. Add new segments when you identify user groups being missed by the current targeting.
