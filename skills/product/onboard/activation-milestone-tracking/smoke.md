---
name: activation-milestone-tracking-smoke
description: >
  Activation Milestone Tracking — Smoke Test. Define 5+ activation milestones,
  instrument them in PostHog, and measure whether at least 40% of a test cohort
  reaches the primary activation event within 14 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "5+ milestones instrumented, ≥40% of test cohort reaches primary milestone within 14 days"
kpis: ["Activation rate", "Milestone completion rate per step", "Time-to-activation (median minutes)"]
slug: "activation-milestone-tracking"
install: "npx gtm-skills add product/onboard/activation-milestone-tracking"
drills:
  - posthog-gtm-events
  - activation-optimization
  - threshold-engine
---

# Activation Milestone Tracking — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

5+ activation milestones defined and instrumented in PostHog. A test cohort of 20-50 new signups produces measurable milestone data. At least 40% of the cohort reaches the primary activation milestone within 14 days. You have a PostHog funnel showing step-by-step conversion from signup to activation.

## Leading Indicators

- All 5+ milestone events are firing in PostHog (verify via Live Events view)
- Funnel visualization renders with non-zero counts at each step
- At least 20 users have entered the funnel within the first 3 days
- Drop-off points between milestones are visible and vary by step (not all zero or all 100%)

## Instructions

### 1. Define your activation milestones

Identify 5-6 sequential actions that represent a new user's path from signup to full product activation. Run the `activation-optimization` drill (Steps 1-2 only) to find the actions that best correlate with 30-day retention. Typical milestone sequence:

1. **Account created** — user completes signup
2. **Profile/workspace configured** — user sets up their environment
3. **First core action** — user performs the product's primary action (e.g., creates a project, imports data, sends a message)
4. **Value moment** — user sees a meaningful result from their action (e.g., receives a report, completes a workflow, gets a response)
5. **Return session** — user comes back within 48 hours and performs another core action
6. **Activation reached** — composite event marking the user as "activated" (typically milestone 3 or 4, validated against retention data)

**Human action required:** Review the milestone definitions with your product team. Confirm that these milestones represent real user value moments, not just UI interactions. Validate that the activation milestone correlates with retention by checking: do users who complete it retain at 2x+ the rate of those who do not?

### 2. Instrument milestone events in PostHog

Run the `posthog-gtm-events` drill to implement tracking for each milestone. For each milestone, create a PostHog event:

- `activation_milestone_1_completed` (account_created)
- `activation_milestone_2_completed` (workspace_configured)
- `activation_milestone_3_completed` (first_core_action)
- `activation_milestone_4_completed` (value_moment)
- `activation_milestone_5_completed` (return_session)
- `activation_reached` (composite activation event)

Attach these properties to every milestone event:
- `milestone_number`: integer (1-6)
- `milestone_name`: string (human-readable name)
- `signup_source`: string (organic, paid, referral, direct)
- `plan_type`: string (free, trial, paid)
- `minutes_since_signup`: integer (time from signup to this milestone)
- `session_number`: integer (which session this occurred in)

Build a PostHog funnel: `signup_completed` → `activation_milestone_1_completed` → ... → `activation_reached`. Break down by signup source and plan type.

### 3. Run the test cohort

Launch the instrumented tracking and wait for 20-50 new signups to enter the funnel over 3-7 days. Do not change the product experience during this period — you are measuring the current state.

Monitor the PostHog Live Events view daily to confirm events are firing correctly. Check for:
- Events with missing properties (fix instrumentation)
- Events firing in the wrong order (fix event logic)
- Duplicate events for the same user-milestone pair (add deduplication)

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure results after the test cohort has had 14 days to activate. Pass criteria:

- **5+ milestones instrumented:** All milestone events appear in PostHog with correct properties.
- **≥40% activation rate:** At least 40% of the test cohort reached the `activation_reached` event within 14 days.

If PASS: You have validated milestone definitions and instrumentation. Proceed to Baseline.

If FAIL on instrumentation: Fix event tracking gaps and re-run with a new cohort.

If FAIL on activation rate: Either the activation threshold is set too aggressively (lower it to match reality) or the product has a genuine activation problem (prioritize fixing the biggest funnel drop-off before proceeding).

## Time Estimate

- 1.5 hours: Define milestones and validate with retention data
- 2 hours: Instrument events in PostHog and build funnel
- 0.5 hours: Monitor and fix instrumentation issues
- 1 hour: Analyze results and evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, cohort analysis | Free up to 1M events/month; paid starts at ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — defines the event taxonomy and implements milestone tracking in PostHog
- `activation-optimization` — identifies the true activation metric by analyzing retained vs. churned users
- `threshold-engine` — evaluates pass/fail against the 40% activation threshold
