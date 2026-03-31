---
name: cta-variant-pipeline
description: Generate, deploy, and measure CTA copy and placement variants using PostHog feature flags and experiments
category: Conversion
tools:
  - PostHog
  - Intercom
  - n8n
  - Anthropic
fundamentals:
  - posthog-feature-flags
  - posthog-experiments
  - posthog-custom-events
  - posthog-funnels
  - intercom-in-app-messages
  - n8n-workflow-basics
  - hypothesis-generation
---

# CTA Variant Pipeline

This drill generates CTA variants (copy, placement, color, urgency framing), deploys them behind PostHog feature flags, measures conversion impact, and promotes winners. It is the core execution loop for CTA optimization plays.

## Input

- At least one live CTA surface with PostHog events flowing (`cta_impression`, `cta_clicked`, `lead_captured` or equivalent conversion event)
- Baseline conversion data: minimum 2 weeks of CTA performance history
- PostHog project with feature flags and experiments enabled
- A conversion metric to optimize (click-through rate, form submission rate, upgrade rate, etc.)

## Steps

### 1. Audit existing CTAs

Query PostHog for all pages and surfaces firing `cta_impression` events. For each CTA surface, pull:

- Impression count (last 14 days)
- Click-through rate (`cta_clicked / cta_impression`)
- Conversion rate (`lead_captured / cta_impression` or the relevant downstream event)
- Device breakdown (desktop vs mobile)
- Page-level breakdown

Using `posthog-funnels`, build a funnel per CTA surface: `cta_impression` -> `cta_clicked` -> conversion event. Identify the CTA with the lowest conversion rate AND sufficient traffic (100+ impressions/week). This is your first optimization target.

### 2. Generate variant hypotheses

Using `hypothesis-generation`, feed the baseline data and generate 3-5 CTA variant hypotheses. Each hypothesis must specify:

- **Element to change:** copy text, button color, placement position, urgency framing, social proof inclusion, or size
- **Specific variant:** exact copy or description of the change (e.g., "Change 'Start Free Trial' to 'See it work in 2 minutes'")
- **Predicted impact:** expected CTR change with reasoning
- **Risk level:** low (copy-only change), medium (placement or design change), high (removes existing information)

Prioritize by expected impact / risk ratio. Only test one element per variant to isolate the variable.

Variant categories to consider:
- **Action specificity:** vague ("Get Started") vs specific ("Build your first workflow in 3 minutes")
- **Urgency framing:** none vs time-limited ("Free for 14 days") vs scarcity ("3 spots left this week")
- **Social proof:** none vs number ("Join 2,400 teams") vs named ("Used by Stripe, Notion, Linear")
- **Benefit framing:** feature-led ("Try AI automation") vs outcome-led ("Save 10 hours/week")
- **Commitment level:** high ("Book a demo") vs low ("See how it works") vs zero ("Watch 90-second video")

### 3. Deploy variants behind feature flags

Using `posthog-feature-flags`, create a multivariate feature flag for the target CTA:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "cta-variant-{surface}-{date}",
  "name": "CTA Variant Test: {surface description}",
  "filters": {
    "multivariate": {
      "variants": [
        {"key": "control", "rollout_percentage": 50},
        {"key": "variant_a", "rollout_percentage": 50}
      ]
    }
  },
  "active": true
}
```

For the first test, use a simple A/B (50/50 control vs one variant). Once you have a winner, test the winner against the next variant.

Implement the variant in your product code:
```javascript
const ctaVariant = posthog.getFeatureFlag('cta-variant-{surface}-{date}')
const ctaConfig = {
  control: { text: 'Start Free Trial', color: 'blue' },
  variant_a: { text: 'See it work in 2 minutes', color: 'blue' }
}
renderCTA(ctaConfig[ctaVariant] || ctaConfig.control)
```

### 4. Configure the experiment

Using `posthog-experiments`, create an experiment linked to the feature flag:

```
POST /api/projects/<id>/experiments/
{
  "name": "CTA Test: {hypothesis summary}",
  "feature_flag_key": "cta-variant-{surface}-{date}",
  "parameters": {
    "feature_flag_variants": [
      {"key": "control"},
      {"key": "variant_a"}
    ],
    "minimum_detectable_effect": 0.05
  },
  "filters": {
    "events": [{"id": "cta_clicked"}],
    "actions": []
  }
}
```

Set the primary metric to `cta_clicked` rate. Add secondary metrics: `lead_captured` rate (to ensure clicks translate to conversions) and `page_bounce_rate` (to ensure the variant does not increase exits).

### 5. Track variant-specific events

Using `posthog-custom-events`, ensure each CTA interaction captures the variant:

```javascript
posthog.capture('cta_impression', {
  page: window.location.pathname,
  surface_type: '{form|calendar|chat|button}',
  cta_variant: posthog.getFeatureFlag('cta-variant-{surface}-{date}'),
  cta_text: ctaConfig[variant].text
})

posthog.capture('cta_clicked', {
  page: window.location.pathname,
  surface_type: '{form|calendar|chat|button}',
  cta_variant: posthog.getFeatureFlag('cta-variant-{surface}-{date}'),
  cta_text: ctaConfig[variant].text
})
```

### 6. Monitor and decide

Let the experiment run until PostHog reports 95% statistical significance or 4 weeks elapse (whichever comes first).

Using `posthog-experiments`, check results:
```
GET /api/projects/<id>/experiments/<experiment_id>/results/
```

Decision framework:
- **Significant winner (95%+ confidence):** Roll out the winner to 100% via the feature flag. Archive the experiment. Log the result.
- **No significant difference after 4 weeks:** The variants perform equivalently. Keep whichever is simpler. Test a bigger change next.
- **Winner on primary but loser on secondary metric:** Investigate. A CTA that gets more clicks but fewer conversions may be misleading users. Do not ship.

### 7. Log and iterate

After each test completes, record in Attio or your experiment log:
- Hypothesis tested
- Variant description
- Sample size per variant
- Primary metric: control rate vs variant rate
- Statistical significance
- Decision: shipped / discarded / extended
- Cumulative lift from all shipped variants (running total)

Queue the next variant from step 2. The pipeline runs continuously: finish one test, start the next.

## Output

- Prioritized list of CTA variant hypotheses
- PostHog feature flag and experiment configured for the top variant
- Variant-specific event tracking deployed
- Decision framework for promoting or discarding variants
- Running experiment log with cumulative lift tracking

## Triggers

Run once to set up the first experiment. Re-run steps 2-7 each time an experiment completes (typically every 2-4 weeks). At Durable level, the `autonomous-optimization` drill automates steps 2-7.
