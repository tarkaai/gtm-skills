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

1. **Create a feature flag via API.** Use the PostHog API or MCP to create flags:
   ```
   POST /api/projects/<id>/feature_flags/
   {
     "key": "new-pricing-page",
     "name": "New Pricing Page",
     "filters": { "groups": [{"rollout_percentage": 10}] },
     "active": true
   }
   ```
   Name flags with clear keys: `new-pricing-page`, `onboarding-v2`, `ai-recommendations`.

2. **Set rollout conditions.** Configure who sees the feature via the API filters:
   - Percentage rollout: `{"rollout_percentage": 10}`
   - Property-based: `{"properties": [{"key": "plan", "value": "pro"}]}`
   - Cohort-based: `{"properties": [{"key": "id", "value": <cohort-id>, "type": "cohort"}]}`
   Start with a small percentage and increase gradually.

3. **Implement in code.** Check the flag before showing the feature:
   ```javascript
   if (posthog.isFeatureEnabled('new-pricing-page')) {
     showNewPricing()
   } else {
     showOldPricing()
   }
   ```
   PostHog evaluates flags locally after initial load, so there is no latency impact.

4. **Track flag-specific events.** PostHog automatically captures a `$feature_flag_called` event when a flag is evaluated. You can also manually track events specific to the feature variant to measure its impact.

5. **Use flags for GTM experiments.** Feature flags enable GTM experiments: test a new onboarding flow with 20% of signups, roll out a new pricing page to specific segments, or A/B test in-app messaging. Connect to PostHog experiments for statistical analysis (see `posthog-experiments`).

6. **Clean up flags via API.** After a feature is fully rolled out (100%) and stable for 2+ weeks, remove the flag from your code and archive it: `PATCH /api/projects/<id>/feature_flags/<flag-id>/ {"deleted": true}`. Stale flags create technical debt. Review active flags monthly.
