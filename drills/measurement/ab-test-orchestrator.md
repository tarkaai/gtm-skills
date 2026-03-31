---
name: ab-test-orchestrator
description: Design, run, and analyze A/B tests for GTM plays using PostHog feature flags and experiments
category: Measurement
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-experiments
  - posthog-event-tracking
  - n8n-workflow-patterns
---

# A/B Test Orchestrator

This drill provides a framework for running rigorous A/B tests on your GTM plays — email copy, landing pages, onboarding flows, pricing, and more. It covers hypothesis creation, test setup, statistical rigor, and decision-making.

## Prerequisites

- PostHog with feature flags and experiments enabled
- Sufficient traffic or volume for the element being tested (minimum 200 per variant for most tests)
- A specific element to test with a clear success metric

## Steps

### 1. Form a hypothesis

Every test starts with a hypothesis, not a hunch. Structure it as:

"If we [change X], then [metric Y] will [increase/decrease] by [estimated amount], because [reasoning]."

Example: "If we shorten the cold email from 150 words to 60 words, then reply rate will increase by 3 percentage points, because shorter emails get read on mobile and feel less like marketing."

Bad hypothesis: "Let's test a new subject line." (No predicted outcome, no reasoning.)

### 2. Calculate sample size

Before launching, determine how many observations you need. Using PostHog's experiment calculator or a manual formula:

- Current baseline conversion rate
- Minimum detectable effect (the smallest improvement worth caring about)
- Statistical significance level (use 95%)
- Statistical power (use 80%)

If you need 500 per variant and get 50 visitors per day, the test runs for 20 days. If you cannot reach sample size within 4 weeks, test a bigger change (larger effect size) or find a higher-traffic element to test.

### 3. Set up the experiment in PostHog

Using the `posthog-feature-flags` fundamental, create a feature flag for the test. Using `posthog-experiments`, configure the experiment:

- Define the variants (control = current, treatment = new)
- Set the allocation percentage (usually 50/50)
- Choose the primary metric (the one that determines the winner)
- Add secondary metrics (guard against improving one metric while hurting another)
- Set the experiment duration based on your sample size calculation

### 4. Implement the variants

For email tests: create both versions in Instantly and use n8n with `n8n-workflow-patterns` to route prospects randomly. For landing page tests: use PostHog feature flags to show different page elements. For in-app tests: use PostHog flags in your product code. Ensure the randomization is user-level (each user always sees the same variant) not session-level.

### 5. Monitor without peeking

Do not check results daily and call winners early — this leads to false positives. Using `posthog-event-tracking`, track both variants but set a calendar reminder for the planned end date. The only reason to stop early: a guardrail metric (like unsubscribe rate or error rate) spikes, indicating the test is causing harm.

### 6. Analyze and decide

When the test reaches its planned sample size:

- Check if the result is statistically significant (95% confidence)
- Check the practical significance (is the improvement large enough to matter?)
- Review secondary metrics (did the winner hurt anything else?)
- Document the result: hypothesis, variants, sample size, result, confidence level, and decision

If significant: implement the winner permanently. If not significant: the variants are equivalent — keep whichever is simpler or cheaper. If the loser won: investigate why your hypothesis was wrong — the learning is more valuable than the test.
