---
name: time-to-value-optimization-smoke
description: >
  Time-to-Value Acceleration — Smoke Test. Instrument the signup-to-activation funnel, observe
  10-50 users completing the onboarding flow, and measure whether 50%+ reach first value in
  under 10 minutes. No automation — agent prepares instrumentation, human observes behavior.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=50% of test cohort reaches first value moment in <10 minutes"
kpis: ["Median time to first value (minutes)", "Activation rate (% reaching value moment within 14 days)", "Step completion rate per onboarding milestone"]
slug: "time-to-value-optimization"
install: "npx gtm-skills add product/onboard/time-to-value-optimization"
drills:
  - posthog-gtm-events
  - onboarding-flow
  - threshold-engine
---

# Time-to-Value Acceleration — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

50% or more of a 10-50 user test cohort reaches the product's first value moment in under 10 minutes from signup. You have a working instrumentation layer that tracks every onboarding milestone and a clear definition of what "first value" means for your product.

## Leading Indicators

- PostHog events firing correctly for every onboarding milestone (signup_completed through activation_reached)
- Onboarding funnel visible in PostHog with step-by-step conversion rates
- At least 10 users have completed the full funnel within the test window
- Time-to-value distribution is measurable (median, p75, p90 visible in PostHog)

## Instructions

### 1. Define the activation metric and onboarding milestones

Run the `onboarding-flow` drill, Step 1 only (Map the onboarding milestones). Define:

- The single action that constitutes "first value" for your product. This is the action most correlated with 30-day retention. Examples: created first project, ran first workflow, saw first result, sent first message.
- 3-5 intermediate milestones between signup and activation. Each must be a discrete, trackable event.

Document the milestones as PostHog event names:
```
signup_completed
profile_completed
first_core_action_taken
value_moment_reached (this is your activation metric)
```

**Human action required:** Validate the activation metric. If you have 30+ days of usage data, check that users who complete this action retain at 2x+ the rate of those who do not. If you lack data, pick the action that most directly delivers the core value promise and validate later at Baseline.

### 2. Instrument the activation funnel in PostHog

Run the `posthog-gtm-events` drill. Configure the following events and properties:

| Event | Properties | Trigger |
|-------|-----------|---------|
| `signup_completed` | `signup_source`, `plan_type`, `timestamp` | User completes registration |
| `onboarding_step_N_completed` | `step_name`, `step_number`, `time_since_signup_seconds` | User completes each milestone |
| `activation_reached` | `activation_type`, `time_to_value_seconds`, `signup_source` | User reaches first value moment |
| `onboarding_abandoned` | `last_step_completed`, `time_since_signup_seconds` | User does not complete next step within 48 hours |

Critical: capture `time_since_signup_seconds` as a numeric property on every event. This is the raw data for the TTV metric. Calculate it server-side as `current_timestamp - signup_timestamp`.

Build a PostHog funnel: `signup_completed` -> each milestone in order -> `activation_reached`. Set the conversion window to 14 days.

### 3. Build the in-app onboarding experience

Run the `onboarding-flow` drill, Steps 2-4 (product tours, contextual messages, email sequence). For the Smoke test, keep it minimal:

- One Intercom product tour that guides users from signup to the first core action (3-5 steps max)
- One Loops welcome email sent immediately on signup with a direct link to the first action (not to the dashboard)
- One contextual Intercom message that appears if the user has not completed the first core action within 2 hours

Do not build the full 7-email sequence at Smoke. One tour, one email, one nudge.

**Human action required:** Review the product tour copy and welcome email before launching. Ensure the CTA links go directly to the action, not to a generic page. Launch to a test group of 10-50 new users.

### 4. Observe and measure

Over 5-7 days, monitor the PostHog funnel daily. For each user in the test cohort:

- Did they complete each milestone?
- How long did each step take?
- Where did users who did NOT activate drop off?
- Were there rage-clicks, repeated actions, or session recordings showing confusion?

Pull session recordings (PostHog session replay) for users who dropped off at each step. Watch 5+ recordings per drop-off point to identify friction patterns.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Measure:

- **Primary metric:** What percentage of the test cohort reached `activation_reached` in under 10 minutes?
- **Threshold:** >= 50%

If PASS: Document the activation metric, the funnel, and the onboarding flow. Proceed to Baseline.

If FAIL: Identify the biggest drop-off step from the funnel data. Simplify that step (reduce fields, add guidance, pre-fill data). Re-run with a fresh cohort of 10-50 users. Do not proceed to Baseline until the Smoke threshold passes.

## Time Estimate

- 1 hour: Define activation metric and milestones
- 1.5 hours: Instrument PostHog events and build the funnel
- 1 hour: Build product tour, welcome email, and contextual message
- 1.5 hours: Monitor, analyze session recordings, and evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, session recordings | Free up to 1M events/mo, 5K recordings/mo — https://posthog.com/pricing |

## Drills Referenced

- `posthog-gtm-events` — instrument the activation funnel with a standard event taxonomy
- `onboarding-flow` — build the in-app onboarding experience (product tour, email, contextual messages)
- `threshold-engine` — evaluate the activation rate against the pass threshold
