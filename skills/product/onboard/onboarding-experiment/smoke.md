---
name: onboarding-experiment-smoke
description: >
  Onboarding A/B Tests — Smoke Test. Run one A/B test on the highest-drop-off
  onboarding surface for 10-50 new signups. Prove that a structured hypothesis
  produces measurable activation lift before investing in always-on experimentation.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: "Treatment variant activation rate >= control AND test reaches >= 20 users per variant"
kpis: ["Activation rate (control vs treatment)", "Tour completion rate by variant", "Time to activation by variant", "Funnel drop-off delta at tested step"]
slug: "onboarding-experiment"
install: "npx gtm-skills add product/onboard/onboarding-experiment"
drills:
  - onboarding-experiment-orchestration
  - threshold-engine
---

# Onboarding A/B Tests — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run one structured A/B test on the single highest-drop-off onboarding surface. Test with 10-50 new signups per variant over 2 weeks. Prove that a data-driven hypothesis about onboarding flow changes produces a measurable signal in activation rate. Pass threshold: treatment variant activation rate equals or exceeds control, and the test reaches at least 20 users per variant.

## Leading Indicators

- Onboarding funnel successfully instrumented in PostHog with per-step drop-off visibility within the first 2 hours
- Hypothesis identifies a specific step where >= 30% of users drop off (clear improvement opportunity exists)
- Feature flag correctly splits new signups into control and treatment (verify in PostHog Live Events within first 24 hours)
- Treatment variant tour completion rate or email CTR is directionally higher than control within the first 5 days (not statistically significant yet, but directionally correct)

## Instructions

### 1. Identify the test target and design the experiment

Run the `onboarding-experiment-orchestration` drill. This produces:
- A PostHog funnel analysis of your current onboarding flow showing per-step drop-off rates
- The single highest-drop-off surface identified (product tour, email, empty state, or checklist)
- A structured hypothesis: "If we [change X], then [metric Y] will [improve by Z], because [data-supported reasoning]"
- A PostHog feature flag splitting new signups 50/50 into control and treatment
- A PostHog experiment configured with activation_reached as primary metric, tour_completed and time_to_activation as secondary metrics
- Tracking events with `experiment_variant` property on all onboarding events

For the smoke test, keep the variant simple. Test ONE change to ONE surface:
- Shorten a 7-step tour to 3 steps
- Change the Day 1 email CTA from generic ("Explore your dashboard") to specific ("Create your first [object]")
- Add sample data to an empty state
- Change tour trigger timing from immediate to after first page view

Do NOT test multiple changes simultaneously — isolate the variable.

**Human action required:** Review the treatment variant before enabling the feature flag. Walk through the variant as a test user. Verify the experience makes sense, CTAs work, and the change matches the hypothesis. Enable the flag only after manual review.

### 2. Run the test for 2 weeks

Let the experiment run without modification. Monitor PostHog Live Events daily (5 minutes) to confirm:
- Both variants are receiving users (flag is working)
- Tracking events fire with correct `experiment_variant` property
- No errors or broken flows in either variant

Do not check activation results until the test period ends. Record qualitative observations (user behavior patterns, support tickets mentioning onboarding) in a note but do not act on them during the test.

### 3. Evaluate against threshold

Run the `threshold-engine` drill with these criteria:

- **Primary:** Treatment variant activation rate >= control activation rate
- **Volume:** At least 20 users in each variant completed the test window (14 days from signup)
- **Guardrail:** Support ticket rate did not spike > 2x for treatment variant

Decision tree:
- **Pass (treatment >= control, sufficient volume):** The hypothesis produced signal. Document the result: variant description, activation rates, qualitative observations. Proceed to Baseline.
- **Marginal (treatment directionally better but < 20 per variant):** Extend the test for 1 more week if possible. If still insufficient volume, document the directional result and proceed to Baseline with the caveat that the first Baseline experiment should re-test this hypothesis at higher volume.
- **Fail (treatment worse than control):** The hypothesis was wrong. Investigate why. Check session recordings for 5 treatment users to understand where they struggled. Generate a new hypothesis targeting a different surface or a different change to the same surface. Re-run this level.

## Time Estimate

- 2 hours: Funnel analysis, hypothesis formation, experiment setup in PostHog
- 1 hour: Build the treatment variant (modified tour, email, or empty state)
- 30 minutes: Manual review and flag activation
- 1.5 hours: Daily monitoring over 2 weeks (5 min/day x 14 days + buffer)
- 1 hour: Final analysis, threshold evaluation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analysis, feature flags, experiment tracking, event analytics | Free tier: 1M events/mo, 1M feature flag requests/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tour variant (if testing tours) | Essential: $29/seat/mo + Proactive Support Plus: $99/mo for 500 messages — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Email sequence variant (if testing emails) | Free tier: 1,000 contacts, 4,000 emails/mo — [loops.so/pricing](https://loops.so/pricing) |

**Estimated monthly cost at this level:** Free (PostHog and Loops free tiers sufficient for smoke-test volume; Intercom only if not already in stack)

## Drills Referenced

- `onboarding-experiment-orchestration` — identifies the highest-drop-off onboarding surface, structures the hypothesis, sets up the PostHog experiment with feature flag splitting and per-variant tracking
- `threshold-engine` — evaluates treatment vs control activation rates against pass/fail criteria and recommends next action
