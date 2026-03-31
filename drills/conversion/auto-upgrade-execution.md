---
name: auto-upgrade-execution
description: Automatically upgrade a customer's Stripe subscription when usage crosses a plan threshold, with opt-out window and rollback safety
category: Conversion
tools:
  - Stripe
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - stripe-subscription-management
  - stripe-usage-records
  - billing-event-streaming
  - posthog-custom-events
  - posthog-feature-flags
  - n8n-workflow-basics
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
  - attio-deals
  - attio-custom-attributes
---

# Auto-Upgrade Execution

This drill builds the system that automatically moves a customer to a higher plan when their usage crosses a defined threshold. It is NOT a prompt-and-wait flow. It is an automatic plan change with an opt-out grace period, designed for products with usage-based pricing where exceeding a limit should result in a seamless tier upgrade rather than a degraded experience.

## Input

- Output from `usage-threshold-detection` — accounts classified as critical (95%+) or exceeded (>100%)
- Stripe subscriptions with defined plan tiers and prices
- Plan tier map: which plan each account should upgrade to based on their current plan and usage pattern
- Opt-out window duration (recommended: 72 hours)

## Steps

### 1. Define the auto-upgrade tier map

Create a JSON configuration that maps current plan + exceeded resource to the target upgrade plan:

```json
{
  "auto_upgrade_rules": [
    {
      "current_plan": "free",
      "resource": "api_calls",
      "threshold_pct": 100,
      "target_plan": "starter",
      "target_price_id": "price_starter_monthly",
      "requires_payment_method": true
    },
    {
      "current_plan": "starter",
      "resource": "api_calls",
      "threshold_pct": 100,
      "target_plan": "pro",
      "target_price_id": "price_pro_monthly",
      "requires_payment_method": false
    },
    {
      "current_plan": "starter",
      "resource": "seats",
      "threshold_pct": 100,
      "target_plan": "pro",
      "target_price_id": "price_pro_monthly",
      "requires_payment_method": false
    }
  ]
}
```

Store this config in n8n as a static data node or an environment variable. Update it whenever pricing tiers change.

### 2. Build the opt-out grace period flow

When `usage-threshold-detection` flags an account as exceeded, do NOT upgrade immediately. Start a 72-hour grace period:

Using `n8n-workflow-basics`, build a workflow triggered by the exceeded webhook:

1. Look up the auto-upgrade rule for this account's current plan + resource
2. If no rule exists (e.g., the account is already on the highest plan), skip — route to sales via `attio-deals` for a custom plan conversation
3. If the account has no payment method on file (`requires_payment_method: true`), skip the auto-upgrade — instead trigger `usage-alert-delivery` to prompt payment method collection
4. Create a pending upgrade record in Attio using `attio-custom-attributes`:
   - `auto_upgrade_status`: pending
   - `auto_upgrade_target_plan`: pro
   - `auto_upgrade_grace_end`: timestamp 72 hours from now
   - `auto_upgrade_resource`: api_calls
5. Notify the user via both channels:

Using `intercom-in-app-messages`, show a persistent banner:
"You've exceeded your {{resource_name}} limit on the {{current_plan}} plan. We'll automatically upgrade you to {{target_plan}} in 72 hours to keep your service running. [View upgrade details] [Opt out]"

Using `loops-transactional`, send an email:
Subject: "Your {{product_name}} plan is upgrading in 72 hours"
Body: Explain what changed (usage exceeded limit), what will happen (auto-upgrade to next tier), what it costs (price difference), how to opt out (link to cancel auto-upgrade), and what happens if they opt out (service degradation or hard limit).

6. Log in PostHog using `posthog-custom-events`:

```javascript
posthog.capture('auto_upgrade_grace_started', {
  account_id: accountId,
  current_plan: 'starter',
  target_plan: 'pro',
  resource: 'api_calls',
  pct_consumed: 105,
  grace_end: graceEndTimestamp
});
```

### 3. Handle opt-out

Using `n8n-triggers`, create a webhook endpoint that the opt-out button calls:

1. Set `auto_upgrade_status` to `opted_out` in Attio
2. Apply the hard limit or degraded experience for the exceeded resource (the product enforces the limit instead of upgrading)
3. Log `auto_upgrade_opted_out` in PostHog with the account context
4. Send a confirmation email via `loops-transactional`: "You've opted out of the automatic upgrade. Your {{resource_name}} is now limited to {{plan_limit}}. You can upgrade anytime from your billing settings."
5. Do NOT re-trigger auto-upgrade for this account+resource for 30 days (cooldown)

### 4. Execute the auto-upgrade

Using `n8n-workflow-basics`, build a scheduled workflow that runs every hour and checks for pending upgrades whose grace period has expired:

1. Query Attio for accounts where `auto_upgrade_status` = pending AND `auto_upgrade_grace_end` < now
2. For each account, execute the Stripe subscription change using `stripe-subscription-management`:

```bash
# Retrieve current subscription
curl "https://api.stripe.com/v1/subscriptions?customer=cus_xxx&status=active" \
  -u "$STRIPE_SECRET_KEY:"

# Update to the new plan
curl https://api.stripe.com/v1/subscriptions/sub_xxx \
  -u "$STRIPE_SECRET_KEY:" \
  -d "items[0][id]=si_xxx" \
  -d "items[0][price]=price_pro_monthly" \
  -d "proration_behavior=create_prorations" \
  -d "metadata[auto_upgrade]=true" \
  -d "metadata[upgrade_resource]=api_calls" \
  -d "metadata[previous_plan]=starter"
```

3. Verify the subscription status is `active` after the update. If the payment fails (card declined), set `auto_upgrade_status` to `payment_failed` and trigger `usage-alert-delivery` to prompt payment method update.

4. Update Attio: set `auto_upgrade_status` to `completed`, record `auto_upgrade_completed_at` timestamp.

5. Notify the user:

Using `intercom-in-app-messages`, show a confirmation: "You've been upgraded to {{target_plan}}. Your new {{resource_name}} limit is {{new_limit}}. [View your updated plan]"

Using `loops-transactional`, send confirmation email with: new plan details, new limits, next billing date, prorated charge amount, link to billing settings.

6. Log in PostHog:

```javascript
posthog.capture('auto_upgrade_completed', {
  account_id: accountId,
  previous_plan: 'starter',
  new_plan: 'pro',
  resource: 'api_calls',
  mrr_increase: 30,
  proration_amount: 15.50,
  grace_period_hours: 72,
  opted_out: false
});
```

### 5. Stream billing changes to PostHog

Using `billing-event-streaming`, ensure the Stripe subscription update event flows into PostHog. This enables downstream analysis: correlating auto-upgrades with retention, ARPU changes, and usage patterns post-upgrade.

### 6. Build the rollback mechanism

If the customer contacts support within 48 hours of an auto-upgrade requesting a revert:

1. Using `stripe-subscription-management`, revert the subscription to the previous plan
2. Issue a credit for the prorated charge
3. Apply the hard limit for the exceeded resource
4. Set `auto_upgrade_status` to `rolled_back` in Attio
5. Log `auto_upgrade_rolled_back` in PostHog
6. Add a 60-day cooldown: do not auto-upgrade this account for any resource for 60 days

### 7. Track auto-upgrade funnel

The complete funnel for measurement:

```
usage_threshold_detected (critical/exceeded)
  -> auto_upgrade_grace_started
    -> auto_upgrade_opted_out OR auto_upgrade_completed
      -> (if completed) auto_upgrade_rolled_back OR auto_upgrade_retained_30d
```

Key metrics:
- **Acceptance rate**: completed / (completed + opted_out). Target: 50%+.
- **Retention rate**: accounts still on the upgraded plan 30 days later. Target: 80%+.
- **Rollback rate**: rolled_back / completed. Target: below 10%.
- **ARPU lift**: average MRR increase from auto-upgrades.
- **Payment failure rate**: payment_failed / attempted. Target: below 5%.

## Output

- n8n workflow that manages the grace period, opt-out, and execution of auto-upgrades
- Intercom in-app messages for grace notification and upgrade confirmation
- Loops emails for grace notification, opt-out confirmation, and upgrade confirmation
- Attio records tracking auto-upgrade status per account
- PostHog events covering the full auto-upgrade funnel
- Rollback mechanism with support for within-48-hours reversals

## Triggers

Fires when `usage-threshold-detection` classifies an account as exceeded (>100% consumed). Grace period check runs hourly via n8n cron. Opt-out webhook fires on user action. Rollback fires on support request.
