---
name: page-layout-testing-baseline
description: >
  UI/UX Experimentation — Baseline Run. Run continuous A/B tests on the winning layout
  direction from Smoke, targeting a statistically significant 15%+ engagement lift.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=15% statistically significant engagement lift (95% confidence)"
kpis: ["Primary engagement metric lift %", "Statistical significance level", "Conversion rate change", "Session duration change"]
slug: "page-layout-testing"
install: "npx gtm-skills add product/retain/page-layout-testing"
drills:
  - ab-test-orchestrator
  - posthog-gtm-events
---

# UI/UX Experimentation — Baseline Run

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Run a properly powered A/B test on the best-performing layout direction from Smoke. Achieve a statistically significant engagement lift of >=15% at 95% confidence. This is the first always-on experiment — the feature flag stays active and PostHog continuously collects data until statistical significance is reached.

## Leading Indicators

- Both variants receiving roughly equal traffic (50/50 split, no sample ratio mismatch)
- Primary metric trending in the hypothesized direction within the first 3 days
- No guardrail metrics breached (bounce rate, error rate stable across variants)
- Sample size accumulating on pace to reach significance within 2 weeks

## Instructions

### 1. Set up comprehensive event tracking

Run the `posthog-gtm-events` drill to instrument the target page with production-grade tracking. Go beyond Smoke-level events:

- `page_layout_test_impression` — variant shown (properties: `test_name`, `variant`, `user_id`, `device_type`, `referrer`)
- `page_layout_test_engaged` — user interacted meaningfully (clicked, typed, expanded, toggled)
- `page_layout_test_converted` — user completed the target action (e.g., submitted a form, started a workflow, upgraded)
- `page_layout_test_retained` — user returned to this page within 7 days

Build PostHog funnels showing the complete path: impression -> engaged -> converted -> retained. Create a dashboard with these funnels segmented by variant.

### 2. Design and launch the A/B test

Run the `ab-test-orchestrator` drill. Take the winning variant direction from Smoke and refine it into a polished production variant:

1. **Calculate required sample size.** Using the Smoke data as your baseline conversion rate and 15% lift as the minimum detectable effect, compute the sample size needed for 95% significance / 80% power. If your page gets 100 visitors/day and you need 400 per variant, the test runs for 8 days.

2. **Create the PostHog experiment.** Link it to the feature flag from the the layout variant builder workflow (see instructions below) drill. Set the primary metric (the engagement event that showed the strongest signal in Smoke). Add secondary metrics: bounce rate, error rate, and conversion rate as guardrails.

3. **Set traffic allocation to 50/50.** At Baseline, you need statistical power — allocate half of all traffic to each variant. No holdout group at this stage.

4. **Set the experiment duration.** Minimum: 7 days (to capture day-of-week effects). Maximum: 14 days. If significance is not reached in 14 days, the effect is too small to matter at this traffic level — either increase traffic or test a bolder change.

### 3. Build the refined layout variant

Run the the layout variant builder workflow (see instructions below) drill to create the production-quality variant:

- Polish the layout change from Smoke into a production-ready implementation
- Ensure responsive behavior across desktop, tablet, and mobile
- Verify all interactive elements function correctly in the variant
- Confirm session recording is active for both variants

**Human action required:** Deploy the refined variant code behind the existing feature flag. QA both variants on staging before enabling the experiment.

### 4. Monitor and evaluate

Do not check results daily and call a winner early. Set a calendar reminder for the planned end date. The only reason to intervene before then:

- A guardrail metric (error rate, bounce rate) spikes >2x in either variant
- Sample ratio mismatch detected (variant/control split deviates >5% from 50/50)
- A critical product bug is introduced in either variant

At the end of the test period, evaluate:
- Is the result statistically significant at 95% confidence?
- Is the lift >=15%?
- Are secondary metrics (bounce rate, error rate) neutral or improved?

**PASS:** Lift >=15% at 95% significance. Implement the winning variant as the new default. Proceed to Scalable.
**FAIL:** Lift <15% or not significant. Review session recordings from both variants to understand why. Form a new hypothesis and re-run at Baseline.

## Time Estimate

- 2 hours: Set up production event tracking and dashboards
- 3 hours: Calculate sample size, configure experiment, build refined variant
- 2 hours: QA both variants across devices
- 1 hour: Deploy and verify experiment is collecting data
- 8 hours: Monitor over 2 weeks (30 min/day check-ins for guardrails only)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, session recording | Free tier covers most startups; paid starts at $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- the layout variant builder workflow (see instructions below) — creates the production-quality layout variant with full instrumentation
- `ab-test-orchestrator` — designs the experiment, calculates sample size, sets significance criteria, and manages the test lifecycle
- `posthog-gtm-events` — sets up comprehensive event tracking for the experiment
