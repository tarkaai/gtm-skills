---
name: setup-wizard-baseline
description: >
  Guided Setup Wizard — Baseline Run. Deploy the wizard to all new signups with
  detailed PostHog event tracking, build activation optimization at the
  highest-dropoff step, and run always-on monitoring. Pass: >=75% completion
  with >=20pp lift over pre-wizard baseline.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=75% wizard completion AND >=20 percentage point lift vs pre-wizard cohort"
kpis: ["Wizard completion rate", "Completion rate lift vs control", "Median time to complete", "Config success rate", "Step-level dropoff"]
slug: "setup-wizard"
install: "npx gtm-skills add product/onboard/setup-wizard"
drills:
  - posthog-gtm-events
  - wizard-step-builder
  - activation-optimization
  - wizard-completion-monitor
---

# Guided Setup Wizard — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=75% of all new signups complete the wizard within 7 days. This represents a >=20 percentage point improvement over the pre-wizard onboarding completion rate. Configuration success rate remains >=85%. The wizard runs for all new signups (not just a test group) with always-on tracking.

## Leading Indicators

- Week 1 completion rate is >=70% (trending toward 75% target)
- The highest-dropoff step from Smoke has improved by >=10pp after optimization
- `wizard_step_failed` rate is <5% per step (down from Smoke's <10% threshold)
- Stall rate (started but not completed or failed within 24h) is <20% per step
- Users who complete the wizard activate (reach aha moment) at 2x the rate of pre-wizard cohort

## Instructions

### 1. Standardize event tracking

Run the `posthog-gtm-events` drill to establish the full event taxonomy for the wizard:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `wizard_impression` | Checklist shown to user | `persona_type`, `wizard_variant`, `signup_source` |
| `wizard_step_started` | User clicks/opens a wizard step | `step_name`, `step_number`, `persona_type` |
| `wizard_step_completed` | Step validation passes | `step_name`, `step_number`, `time_on_step_seconds`, `persona_type` |
| `wizard_step_failed` | Step validation fails | `step_name`, `step_number`, `error_type`, `persona_type` |
| `wizard_step_skipped` | User explicitly skips optional step | `step_name`, `step_number`, `persona_type` |
| `wizard_completed` | All required steps done | `total_time_minutes`, `steps_completed`, `steps_skipped`, `persona_type` |
| `wizard_abandoned` | User does not complete within 7 days | `last_step_completed`, `persona_type`, `days_active` |

Build PostHog funnels:
- **Full wizard funnel**: `wizard_impression` -> each step -> `wizard_completed`
- **Step-level funnels**: Individual step `started` -> `completed` broken down by error type

### 2. Upgrade the wizard for production

Run the `wizard-step-builder` drill again, upgrading from Smoke:
- Add Product Tour stops for the 2-3 most complex steps (the ones with the highest dropoff or longest time-on-step from Smoke data)
- Add stall detection: the n8n workflow that nudges users who get stuck at a step for >4 hours
- Add the Loops email sequence: Day 1 nudge if wizard not started, Day 3 nudge if wizard not completed, Day 5 offer to help
- Enable the wizard for 100% of new signups by updating the PostHog feature flag

### 3. Optimize the highest-dropoff step

Run the `activation-optimization` drill focused specifically on the wizard step with the worst completion rate from Smoke:

1. Pull PostHog session recordings of users who dropped off at that step
2. Categorize the failure modes: confusion (did not know what to do), effort (too many fields), technical error (integration failed), value unclear (skipped because they did not understand why)
3. Based on the dominant failure mode, implement a fix:
   - Confusion: Add a 2-step Product Tour at this step with clear instructions
   - Effort: Reduce required fields, add smart defaults, or offer a "quick setup" option
   - Technical error: Improve error messages, add retry logic, add a help link
   - Value unclear: Add inline copy explaining why this step matters with a concrete example
4. Deploy the fix behind a PostHog feature flag (50/50 split) and measure step completion rate for 1 week

### 4. Start always-on monitoring

Run the `wizard-completion-monitor` drill to build:
- The "Setup Wizard Health" PostHog dashboard
- Daily anomaly detection via n8n (alerts if completion drops >20% from rolling average)
- Weekly wizard report posted to Slack

This monitoring runs continuously from Baseline onward.

### 5. Evaluate against threshold

After 2 weeks of production data:

- **Primary:** >=75% overall wizard completion rate
- **Lift:** >=20pp improvement over the pre-wizard onboarding completion rate (compare wizard cohort vs historical cohort in PostHog)
- **Config success:** >=85% of completed wizards produce a working configuration
- **Step health:** No single step has >25% dropoff

If PASS: Document per-step performance, identify persona-specific patterns, proceed to Scalable.

If FAIL: Focus on the step with the highest dropoff. Run one more optimization cycle using `activation-optimization`. If still failing after 2 cycles, simplify the wizard (remove or combine steps) and re-evaluate.

## Time Estimate

- 3 hours: Implement full event taxonomy and build PostHog funnels
- 4 hours: Upgrade wizard with Product Tours, stall detection, email sequence
- 4 hours: Analyze dropoff data, implement and test fix for worst step
- 2 hours: Build monitoring dashboard and n8n workflows
- 3 hours: Analyze 2-week results, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, feature flags, session recordings | Free up to 1M events + 5K recordings/mo; ~$0 at <500 users ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, Product Tours, in-app messages | $29/seat/mo Essential; Product Tours may require Advanced at $85/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Onboarding email nudge sequence | Free up to 1,000 contacts; $49/mo above that ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Stall detection workflow, monitoring automation | Free self-hosted; $24/mo cloud Starter ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at Baseline:** $29-134/mo depending on Intercom plan and user volume

## Drills Referenced

- `posthog-gtm-events` -- standardizes the wizard event taxonomy across all tracking
- `wizard-step-builder` -- upgrades the wizard with Product Tours, stall detection, and email nudges
- `activation-optimization` -- diagnoses and fixes the highest-dropoff wizard step
- `wizard-completion-monitor` -- builds always-on dashboard and anomaly detection
