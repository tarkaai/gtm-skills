---
name: freemium-model-baseline
description: >
  Freemium Tier Strategy — Baseline Run. Instrument the full free-to-paid funnel in PostHog,
  deploy automated upgrade prompts triggered by usage thresholds and feature gates, and run
  always-on for 2 weeks to validate >=8% free-to-paid conversion.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=8% free-to-paid conversion with automated prompts running always-on"
kpis: ["Free signups", "Free-to-paid rate", "Median days to upgrade", "Upgrade prompt CTR"]
slug: "freemium-model"
install: "npx gtm-skills add product/onboard/freemium-model"
drills:
  - posthog-gtm-events
  - upgrade-prompt
  - usage-threshold-detection
---

# Freemium Tier Strategy — Baseline Run

> **Stage:** Product -> Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The free-to-paid conversion system runs always-on for the first time. Automated upgrade prompts fire when free users hit plan limits or feature gates. The full funnel is instrumented in PostHog: signup -> activation -> limit encounter -> prompt shown -> upgrade started -> upgrade completed. The system should convert 8%+ of free users to paid without any manual outreach.

## Leading Indicators

- PostHog events flowing for all conversion funnel steps: `signup_completed`, `first_value_action`, `usage_limit_hit`, `feature_gate_hit`, `upgrade_prompt_shown`, `upgrade_prompt_clicked`, `upgrade_started`, `upgrade_completed`
- Usage threshold detection workflow running daily in n8n, flagging accounts at 70%+, 85%+, 95%+ of plan limits
- Upgrade prompts firing automatically when users hit defined thresholds (no manual triggering)
- At least 50% of free users who see an upgrade prompt engage with it (click, expand, or interact -- not just dismiss)
- Upgrade prompt-to-checkout CTR exceeds 10% for limit-proximity triggers

## Instructions

### 1. Instrument the full free-to-paid funnel

Run the `posthog-gtm-events` drill to establish the complete event taxonomy for this play. Define and implement these events:

| Event | When It Fires | Key Properties |
|-------|--------------|----------------|
| `signup_completed` | User creates a free account | `signup_source`, `utm_campaign`, `referrer` |
| `first_value_action` | User completes the core action (from Smoke learnings) | `action_type`, `time_since_signup_hours` |
| `usage_limit_approaching` | User reaches 80% of any plan cap | `resource_type`, `current_count`, `plan_limit`, `pct_used` |
| `usage_limit_hit` | User reaches 100% of a plan cap | `resource_type`, `current_count`, `plan_limit` |
| `feature_gate_hit` | User attempts a gated feature | `feature_name`, `gate_type`, `user_plan` |
| `upgrade_prompt_shown` | In-app prompt or email delivered | `prompt_type`, `trigger`, `surface` |
| `upgrade_prompt_clicked` | User clicks the upgrade CTA | `prompt_type`, `trigger`, `surface` |
| `upgrade_prompt_dismissed` | User dismisses the prompt | `prompt_type`, `trigger`, `dismissal_count` |
| `upgrade_started` | User enters the checkout flow | `plan_selected`, `billing_interval`, `trigger_source` |
| `upgrade_completed` | Stripe confirms the subscription | `plan_name`, `mrr`, `days_since_signup`, `trigger_source` |

Build PostHog funnels:
- **Full conversion funnel**: `signup_completed` -> `first_value_action` -> `upgrade_prompt_shown` -> `upgrade_prompt_clicked` -> `upgrade_started` -> `upgrade_completed`
- **Limit-driven funnel**: `usage_limit_approaching` -> `usage_limit_hit` -> `upgrade_prompt_shown` -> `upgrade_completed`
- **Gate-driven funnel**: `feature_gate_hit` -> `upgrade_prompt_shown` -> `upgrade_completed`

### 2. Deploy automated usage threshold detection

Run the `usage-threshold-detection` drill to build the always-on system that identifies free users approaching plan limits:

- Configure the plan cap mapping from the free tier definition (Smoke step 1): resource type, free tier limit, urgency tiers at 70%, 85%, 95%, 100%
- Build the daily n8n workflow that queries PostHog for all free users at 70%+ of any limit
- Compute consumption velocity: is the user on track to hit the limit this billing period or just at a static level
- Classify each flagged user into urgency tiers: approaching (70-84%), imminent (85-94%), critical (95-100%), exceeded (100%+)
- Store threshold data in Attio: `usage_alert_tier`, `usage_alert_resource`, `usage_pct_consumed`
- When a user enters the imminent or critical tier, fire a webhook to trigger the upgrade prompt

### 3. Deploy automated upgrade prompts

Run the `upgrade-prompt` drill to build contextual upgrade messaging that fires automatically:

**Limit-proximity prompts (highest converting):**
- Trigger: user enters imminent tier (85%+ of a plan cap)
- Intercom in-app message: "You've used {current_count} of {plan_limit} {resource_type}. Upgrade to {paid_plan} for {paid_limit}." Include the specific numbers and a one-click upgrade button.
- Loops email (24h later if no action): usage summary + upgrade link + what they get on paid

**Feature-gate prompts:**
- Trigger: `feature_gate_hit` event fires
- Intercom in-app message (immediate): "This feature is available on {paid_plan}. Here's what you'll get: {feature list}." Show a preview or screenshot of the gated feature in action.
- Do not repeat the same gate prompt more than 2x per feature per user

**Time-based prompts (lowest priority):**
- Trigger: free user active 14+ days, completed value action, has not seen an upgrade prompt in 7+ days
- Loops email: "You've been using {product} for {days} days. Here's what {paid_plan} unlocks." Personalize with their actual usage data.

**Route high-value accounts to sales:**
- If the free account has 5+ team members or is at a company with 100+ employees (from Attio enrichment), do not self-serve. Create an Attio deal and assign to the account owner with usage context.

### 4. Monitor for 2 weeks and evaluate

Let the system run always-on for 2 full weeks. Do not adjust prompts during this period. Monitor:

- Daily: check PostHog live events to confirm prompts are firing, check Stripe for new subscriptions
- Weekly: review the conversion funnel for drop-off points, check prompt CTR by trigger type

After 2 weeks, evaluate against the pass threshold:
- Free-to-paid rate = (users who upgraded) / (total free signups during the 2-week window)
- Pass threshold: >=8% free-to-paid conversion

If PASS: automated prompts are converting free users at a sustainable rate. Proceed to Scalable.

If FAIL, diagnose by examining the funnel:
- Signup to activation drop-off >50%: onboarding friction (revisit onboarding flow)
- Activation to limit encounter <30%: free tier too generous (tighten limits or add feature gates)
- Prompt shown to prompt clicked <10%: prompt copy or placement (test different messaging)
- Prompt clicked to upgrade completed <30%: checkout friction (simplify pricing page, reduce steps)
- Check prompt fatigue: are users dismissing prompts repeatedly? If dismissal rate >60%, reduce prompt frequency.

## Time Estimate

- 3 hours: instrument the full event taxonomy and build PostHog funnels
- 3 hours: configure usage threshold detection (plan cap mapping, n8n workflow, Attio sync)
- 4 hours: deploy upgrade prompts (Intercom messages, Loops emails, routing rules)
- 4 hours: monitoring over 2 weeks (~2 hours/week of active review)
- 2 hours: analysis, funnel diagnosis, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, session recordings | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app upgrade prompts (limit alerts, feature gates) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Upgrade emails (limit nudges, time-based nurture) | $49/mo for 5,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | CRM records with usage alert tiers and deal tracking | Free up to 3 seats -- [attio.com/pricing](https://attio.com/pricing) |
| n8n | Usage threshold detection workflow, webhook routing | Free self-hosted; cloud from $24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Stripe | Checkout sessions, subscription creation | 2.9% + $0.30 per transaction -- [stripe.com/pricing](https://stripe.com/pricing) |

**Estimated play-specific cost: ~$80-130/mo** (Intercom + Loops + n8n; PostHog and Attio free tiers likely sufficient)

## Drills Referenced

- `posthog-gtm-events` -- establishes the full event taxonomy for the free-to-paid funnel
- `upgrade-prompt` -- builds contextual upgrade messaging triggered by usage thresholds and feature gates
- `usage-threshold-detection` -- detects free users approaching plan limits and classifies urgency for prompt routing
