---
name: onboarding-flow
description: Build a multi-channel onboarding experience using in-app tours, lifecycle emails, and analytics tracking
category: Product
tools:
  - Intercom
  - Loops
  - PostHog
fundamentals:
  - intercom-product-tours
  - intercom-in-app-messages
  - loops-transactional-emails
  - posthog-funnel-tracking
---

# Onboarding Flow

This drill builds a complete onboarding experience that guides new users from signup to their first value moment. It combines in-app guidance via Intercom, lifecycle emails via Loops, and funnel tracking via PostHog.

## Prerequisites

- Intercom installed in your application with Messenger enabled
- Loops account configured for transactional and lifecycle emails
- PostHog tracking installed with user identification
- Clear definition of your product's "aha moment" (the first action that correlates with retention)

## Steps

### 1. Map the onboarding milestones

Define 4-6 milestones between signup and activation. Example for a SaaS product:

1. Account created
2. Profile completed
3. First core action taken (e.g., created a project, imported data, invited a teammate)
4. Value moment reached (e.g., saw their first result, completed their first workflow)
5. Second session within 48 hours (habit forming)

Each milestone becomes a tracked event in PostHog and a trigger point for Intercom and Loops.

### 2. Build in-app product tours

Using the `intercom-product-tours` fundamental, create guided tours for new users. Keep each tour short — 3-5 steps maximum. Focus the first tour on reaching Milestone 3 (the first core action). Do not try to show everything; show only what matters most. Trigger tours based on user state, not just time since signup.

### 3. Set up contextual in-app messages

Using the `intercom-in-app-messages` fundamental, create targeted messages that appear when users get stuck or when they reach a milestone. Examples:

- User has not completed Milestone 2 after 24 hours: show a tooltip pointing to the setup step
- User completed Milestone 3: show a congratulations banner with the next suggested action
- User returns for their second session: show a "welcome back" message with a shortcut to their last action

### 4. Build the email onboarding sequence

Using the `loops-transactional-emails` fundamental, create a 5-7 email sequence:

- **Email 1 (immediate)**: Welcome email with one clear next step. Link directly to the action, not to the dashboard.
- **Email 2 (Day 1)**: Quick-start guide. Show the fastest path to value with a short tutorial.
- **Email 3 (Day 3)**: Social proof. Share how similar users got value from the product.
- **Email 4 (Day 5)**: Overcome objections. Address common blockers and offer help.
- **Email 5 (Day 7)**: Check-in from a real person. Ask if they need help. Include a calendar link.

Each email should be skipped if the user has already completed the relevant milestone.

### 5. Instrument the funnel

Using the `posthog-funnel-tracking` fundamental, build an onboarding funnel that tracks conversion between each milestone. Set up cohort analysis to compare onboarding performance across signup sources, plans, and time periods. Identify where users drop off most.

### 6. Iterate based on data

Review the onboarding funnel weekly. Find the biggest drop-off point and focus all effort there. Test changes to the product tour, email copy, or in-app messages at that step. A 10% improvement at the biggest drop-off point has more impact than optimizing steps that already work well.
