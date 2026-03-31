---
name: setup-wizard-smoke
description: >
  Guided Setup Wizard — Smoke Test. Build a minimal interactive setup wizard for
  one persona, instrument it with PostHog tracking, launch to 10-20 users, and
  measure whether >=65% complete the wizard within 7 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=65% wizard completion rate among test cohort within 7 days"
kpis: ["Wizard completion rate", "Median time to complete (minutes)", "Config success rate", "Step-level dropoff"]
slug: "setup-wizard"
install: "npx gtm-skills add product/onboard/setup-wizard"
drills:
  - wizard-step-builder
  - onboarding-flow
  - threshold-engine
---

# Guided Setup Wizard — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=65% of test users who start the wizard complete all steps within 7 days. Configurations created by the wizard actually work (data source connected, workspace configured, first object created). Median time to complete is under 15 minutes.

## Leading Indicators

- Step 1 (profile completion) has >90% completion within 1 hour of signup
- No single step has >40% dropoff
- `wizard_step_failed` events are <10% of `wizard_step_started` events per step
- Users who complete the wizard return for a second session within 48 hours at 2x the rate of users who do not

## Instructions

### 1. Define the wizard steps for your primary persona

Choose your highest-volume persona (the one most new signups match). Define 4-6 setup steps using the `wizard-step-builder` drill. Each step must have:
- A clear action the user takes
- A binary validation (done or not done)
- A PostHog event that fires on completion

For the Smoke test, build ONE wizard variant for ONE persona. Do not build persona routing yet.

**Human action required:** Review the step list before building. Confirm each step is necessary for initial setup and can be completed in under 3 minutes. Remove any step that is "nice to have" rather than required.

### 2. Build the wizard using Intercom Checklists

Run the `wizard-step-builder` drill to create:
- An Intercom Checklist with the steps from Step 1
- Auto-completion rules tied to your app's user attribute updates
- PostHog event tracking for every step: `wizard_step_started`, `wizard_step_completed`, `wizard_step_failed`
- A completion event: `wizard_completed`

Skip the persona-variant feature flags for Smoke -- hardcode the single variant. Skip the Product Tour stops for now -- use simple link actions in the checklist that deep-link to the relevant setup page.

### 3. Set up the onboarding flow around the wizard

Run the `onboarding-flow` drill to configure:
- An Intercom in-app welcome message that introduces the checklist on first login
- A Loops welcome email (sent immediately on signup) with one CTA: "Complete your setup" linking to your app's setup page
- A PostHog funnel tracking: `signup_completed` -> `wizard_step_completed (step=1)` -> ... -> `wizard_completed`

### 4. Launch to a test group

Use a PostHog feature flag to show the wizard only to 10-20 new signups. Set the flag to target users where `signup_completed_at` is within the test period.

**Human action required:** Monitor the first 3-5 users manually. Watch PostHog Live Events to confirm events fire correctly. If any step's events are not firing, fix the instrumentation before continuing.

### 5. Evaluate against threshold

After 7 days, run the `threshold-engine` drill to measure:
- **Primary threshold:** >=65% of test users completed the wizard
- **Config success:** >=80% of completed wizards produced a working configuration (connected data source, created object, etc.)
- **Time check:** Median time to complete is under 15 minutes

If PASS: Document what worked, note the step with the highest dropoff (target for Baseline optimization), and proceed to Baseline.

If FAIL: Identify the step with the worst dropoff. Simplify that step (fewer fields, better defaults, add inline help text). Re-run with another 10-20 users.

## Time Estimate

- 2 hours: Define wizard steps and build the Intercom Checklist
- 1 hour: Instrument PostHog events and build the funnel
- 0.5 hours: Configure Intercom welcome message and Loops email
- 0.5 hours: Launch feature flag and verify events
- 1 hour: Analyze results after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, in-app messages | $29/seat/mo Essential plan; Early Stage program up to 90% off ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Welcome email sequence | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Smoke:** $0-29/mo (free tiers likely sufficient for 10-20 test users)

## Drills Referenced

- `wizard-step-builder` -- builds the Intercom Checklist with step validation and PostHog tracking
- `onboarding-flow` -- configures welcome messaging and email around the wizard
- `threshold-engine` -- evaluates wizard completion rate against the 65% pass threshold
