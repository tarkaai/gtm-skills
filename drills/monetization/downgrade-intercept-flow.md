---
name: downgrade-intercept-flow
description: Build and deploy in-product and email intervention surfaces that intercept users showing downgrade intent with personalized retention offers
category: Conversion
tools:
  - Intercom
  - Loops
  - PostHog
  - n8n
  - Attio
fundamentals:
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - loops-transactional
  - posthog-custom-events
  - posthog-feature-flags
  - posthog-cohorts
  - n8n-triggers
  - n8n-workflow-basics
  - attio-contacts
  - attio-deals
---

# Downgrade Intercept Flow

This drill builds the intervention surface that fires when the `downgrade-intent-detection` drill identifies a user at risk of downgrading. It deploys personalized in-product messages, email sequences, and retention offers matched to the user's specific situation. The goal is to demonstrate the value the user is about to lose and offer a path to stay.

## Prerequisites

- `downgrade-intent-detection` drill running (provides scored cohorts)
- Intercom configured with in-app messaging permissions
- Loops configured with transactional and sequence email capabilities
- PostHog feature flags enabled
- Defined retention offers approved by the team (discounts, plan pauses, feature coaching)
- Understanding of your plan tiers and what premium features differentiate them

## Steps

### 1. Design tiered interventions matched to intent severity

Each intervention tier maps to a downgrade intent tier from the detection drill:

**Moderate intent (score 36-60) -- Feature education:**
The user is underutilizing premium features. The intervention highlights the value they are not capturing.

Using `intercom-in-app-messages`, deploy a targeted in-app message to the "Downgrade Intent: Moderate" PostHog cohort:
- Trigger: user logs in while in the moderate cohort
- Message type: Banner (non-blocking)
- Content: "Did you know? Your [plan name] plan includes [specific premium feature they have not used recently]. Here's how teams like yours use it to [specific outcome]."
- CTA: "Show me how" -> link to a product tour or help article for that feature
- Frequency: once per week, maximum 3 times total per user

Using `loops-sequences`, enroll moderate-intent users in a 3-email "feature value" sequence:
- Email 1 (day 0): "You have access to [feature] but haven't used it recently. Here's a 2-minute setup."
- Email 2 (day 3): "Teams using [feature] see [quantified outcome]. Here's a quick start guide."
- Email 3 (day 7): "Need help getting value from your plan? Reply to this email or book a 15-minute session."

**High intent (score 61-85) -- Personalized retention offer:**
The user is actively evaluating a downgrade. The intervention presents a concrete reason to stay.

Using `intercom-in-app-messages`, deploy a targeted message to the "Downgrade Intent: High" cohort:
- Trigger: user logs in while in the high cohort
- Message type: Modal (attention-grabbing but dismissible)
- Content: personalized based on their usage. Use PostHog properties to populate:
  - If they use premium features: "You've used [feature] [N] times this month. On the [lower plan], you would lose access to this."
  - If they have team members: "Your team of [N] relies on [feature]. Downgrading would remove [specific capability]."
- CTA primary: "Keep my current plan"
- CTA secondary: "Talk to someone about my options"

Using `loops-transactional`, send a personalized email within 2 hours of entering high intent tier:
- Subject: "Before you make any changes to your plan"
- Body: usage summary showing what they would lose, plus a retention offer (e.g., 20% discount for 3 months, or a free month)
- CTA: "Claim your offer" with a unique link that applies the discount automatically

**Imminent intent (score 86-100) -- High-touch human outreach:**
Using `attio-contacts`, create an urgent task for the account owner with:
- User's name, plan, MRR at risk
- Top downgrade signals and their scores
- Recommended talking points based on usage data
- A pre-drafted email/message the account owner can personalize and send within 4 hours

Using `loops-transactional`, simultaneously send a "plan pause" offer:
- "Not getting enough value right now? Pause your plan for up to 30 days instead of downgrading. Your data, settings, and team access stay intact."

### 2. Build the downgrade page intercept

This is the critical moment -- the user has clicked "Downgrade" or "Change Plan" in your billing settings. Using `posthog-feature-flags`, gate the downgrade flow to insert an intercept page:

1. When the user lands on the downgrade page, show a personalized retention summary:
   - "Here's what you used this month on your [current plan]:"
   - List their top 3 premium feature usages with specific counts
   - "On [lower plan], you would lose access to: [list of features]"
   - Show a comparison table: current plan vs. target plan, highlighting what disappears
2. Below the summary, present 3 options:
   - "Keep my plan" (primary CTA)
   - "I'd like a discount" -> triggers the retention offer workflow
   - "Continue with downgrade" -> proceeds to standard downgrade flow but logs `downgrade_intercept_bypassed`

Track all interactions via `posthog-custom-events`:
```javascript
posthog.capture('downgrade_intercept_shown', {
  current_plan: 'pro',
  target_plan: 'starter',
  mrr_at_risk: 70,
  premium_features_used: ['advanced_analytics', 'api_access', 'team_roles'],
  premium_feature_count_30d: 47
});

posthog.capture('downgrade_intercept_action', {
  action: 'keep_plan',  // or 'request_discount' or 'continue_downgrade'
  current_plan: 'pro',
  target_plan: 'starter',
  offer_shown: 'none'  // or '20pct_3mo' or 'pause_30d'
});
```

### 3. Build the retention offer fulfillment workflow

Using `n8n-triggers`, create a webhook workflow that fires when a user accepts a retention offer:

1. Receive the offer acceptance event from PostHog or Intercom
2. Apply the offer in your billing system:
   - Discount: apply the coupon code via your billing API (Stripe, Paddle, etc.)
   - Plan pause: set the subscription to pause at end of current billing period
   - Free coaching session: create a Cal.com booking link and email it to the user
3. Update Attio with `attio-deals`: create a "Retention Save" deal with: user, offer type, MRR saved, offer cost
4. Send confirmation via `loops-transactional`: confirm what was applied, when it takes effect, and how to get maximum value during the retention period
5. Log the outcome in PostHog: `retention_offer_fulfilled` with offer details

### 4. Handle offer expiration

For time-limited offers (discounts, pauses), build an n8n workflow that:
- 7 days before expiration: send a reminder email via Loops. "Your [discount/pause] ends on [date]. Here's what to expect."
- Include a usage summary showing engagement during the retention period
- If usage increased during the retention period: "Great news -- you've been using [feature] [X]% more. Looks like your plan is working for you."
- If usage stayed flat: "We noticed you're still not using [feature]. Here's a 5-minute guide to getting started."
- On expiration day: transition back to full price or reactivate the subscription. Log `retention_offer_expired` in PostHog.

### 5. Track intervention effectiveness

Using `posthog-custom-events`, build a complete intervention funnel:

| Event | When |
|-------|------|
| `downgrade_intent_scored` | Daily scoring identifies intent |
| `downgrade_intervention_sent` | In-app message shown or email sent |
| `downgrade_intervention_engaged` | User clicked CTA, opened email, or responded |
| `downgrade_intercept_shown` | User reached downgrade page and saw intercept |
| `downgrade_intercept_action` | User chose keep/discount/continue |
| `retention_offer_shown` | Retention offer presented |
| `retention_offer_accepted` | User accepted the offer |
| `retention_offer_fulfilled` | Offer applied to their account |
| `downgrade_prevented` | User remained on current plan 30 days after intervention |
| `downgrade_completed` | User downgraded despite intervention |

Using `posthog-cohorts`, create a "Saved from Downgrade" cohort: users who were scored high/imminent, received intervention, and remained on their current plan for 30+ days.

## Output

- Tiered in-product intervention messages deployed via Intercom
- Email sequences and transactional emails via Loops matched to intent severity
- Downgrade page intercept with personalized usage summary and retention options
- Retention offer fulfillment workflow in n8n
- Offer expiration handling with follow-up messaging
- Complete PostHog event funnel tracking the full intervention lifecycle

## Triggers

- Moderate interventions: triggered by daily detection workflow when users enter moderate cohort
- High interventions: triggered within 2 hours of entering high cohort
- Imminent interventions: triggered immediately, task created for human outreach
- Downgrade page intercept: triggered in real-time when user visits downgrade page
- Offer expiration: triggered by n8n cron 7 days before and on expiration date
