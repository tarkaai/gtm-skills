---
name: pricing-experiment-runner
description: Run controlled pricing experiments using Stripe price objects, PostHog feature flags, and cohort-based rollout
category: Product
tools:
  - PostHog
  - Stripe
  - n8n
  - Intercom
fundamentals:
  - posthog-feature-flags
  - posthog-experiments
  - posthog-custom-events
  - stripe-pricing-tables
  - stripe-subscription-management
  - intercom-in-app-messages
  - n8n-workflow-basics
---

# Pricing Experiment Runner

This drill manages the lifecycle of a pricing experiment: creating the variant price in Stripe, assigning users via PostHog feature flags, monitoring billing and behavior data, and making the adopt/revert decision.

Pricing experiments are higher-risk than UI experiments. A bad pricing change directly impacts revenue and customer trust. This drill includes guardrails that standard A/B tests do not need.

## Prerequisites

- `usage-pricing-model-analysis` drill completed with a recommended pricing model
- PostHog feature flags enabled in your product
- Stripe configured with current prices and subscriptions
- At least 200 active paying customers (fewer makes statistical significance unreachable in reasonable time)

## Steps

### 1. Define the experiment hypothesis

Structure: "If we change from [current pricing] to [new pricing], then [primary metric] will [improve/maintain] by [amount] because [reasoning], and [guardrail metric] will not degrade by more than [limit]."

Example: "If we change from flat $49/mo to $29/mo base + $0.005/API call overage above 5,000, then net revenue retention will increase by 5pp because low-usage churners will pay less and stay, and gross revenue will not decrease by more than 10%."

### 2. Create the variant price in Stripe

Using `stripe-pricing-tables`, create new Price objects that represent the experiment variant. Do NOT modify existing prices — create new ones:

```bash
# Create the base component of hybrid pricing
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "unit_amount=2900" \
  -d "currency=usd" \
  -d "recurring[interval]=month" \
  -d "metadata[experiment]=pricing_v2" \
  -d "metadata[variant]=treatment"

# Create the usage overage component
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_xxx" \
  -d "currency=usd" \
  -d "recurring[interval]=month" \
  -d "recurring[usage_type]=metered" \
  -d "billing_scheme=tiered" \
  -d "tiers_mode=graduated" \
  -d "tiers[0][up_to]=5000" \
  -d "tiers[0][unit_amount]=0" \
  -d "tiers[1][up_to]=inf" \
  -d "tiers[1][unit_amount]=1" \
  -d "meter=mtr_xxx" \
  -d "metadata[experiment]=pricing_v2" \
  -d "metadata[variant]=treatment"
```

Tag all experiment prices with metadata so they can be identified and cleaned up later.

### 3. Set up the PostHog feature flag

Using `posthog-feature-flags`, create a flag `pricing-experiment-v2` with:

- **Rollout:** 50% control / 50% treatment
- **Targeting:** Only active paying customers on the plan being tested. Exclude: enterprise contracts, customers with custom pricing, accounts less than 30 days old.
- **Stickiness:** User-level (once assigned, a user stays in their group for the full experiment)

### 4. Build the subscription migration workflow

Using `n8n-workflow-basics`, create an n8n workflow triggered by the PostHog feature flag assignment:

1. When a user is assigned to the treatment group, check their current Stripe subscription
2. Using `stripe-subscription-management`, swap their subscription items from the control price to the treatment prices
3. Set `proration_behavior=none` — the new pricing takes effect at the next billing cycle (never mid-cycle for pricing experiments)
4. Log the migration in PostHog: `pricing_experiment_enrolled` with properties `variant`, `previous_price`, `new_price`, `enrollment_date`
5. Send an Intercom in-app message using `intercom-in-app-messages` explaining the pricing change: "We're updating your billing to better match your usage. Here's what's changing..."

**Human action required:** Review the in-app message copy before the experiment launches. Pricing changes require clear, honest communication.

### 5. Define success and guardrail metrics

Track in PostHog using `posthog-custom-events`:

**Primary metrics (must improve):**
- Net revenue retention (NRR): `(MRR at end + expansion - contraction - churn) / MRR at start`
- 30-day churn rate: percentage of treatment users who cancel within 30 days of enrollment

**Secondary metrics (must not degrade):**
- Gross revenue per user: total revenue / users in group
- Support ticket volume mentioning pricing
- NPS score for treatment group vs. control

**Guardrail metrics (auto-revert if breached):**
- Churn rate in treatment group exceeds control by >50% at any weekly check
- Gross revenue in treatment group drops >15% vs. control
- More than 10 support tickets in 7 days specifically about the pricing change

### 6. Monitor the experiment

Build an n8n workflow that runs weekly:

1. Query PostHog for all experiment metrics, segmented by control vs. treatment
2. Check guardrails — if any are breached, trigger auto-revert (Step 7)
3. Check if sample size has reached statistical significance (use PostHog experiments API)
4. Generate a weekly experiment status report: metrics by group, confidence interval, estimated time to significance
5. Post report to Slack and store in Attio

Minimum experiment duration: 2 full billing cycles (60 days for monthly billing). Pricing experiments need more time than UI tests because the impact takes a billing cycle to materialize.

### 7. Auto-revert mechanism

If a guardrail is breached:

1. Disable the PostHog feature flag (stops new enrollments)
2. For all treatment users, revert their Stripe subscriptions back to control prices using `stripe-subscription-management`
3. Send an Intercom message: "We've reverted a recent billing change on your account. No action is needed."
4. Log `pricing_experiment_reverted` event in PostHog with properties: `reason`, `revert_date`, `users_affected`
5. Archive the experiment with full data in Attio

### 8. Make the decision

When the experiment reaches significance:

- **Adopt:** Migrate all remaining control users to the new pricing. Archive old prices in Stripe (set `active=false`). Update the pricing page.
- **Iterate:** If results are directionally positive but not significant, extend the experiment or design a new variant based on learnings.
- **Revert:** If treatment performed worse, revert all treatment users and document why the hypothesis was wrong.

## Output

- A controlled pricing experiment with proper statistical rigor
- Automated weekly monitoring with guardrail-triggered auto-revert
- A final decision (adopt/iterate/revert) backed by data
- Full audit trail of every pricing change per user

## Triggers

Run once per experiment cycle. Maximum 1 active pricing experiment at a time. Minimum 30 days between experiments on the same plan.
