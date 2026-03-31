---
name: posthog-experiments
description: Run A/B experiments in PostHog to optimize GTM flows
tool: PostHog
difficulty: Advanced
---

# Run Experiments in PostHog

## Prerequisites
- PostHog project with feature flags set up (see `posthog-feature-flags`)
- Sufficient traffic (minimum 500 users per variant per week)
- Clear hypothesis and success metric defined

## Steps

1. **Define your experiment via API.** Create an experiment using the PostHog API:
   ```
   POST /api/projects/<id>/experiments/
   {
     "name": "CTA Copy Test",
     "description": "Changing CTA from 'Start Free Trial' to 'See It In Action' will increase signup rate by 15%",
     "feature_flag_key": "cta-copy-test",
     "parameters": { "feature_flag_variants": [{"key": "control"}, {"key": "test"}] },
     "filters": { "events": [{"id": "signup_completed"}] }
   }
   ```
   Define the primary metric (signup conversion rate) and any secondary metrics.

2. **Create variants.** Set up control (existing experience) and test (new experience) variants. PostHog creates a linked feature flag automatically. For simple A/B tests, use two variants. For multivariate tests, add up to 4 variants but ensure you have enough traffic.

3. **Set traffic allocation.** Split traffic evenly between variants (50/50 for A/B). PostHog uses a consistent hash on user ID so each user always sees the same variant. Set the minimum sample size based on your expected effect size.

4. **Implement variants in code.** Use the experiment's feature flag to render different experiences:
   ```javascript
   const variant = posthog.getFeatureFlag('cta-copy-test')
   if (variant === 'test') { showNewCTA() } else { showOldCTA() }
   ```

5. **Monitor results via MCP.** Use the PostHog MCP `get_experiment_results` operation to check statistical significance. PostHog uses Bayesian analysis. Do not make decisions until the experiment reaches 95% significance. Check weekly but resist stopping early -- initial results are unreliable.

6. **Act on results.** When the experiment reaches significance: if the test variant wins, roll it out to 100% via the feature flag API and clean up the control code. If the control wins, document the learning and design the next experiment. Always record results for institutional memory.
