---
name: personalized-onboarding-path-smoke
description: >
  Adaptive Onboarding Paths — Smoke Test. Route 20-50 new signups into
  2 persona-specific onboarding tours based on role and use case. Measure
  whether persona-routed users activate at higher rates than generic-tour users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Persona-routed cohort activation rate >= 50% AND >= 10pp above generic-tour control group"
kpis: ["Activation rate by persona", "Tour completion rate by persona", "Time to activation by persona", "Persona classification accuracy"]
slug: "personalized-onboarding-path"
install: "npx gtm-skills add product/onboard/personalized-onboarding-path"
drills:
  - onboarding-personalization
  - threshold-engine
---

# Adaptive Onboarding Paths — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Route 20-50 new signups into 2 persona-specific onboarding tours. Each persona sees a product tour tailored to their role and fastest path to activation. Measure whether persona-routed users activate at a higher rate than users who received the generic tour. Pass threshold: persona-routed cohort activation rate >= 50% AND >= 10 percentage points above the generic-tour control group.

## Leading Indicators

- Tour completion rate for persona-specific tours exceeds 60% (generic tours typically complete at 40-50%)
- At least 1 persona cohort reaches activation faster (fewer median hours from signup) than the control group
- Persona classification matches self-reported role in >= 80% of cases (verify with a post-tour micro-survey)
- Drop-off at tour step 2 is lower for persona tours than for the generic tour (step 2 is where generic tours lose relevance)

## Instructions

### 1. Define persona segments and build persona-specific tours

Run the `onboarding-personalization` drill. This produces:
- 2 persona segments defined from your existing activated-user data in PostHog (e.g., "Solo Creator" vs "Team Lead", or "Marketer" vs "Developer")
- A persona-specific activation metric for each segment (the action that best predicts retention for that persona)
- 2 Intercom product tours, each 3-5 steps, focused on reaching that persona's activation metric
- A PostHog feature flag `onboarding-tour-persona` routing users to the correct tour based on `persona_type` property
- Per-persona tracking events: `tour_started`, `tour_step_completed`, `tour_completed`, `tour_dismissed`, `activation_reached` — all with `persona_type` property

For the smoke test, keep persona detection simple: use a single signup-form dropdown ("What best describes your role?") mapped to `persona_type` in both PostHog and Intercom. Do not build automated classification yet — that comes at Scalable.

Fallback: users without a detected persona get the existing generic tour.

### 2. Select and split the test cohort

Identify 40-100 upcoming signups (or wait for them to accumulate over 3-5 days). Split them:
- **Treatment group (20-50 users):** Routed to persona-specific tours via the PostHog feature flag
- **Control group (20-50 users):** Receive the existing generic onboarding tour

Log group assignment as a PostHog person property: `onboarding_path_cohort: "personalized"` or `"generic"`.

**Human action required:** Review each persona tour in Intercom before launching. Walk through every step as a test user. Verify that tooltips point to the correct UI elements, CTAs are clickable, and the copy is specific to the persona (not generic advice). Enable the feature flag only after manual review passes.

### 3. Run the test for 7 days

During the 7-day test window:
- Monitor PostHog Live Events daily to confirm tour events are firing with correct `persona_type` values
- Check for classification errors: if a user's actual behavior contradicts their persona assignment (e.g., a "Team Lead" who never invites anyone), note it
- Do not change the tours mid-test — record observations for post-test iteration

### 4. Evaluate against threshold

Run the `threshold-engine` drill with these criteria:

- **Activation rate >= 50%** for the persona-routed treatment group (combined across all personas)
- **Lift >= 10pp** above the generic-tour control group's activation rate
- **Per-persona check:** Neither persona's activation rate falls below 35% (if one persona drags down the average, the persona definition or tour needs iteration, not the overall approach)

Decision tree:
- **Pass (>= 50% activation, >= 10pp lift):** Proceed to Baseline. Document which persona activated fastest and why.
- **Marginal (>= 40% activation OR >= 5pp lift but not both):** Iterate on the weaker persona's tour. Re-run with 20 more users.
- **Fail (< 40% activation AND < 5pp lift):** The persona segments may be wrong. Re-analyze activated users in PostHog to find better segmentation dimensions. Re-run.

## Time Estimate

- 2 hours: Persona analysis and segment definition (PostHog cohort analysis)
- 2 hours: Building 2 persona-specific Intercom tours + feature flag setup
- 30 minutes: Cohort selection and group assignment
- 30 minutes: Daily monitoring (5 min/day x 7 days)
- 1 hour: Final analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohort analysis, feature flags, event tracking, funnels | Free tier: 1M events/mo, 1M feature flag requests/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tours (2 persona-specific + 1 generic fallback) | Essential: $29/seat/mo + Proactive Support Plus add-on: $99/mo for 500 messages — [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated monthly cost at this level:** $0-128/mo (PostHog free tier likely sufficient; Intercom only if not already in stack)

## Drills Referenced

- `onboarding-personalization` — defines persona segments, builds persona-specific Intercom tours, sets up PostHog feature flag routing and per-persona tracking events
- `threshold-engine` — evaluates activation rate and lift against pass/fail criteria and recommends next action
