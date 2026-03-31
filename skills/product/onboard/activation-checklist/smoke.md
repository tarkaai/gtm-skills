---
name: activation-checklist-smoke
description: >
  Onboarding Checklist Workflow — Smoke Test. Build a 4-6 step activation checklist
  for new users, deploy it via Intercom product tours and a Loops email sequence,
  and validate that ≥ 60% of test users complete the checklist within 7 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥ 60% checklist completion rate within 7 days from ≥ 20 new signups"
kpis: ["Checklist completion rate (target ≥ 60%)", "Per-step completion rate", "Time to activation (median days from signup to final step)"]
slug: "activation-checklist"
install: "npx gtm-skills add product/onboard/activation-checklist"
drills:
  - onboarding-sequence-design
  - onboarding-flow
  - threshold-engine
---

# Onboarding Checklist Workflow — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove that a structured activation checklist increases the percentage of new users who reach the product's value moment. The checklist makes the path from signup to activation explicit: users see exactly what steps remain, get contextual help at each step, and receive celebration when they complete milestones.

Pass: ≥ 60% of ≥ 20 new signups complete all checklist steps within 7 days.
Fail: < 60% completion after 20+ signups, or fewer than 20 signups in the test window.

## Leading Indicators

- First user completes the full checklist within 48 hours of deployment (the steps are achievable and clear)
- Per-step drop-off is < 20% between any two consecutive steps (no single step is a blocker)
- At least 3 users complete the checklist without contacting support (the checklist is self-serve)
- Email open rate on the onboarding sequence exceeds 40% (the nudges are relevant)
- Median time-to-activation is under 3 days (the checklist accelerates the journey)

## Instructions

### 1. Design the checklist milestones and email sequence

Run the `onboarding-sequence-design` drill. This produces:

- **The activation metric:** the single action that best predicts 30-day retention. Use PostHog cohort analysis (`posthog-cohorts` fundamental) to compare retained vs churned users. If you lack data, pick the action that delivers the core value promise.
- **The milestone ladder:** 4-6 intermediate steps from signup to activation. Each step must be trackable as a PostHog event, achievable in a single session, and on the critical path to activation. Example:
  1. `signup_completed` -- account created
  2. `profile_completed` -- name, role, company set
  3. `first_core_action` -- created first project / imported data / connected integration
  4. `value_moment_reached` -- saw first result or completed first workflow
  5. `second_session` -- returned within 48 hours
- **The email sequence:** 5-7 behavioral emails with subject lines, body copy, CTAs, send timing, and skip conditions. Each email maps to a milestone: it nudges users who have not reached that milestone and is skipped for users who have.

Document the milestone ladder and email specs in a reference file. This is the blueprint for in-app and email delivery.

### 2. Build the in-app checklist experience

Run the `onboarding-flow` drill. Using the milestone ladder from step 1:

- Use the `intercom-product-tours` fundamental to create a guided tour for each milestone. Keep each tour to 3-5 steps. Focus the first tour on reaching the first core action (Milestone 3).
- Use the `intercom-in-app-messages` fundamental to create a persistent checklist widget or progress banner. Show completed steps with checkmarks and highlight the next step. Display a progress indicator (e.g., "3 of 5 steps complete").
- Use the `intercom-in-app-messages` fundamental to create celebration messages when users complete each milestone. Keep celebrations brief and suggest the next step.
- Use the `posthog-funnels` fundamental to build an onboarding funnel tracking conversion between each milestone.

**Human action required:** Review the checklist copy and tour flows before launching. Ensure each step has a clear, specific CTA (not "complete your setup" but "create your first project"). Deploy to a test group of 20-50 new signups.

### 3. Track checklist interactions

Instrument the following PostHog events using the `posthog-custom-events` fundamental:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `checklist_shown` | Checklist widget renders for a new user | `user_id`, `signup_date`, `total_steps` |
| `checklist_step_completed` | User completes a milestone | `user_id`, `step_number`, `step_name`, `time_since_signup_hours` |
| `checklist_completed` | User completes all steps | `user_id`, `total_time_hours`, `steps_completed` |
| `checklist_dismissed` | User hides or dismisses the checklist | `user_id`, `steps_completed_at_dismiss` |

Build a PostHog funnel: `checklist_shown` -> `checklist_step_completed (step 1)` -> ... -> `checklist_completed`. Break down by signup source and plan type.

### 4. Evaluate after 7 days

Run the `threshold-engine` drill to measure against the pass threshold.

Count: total users who saw the checklist, total who completed all steps, completion rate, per-step drop-off rates.

- **PASS (≥ 60% completion from ≥ 20 users):** The checklist works. Document: the milestone ladder, which steps had highest/lowest completion, median time-to-activation, and email sequence performance. Proceed to Baseline.
- **MARGINAL (40-59% completion):** Identify the step with the largest drop-off. Is it too hard, too confusing, or not clearly explained? Simplify that step or add a contextual help message. Re-run with 20 fresh signups.
- **FAIL (< 40% or fewer than 20 signups):** Diagnose: Did users see the checklist (check `checklist_shown` events)? Did they complete step 1 but stall (the second step is too hard)? Did they dismiss the checklist entirely (it felt irrelevant)? Fix the root cause and re-test.

## Time Estimate

- Milestone definition and email sequence design: 2 hours
- In-app checklist build (Intercom tours + messages): 1.5 hours
- PostHog event instrumentation: 30 minutes
- Monitoring over 7 days and evaluation: 1 hour
- Total: ~5 hours of active work over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, cohort comparison | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app checklist widget, celebration messages | Essential $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Behavioral onboarding email sequence | Free under 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM -- log user activation status | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Smoke:** $29 (Intercom Essential, 1 seat). PostHog, Loops, and Attio on free tiers.

## Drills Referenced

- `onboarding-sequence-design` -- map activation milestones, write the behavioral email sequence, define timing and branching logic
- `onboarding-flow` -- build the in-app checklist using Intercom product tours, contextual messages, and PostHog funnel tracking
- `threshold-engine` -- evaluate checklist completion rate against the pass threshold and recommend next action
