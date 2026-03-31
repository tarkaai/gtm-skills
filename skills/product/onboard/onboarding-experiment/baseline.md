---
name: onboarding-experiment-baseline
description: >
  Onboarding A/B Tests — Baseline Run. Run always-on onboarding experiments with
  automated variant assignment, continuous funnel tracking, and a structured
  experiment cadence targeting >= 15% activation lift over 4 weeks.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 4 weeks"
outcome: "Winning variant activation rate >= 15% above pre-experiment baseline, validated with >= 100 users per variant"
kpis: ["Activation rate by variant", "Statistical significance (p < 0.05)", "Time to activation by variant", "Tour completion rate by variant", "Email sequence CTR by variant"]
slug: "onboarding-experiment"
install: "npx gtm-skills add product/onboard/onboarding-experiment"
drills:
  - experiment-hypothesis-design
  - posthog-gtm-events
  - activation-optimization
---

# Onboarding A/B Tests — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run 2-3 sequential always-on onboarding experiments over 4 weeks. Each experiment tests a specific hypothesis about the onboarding flow, runs to statistical significance, and produces a clear adopt/revert decision. The cumulative result: a winning onboarding variant that activates users at >= 15% above the pre-experiment baseline, validated with at least 100 users per variant.

## Leading Indicators

- PostHog event taxonomy covers the full onboarding funnel from signup to activation with per-step tracking within the first 2 hours
- First experiment reaches 50 users per variant within 10 days (sufficient signup velocity for the experiment cadence)
- At least 1 of the first 2 experiments shows a statistically significant lift on a secondary metric (tour completion, email CTR) even if primary metric lift is not yet significant
- Experiment cycle time (hypothesis to result) is <= 14 days, enabling 2-3 experiments within the 4-week window

## Instructions

### 1. Instrument the full onboarding funnel

Run the `posthog-gtm-events` drill to establish comprehensive tracking:
- `signup_completed` with properties: signup_source, plan_type, persona_type
- `tour_started`, `tour_step_completed` (with step_number, step_name), `tour_completed`, `tour_dismissed` (with step_number)
- `email_sent`, `email_opened`, `email_clicked` (with email_step, subject_line, variant)
- `first_action_taken` (with action_type), `activation_reached` (with days_since_signup)
- `session_started` for Day 1, Day 3, Day 7 return tracking

Build a PostHog onboarding funnel dashboard showing conversion between each step, filterable by experiment variant and time period.

### 2. Generate the experiment backlog

Run the `experiment-hypothesis-design` drill with target_metric = activation_rate. This produces:
- 3-5 ranked hypotheses based on funnel drop-off analysis, cohort comparison, and session pattern analysis
- Sample size calculations for each hypothesis
- A prioritized backlog in Attio with the top hypothesis marked as "next"

Ensure each hypothesis targets a different onboarding surface or a different aspect of the same surface. Do not queue 3 hypotheses that all test tour copy variations — diversify across tour structure, email timing, empty state design, and in-app nudges.

### 3. Run experiment 1

Run the the onboarding experiment orchestration workflow (see instructions below) drill for the top-ranked hypothesis. This produces:
- PostHog experiment with feature flag, primary/secondary/guardrail metrics
- Variant implemented in Intercom (tour), Loops (email), or product code (empty state)
- Tracking with experiment_variant property on all onboarding events

Let the experiment run until it reaches the required sample size or 14 days, whichever comes first. Do not peek at results.

### 4. Evaluate experiment 1 and launch experiment 2

When experiment 1 completes:
1. Evaluate using the criteria from the the onboarding experiment orchestration workflow (see instructions below) drill
2. If the treatment won: implement permanently, update the baseline activation rate
3. If inconclusive or treatment lost: revert, log the learning
4. Immediately launch experiment 2 from the backlog (the next highest-priority hypothesis)

The key at Baseline is velocity: complete each experiment cleanly, learn, and move to the next one. Do not spend weeks deliberating on marginal results.

### 5. Identify and fix the activation bottleneck

Run the `activation-optimization` drill in parallel with the experiments. This produces:
- Identification of the true activation metric (the action most correlated with 30-day retention)
- Measurement of current activation rate broken down by signup source, plan, and persona
- Friction diagnosis at each drop-off step
- Targeted nudges via Intercom for users stalling at specific steps

The activation optimization work feeds better hypotheses into the experiment pipeline. If the activation metric changes based on this analysis, update the experiment primary metric accordingly.

### 6. Evaluate cumulative result

After 4 weeks and 2-3 experiments:

Run the `threshold-engine` drill (implicit) with this criterion:
- **Pass:** Current activation rate >= 15% above the pre-experiment baseline (the rate before experiment 1 launched). Example: if baseline was 30%, current must be >= 34.5%.
- **Volume:** At least 100 users have gone through the winning onboarding variant
- **Stability:** The winning variant's activation rate in week 4 is within 5pp of its activation rate in week 3 (not a one-time spike)

Decision:
- **Pass:** Proceed to Scalable. Document the winning onboarding configuration, the experiments that got you there, and the hypotheses that failed (equally valuable).
- **Marginal (10-15% lift):** Run 1-2 more experiments targeting the next-highest drop-off step. Re-evaluate after 2 more weeks.
- **Fail (< 10% lift after 3 experiments):** Reassess the activation metric. It may be the wrong metric, or the onboarding problem may require product changes rather than flow optimization.

## Time Estimate

- 3 hours: Event taxonomy setup and funnel dashboard build
- 2 hours: Hypothesis generation and backlog creation
- 3 hours: Experiment 1 setup and variant build
- 2 hours: Experiment 1 evaluation and experiment 2 launch
- 2 hours: Experiment 2 setup and variant build
- 2 hours: Activation optimization analysis (parallel)
- 2 hours: Final evaluation, documentation, and Scalable planning

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel tracking, experiments, feature flags, cohort analysis | Free tier: 1M events/mo, 1M feature flag requests/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Product tour variants, in-app nudge messages | Essential: $29/seat/mo + Proactive Support Plus: $99/mo for 500 messages — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Email sequence variants, behavioral triggers | Free tier: 1,000 contacts, 4,000 emails/mo; Starter: $49/mo for 5,000 contacts — [loops.so/pricing](https://loops.so/pricing) |

**Estimated monthly cost at this level:** $0-148/mo (PostHog free tier likely sufficient; Intercom Proactive Support Plus if testing tours; Loops free tier if under 1,000 contacts)

## Drills Referenced

- the onboarding experiment orchestration workflow (see instructions below) — designs, instruments, runs, and evaluates each A/B test on the onboarding flow with PostHog experiments and per-variant tracking
- `experiment-hypothesis-design` — generates ranked hypotheses from funnel drop-off data and calculates sample sizes for each
- `posthog-gtm-events` — establishes the event taxonomy covering the full onboarding funnel from signup to activation
- `activation-optimization` — identifies the true activation metric, measures current rates, and builds nudges for stalled users
