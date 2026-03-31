---
name: time-to-value-optimization-baseline
description: >
  Time-to-Value Acceleration — Baseline Run. Wire behavioral onboarding emails and in-app
  nudges to PostHog events via n8n for always-on delivery. Run the activation funnel continuously
  for 2 weeks and optimize the biggest drop-off point. Target: 60%+ activation rate with
  median TTV under 8 minutes.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=60% activation rate with median TTV <8 minutes, >=15pp improvement over Smoke baseline"
kpis: ["Median time to first value (minutes)", "Activation rate (%)", "Step completion rate per milestone", "Email open rate", "Email click-to-activation rate"]
slug: "time-to-value-optimization"
install: "npx gtm-skills add product/onboard/time-to-value-optimization"
drills:
  - onboarding-sequence-design
  - onboarding-sequence-automation
  - activation-optimization
---

# Time-to-Value Acceleration — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

60%+ of all new signups reach activation with a median TTV under 8 minutes, representing at least a 15 percentage point improvement over the Smoke baseline. The onboarding system runs continuously — behavioral emails fire based on user state, in-app nudges trigger on drop-off signals, and the activation funnel is monitored daily without manual intervention.

## Leading Indicators

- Behavioral email sequence live and firing based on PostHog milestone events (not just time delays)
- n8n workflows connecting PostHog events to Loops sequences and Intercom messages without errors
- Email open rate >= 40% for welcome email, click rate >= 10%
- Biggest drop-off step from Smoke showing measurable improvement after targeted intervention
- At least 100 users have gone through the automated funnel

## Instructions

### 1. Design the full onboarding email sequence

Run the `onboarding-sequence-design` drill. Using the activation metric and milestones defined in Smoke, create a 5-7 email behavioral sequence:

- **Email 1 (immediate on signup):** Welcome with one clear next step. Link directly to the action for Milestone 2.
- **Email 2 (24h after signup IF Milestone 2 not completed):** "Did you get stuck?" with a 60-second setup guide or video link.
- **Email 3 (48h or on Milestone 2 completion):** Use case inspiration showing how a similar user reached value.
- **Email 4 (Day 5 if not activated):** Social proof — "[X] users activated this week, here's what they did first."
- **Email 5 (Day 7 if not activated):** Personal help offer from a real person with a Cal.com booking link.
- **Email 6 (immediately on activation):** Celebration email suggesting the next valuable action.
- **Email 7 (2 days after activation):** Bridge email from onboarding to regular product usage.

Key rules: never send more than 1 email per day. Exit the "not activated" branch immediately when activation occurs. Skip emails for milestones the user already completed.

Write the actual subject lines, preview text, body copy, and CTAs. Do not use placeholders. Each email must be specific to your product and activation metric.

### 2. Wire the automation pipeline

Run the `onboarding-sequence-automation` drill. Build the following n8n workflows:

**Enrollment workflow:**
```
PostHog webhook (signup_completed)
  -> Extract user email, name, signup_source, plan_type
  -> POST to Loops /api/v1/contacts/create with properties
  -> Loops auto-starts onboarding sequence
  -> Log onboarding_email_enrolled event back to PostHog
```

**Milestone sync workflows (one per milestone):**
```
PostHog webhook (onboarding_step_N_completed)
  -> Extract user email and milestone details
  -> PUT to Loops /api/v1/contacts/update with {milestone_N_completed: true}
  -> POST to Loops /api/v1/events/send with {eventName: "milestone_N_completed"}
  -> Loops sequence branches/skips emails based on contact properties
```

**Activation exit workflow:**
```
PostHog webhook (activation_reached)
  -> Update Loops contact: {activated: true, activation_date: timestamp}
  -> Send Loops event: activation_reached
  -> Sequence exits "not activated" branch, sends Email 6 (celebration)
```

**Stall detection workflow:**
```
n8n cron (daily at 09:00 UTC)
  -> Query PostHog: users with signup > 2h ago AND milestone_2 NOT completed
  -> For each: trigger Intercom in-app message offering help
  -> Query PostHog: users with signup > 48h ago AND NOT activated
  -> For each: check if Loops email sequence is progressing normally
```

Test the full pipeline end-to-end: create a test user, verify all webhooks fire, verify emails arrive, verify milestone syncs work, verify activation exit triggers correctly.

### 3. Optimize the biggest drop-off point

Run the `activation-optimization` drill. Using the funnel data from Smoke and the first week of Baseline:

1. Identify the milestone step with the largest absolute drop-off.
2. Diagnose the friction type: confusion (users do not know what to do), effort (step requires too much work), value unclear (users do not see why this matters), or technical (bugs/errors).
3. Implement a targeted fix:
   - **Confusion:** Add an Intercom product tour for that specific step. 3 steps max, pointing to the exact UI elements.
   - **Effort:** Simplify the step — pre-fill fields, offer templates, reduce required inputs.
   - **Value unclear:** Add an Intercom contextual message explaining the benefit of completing this step with a concrete example.
   - **Technical:** Fix the bug. Check PostHog session recordings for error patterns.
4. Measure the impact: compare step conversion rate before and after the fix over 5+ days with 50+ users per variant.

### 4. Monitor and evaluate

Over the 2-week period, track daily:
- New signups and activations
- Median TTV for activated users
- Email engagement (opens, clicks, activation from email)
- Funnel step conversion rates

At the end of 2 weeks, evaluate:
- **Primary:** >= 60% activation rate with median TTV < 8 minutes
- **Secondary:** >= 15 percentage point improvement over Smoke baseline

If PASS: Document the sequence, the automation pipeline, and the optimization that worked. Proceed to Scalable.

If FAIL: Identify whether the issue is TTV (users activate but slowly) or activation rate (users do not activate at all). For TTV: simplify the onboarding flow — fewer steps, more pre-filled data. For activation rate: test a different activation metric that is easier to reach. Re-run Baseline.

## Time Estimate

- 3 hours: Design the 7-email sequence with copy
- 4 hours: Build n8n workflows (enrollment, milestone sync, activation exit, stall detection)
- 2 hours: End-to-end testing of the automation pipeline
- 3 hours: Analyze funnel data and implement drop-off fix
- 4 hours: Monitor daily metrics and evaluate at end of 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Behavioral onboarding email sequences | Free up to 1K contacts; Starter $49/mo — https://loops.so/pricing |
| Intercom | In-app product tours and contextual messages | Starter $39/seat/mo — https://www.intercom.com/pricing |
| Cal.com | Booking link for personal help offers in emails | Free for individuals — https://cal.com/pricing |

## Drills Referenced

- `onboarding-sequence-design` — design the 7-email behavioral sequence with content, triggers, and branching logic
- `onboarding-sequence-automation` — wire PostHog events to Loops sequences via n8n for always-on delivery
- `activation-optimization` — find the biggest funnel drop-off and implement a targeted fix
