---
name: proactive-card-expiry-detection
description: Detect cards expiring within 30 days and trigger pre-failure update prompts before payment is attempted
category: Product
tools:
  - Stripe
  - Loops
  - Intercom
  - n8n
  - PostHog
fundamentals:
  - stripe-subscription-status
  - payment-method-update-link
  - loops-transactional
  - intercom-in-app-messages
  - n8n-scheduling
  - posthog-custom-events
---

# Proactive Card Expiry Detection

This drill prevents payment failures before they happen by detecting cards that will expire within 30 days and prompting customers to update their payment method. The cheapest recovery is the one you never need to run.

## Prerequisites

- Stripe API access with permission to list payment methods
- n8n instance for scheduled detection
- Loops for proactive emails
- Intercom for in-app prompts
- PostHog for tracking

## Steps

### 1. Build the daily expiry scan

Using `n8n-scheduling`, create a workflow that runs daily at 06:00 UTC:

Query Stripe for all active subscriptions and their default payment methods. For card payment methods, check the `exp_month` and `exp_year` fields:

```javascript
const subscriptions = await stripe.subscriptions.list({
  status: 'active',
  limit: 100,
  expand: ['data.default_payment_method']
});

const expiringSoon = subscriptions.data.filter(sub => {
  const pm = sub.default_payment_method;
  if (!pm || pm.type !== 'card') return false;
  const expiryDate = new Date(pm.card.exp_year, pm.card.exp_month, 0); // last day of exp month
  const daysUntilExpiry = Math.floor((expiryDate - new Date()) / (1000 * 60 * 60 * 24));
  return daysUntilExpiry > 0 && daysUntilExpiry <= 30;
});
```

Classify by urgency:
- **30-15 days out:** Low urgency. Gentle prompt.
- **14-7 days out:** Medium urgency. Direct ask.
- **6-0 days out:** High urgency. Prominent warning.

### 2. Send proactive update emails

Using `loops-transactional`, send a pre-failure email:

**30-15 days out:**
Subject: "Heads up: your card ending in {{last4}} expires soon"
Body: "Your {{cardBrand}} card ending in {{last4}} expires on {{expDate}}. Update your payment method now to avoid any interruption to your {{productName}} subscription."
CTA: "Update Card" -> {{update_link}}
Tone: casual, informational.

**14-7 days out (if not yet updated):**
Subject: "Your card expires in {{daysLeft}} days — update now"
Body: More direct. Mention the specific renewal date and what happens if the card fails.
CTA: "Update Payment Method" -> {{update_link}}

**6-0 days out (if not yet updated):**
Subject: "Urgent: your card expires {{expDateRelative}}"
Body: Clear consequence: "Your next payment will fail unless you update your card. This could interrupt your access to {{productName}}."
CTA: "Update Now" -> {{update_link}}

Generate a fresh `{{update_link}}` via `payment-method-update-link` at each send.

### 3. Display in-app prompts

Using `intercom-in-app-messages`, display a non-intrusive banner when expiring-card customers log in:

"Your card ending in {{last4}} expires on {{expDate}}. [Update now →]"

Increase prominence as expiry approaches: subtle banner at 30 days, prominent banner at 14 days, modal at 7 days.

### 4. Track outcomes

Using `posthog-custom-events`, log:

```javascript
posthog.capture('card_expiry_warning_sent', {
  customer_id: 'cus_XXXXX',
  days_until_expiry: 21,
  channel: 'email', // or 'in_app'
  urgency_tier: 'low'
});

posthog.capture('card_updated_proactively', {
  customer_id: 'cus_XXXXX',
  days_before_expiry: 18,
  trigger_channel: 'email' // which prompt drove the update
});
```

The key metric is **proactive update rate**: what percentage of customers with expiring cards update before their payment is attempted? Target: 50%+ update rate. Each proactive update is a payment failure that never happens.

### 5. Exclude already-handled customers

Build suppression logic:
- If Stripe's card updater service already refreshed the card (some banks auto-update), skip the customer
- If the customer has already updated their payment method since the last scan, remove them from the sequence
- If the customer is already in an active dunning sequence (payment already failed), do not send expiry warnings — the dunning sequence handles it

## Output

- Daily scan of expiring cards with urgency classification
- 3-tier proactive email sequence (30d, 14d, 7d)
- In-app prompts with escalating prominence
- Proactive update rate tracking in PostHog
- Suppression logic to avoid duplicate communications

## Triggers

- Daily at 06:00 UTC via n8n cron
- Sequence emails at 30d, 14d, 7d before expiry
- In-app prompts on login for customers with expiring cards
