---
name: page-layout-testing-smoke
description: >
  UI/UX Experimentation — Smoke Test. Manually test 3 page layout variations on a small
  user sample to validate that layout changes produce measurable engagement signal.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Test 3 layouts and measure engagement delta on each"
kpis: ["Click-through rate per layout variant", "Scroll depth per variant", "Time-on-page per variant"]
slug: "page-layout-testing"
install: "npx gtm-skills add product/retain/page-layout-testing"
drills:
  - threshold-engine
---

# UI/UX Experimentation — Smoke Test

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Test 3 distinct page layout variations on 10-50 users each. For each variant, capture click-through rate, scroll depth, and time-on-page. Pass threshold: at least one variant shows a measurable engagement delta (positive or negative) relative to the current layout — proving that layout changes move the metric at all.

## Leading Indicators

- PostHog events firing correctly for all 3 variants within the first 24 hours
- Session recordings captured for at least 10 users per variant
- At least one friction pattern identified from recording review

## Instructions

### 1. Identify the target page and form hypotheses

Select the highest-traffic page that contributes to retention (e.g., the main dashboard, a key feature page, or the settings/configuration flow). Using PostHog funnel data, identify the page with the highest drop-off rate.

Form 3 hypotheses — one per variant. Each hypothesis must follow the format: "If we [specific layout change], then [metric] will [change by X%], because [reason]."

Example hypotheses for a dashboard page:
- Variant A: Move the primary CTA above the fold. Expected: +10% click-through because 60% of users never scroll past the fold.
- Variant B: Replace the feature grid with a single-column list. Expected: +15% scroll depth because list layouts reduce cognitive load.
- Variant C: Add contextual tooltips to the 3 most-used elements. Expected: +8% time-on-page because tooltips increase exploration.

### 2. Build and instrument the 3 layout variants

Run the the layout variant builder workflow (see instructions below) drill for each of the 3 variants. For the Smoke level, create PostHog feature flags with low rollout percentages (10-20% per variant, remaining traffic stays on control). Instrument these events on every variant:

- `layout_variant_viewed` — user saw this variant (with `variant` property)
- `layout_cta_clicked` — user clicked the primary CTA
- `layout_scroll_depth` — scroll milestones at 25%, 50%, 75%, 100%
- `layout_time_on_page` — time spent before navigating away

**Human action required:** Implement the actual layout changes in your product code behind the feature flags. The agent instruments events and creates flags; a developer deploys the code changes.

### 3. Review session recordings for friction signals

Run the the session recording friction analysis workflow (see instructions below) drill on the target page. Review 10-15 recordings of the current layout (before variants go live) to establish a baseline friction profile. Document:

- Where users hesitate or scroll back and forth
- Which elements get rage-clicked
- Where users abandon the page

After variants are live for 3+ days with 10+ users per variant, review recordings for each variant to compare friction patterns against the baseline.

### 4. Evaluate against pass threshold

Run the `threshold-engine` drill. Pass criteria: at least one of the 3 variants shows a measurable engagement delta (>5% change in any primary metric). This proves that layout changes affect user behavior on this page and justifies investing in structured A/B testing at Baseline.

If none of the 3 variants move any metric, either the page is already well-optimized (unlikely) or the changes were too subtle. Test bolder layout changes.

## Time Estimate

- 1 hour: Identify target page, analyze funnel data, form hypotheses
- 2 hours: Build feature flags, instrument events, configure recordings
- 1 hour: Review baseline session recordings and document friction
- 1 hour: Review variant recordings and evaluate threshold after 5-7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, session recording, funnels | Free tier: 1M events + 5K recordings/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- the layout variant builder workflow (see instructions below) — creates feature flags, instruments events, and wires up variant rendering for each layout test
- the session recording friction analysis workflow (see instructions below) — reviews session recordings to identify friction patterns and quantify their impact
- `threshold-engine` — evaluates measured results against the pass/fail threshold
