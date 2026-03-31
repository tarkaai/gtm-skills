---
name: multiyear-commitment-smoke
description: >
  Multi-Year Deal Incentives — Smoke Test. Manually identify 10-20 commitment-ready accounts,
  build one annual price in Stripe, deliver a single offer via email, and measure whether
  any convert. Validates that customers will trade upfront payment for a discount.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥2 of 20 accounts convert to annual commitment"
kpis: ["Offer-to-conversion rate", "Average discount accepted", "ARR locked"]
slug: "multiyear-commitment"
install: "npx gtm-skills add product/upsell/multiyear-commitment"
drills:
  - lead-capture-surface-setup
---

# Multi-Year Deal Incentives — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Prove that existing monthly customers will switch to annual billing when offered a meaningful discount. The test is binary: do any of the 20 targeted accounts convert? If yes, the commitment motion has signal and deserves automation.

## Leading Indicators

- Email open rate on the offer email (target: >40% — these are existing customers, not cold)
- Click rate on the upgrade link (target: >15%)
- Stripe Checkout session started (any non-zero count confirms intent)
- Accounts that reply asking questions about the offer (signal even if they do not convert)

## Instructions

### 1. Build the offer capture surface

Run the `lead-capture-surface-setup` drill to create a single landing page (or billing page section) with an annual plan CTA. The surface is a Stripe Checkout embed or link that converts a monthly subscriber to an annual price.

Configure:
- Surface type: Stripe Checkout link (self-serve)
- CTA: "Switch to annual — save [X]%"
- PostHog events: `cta_impression`, `cta_clicked`, `lead_captured` (maps to `multiyear_offer_clicked`, `multiyear_offer_started`, `multiyear_offer_converted`)
- Route conversion webhook to Attio to create an expansion deal

### 2. Build the first annual offer

Run the the multiyear offer engine workflow (see instructions below) drill — but only Steps 1 and 2 (readiness scoring and Stripe price creation). Skip the automation workflows for this level. Execute manually:

1. Query PostHog for accounts with tenure > 6 months, no churn risk signals, and positive usage trend. Select 20 accounts manually.
2. Create ONE annual price in Stripe: 2 months free (17% discount). Tag with `metadata[commitment_type]=annual` and `metadata[experiment]=smoke_v1`.
3. Generate a Stripe Checkout link for each of the 20 accounts using their existing customer ID.

### 3. Send the offer via email

**Human action required:** Compose and send a personal email to the billing contact at each of the 20 accounts. Use Loops or your personal email. Do not use a mass email tool — this is a personal outreach test.

Email structure:
- Subject: "Save $[amount] — switch to annual billing"
- Body paragraph 1: "You have been using [product] for [X months]. Your team has [usage stat, e.g., 'created 340 projects']."
- Body paragraph 2: "We are offering annual billing at [discount]. Instead of $[monthly x 12], you would pay $[annual price] — saving $[amount]."
- Body paragraph 3: "Switch here: [Stripe Checkout link]. Takes 30 seconds."
- Sign-off: from the founder or account owner, not a marketing address

### 4. Track responses and conversions

Log every response manually in Attio:
- Email opened (if tracking available)
- Link clicked (Stripe Checkout session created)
- Converted (subscription updated to annual)
- Replied with questions (capture the question — this is research data)
- No response after 5 days

After 7 days, compute:
- Conversion rate: accounts converted / 20
- Revenue locked: sum of annual commitments
- Average discount given

### 5. Evaluate against threshold

Pass threshold: **2 or more of 20 accounts convert to annual billing** (10% rate).

If PASS: The commitment motion works. Proceed to Baseline to automate scoring and delivery.

If FAIL: Analyze the non-converters. Did they open the email? Did they click? Did they start checkout but not complete? The drop-off point determines the fix:
- Low open rate → subject line or sender trust issue
- Opens but no clicks → offer is not compelling enough (test higher discount)
- Clicks but no conversion → checkout friction or price anxiety (test with a money-back guarantee)

Iterate and re-run before moving to Baseline.

## Time Estimate

- 1 hour: query PostHog, select 20 accounts, review their health
- 1 hour: create annual price in Stripe, generate checkout links
- 1 hour: set up the landing page/checkout surface with tracking
- 2 hours: write and send 20 personalized emails
- 1 hour: log responses, compute results, document learnings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Account usage data + event tracking | Free tier covers this volume |
| Stripe | Annual price + Checkout sessions | 2.9% + $0.30 per transaction (standard Stripe fees) |
| Loops | Email delivery (or use personal email) | Free tier covers 20 emails |
| Attio | Deal tracking + response logging | Included in existing CRM subscription |

## Drills Referenced

- `lead-capture-surface-setup` — builds the Stripe Checkout surface with PostHog tracking and Attio routing
- the multiyear offer engine workflow (see instructions below) — Steps 1-2 only: readiness signal identification and Stripe price creation
