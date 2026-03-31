---
name: activation-checklist-baseline
description: >
  Onboarding Checklist Workflow — Baseline Run. Wire the activation checklist to
  always-on behavioral automation: PostHog events trigger Loops emails and Intercom
  messages via n8n. Validate ≥ 65% completion with ≥ 15pp lift over pre-checklist baseline.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥ 65% checklist completion rate AND ≥ 15pp lift vs pre-checklist cohort"
kpis: ["Checklist completion rate (target ≥ 65%)", "Lift vs pre-checklist baseline (target ≥ 15pp)", "Per-step drop-off rate", "Email sequence engagement (open rate, click rate)", "Median time to activation"]
slug: "activation-checklist"
install: "npx gtm-skills add product/onboard/activation-checklist"
drills:
  - onboarding-sequence-automation
  - posthog-gtm-events
  - activation-optimization
---

# Onboarding Checklist Workflow — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Turn the Smoke-validated checklist into an always-on system. Every new signup automatically enters the checklist experience: in-app progress tracking via Intercom, behavioral email nudges via Loops triggered by PostHog events through n8n, and a PostHog dashboard showing real-time activation health. The system runs without manual intervention.

Pass: ≥ 65% checklist completion rate across all new signups over 2 weeks AND ≥ 15 percentage point lift compared to the pre-checklist historical activation rate.
Fail: < 65% completion or < 15pp lift after 2 full weeks of always-on operation.

## Leading Indicators

- n8n webhook pipeline processes 100% of signup events within 60 seconds (the automation is reliable)
- Email sequence open rate exceeds 35% across all steps (nudges are reaching users)
- Per-step drop-off improves vs Smoke test for the previously worst-performing step (the optimization worked)
- Zero failed webhook deliveries or orphaned leads over 48 hours (the pipeline has no gaps)
- Activation rate for week 2 is equal to or better than week 1 (results hold over time, not just novelty)

## Instructions

### 1. Instrument the full event taxonomy

Run the `posthog-gtm-events` drill to establish a complete event taxonomy for the activation checklist. Configure the following events using the `posthog-custom-events` fundamental:

**Checklist lifecycle events:**
| Event | When | Properties |
|-------|------|-----------|
| `activation-checklist_impression` | Checklist widget renders | `user_id`, `signup_source`, `plan_type`, `variant` |
| `activation-checklist_step_started` | User begins a checklist step | `step_number`, `step_name`, `time_since_signup_hours` |
| `activation-checklist_step_completed` | User finishes a checklist step | `step_number`, `step_name`, `time_since_signup_hours`, `time_on_step_minutes` |
| `activation-checklist_engaged` | User completes ≥ 50% of steps | `steps_completed`, `total_steps`, `time_since_signup_hours` |
| `activation-checklist_converted` | User completes all checklist steps | `total_time_hours`, `steps_completed`, `signup_source` |
| `activation-checklist_dismissed` | User hides the checklist | `steps_completed_at_dismiss`, `time_since_signup_hours` |
| `activation-checklist_retained` | User active 7 days post-completion | `days_since_activation`, `sessions_since_activation` |

**Email sequence events:**
| Event | When | Properties |
|-------|------|-----------|
| `onboarding_email_sent` | Loops sends an email | `email_step`, `subject`, `user_email` |
| `onboarding_email_opened` | User opens the email | `email_step` |
| `onboarding_email_clicked` | User clicks a CTA in the email | `email_step`, `cta_url` |

Build PostHog funnels:
- **Checklist funnel:** `activation-checklist_impression` -> step 1 completed -> step 2 completed -> ... -> `activation-checklist_converted`
- **Email engagement funnel:** `onboarding_email_sent` -> opened -> clicked -> `activation-checklist_converted`
- **Retention funnel:** `activation-checklist_converted` -> `activation-checklist_retained`

Set up cohort analysis using `posthog-cohorts`: compare activation rates by signup week, signup source, and plan type.

### 2. Wire the always-on automation pipeline

Run the `onboarding-sequence-automation` drill. Build the following n8n workflows:

**Enrollment workflow** (using `n8n-triggers` + `n8n-workflow-basics`):
```
PostHog webhook: signup_completed
  -> Extract user email, name, signup_source, plan_type
  -> POST to Loops API: create contact with properties
  -> Loops auto-starts the onboarding sequence
  -> Log onboarding_email_enrolled event back to PostHog
```

**Milestone sync workflow** (one per milestone):
```
PostHog webhook: checklist_step_N_completed
  -> Extract user email and milestone details
  -> PUT to Loops API: update contact {milestone_N_completed: true}
  -> POST to Loops API: send event {milestone_N_completed}
  -> Loops sequence branches: skip nudge emails for completed steps
```

**Activation exit workflow:**
```
PostHog webhook: activation-checklist_converted
  -> Update Loops contact: {activated: true, activation_date: timestamp}
  -> Send Loops event: activation_reached
  -> Loops exits the non-activated branch, sends celebration email
  -> Update Attio contact record with activation status
```

**Daily monitoring workflow** (using `n8n-scheduling`):
```
Cron: daily at 09:00 UTC
  -> Query PostHog: yesterday's checklist metrics (impressions, completions, per-step counts)
  -> Compare to thresholds: completion rate < 50% or any step drop-off > 30% triggers alert
  -> Check for errors: failed webhooks, bounced emails, broken connections
  -> Send daily digest to Slack: enrollments, completion rate, email open/click rates, errors
```

Test the full pipeline end-to-end: create a test user, verify PostHog fires `signup_completed`, verify n8n enrolls them in Loops, verify emails arrive on schedule, simulate milestone completions, verify skip logic works, simulate activation and verify celebration email fires.

### 3. Optimize the activation bottleneck

Run the `activation-optimization` drill. Using the PostHog funnel data from step 1:

1. Identify the step with the largest drop-off in the checklist funnel.
2. Diagnose the friction at that step:
   - **Confusion:** Users do not know what to do. Add a contextual Intercom product tour at that step using `intercom-product-tours`.
   - **Effort:** The step requires too much work. Simplify: offer templates, pre-fill data, or break it into sub-steps.
   - **Value unclear:** Users do not see why the step matters. Add context: "This step unlocks [specific benefit]."
   - **Technical:** Errors or slow loading. Fix the bugs.
3. Implement the fix and monitor the per-step completion rate for 3 days.
4. If the fix improved the drop-off by ≥ 5pp, move to the next worst step. If not, try a different approach.

### 4. Evaluate after 2 weeks

Measure against the pass threshold:

- **Completion rate:** Total users who completed all checklist steps / total users who saw the checklist.
- **Lift calculation:** Compare the current completion rate to the historical pre-checklist activation rate. The difference is the lift.
- **Sustainability:** Compare week 1 vs week 2 completion rates. If week 2 is within 5pp of week 1, the results are holding.

Decision:
- **PASS (≥ 65% completion AND ≥ 15pp lift):** The always-on checklist is working. Document: the pipeline architecture, which bottleneck you fixed and by how much, email sequence metrics, and the per-step completion rates. Proceed to Scalable.
- **MARGINAL (55-64% or 10-14pp lift):** The system works but underperforms. Check: Are emails being delivered (Loops bounce rate)? Are in-app messages rendering (Intercom delivery stats)? Is the biggest drop-off still the same step you already fixed? Optimize and run for 1 more week.
- **FAIL (< 55% or < 10pp lift):** Diagnose: Is the automation pipeline dropping events (check n8n execution logs)? Are users dismissing the checklist before engaging (check `checklist_dismissed` events)? Is the checklist too long (> 6 steps may overwhelm)? Fix the root cause and re-run.

## Time Estimate

- Event taxonomy and PostHog instrumentation: 3 hours
- n8n automation pipeline (4 workflows): 6 hours
- End-to-end testing: 2 hours
- Activation bottleneck analysis and fix: 3 hours
- Monitoring and evaluation over 2 weeks: 2 hours
- Total: ~16 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, dashboards | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Webhook routing, behavioral triggers, scheduling | Starter €24/mo for 2,500 executions or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Behavioral onboarding email sequence | Free under 1,000 contacts; $49/mo for paid ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | Product tours, in-app checklist, contextual messages | Essential $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | CRM -- activation status tracking | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Baseline:** $53-102 (Intercom $29 + n8n $24 + Loops $0-49 depending on contact count). PostHog and Attio on free tiers.

## Drills Referenced

- `onboarding-sequence-automation` -- wire the email sequence to PostHog behavioral triggers via n8n for always-on delivery
- `posthog-gtm-events` -- define and implement the full event taxonomy for checklist tracking
- `activation-optimization` -- identify the activation bottleneck in the funnel and systematically remove friction
