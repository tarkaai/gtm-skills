---
name: posthog-experiments
description: Run A/B experiments in PostHog to optimize GTM flows
tool: PostHog
difficulty: Advanced
---

# Run Experiments in PostHog

## Prerequisites
- PostHog project with feature flags set up (see `fundamentals/analytics/posthog-feature-flags`)
- Sufficient traffic (minimum 500 users per variant per week)
- Clear hypothesis and success metric defined

## Steps

1. **Define your experiment.** In PostHog, go to Experiments > New. Write a clear hypothesis: "Changing the CTA from 'Start Free Trial' to 'See It In Action' will increase signup rate by 15%." Define the primary metric (signup conversion rate) and any secondary metrics (time to signup, activation rate).

2. **Create variants.** Set up control (existing experience) and test (new experience) variants. PostHog creates a linked feature flag automatically. For simple A/B tests, use two variants. For multivariate tests, add up to 4 variants but ensure you have enough traffic.

3. **Set traffic allocation.** Split traffic evenly between variants (50/50 for A/B). PostHog uses a consistent hash on user ID so each user always sees the same variant. Set the minimum sample size based on your expected effect size -- PostHog's calculator helps with this.

4. **Implement variants in code.** Use the experiment's feature flag to render different experiences. PostHog's `getFeatureFlag()` returns the variant key ("control" or "test"). Build both variants in your code and gate them on the flag value.

5. **Monitor results.** PostHog calculates statistical significance automatically using Bayesian analysis. Do not make decisions until the experiment reaches 95% significance. Check weekly but resist the urge to stop early based on initial results -- early results are unreliable.

6. **Act on results.** When the experiment reaches significance: if the test variant wins, roll it out to 100% and clean up the control code. If the control wins, document the learning and design the next experiment. Always record results in your experiment log for institutional memory.
