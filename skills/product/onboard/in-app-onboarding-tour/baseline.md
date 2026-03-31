---
name: in-app-onboarding-tour-baseline
description: >
  Interactive Product Tour — Baseline Run. Deploy always-on onboarding automation with behavioral
  email sequences, detailed funnel tracking, and A/B testing against a control group to prove
  sustained activation lift.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=50% activation rate AND >=10pp lift over control group"
kpis: ["7-day activation rate", "Tour completion rate", "Median time to activation", "Activation lift vs control"]
slug: "in-app-onboarding-tour"
install: "npx gtm-skills add product/onboard/in-app-onboarding-tour"
drills:
  - posthog-gtm-events
  - onboarding-sequence-automation
  - activation-optimization
---

# Interactive Product Tour — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Deploy a production-quality onboarding experience with always-on automation: the product tour from Smoke is refined, behavioral email sequences fire based on milestone progress, and a 50/50 A/B test proves the tour delivers a statistically significant activation lift over the control (no tour).

Pass threshold: >=50% activation rate in the tour group AND >=10 percentage point lift over the control group, measured over 2 weeks with at least 100 users per variant.

## Leading Indicators

- Tour group activation rate trending above control group within the first 5 days
- Email sequence open rate >=40% for Email 1 (welcome)
- Email sequence click rate >=8% for emails with CTAs
- Tour completion rate >=55% (improved from Smoke)
- Stalled users receiving nudge emails re-engage within 48 hours at >=20% rate
- No single funnel step drops below 60% conversion

## Instructions

### 1. Set up comprehensive event tracking

Run the `posthog-gtm-events` drill. Implement the full onboarding event taxonomy:

- `onboarding_tour_impression` — tour was shown to the user
- `onboarding_tour_started` — user interacted with first step
- `onboarding_tour_step_completed` with `{step_number, step_name, duration_seconds}`
- `onboarding_tour_completed` with `{total_steps, total_duration_seconds}`
- `onboarding_tour_dismissed` with `{step_number, reason}`
- `onboarding_email_sent` with `{email_step, subject}`
- `onboarding_email_opened` with `{email_step}`
- `onboarding_email_clicked` with `{email_step, cta_url}`
- `onboarding_milestone_reached` with `{milestone_name, milestone_number, days_since_signup}`
- `activation_reached` with `{activation_type, days_since_signup, tour_variant}`

Build PostHog funnels:
- **Tour funnel**: `tour_started` → step 1 → step 2 → ... → `tour_completed` → `activation_reached`
- **Email funnel**: `email_sent` → `email_opened` → `email_clicked` → `activation_reached` (breakdown by email step)
- **Overall onboarding funnel**: `signup_completed` → each milestone → `activation_reached`

Build PostHog cohorts: "Tour group" (saw the tour), "Control group" (no tour), "Activated", "Stalled 3+ days".

### 2. Wire behavioral email automation

Run the `onboarding-sequence-automation` drill. Connect PostHog milestone events to Loops email triggers via n8n:

- On `signup_completed`: enroll in Loops sequence, send welcome email immediately
- On milestone completion: update Loops contact properties, skip irrelevant emails
- On `activation_reached`: exit the non-activated branch, send celebration email
- On no milestone progress after 24h/48h/5d/7d: send nudge emails with contextual help

Emails fire based on real behavior, not just time delays. A user who activates in 2 hours gets the celebration email and skips all nudges.

### 3. Launch the A/B test

Create a PostHog feature flag `onboarding-tour-baseline` with 50/50 split:
- **Treatment**: Full product tour + behavioral emails
- **Control**: No tour, standard emails only (time-based welcome sequence)

Set minimum experiment duration: 14 days or until 100+ users per variant, whichever is longer. Configure PostHog experiment with primary metric = `activation_reached` conversion rate.

**Human action required:** Verify the tour renders correctly in the treatment variant and is completely hidden in the control variant. Test both paths with a test account before launching to real users.

### 4. Optimize the biggest drop-off

Run the `activation-optimization` drill. After the first week of data:

1. Identify the largest drop-off step in the onboarding funnel
2. Diagnose the cause: confusion (users do not know what to do), effort (step requires too much work), unclear value (users do not see why), or technical blocker
3. Implement a fix targeting that specific step: revise the tour step copy, add a contextual in-app message, simplify the UI, or add a progress indicator
4. Use PostHog session recordings to watch 5-10 users navigating the drop-off step

### 5. Monitor weekly

Check the experiment weekly but do not stop early. Review:
- Activation rate: treatment vs control
- Tour completion rate trend
- Email open/click rates by step
- Any guardrail violations (e.g., negative reply rate >5%, bounce rate >3%)

### 6. Evaluate at 2 weeks

Query PostHog experiment results. Require 95% statistical significance.

**PASS** (>=50% activation AND >=10pp lift): Roll the tour to 100% of users. Disable the control variant. Document the activation rate, lift, and key learnings. Proceed to Scalable.
**FAIL**: Diagnose — is the tour helping but not enough (iterate on tour), or is there no difference (the tour is not addressing the real blocker)? Fix the identified issue and re-run for another 2-week cycle.

## Time Estimate

- 3 hours: Set up event tracking and funnels
- 4 hours: Wire behavioral email automation via n8n
- 2 hours: Configure A/B test and launch
- 4 hours: Analyze drop-offs and implement fixes (week 1)
- 2 hours: Evaluate results and document (week 2)
- 1 hour: Roll out winner or plan iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, experiments, feature flags | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app messages | Essential $39/seat/mo + Proactive Support Plus $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Behavioral onboarding emails | Free up to 1K contacts; $49/mo for paid ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Workflow automation (PostHog → Loops bridge) | Starter: EUR 24/mo (2,500 executions) or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost at this level:** $162-$201/mo (Intercom $138 + Loops $0-49 + n8n $24; PostHog free tier)

## Drills Referenced

- `posthog-gtm-events` — establishes the full event taxonomy for onboarding tracking
- `onboarding-sequence-automation` — wires PostHog milestone events to Loops email triggers via n8n for behavioral email delivery
- `activation-optimization` — identifies and fixes the largest funnel drop-off to improve activation rate
