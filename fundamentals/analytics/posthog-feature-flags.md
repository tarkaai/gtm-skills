---
name: posthog-feature-flags
description: Use PostHog feature flags for controlled GTM feature rollouts
tool: PostHog
difficulty: Intermediate
---

# Use Feature Flags in PostHog

## Prerequisites
- PostHog project with SDK installed and user identification set up
- Feature or change you want to roll out gradually

## Steps

1. **Create a feature flag.** In PostHog, go to Feature Flags > New. Name it with a clear key: "new-pricing-page", "onboarding-v2", "ai-recommendations". Add a description explaining what the flag controls and when it should be removed.

2. **Set rollout conditions.** Configure who sees the feature. Options: Percentage rollout (e.g., 10% of users), Property-based (e.g., plan = "pro"), Cohort-based (e.g., "Beta Users" cohort), or specific user IDs for internal testing. Start with a small percentage and increase gradually.

3. **Implement in code.** In your application, check the flag before showing the feature: `if (posthog.isFeatureEnabled('new-pricing-page')) { showNewPricing() } else { showOldPricing() }`. PostHog evaluates flags locally after initial load, so there is no latency impact.

4. **Track flag-specific events.** When a user experiences the flagged feature, PostHog automatically captures a `$feature_flag_called` event. You can also manually track events specific to the feature variant to measure its impact.

5. **Use flags for GTM experiments.** Feature flags enable GTM experiments: test a new onboarding flow with 20% of signups, roll out a new pricing page to specific segments, or A/B test in-app messaging. Connect to PostHog experiments for statistical analysis (see `fundamentals/analytics/posthog-experiments`).

6. **Clean up flags.** After a feature is fully rolled out (100%) and stable for 2+ weeks, remove the flag from your code and archive it in PostHog. Stale flags create technical debt and confusion. Review active flags monthly.
