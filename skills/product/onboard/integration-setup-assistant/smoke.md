---
name: integration-setup-assistant-smoke
description: >
  Integration Setup Assistant -- Smoke Test. Build an AI-guided integration wizard
  that helps new users connect their first integration during onboarding.
  Run with 10-20 users to validate that guided setup produces higher integration
  completion than unguided setup.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=55% of test users complete at least 1 integration within 7 days"
kpis: ["Integration setup start rate", "Integration setup success rate", "Time to first integration", "Post-integration activation rate"]
slug: "integration-setup-assistant"
install: "npx gtm-skills add product/onboard/integration-setup-assistant"
drills:
  - posthog-gtm-events
  - threshold-engine
---

# Integration Setup Assistant -- Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=55% of test users (10-20 users) complete at least 1 integration within 7 days of signup. This validates that an AI-guided integration wizard produces higher setup completion than the current unguided experience.

## Leading Indicators

- Wizard checklist open rate >80% (users see and engage with the wizard)
- Integration setup attempt rate >60% (users click through to at least one integration)
- Setup failure rate <30% (the guided flow reduces errors vs. unguided)
- Rescue message engagement >20% (stalled users respond to contextual help)

## Instructions

### 1. Set up event tracking for the integration wizard

Run the `posthog-gtm-events` drill to define and implement the integration-specific event taxonomy in PostHog. At minimum, instrument these events:

- `integration_wizard_started` -- user opens the integration setup checklist
- `integration_step_started` -- user begins setting up a specific integration (properties: `integration_name`, `step_number`)
- `integration_setup_attempted` -- user initiates the connection (clicks Connect, submits API key)
- `integration_setup_succeeded` -- integration verified as connected (properties: `integration_name`, `time_to_connect_seconds`)
- `integration_setup_failed` -- connection attempt failed (properties: `integration_name`, `error_type`, `error_message`)
- `integration_wizard_completed` -- user finishes at least 1 integration

Build a PostHog funnel: `integration_wizard_started` -> `integration_step_started` -> `integration_setup_attempted` -> `integration_setup_succeeded` -> `integration_wizard_completed`. Set the funnel window to 7 days.

### 2. Build the integration wizard

Run the the integration wizard build workflow (see instructions below) drill. For the Smoke test, limit scope to:

- Select the top 3 integrations by activation impact (query PostHog retention data, or rank by core value delivery if no data exists)
- Build the Intercom checklist with 3 integration steps plus a completion step
- Build one contextual Intercom bot for the most common integration (the one with highest volume or highest failure rate)
- Build the basic failure detection n8n workflow for the top 3 integrations
- Build the stalled-user rescue workflow (6-hour check + 48-hour email fallback)
- Skip persona-specific variants -- use one generic wizard for all users

**Human action required:** Review the Intercom checklist copy before launching. Ensure each step's description clearly states what the integration does for the user and how long setup takes. Approve the bot conversation flow.

### 3. Launch to a small test group

Create a PostHog feature flag `integration-wizard-smoke` set to roll out to the next 10-20 new signups. Users in the flag group see the Intercom integration checklist on first login. Users outside the flag group get the existing unguided experience.

**Human action required:** Enable the feature flag and monitor the first 2-3 users through the wizard. Watch PostHog Live Events to confirm all events fire correctly. Watch Intercom for bot conversations to confirm the guidance flow works. Fix any broken steps before continuing.

### 4. Monitor for 7 days

Check PostHog daily during the test period:
- Are users starting the wizard? (Check `integration_wizard_started` count)
- Where are they dropping off? (Check the setup funnel step-by-step)
- What errors are they hitting? (Check `integration_setup_failed` by `error_type`)
- Are rescue messages working? (Check if stalled users return after receiving messages)

Log observations in Attio as notes on the play record.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass criteria:

- **Primary metric:** % of test users who completed at least 1 integration within 7 days
- **Pass threshold:** >=55%
- **Secondary metrics:** wizard start rate, per-integration success rate, average time to connect, rescue recovery rate

If PASS (>=55%): Document what worked -- which integrations had highest/lowest success rates, what error types were most common, whether rescue messages were effective. Proceed to Baseline.

If FAIL (<55%): Diagnose using the PostHog funnel. If users are not starting the wizard, the checklist is not visible enough or the copy is not compelling. If users start but fail, the setup guidance or error recovery needs improvement. Fix the biggest drop-off point and re-run with another 10-20 users.

## Time Estimate

- 2 hours: Event tracking setup and wizard build (Steps 1-2)
- 0.5 hours: Feature flag setup and launch review (Step 3)
- 1.5 hours: Daily monitoring over 7 days (Step 4)
- 1 hour: Analysis and threshold evaluation (Step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free tier: 1M events/mo, unlimited feature flags ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, bots, in-app messages | Essential: $29/seat/mo; Early Stage: up to 90% off year 1 ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Failure detection and rescue workflows | Free self-hosted; Cloud Starter: $24/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Loops | Fallback rescue emails | Free: 1,000 contacts, 4,000 emails/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Smoke:** Free (all tools within free tier limits for 10-20 users)

## Drills Referenced

- the integration wizard build workflow (see instructions below) -- builds the Intercom checklist, contextual bots, failure detection, and rescue workflows
- `posthog-gtm-events` -- defines and implements the event taxonomy for integration tracking
- `threshold-engine` -- evaluates pass/fail against the 55% completion threshold
