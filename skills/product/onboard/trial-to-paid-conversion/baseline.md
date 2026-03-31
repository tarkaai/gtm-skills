---
name: trial-to-paid-conversion-baseline
description: >
  Trial-to-Paid Conversion — Baseline Run. First always-on automation. Behavioral email
  sequences fire based on PostHog events. Trial health scoring segments users into Hot, Warm,
  and Cold for targeted interventions. Runs continuously for all new trial signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=45% trial-to-paid conversion rate sustained over 2 weeks with 30-50 trial starts"
kpis: ["Trial-to-paid conversion rate", "Activation milestone completion rate", "Trial health score distribution", "Time to activation"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add product/onboard/trial-to-paid-conversion"
drills:
  - posthog-gtm-events
  - onboarding-sequence-automation
---

# Trial-to-Paid Conversion — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

The trial-to-paid conversion system runs continuously for all new trial signups (30-50 over 2 weeks). Behavioral email sequences fire automatically based on PostHog events and milestone completion. A daily-refreshed trial health score segments users into Hot, Warm, and Cold. In-app messages trigger based on user behavior. Conversion sustains at >= 45% over 2 weeks, and Hot-segment users convert at >= 60%.

## Leading Indicators

- PostHog funnel shows clear step-by-step conversion from trial_started to payment_completed
- 72-hour activation rate exceeds 55% across all trial signups
- Email sequence engagement: open rate > 40%, click rate > 8%
- Trial health score segments show expected distribution: 20-30% Hot, 40-50% Warm, 20-30% Cold
- Hot-segment users convert at >= 60%, validating the scoring model

## Instructions

### 1. Deploy full event taxonomy

Run the `posthog-gtm-events` drill to establish comprehensive tracking for the trial conversion funnel. Implement these events with standardized properties:

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `trial_started` | User creates account on trial plan | `signup_source`, `plan_interest`, `company_size`, `use_case` |
| `onboarding_tour_started` | Product tour begins | `tour_version` |
| `onboarding_tour_completed` | Product tour final step reached | `tour_version`, `completion_time_seconds` |
| `milestone_1_completed` | First intermediate milestone | `milestone_name`, `days_since_trial_start` |
| `milestone_2_completed` | Second intermediate milestone | `milestone_name`, `days_since_trial_start` |
| `milestone_3_completed` | Third intermediate milestone | `milestone_name`, `days_since_trial_start` |
| `activation_reached` | User completes the activation milestone | `days_since_trial_start`, `path_taken` |
| `feature_used` | User interacts with any trackable feature | `feature_name`, `trial_day` |
| `teammate_invited` | User invites a team member | `invite_count`, `trial_day` |
| `upgrade_prompt_shown` | Any upgrade CTA rendered | `prompt_type`, `trigger_reason`, `trial_day` |
| `upgrade_started` | User enters billing flow | `prompt_type`, `trial_day` |
| `payment_completed` | Successful payment processed | `plan_selected`, `trial_duration_days`, `activation_day` |
| `trial_expired` | Trial window ends without conversion | `activation_reached` (boolean), `milestones_completed`, `last_active_day` |

Build PostHog funnels:
- **Full conversion funnel:** trial_started -> onboarding_tour_completed -> activation_reached -> upgrade_started -> payment_completed
- **Activation funnel:** trial_started -> milestone_1_completed -> milestone_2_completed -> milestone_3_completed -> activation_reached
- **Upgrade funnel:** upgrade_prompt_shown -> upgrade_started -> payment_completed

Create PostHog cohorts:
- Activated trial users (activation_reached = true, within 72h of trial_started)
- Stalled trial users (no activation_reached after 72h, still logging in)
- Ghost trial users (no session after Day 1)
- Converted trial users (payment_completed = true)

### 2. Automate the onboarding email sequence

Run the `onboarding-sequence-automation` drill to wire the touchpoint sequence from Smoke into always-on automation:

1. Connect PostHog events to Loops via n8n webhooks. When `trial_started` fires, enroll the user in the Loops onboarding sequence.
2. Configure behavioral branching:
   - If `milestone_1_completed` fires before Day 1, skip the Day 1 setup nudge email
   - If `activation_reached` fires at any point, exit the "not activated" email branch and send the celebration/next-steps email
   - If `payment_completed` fires, exit all trial sequences immediately
3. Implement the full email sequence from the Smoke test with the timing and skip logic:
   - Email 1 (Day 0): Welcome + first action CTA
   - Email 2 (Day 1, if Milestone 1 not done): Setup help
   - Email 3 (Day 3): Use-case coaching
   - Email 4 (Day 5, if not activated): Social proof
   - Email 5 (Day 7, if not activated): Personal check-in from founder + Cal.com link
   - Email 6 (on activation): Celebration + next steps
   - Email 7 (Day 10, if activated but not converted): Upgrade nudge with value summary
   - Email 8 (Day 12-13): Urgency — trial expiring, keep your work
4. Track email events in PostHog: `onboarding_email_sent`, `onboarding_email_opened`, `onboarding_email_clicked` with `email_step` property

### 3. Build and deploy trial health scoring

Run the the trial activation scoring workflow (see instructions below) drill to create the real-time scoring model:

1. Configure the four scoring dimensions with weights calibrated to Smoke test data:
   - Activation progress (40%): milestones completed / total milestones
   - Feature usage depth (25%): unique features used / trackable features
   - Engagement recency (20%): inverse of days since last session
   - Team signals (15%): teammates invited + shared artifacts

2. Deploy the daily n8n scoring workflow that:
   - Queries PostHog for all active trial users
   - Computes the composite 0-100 health score
   - Classifies users: Hot (>= 70), Warm (35-69), Cold (< 35)
   - Syncs scores and segments to Attio custom attributes
   - Flags segment transitions (e.g., Warm -> Cold) for intervention

3. Create in-app messages in Intercom targeted by PostHog cohort:
   - **Hot users (Day 8+):** Show a non-blocking banner: "You've completed [N milestones]. Upgrade to [Plan] to unlock [specific benefit]."
   - **Warm users (Day 3+):** Show a contextual tooltip: "Next step: [next milestone action]. Here's a quick guide."
   - **Cold users (Day 2+):** Show a help offer: "Need help getting started? Book a 15-minute call: [Cal.com link]"

4. Validate the scoring model after 2 weeks: Hot users should convert at >= 60%. If they do not, re-calibrate the dimension weights.

### 4. Evaluate against threshold

Measure after 2 full weeks of continuous operation with 30-50 trial starts:

- **Primary:** trial-to-paid conversion rate (target: >= 45%)
- **Segment performance:** Hot conversion rate >= 60%, Warm >= 30%, Cold < 15%
- **Supporting:** 72-hour activation rate, email sequence engagement, in-app message interaction rates, scoring model accuracy

If PASS: document the baseline metrics. The conversion rate by segment, the email engagement benchmarks, and the scoring model weights become the reference for Scalable experiments. Proceed to Scalable.
If FAIL: pull the PostHog funnel to find the highest drop-off step. Review session recordings for 10 users who dropped at that step. Fix the single highest-impact friction point and re-run for another week.

## Time Estimate

- 4 hours: Full event taxonomy deployment, funnel/cohort setup
- 6 hours: Email sequence automation (n8n webhooks, Loops configuration, behavioral branching)
- 6 hours: Trial health scoring (PostHog queries, n8n scoring workflow, Attio sync, Intercom messages)
- 4 hours: Monitoring, analysis, scoring model validation
- 4 hours: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, session recordings | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Behavioral email sequences | From $49/mo for 1,000+ contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app messages, product tours | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Webhook workflows, scoring workflow, CRM sync | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Attio | CRM, trial health score storage, intervention logging | Standard stack |
| Cal.com | Booking links for onboarding calls | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost:** ~$50-150/mo (PostHog likely within free tier; Loops and Intercom are shared stack costs)

## Drills Referenced

- `posthog-gtm-events` — deploys the full event taxonomy and builds funnels/cohorts for the trial conversion pipeline
- `onboarding-sequence-automation` — wires the behavioral email sequence to PostHog events via n8n, with milestone-based branching and skip logic
- the trial activation scoring workflow (see instructions below) — builds the daily-refreshed 0-100 health score that segments trial users into Hot/Warm/Cold for targeted interventions
