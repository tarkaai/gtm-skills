---
name: in-app-onboarding-tour-smoke
description: >
  Interactive Product Tour — Smoke Test. Build a minimal in-app product tour for 10-50 new users
  and measure whether guided onboarding produces any activation signal within 7 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=40% of test users reach activation within 7 days"
kpis: ["7-day activation rate", "Tour completion rate", "Median time to activation"]
slug: "in-app-onboarding-tour"
install: "npx gtm-skills add product/onboard/in-app-onboarding-tour"
drills:
  - onboarding-flow
  - threshold-engine
---

# Interactive Product Tour — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run a single product tour for a small group of new users (10-50) and determine whether guided onboarding produces a measurable activation lift. No always-on automation. The agent builds the tour, a human reviews and launches it, and the agent evaluates results after 7 days.

Pass threshold: >=40% of test cohort users reach the activation event within 7 days of signup.

## Leading Indicators

- Tour start rate: >=80% of new users who land on the dashboard see the tour trigger
- Tour completion rate: >=50% of users who start the tour complete all steps
- First-milestone conversion: >=60% of tour completers perform the first core action within 24 hours
- Zero-state escape: >=70% of test users move past the empty state within 48 hours

## Instructions

### 1. Define the activation metric

Identify the single user action that best predicts 30-day retention. Query PostHog to compare retained users (active at day 30) against churned users (inactive by day 30) using cohort analysis. The action that most clearly separates the two groups is your activation metric.

If insufficient data exists, choose the action that most directly delivers your product's core value promise. Document it as a PostHog event: `activation_reached` with properties `{activation_type: "...", days_since_signup: N}`.

### 2. Map onboarding milestones

Define 3-5 milestones on the path from signup to activation. Each milestone is a trackable PostHog event. Example:
1. `signup_completed`
2. `profile_completed`
3. `first_core_action` (e.g., created a project, imported data)
4. `activation_reached`

Instrument each milestone in PostHog using `posthog-custom-events`.

### 3. Build the product tour

Run the `onboarding-flow` drill. Build an Intercom product tour with 3-5 steps that guide users from signup to their first core action. Requirements:
- Each step targets a specific UI element via CSS selector
- At least 2 steps are interactive (user must perform the action to proceed)
- Each step has <25 words of instruction text
- Tour triggers automatically on first login when `onboarding_complete = false`
- Tour includes a skip/dismiss option

Also set up 2-3 contextual in-app messages for users who get stuck (e.g., no progress after 24 hours).

### 4. Set up tracking

Instrument the following PostHog events:
- `tour_started` with `{tour_version: "smoke_v1"}`
- `tour_step_completed` with `{step_number: N, step_name: "..."}`
- `tour_completed` with `{duration_seconds: N}`
- `tour_dismissed` with `{step_number: N}`

Build a PostHog funnel: `tour_started` → `tour_step_1` → `tour_step_2` → ... → `tour_completed` → `activation_reached`.

### 5. Launch to test cohort

**Human action required:** Review the tour experience before launch. Walk through it yourself. Verify all CSS selectors target the correct elements. Then enable the tour via PostHog feature flag for 10-50 new signups only. Monitor the first 2-3 users manually to catch any broken steps.

### 6. Evaluate results

After 7 days, run the `threshold-engine` drill. Query PostHog for the test cohort:
- How many users started the tour?
- How many completed it?
- How many reached activation within 7 days?
- Where did users drop off in the funnel?

Compute: activation rate = (users who reached activation / total test cohort users) * 100.

**PASS** (>=40%): Document what worked. Proceed to Baseline.
**FAIL** (<40%): Analyze the funnel drop-off. If users abandon at a specific step, simplify that step. If users complete the tour but do not activate, the tour is guiding them to the wrong action. Revise the activation metric or the tour flow and re-run.

## Time Estimate

- 1 hour: Define activation metric and milestones
- 2 hours: Build the product tour and instrument tracking
- 0.5 hours: Human review and launch
- 1 hour: Evaluate results after 7 days
- 0.5 hours: Document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free tier: 1M events/mo, 5K session replays ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app messages | Essential: $39/seat/mo + Proactive Support Plus add-on: $99/mo for 500 messages ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated monthly cost at this level:** $0-$138/mo (PostHog free tier likely sufficient; Intercom Proactive Support Plus needed for Product Tours)

## Drills Referenced

- `onboarding-flow` — builds the Intercom product tour, in-app messages, and email sequence for the onboarding experience
- `threshold-engine` — evaluates activation rate against the >=40% pass threshold and recommends next action
