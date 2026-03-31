---
name: payment-failure-detection
description: Detect payment failures from billing system webhooks, classify failure types, and score recovery likelihood per account
category: Product
tools:
  - Stripe
  - PostHog
  - n8n
  - Attio
fundamentals:
  - stripe-payment-failure-webhook
  - stripe-subscription-status
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
  - attio-custom-attributes
  - attio-contacts
---

# Payment Failure Detection

This drill builds the detection layer for involuntary churn from failed payments. It listens for payment failure webhooks, classifies the failure type, scores recovery likelihood, and routes the data to PostHog and Attio for downstream intervention.

## Prerequisites

- Stripe (or equivalent billing platform) with webhook access
- n8n instance for webhook processing
- PostHog for event tracking and cohort analysis
- Attio for CRM enrichment and team visibility
- At least 10 past payment failures to calibrate classification

## Steps

### 1. Set up the payment failure webhook listener

Use the `stripe-payment-failure-webhook` fundamental to configure Stripe webhooks for `invoice.payment_failed`, `charge.failed`, and `payment_intent.payment_failed` events. Point them at an n8n webhook node.

Using `n8n-triggers`, create a webhook node that receives Stripe events. Verify the webhook signature using the Stripe signing secret. Reject unverified payloads with HTTP 400.

### 2. Classify the failure type

When a payment failure event arrives, classify it by recovery likelihood:

| Failure Code | Classification | Recovery Likelihood | Recommended Action |
|-------------|---------------|--------------------|--------------------|
| `expired_card` | Card expired | High (85%) | Send update link immediately |
| `insufficient_funds` | Temporary | Medium (60%) | Wait for retry, then nudge |
| `authentication_required` | SCA needed | High (75%) | Send authentication link |
| `card_declined` (generic) | Unknown | Medium (50%) | Send update link after 1st retry fails |
| `processing_error` | Transient | Very High (90%) | Wait for automatic retry |
| `do_not_honor` | Bank block | Low (30%) | Send update link, suggest different card |
| `fraudulent` | Fraud flag | Very Low (10%) | Do not retry, require new method |

Using `n8n-workflow-basics`, build a switch node that routes each failure to the appropriate classification.

### 3. Enrich with account context

Use the `stripe-subscription-status` fundamental to pull the subscription details: plan, MRR, subscription age, retry attempt count, and next retry date.

Use `attio-contacts` to pull account context: company name, account owner, lifecycle stage, total lifetime value.

Compute a recovery priority score:

```
recovery_priority = (MRR_weight * normalized_MRR) +
                    (likelihood_weight * recovery_likelihood) +
                    (tenure_weight * normalized_tenure)
```

Where:
- MRR_weight = 0.4 (higher-value accounts get priority)
- likelihood_weight = 0.35 (higher-likelihood failures get faster action)
- tenure_weight = 0.25 (longer-tenured customers get more effort)

### 4. Log events to PostHog

Use `posthog-custom-events` to fire a `payment_failure_detected` event per failure:

```javascript
posthog.capture('payment_failure_detected', {
  customer_id: 'cus_XXXXX',
  failure_code: 'expired_card',
  failure_classification: 'card_expired',
  recovery_likelihood: 0.85,
  recovery_priority: 78,
  attempt_count: 1,
  amount_due: 4900,
  currency: 'usd',
  subscription_age_days: 365,
  mrr: 49,
  next_retry_at: '2024-01-15T10:00:00Z'
});
```

Create PostHog cohorts:
- "Payment Failed — Active Recovery" (failures in last 14 days, not yet resolved)
- "Payment Failed — High Priority" (recovery_priority > 70)
- "Payment Failed — Expired Card" (failure_classification = card_expired)

### 5. Enrich CRM records

Use `attio-custom-attributes` to update the account in Attio:

- `payment_status`: `healthy` | `failed` | `recovering` | `recovered` | `churned`
- `payment_failure_code`: the specific failure reason
- `payment_recovery_priority`: 0-100 score
- `payment_failure_date`: timestamp of first failure
- `payment_retry_count`: number of retry attempts so far
- `payment_amount_at_risk`: the unpaid invoice amount

For high-priority failures (recovery_priority > 80), use `attio-contacts` to create a task for the account owner with a 24-hour deadline.

### 6. Track resolution

Build a follow-up n8n workflow that checks open invoices daily using `stripe-subscription-status`:
- If invoice status changes to `paid`, fire `payment_failure_recovered` event in PostHog and update Attio to `recovered`
- If subscription status changes to `canceled`, fire `payment_failure_churned` event and update Attio to `churned`
- If still open after 14 days with no recovery, escalate priority

## Output

- Real-time payment failure detection via Stripe webhooks
- Classified failure types with recovery likelihood scores
- PostHog events and cohorts for all payment failures
- Attio records enriched with payment status and recovery priority
- Resolution tracking that catches recoveries and churns

## Triggers

- Real-time: fires on every Stripe `invoice.payment_failed` webhook
- Daily: resolution tracking workflow checks all open failures
- Weekly: calibrate recovery likelihood percentages against actual outcomes
