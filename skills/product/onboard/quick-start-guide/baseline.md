---
name: quick-start-guide-baseline
description: >
  Quick Start Guide — Baseline Run. Wire the quick-start guide to behavioral triggers via n8n,
  instrument full event tracking in PostHog, and optimize the activation funnel to sustain
  ≥ 50% guide view rate and ≥ 30% completion rate over 2 weeks with always-on automation.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥ 50% guide view rate within 3 days and ≥ 30% guide completion rate within 7 days, sustained over 2 weeks with ≥ 8pp lift in activation rate vs non-guide users"
kpis: ["Guide view rate (target ≥ 50%)", "Guide completion rate (target ≥ 30%)", "Activation lift vs control (target ≥ 8pp)", "Email sequence engagement (open rate, click rate)"]
slug: "quick-start-guide"
install: "npx gtm-skills add product/onboard/quick-start-guide"
drills:
  - onboarding-sequence-automation
  - posthog-gtm-events
  - activation-optimization
---

# Quick Start Guide — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

The quick-start guide is always-on: every new signup automatically receives the guide in-app and via email, behavioral triggers adjust delivery based on user progress, and full PostHog instrumentation measures the guide's impact on activation. The guide runs continuously without manual intervention.

Pass: ≥ 50% guide view rate within 3 days AND ≥ 30% guide completion rate within 7 days, sustained over 2 weeks. Activation rate for guide completers is ≥ 8 percentage points higher than non-guide users.
Fail: View rate drops below 45% or completion rate below 25% for 2+ consecutive cohorts, or activation lift is < 5pp.

## Leading Indicators

- Guide delivery automation runs for 7 days without errors (the n8n workflows are stable)
- Email open rate for the guide email exceeds 40% (the subject line and timing are working)
- Guide completion rate is consistent across 3 consecutive daily cohorts (the guide works reliably, not just for early adopters)
- PostHog funnel shows guide completers activate at a measurably higher rate than non-completers (the guide causes activation, not just correlates with it)
- At least one drop-off point is identified and a fix is tested (the optimization loop is working)

## Instructions

### 1. Instrument full event tracking

Run the `posthog-gtm-events` drill to establish a complete event taxonomy for the quick-start guide. Configure these events using `posthog-custom-events`:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `guide_impression` | In-app message or email CTA shown to user | `surface`, `user_id`, `days_since_signup`, `cohort_week` |
| `guide_viewed` | User opens the guide (any surface) | `surface`, `user_id`, `days_since_signup` |
| `guide_step_completed` | User completes a guide section | `step_number`, `step_name`, `surface`, `time_spent_seconds` |
| `guide_completed` | User completes all guide sections | `surface`, `total_time_seconds`, `days_since_signup` |
| `guide_abandoned` | User opened guide but did not complete within 24h | `last_step_completed`, `surface`, `time_since_open_hours` |
| `guide_feedback` | User clicks helpful/not helpful | `response`, `surface` |
| `guide_to_activation` | User reaches activation metric after guide completion | `time_guide_to_activation_hours`, `guide_surface` |

Build PostHog funnels:
- **Guide funnel:** `guide_impression` -> `guide_viewed` -> `guide_step_completed (step 1)` -> ... -> `guide_completed`
- **Guide-to-activation funnel:** `guide_completed` -> `activation_reached`
- **Comparison funnel:** activation rate for users with `guide_completed = true` vs users with `guide_viewed = false`

Build PostHog cohorts:
- "Guide completers" (guide_completed event exists)
- "Guide viewers, non-completers" (guide_viewed exists, guide_completed does not)
- "Guide non-viewers" (no guide_viewed event)

### 2. Wire behavioral automation

Run the `onboarding-sequence-automation` drill to connect the guide to behavioral triggers via n8n:

**Enrollment workflow (n8n):**
```
PostHog webhook (signup_completed)
  -> Create Loops contact with signup properties
  -> Set guide_status = "not_started"
  -> Loops auto-starts onboarding sequence (Email 1: welcome)
```

**Guide delivery workflow (n8n):**
```
PostHog webhook (24h after signup, milestone_2 NOT completed)
  -> Trigger Loops to send Email 2 (inline quick-start guide)
  -> Update guide_status = "email_sent"
```

**Guide progress sync (n8n):**
```
PostHog webhook (guide_step_completed)
  -> Update Loops contact: last_guide_step = N
  -> If guide_completed: update guide_status = "completed", skip remaining nudge emails
```

**Stall intervention workflow (n8n):**
```
Daily cron at 09:00 UTC
  -> Query PostHog: users with guide_viewed but NOT guide_completed, guide_viewed > 48h ago
  -> For each stalled user: trigger Intercom in-app message "Pick up where you left off — Step {N+1}"
  -> Log stall_intervention_sent event to PostHog
```

### 3. Optimize the activation funnel

Run the `activation-optimization` drill. Using the PostHog funnels from Step 1:

1. Identify the guide step with the largest drop-off. This is where users get stuck.
2. Diagnose the friction:
   - If step instructions are unclear: rewrite using simpler language and add a screenshot/GIF
   - If the product action is too complex: consider simplifying the UI for that action or breaking the step into sub-steps
   - If users abandon after viewing but before starting: the guide is not compelling enough — rewrite the intro to emphasize the outcome
3. Use PostHog session recordings (if enabled) to watch 5-10 users who abandoned at the problem step. Note exactly where they hesitate or leave.
4. Test one change at a time. Deploy to 50% of new signups via PostHog feature flag. Compare guide completion rate between control and variant after 100+ users per group.

**Human action required:** Review session recordings to understand why users abandon. Approve any changes to the guide content or in-app messaging before deploying to all users.

### 4. Evaluate against threshold

Measure at the end of 2 weeks:

- **Guide view rate:** guide_viewed / new signups, within 3 days of signup. Target: ≥ 50%.
- **Guide completion rate:** guide_completed / new signups, within 7 days. Target: ≥ 30%.
- **Activation lift:** activation rate for guide completers minus activation rate for guide non-viewers. Target: ≥ 8pp.
- **Email engagement:** open rate and click rate for the guide email. Benchmark: > 40% open, > 10% click.

- **PASS:** All targets met for 2 consecutive weekly cohorts. Document: the working guide content, automation workflows, per-step completion rates, and activation lift data. Proceed to Scalable.
- **MARGINAL:** View rate 45-49% or completion rate 25-29% or activation lift 5-7pp. Focus on the weakest metric. If view rate is low, test a different in-app message format or email subject line. If completion rate is low, simplify the highest-dropoff step. If activation lift is low, the guide may be teaching the wrong actions — revisit the milestone ladder.
- **FAIL:** Any metric significantly below target. Check: Are n8n workflows running without errors? Is the guide email being delivered (check Loops delivery rates)? Are PostHog events firing (check live events)? Fix the broken component and re-run.

## Time Estimate

- Event instrumentation and PostHog funnel setup: 3 hours
- n8n workflow builds (enrollment, delivery, progress sync, stall intervention): 5 hours
- Activation funnel analysis and first optimization: 4 hours
- Monitoring over 2 weeks and evaluation: 4 hours
- Total: ~16 hours of active work over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags, session recordings | Free 1M events/mo; paid starts $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Behavioral trigger workflows, stall interventions, cron scheduling | Starter €24/mo for 2,500 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app guide surface, stall intervention messages | Essential $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Onboarding email sequence with inline guide, behavioral branching | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Baseline:** ~$100 (Intercom $29 + n8n €24 + Loops $49). PostHog on free tier for most early-stage products.

## Drills Referenced

- `onboarding-sequence-automation` -- wire the onboarding email sequence (including the inline guide) to PostHog behavioral triggers via n8n, with milestone-based branching and stall interventions
- `posthog-gtm-events` -- establish the complete event taxonomy for guide tracking: impressions, views, step completions, abandonment, feedback, and guide-to-activation attribution
- `activation-optimization` -- analyze the PostHog funnel to find the highest-dropoff guide step, diagnose friction causes, and test improvements using feature flags
