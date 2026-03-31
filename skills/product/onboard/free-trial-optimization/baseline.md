---
name: free-trial-optimization-baseline
description: >
  Trial Conversion Optimization — Baseline Run. First always-on trial conversion system.
  Full event taxonomy, activation funnel analysis, and automated onboarding sequences
  running continuously for all new trial users.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=35% trial-to-paid conversion sustained over 2 weeks with 50+ trial starts"
kpis: ["Trial-to-paid conversion rate", "72-hour activation rate", "Funnel step drop-off rates", "Email sequence engagement"]
slug: "free-trial-optimization"
install: "npx gtm-skills add product/onboard/free-trial-optimization"
drills:
  - posthog-gtm-events
  - activation-optimization
  - feature-announcement
---

# Trial Conversion Optimization — Baseline Run

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The trial onboarding experience runs continuously for all new trial signups. Full PostHog event taxonomy captures every step from trial start to payment. Activation rate and conversion rate are measured by cohort week. The biggest funnel drop-off point is identified and improved. Conversion sustains at >=35% over 2 weeks with 50+ trial starts.

## Leading Indicators

- PostHog funnel shows clear step-by-step conversion from trial_started to payment_completed
- Activation rate (72h) exceeds 60% for the first week's cohort
- The single biggest drop-off step improves by >=10 percentage points after optimization
- Session recordings reveal specific friction patterns that are addressable

## Instructions

### 1. Deploy full event taxonomy

Run the `posthog-gtm-events` drill to establish comprehensive tracking for the trial conversion funnel. Implement these events with standardized properties:

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `trial_started` | User creates account on trial plan | `signup_source`, `plan_interest`, `company_size` |
| `onboarding_tour_started` | Product tour begins | `tour_version`, `persona_type` |
| `onboarding_tour_completed` | Product tour final step reached | `tour_version`, `completion_time_seconds` |
| `onboarding_tour_abandoned` | User dismisses tour before completion | `tour_version`, `last_step_completed` |
| `activation_reached` | User completes the activation milestone | `days_since_trial_start`, `path_taken` |
| `feature_explored` | User tries a feature beyond the core action | `feature_name`, `trial_day` |
| `upgrade_prompt_shown` | Any upgrade CTA rendered | `prompt_type`, `trigger_reason`, `trial_day` |
| `upgrade_started` | User clicks to upgrade / enters billing flow | `prompt_type`, `trial_day` |
| `payment_completed` | Successful payment processed | `plan_selected`, `trial_duration_days`, `activation_day` |
| `trial_expired` | Trial window ends without conversion | `activation_reached` (boolean), `last_active_day` |

Build PostHog funnels:
- **Full conversion funnel:** trial_started -> onboarding_tour_completed -> activation_reached -> upgrade_started -> payment_completed
- **Activation funnel:** trial_started -> first_login -> onboarding_tour_started -> onboarding_tour_completed -> activation_reached
- **Upgrade funnel:** upgrade_prompt_shown -> upgrade_started -> payment_completed

Create PostHog cohorts:
- Activated trial users (activation_reached within 72h)
- Stalled trial users (no activation after 72h, still logging in)
- Ghost trial users (no login after Day 1)
- Converted trial users (payment_completed)

### 2. Optimize the activation bottleneck

Run the `activation-optimization` drill against the PostHog funnel data:

1. Pull the activation funnel and identify the step with the highest absolute drop-off
2. Review PostHog session recordings for 10-15 users who dropped at that step. Categorize the friction: confusion (did not know what to do), effort (too many steps), value unclear (did not see the point), or technical (error/slow load)
3. Design 2-3 specific fixes targeting the dominant friction type. Examples:
   - If confusion: add a contextual tooltip at the drop-off point using Intercom
   - If effort: reduce required fields or pre-fill data
   - If value unclear: add a progress indicator showing "2 steps to your first [outcome]"
4. Implement the top fix and measure the activation funnel for the next cohort

Use PostHog feature flags to A/B test if volume permits (25+ users per variant). Otherwise, deploy the fix and compare the next cohort week-over-week.

### 3. Launch feature-guided engagement

Run the `feature-announcement` drill to configure targeted in-app messages that guide activated trial users to explore features beyond the core action:

- After activation: show a "What's next" message highlighting 2-3 features that drive stickiness
- At Day 7 (mid-trial): show a usage summary — "You've done X, Y, Z this week" — with a prompt to try a feature they have not used
- At Day 10 (pre-expiry): show a value recap with a clear upgrade CTA — "Your trial ends in [N] days. Here's what you'll keep with [Plan Name]."

Track each message: impression, click, feature_explored event within 24h of click.

### 4. Evaluate against threshold

Measure after 2 full weeks of continuous operation with 50+ trial starts:
- Primary: trial-to-paid conversion rate (target: >=35%)
- Supporting: 72-hour activation rate, funnel step improvements, email engagement rates

If PASS: document the funnel baseline metrics (these become the reference for Scalable experiments). Proceed to Scalable.
If FAIL: pull the updated funnel, find the new biggest drop-off, and iterate. Re-evaluate after another week.

## Time Estimate

- 3 hours: Event taxonomy deployment and funnel/cohort setup
- 5 hours: Activation bottleneck analysis (session recordings, friction categorization, fix design)
- 4 hours: Feature-guided engagement messages (copy, targeting, tracking)
- 2 hours: A/B test setup or cohort comparison analysis
- 2 hours: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, session recordings, feature flags, cohorts | Free tier: 1M events/mo, 5K recordings/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app messages, contextual tooltips | From $29/seat/mo; Proactive Support add-on $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle email sequences | From $49/mo for 1,000+ contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Webhook workflows for CRM routing | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |

**Estimated play-specific cost:** ~$50-150/mo (PostHog likely within free tier; Intercom and Loops are shared stack costs)

## Drills Referenced

- `posthog-gtm-events` — deploys the full event taxonomy and builds funnels/cohorts for the trial conversion pipeline
- `activation-optimization` — identifies and fixes the biggest activation bottleneck using funnel data and session recordings
- `feature-announcement` — creates targeted in-app messages that guide trial users from activation to feature exploration to upgrade
