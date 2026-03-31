---
name: onboarding-email-sequence-baseline
description: >
  Onboarding email sequence — Baseline Run. Automate the 7-email onboarding
  sequence with behavioral triggers via n8n, Loops, and PostHog. Run always-on
  for 2 weeks and measure activation rate lift.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Email"
level: "Baseline Run"
time: "10 hours over 2 weeks"
outcome: "Activation rate >= 25% for emailed users at day 7, with >= 5 percentage point lift over no-email control"
kpis: ["Activation rate at day 7", "Activation rate lift vs control", "Email open rate per step", "Email click rate per step", "Time to activation (days)", "Email-to-activation funnel conversion"]
slug: "onboarding-email-sequence"
install: "npx gtm-skills add product/onboard/onboarding-email-sequence"
drills:
  - onboarding-sequence-automation
  - posthog-gtm-events
  - threshold-engine
---

# Onboarding Email Sequence — Baseline Run

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Email

## Outcomes

Automate the full 7-email onboarding sequence with behavioral triggers. Every new signup automatically enters the sequence, receives emails based on their actual behavior (milestones reached or missed), and exits when they activate. Run always-on for 2 weeks. Pass threshold: activation rate >= 25% at day 7 for emailed users, with at least 5 percentage points lift over users who did not receive the sequence.

## Leading Indicators

- Enrollment rate: 95%+ of new signups are correctly enrolled in the sequence within 5 minutes of signup
- Email 1 open rate holds above 50% with automated sending (consistent with or better than smoke test)
- Behavioral triggers fire correctly: Email 2 is skipped for users who completed Milestone 2 within 24h
- Activation email (Email 6) sends within 1 hour of activation event
- Zero missed enrollments or broken webhook connections in the daily monitoring report

## Instructions

### 1. Set up event tracking infrastructure

Run the `posthog-gtm-events` drill to establish the full event taxonomy for this play. Beyond the smoke test events, add:

- `onboarding_email_enrolled` — fires when a new user is added to the Loops sequence
- `onboarding_email_skipped` with `{email_step: N, reason: "milestone_already_reached"}` — tracks behavioral skipping
- `onboarding_milestone_reached` with `{milestone: "milestone_2" | "milestone_3" | ... | "activation"}`
- `onboarding_sequence_completed` — fires when user finishes the sequence (either via activation or all 7 emails sent)

Create a PostHog funnel: `onboarding_email_enrolled` > `email_1_opened` > `milestone_2_completed` > `milestone_3_completed` > `activation_reached`. Break down by `signup_source` and `plan_type`.

### 2. Automate the sequence

Run the `onboarding-sequence-automation` drill. This creates the always-on pipeline:

1. **Enrollment workflow (n8n):** PostHog fires `signup_completed` webhook > n8n creates Loops contact with properties > Loops auto-starts the onboarding sequence
2. **Milestone sync workflows (n8n):** PostHog fires milestone webhooks > n8n updates Loops contact properties > Loops sequence branches based on updated properties
3. **Activation exit workflow (n8n):** PostHog fires `activation_reached` > n8n updates Loops contact > Loops exits the "not activated" branch and sends Email 6 (celebration)

**Human action required:** Before enabling the automation for all users, run the full test pipeline described in Step 8 of the `onboarding-sequence-automation` drill. Create a test user, walk through every branch, and verify every email fires at the right time. Fix any issues before going live.

### 3. Expand to 7 emails

Add the two post-activation emails that were deferred from the smoke test:

- **Email 6 — Milestone celebration (trigger: immediately on activation):** Congratulate the user on their specific achievement. Suggest the next high-value action (invite teammates, connect integrations, explore advanced features). CTA links directly to the next action.
- **Email 7 — Next steps (trigger: 2 days after activation):** Bridge from onboarding to habitual usage. Highlight an advanced feature or integration relevant to their use case. Include a link to the help center or community.

Add these to the Loops sequence with the appropriate triggers and timing.

### 4. Maintain the holdout control group

Continue holding out 10-20% of new signups from the email sequence to measure the true lift. In n8n, add a random assignment step after the enrollment trigger:

```
PostHog Webhook (signup_completed)
  → Generate random number 0-100
  → IF random < 15: assign control group (set PostHog property, do NOT enroll in Loops)
  → ELSE: enroll in Loops sequence as treatment
```

Log group assignment as a PostHog person property: `onboarding_email_group: "treatment"` or `"control"`.

### 5. Set up daily monitoring

Create an n8n scheduled workflow that runs every morning:

1. Query PostHog for yesterday's metrics: new enrollments, emails sent per step, opens per step, clicks per step, milestones reached, activations
2. Check for errors: failed webhook deliveries, Loops API errors, enrollment failures
3. Calculate running totals: overall open rate, click rate, activation rate for treatment vs control
4. Send a digest to Slack or email with: yesterday's numbers, running totals, and any alerts

Alert conditions:
- Open rate for any email step drops below 30%
- More than 5% of signups fail to enroll in the sequence
- Activation rate for treatment group falls below control group (the sequence is hurting, not helping)

### 6. Evaluate at day 14

Run the `threshold-engine` drill with these criteria:

- **Activation rate >= 25% at day 7** for the treatment group (users who received the sequence)
- **Activation rate lift >= 5 percentage points** over the control group
- **Sequence health:** Open rate >= 40% across all steps, click rate >= 5% for Emails 2-5

Calculate time-to-activation for both groups. The treatment group should activate faster (fewer days from signup to activation) than the control group.

If PASS: The automated sequence lifts activation. Proceed to Scalable to optimize and segment.
If FAIL on activation rate: Analyze the PostHog funnel to find the biggest drop-off. Is it email engagement (low opens/clicks) or product friction (clicking but not completing the action)? Fix the weaker link.
If FAIL on lift vs control: The emails may not be adding value beyond what users discover on their own. Test more targeted timing (e.g., send only when user is stuck, not on a fixed schedule) or more compelling CTAs.

## Time Estimate

- 4 hours: Set up event tracking, build n8n workflows, test the full pipeline
- 2 hours: Expand to 7 emails, configure monitoring
- 2 hours: Daily monitoring over 2 weeks (10 min/day)
- 2 hours: Analysis and threshold evaluation

Total: ~10 hours spread over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Automated email sequences with behavioral branching | Free up to 1,000 contacts. $49/mo for unlimited emails. [Pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, cohort comparison | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Workflow automation connecting PostHog to Loops | Free self-hosted. Cloud from €24/mo (2,500 executions). [Pricing](https://n8n.io/pricing/) |
| Cal.com | Booking link in Email 5 (personal help offer) | Free for 1 user. [Pricing](https://cal.com/pricing) |

**Estimated monthly cost: $49-73/mo** (Loops $49 + n8n cloud €24 if not self-hosted. PostHog and Cal.com free tier.)

## Drills Referenced

- `onboarding-sequence-automation` — wires the email sequence to behavioral triggers via n8n, PostHog, and Loops
- `posthog-gtm-events` — establishes the event taxonomy and funnel tracking for the onboarding email play
- `threshold-engine` — evaluates activation rate and lift against pass/fail criteria
