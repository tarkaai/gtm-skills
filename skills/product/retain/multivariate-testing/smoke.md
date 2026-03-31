---
name: multivariate-testing-smoke
description: >
  Multivariate Experiments — Smoke Test. Design and run your first multivariate test
  to prove that testing multiple variables simultaneously produces combination insights
  that A/B tests cannot.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Run 2 MVTs with documented combination rankings"
kpis: ["MVT velocity", "Win rate", "Combination insights"]
slug: "multivariate-testing"
install: "npx gtm-skills add product/retain/multivariate-testing"
drills:
  - threshold-engine
---

# Multivariate Experiments — Smoke Test

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Run 2 complete multivariate experiments against in-product retention surfaces. Each experiment must test at least 2 variables simultaneously and produce a ranked list of combinations with conversion rates. The goal is to prove that MVT reveals interaction effects (synergies or conflicts between variables) that sequential A/B tests miss.

## Leading Indicators

- Test matrix designed with orthogonal variable assignment within the first 2 hours
- Feature flags created in PostHog with even traffic split across all cells within 1 day
- Per-cell event data flowing in PostHog within 48 hours of launch
- At least 1 experiment reaches minimum sample size within the week

## Instructions

### 1. Select your first MVT surface

Pick a retention-relevant in-product surface with enough traffic for a 2x2 test (4 cells). Good candidates:

- **Upgrade prompt**: test copy framing (loss-aversion vs. gain) x CTA placement (inline vs. modal)
- **Feature discovery tooltip**: test tooltip timing (immediate vs. after 3rd session) x content type (text vs. animated GIF)
- **Re-engagement in-app message**: test urgency level (gentle vs. strong) x personalization (generic vs. usage-based)

You need at least 200 users per cell per week. If your product has <800 weekly active users on this surface, pick a higher-traffic surface or reduce to a 2x2 matrix.

### 2. Design the experiment matrix

Run the the mvt experiment design workflow (see instructions below) drill. For this smoke test, keep it minimal:

- 2 variables, 2 levels each (4 cells total)
- Document the exact experience each cell sees
- Create PostHog feature flags for each variable
- Set the primary metric: the retention or conversion event you want to improve
- Set guardrail metrics: error rate, support ticket rate

**Human action required:** Review the test matrix before launching. Confirm that all 4 cell experiences are implemented correctly by manually testing each variant combination. Verify events fire for each cell.

### 3. Run the first experiment

Launch the experiment. Monitor PostHog daily to confirm traffic is splitting evenly across cells. After reaching minimum sample size (or 5 days, whichever comes first), stop enrollment and allow 48 hours for lagging conversions.

Manually analyze results: rank all 4 cells by conversion rate. Identify the winning combination. Check for interaction effects -- does any combination perform notably better or worse than the individual variable effects would predict?

### 4. Run the second experiment

Apply learnings from experiment 1. Either:
- Test different variables on the same surface
- Test the same variables on a different retention surface
- Extend the winning combination with a third variable (producing a 2x2x2 = 8 cells, if traffic allows)

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: Run 2 MVTs with documented combination rankings. If PASS, proceed to Baseline. If FAIL, diagnose: was traffic insufficient (pick a higher-traffic surface), were variables poorly chosen (pick variables with more expected impact), or was the metric too noisy (pick a cleaner conversion event).

## Time Estimate

- 1 hour: surface selection and variable identification
- 1.5 hours: experiment matrix design and PostHog configuration
- 0.5 hours: implementation verification
- 1 hour: monitoring and first experiment analysis
- 1 hour: second experiment design, run, and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking | Free tier: 1M flag requests/mo, 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- the mvt experiment design workflow (see instructions below) — designs the test matrix, configures feature flags, and computes sample size requirements
- `threshold-engine` — evaluates pass/fail against the smoke test threshold
