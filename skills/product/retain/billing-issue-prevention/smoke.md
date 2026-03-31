---
name: billing-issue-prevention-smoke
description: >
  Payment Failure Recovery — Smoke Test. Manually detect failed payments from Stripe, classify
  failure types, send one-click recovery links, and validate that at least 60% of customers
  recover within 7 days.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥60% recovery rate from manually identified failures"
kpis: ["Recovery rate", "Involuntary churn count", "Time to recovery (median days)"]
slug: "billing-issue-prevention"
install: "npx gtm-skills add product/retain/billing-issue-prevention"
drills:
  - threshold-engine
---

# Payment Failure Recovery — Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove the concept: can you detect failed payments, classify the failure reason, send a one-click recovery link, and get customers to update their payment method? No automation, no always-on. Run one manual cycle against your current batch of failed payments and measure how many recover. The pass threshold is that 60%+ of contacted customers recover their payment within 7 days.

## Leading Indicators

- Stripe API returns usable failure metadata (failure codes, attempt counts, card details) for 90%+ of failures
- Recovery links generated via Stripe Billing Portal are functional and load correctly
- At least 3 out of the first 5 contacted customers open the recovery email within 48 hours
- At least 1 customer successfully updates their payment method within 24 hours of receiving the link

## Instructions

### 1. Pull your current failed payments from Stripe

Query the Stripe API for all currently past-due subscriptions and open invoices. The the payment failure detection workflow (see instructions below) drill walks you through this in detail, but for the Smoke test, run it manually:

```bash
curl "https://api.stripe.com/v1/subscriptions?status=past_due&limit=100&expand[]=data.latest_invoice&expand[]=data.default_payment_method" \
  -u sk_live_YOUR_KEY:
```

For each past-due subscription, extract: customer ID, failure code, card last 4, card expiry, amount due, attempt count, subscription start date.

**Human action required:** Review the list. Remove any test accounts, internal users, or accounts already in communication with your team. You want a clean sample of 10-50 real failed payments.

### 2. Classify each failure

Using the classification table from the the payment failure detection workflow (see instructions below) drill, categorize each failure:

| Failure Code | Action |
|-------------|--------|
| `expired_card` | Send update link — high likelihood of recovery |
| `insufficient_funds` | Send update link — suggest trying a different card |
| `authentication_required` | Send authentication link |
| `card_declined` (generic) | Send update link |
| `processing_error` | Wait for automatic retry — do not contact yet |
| `fraudulent` | Skip — do not contact |

Remove `processing_error` and `fraudulent` from your outreach list. The rest are your recovery targets.

### 3. Generate recovery links and send emails

For each recovery target, generate a Stripe Billing Portal session link:

```bash
curl https://api.stripe.com/v1/billing_portal/sessions \
  -u sk_live_YOUR_KEY: \
  -d customer="cus_XXXXX" \
  -d return_url="https://app.yourproduct.com/billing?recovered=true"
```

Send a manual email to each customer. Subject: "Action needed: update your payment method." Body: explain the failure in plain language, include the one-click update link, mention what happens if not resolved (service interruption). Be helpful, not threatening.

**Human action required:** Send the emails manually via your email client or Loops. This is a Smoke test — no automation yet. Personalize each email with the specific failure reason and card details.

### 4. Track responses for 7 days

Monitor daily: check which invoices moved from `open` to `paid` in Stripe. For each recovery, note:
- Days from email to recovery
- Which failure type recovered
- Whether the customer replied, clicked the link, or updated independently

Log all outcomes in a spreadsheet or PostHog. At the end of 7 days, compute:
- Recovery rate = recovered / total contacted
- Median time to recovery = median days from email to payment
- Involuntary churn = customers whose subscriptions canceled during this period

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did 60%+ of contacted customers recover their payment within 7 days?

If PASS, proceed to Baseline. The manual approach works; now automate it.

If FAIL, diagnose:
- Did customers open the emails? (If not: subject line or deliverability problem)
- Did customers click the link? (If not: email copy or trust problem)
- Did customers complete the update? (If not: Stripe Portal UX problem)
- Were most failures unrecoverable types? (If so: focus on proactive card expiry detection instead)

## Time Estimate

- 1 hour: query Stripe, extract failed payments, classify failures
- 1 hour: generate recovery links, draft and send emails
- 0.5 hours/day for 7 days: monitor recoveries and log outcomes (3.5 hours total, but only ~30 min of active work per day)
- 0.5 hours: compute results and evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stripe | Payment failure data, retry schedule, billing portal links | 2.9% + $0.30 per transaction (no additional cost for API access) — [stripe.com/pricing](https://stripe.com/pricing) |
| PostHog | Event logging for recovery tracking (optional at Smoke) | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost: Free** (Stripe API access is included in your Stripe account; PostHog free tier is sufficient)

## Drills Referenced

- the payment failure detection workflow (see instructions below) — extracts payment failures from Stripe, classifies by type, and scores recovery likelihood
- `threshold-engine` — evaluates whether recovery rate meets the 60% pass threshold
