---
name: layout-variant-builder
description: Design, instrument, and deploy page layout variants for A/B testing using PostHog feature flags
category: Experimentation
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-session-recording
  - n8n-workflow-basics
---

# Layout Variant Builder

This drill produces deployable page layout variants — each instrumented with PostHog events so an A/B test can measure which layout performs better. It covers variant specification, event instrumentation, feature flag wiring, and QA validation.

## Prerequisites

- PostHog SDK installed in the product with feature flags enabled
- Session recording enabled for qualitative review
- A hypothesis about which layout element to change and the expected impact
- A primary metric already tracked in PostHog (e.g., `cta_clicked`, `form_submitted`, `page_scroll_depth`)

## Input

- **Target page:** The URL path or route of the page being tested
- **Element to vary:** What changes between control and variant (e.g., hero section order, CTA placement, sidebar vs. no sidebar, card grid vs. list view)
- **Hypothesis:** "If we [change], then [metric] will [improve by X%], because [reason]"
- **Primary metric event name:** The PostHog event that determines the winner

## Steps

### 1. Specify variants

Define exactly what differs between control and variant. Be precise:

- **Control (A):** Current production layout. Document the current state: element order, spacing, CTA position, content hierarchy.
- **Variant (B):** The changed layout. Describe the exact difference. Only change one layout variable per test — if you change CTA position AND headline copy simultaneously, you cannot attribute the result.

If testing more than 2 variants (multivariate), ensure traffic supports it. Each variant needs a minimum 200 conversions for statistical power. Three variants = 3x the traffic requirement.

### 2. Create the PostHog feature flag

Using the `posthog-feature-flags` fundamental, create a feature flag for the test:

```
POST /api/projects/<project_id>/feature_flags/
{
  "key": "layout-test-<page>-<element>-<date>",
  "name": "Layout test: <description>",
  "filters": {
    "groups": [{
      "properties": [],
      "rollout_percentage": 100
    }],
    "multivariate": {
      "variants": [
        {"key": "control", "rollout_percentage": 50},
        {"key": "variant-b", "rollout_percentage": 50}
      ]
    }
  }
}
```

Use a descriptive flag key that includes the page, element, and date. This prevents confusion when multiple layout tests run over time.

### 3. Instrument variant rendering

In your product code, check the feature flag and render the appropriate layout:

```javascript
const variant = posthog.getFeatureFlag('layout-test-<page>-<element>-<date>')

// Track that the user saw this variant
posthog.capture('layout_variant_viewed', {
  test_name: '<test-name>',
  variant: variant,
  page: '<page-path>'
})

// Render the correct layout
if (variant === 'variant-b') {
  renderVariantB()
} else {
  renderControl()
}
```

Using `posthog-custom-events`, instrument every interaction point within the layout:

- `layout_element_visible` — the element entered the viewport (use IntersectionObserver)
- `layout_cta_clicked` — user clicked the primary CTA
- `layout_scroll_depth` — user scrolled past 25%, 50%, 75%, 100% of the page
- `layout_time_on_section` — time spent in the changed section (fire on section exit)

Each event must include `test_name` and `variant` as properties so results can be filtered.

### 4. Enable session recording for the test

Using `posthog-session-recording`, configure recording for users in the test:

- Set a recording filter for users where the feature flag is active
- This captures qualitative data: do users in variant B scroll differently? Do they hesitate at the CTA? Do they rage-click anything?
- Plan to review 10-15 recordings per variant after the test ends

### 5. QA the variants

Before launching, verify both variants:

1. Force the feature flag to `control` — confirm the page renders correctly, all events fire, and session recording captures
2. Force the feature flag to `variant-b` — confirm the layout change is visible, all events fire with the correct variant property
3. Check that the primary metric event fires in both variants
4. Verify on mobile, tablet, and desktop viewports

### 6. Launch and hand off to experiment

Using `n8n-workflow-basics`, create a workflow that monitors the test status:

- Trigger: daily cron
- Check: query PostHog for sample size per variant
- If both variants have reached the target sample size, send a notification that the experiment is ready for analysis
- If a guardrail metric (error rate, bounce rate) spikes >2x in either variant, send an alert and disable the flag

## Output

- A PostHog feature flag controlling the layout variants
- Instrumented events on both variants tracking all interactions
- Session recordings capturing qualitative behavior data
- A monitoring workflow alerting when the test is ready for analysis or when guardrails are breached
