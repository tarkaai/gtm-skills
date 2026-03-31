---
name: dunning-sequence-automation
description: Automated multi-channel dunning sequence that escalates from in-app to email to human outreach based on failure type and recovery stage
category: Revenue Ops
tools:
  - Loops
  - Intercom
  - Stripe
  - n8n
  - Attio
fundamentals:
  - payment-method-update-link
  - loops-transactional
  - loops-sequences
  - intercom-in-app-messages
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-contacts
  - attio-notes
---

# Dunning Sequence Automation

This drill builds the multi-channel recovery sequence that activates when a payment fails. It coordinates in-app messages, emails, and human outreach in a time-boxed escalation ladder. The goal is to recover the payment before the subscription cancels, with minimum friction for the customer.

## Prerequisites

- Payment failure detection running (`payment-failure-detection` drill)
- Stripe Customer Portal configured for payment method updates
- Loops configured for transactional and sequence emails
- Intercom configured for in-app messaging
- n8n instance for orchestration

## Steps

### 1. Generate one-click recovery links

Use the `payment-method-update-link` fundamental to generate a Stripe Billing Portal session URL for each customer with a failed payment. This link lets them update their card without logging in.

**Critical:** Generate links at send-time, not in advance. Portal sessions expire in 24 hours. Build the link generation into each step of the dunning sequence, not as a batch pre-step.

### 2. Build the in-app recovery banner (Day 0 — immediate)

Using `intercom-in-app-messages`, create a persistent banner that appears the moment the customer next logs in:

**For expired_card failures:**
Message: "Your card ending in {{last4}} has expired. Update your payment method to keep your account active."
CTA: "Update Card" -> {{update_link}}

**For insufficient_funds or generic declines:**
Message: "We could not process your latest payment. Please update your payment method to avoid service interruption."
CTA: "Update Payment" -> {{update_link}}

**For authentication_required:**
Message: "Your bank requires additional verification for your payment. Complete verification to keep your account active."
CTA: "Verify Payment" -> {{auth_link}}

Display rules: show on every page load until the invoice is paid. Dismiss temporarily (24h) on close, but re-display if still unpaid.

### 3. Build the email dunning sequence

Using `loops-sequences`, create a 4-email recovery sequence triggered by the `payment_failure_detected` event:

**Email 1 — Day 0 (immediate after first failure):**
Subject: "Action needed: update your payment method"
Body: Explain the failure in plain language (do not use technical jargon like "card_declined"). Include the one-click update link. Mention what happens if not resolved (service interruption in X days). Do not threaten — be helpful.
Generate a fresh `{{update_link}}` via `payment-method-update-link` at send time.

**Email 2 — Day 3 (after first retry fails):**
Subject: "Your {{productName}} account needs attention"
Body: Remind them of the failed payment. If the failure was `expired_card`, explicitly say "Your card ending in {{last4}} expired on {{exp_date}}." Include the update link. Mention the specific date their access will be affected.

**Email 3 — Day 7 (escalation):**
Subject: "We want to help you stay on {{productName}}"
Body: More personal tone. Acknowledge this might be an oversight. Offer two options: (1) update payment method via the link, (2) reply to this email for help. For high-MRR accounts, this email should come from the account owner's name and reply-to.

**Email 4 — Day 12 (final notice):**
Subject: "Last chance to keep your {{productName}} account active"
Body: Clear deadline: "Your account will be downgraded/suspended on {{deadline_date}} unless payment is resolved." Include the update link. Offer to pause instead of cancel. Include a direct calendar link to talk to support.

Using `loops-transactional` for each email, pass dynamic variables: `firstName`, `last4`, `planName`, `amountDue`, `update_link`, `deadline_date`.

### 4. Build human outreach for high-value accounts

For accounts with MRR > $500 or recovery_priority > 80:

Using `attio-contacts`, create a task for the account owner on Day 1:
- Title: "Payment failed — {{company_name}} — ${{mrr}}/mo at risk"
- Description: failure code, attempt count, card details, recovery priority score
- Deadline: 48 hours

Using `attio-notes`, log a note on the account with the full failure context so the account owner can make a personal call or send a customized email.

**Human action required:** Account owner reaches out within 48 hours for high-value accounts. The system prepares the context; the human delivers the personal touch.

### 5. Build the sequence orchestrator in n8n

Using `n8n-workflow-basics` and `n8n-scheduling`, build a workflow that:

1. Receives payment failure events from the detection drill
2. Checks if a dunning sequence is already active for this customer (prevent duplicate sequences)
3. Triggers the in-app banner immediately via Intercom
4. Enrolls the customer in the Loops email sequence
5. If high-value: creates the Attio task for human outreach
6. Monitors daily: if the invoice is paid at any point, immediately:
   - Cancel the remaining email sequence in Loops
   - Remove the in-app banner in Intercom
   - Fire a `payment_failure_recovered` event in PostHog
   - Update Attio record to `recovered`
   - Send a "Thank you — you're all set" confirmation email

### 6. Handle edge cases

- **Customer contacts support during dunning:** If Intercom detects a conversation from a dunning customer, pause the email sequence for 72 hours. Let the support interaction resolve first.
- **Multiple simultaneous failures:** If a customer has 2+ failed invoices, consolidate into a single dunning sequence. The update link resolves all open invoices at once.
- **Customer on annual plan:** Increase urgency and escalation speed. Annual failures are higher-value; compress the sequence to Day 0, Day 1, Day 3, Day 5.
- **Previously recovered customers:** If a customer has been through dunning before, skip Email 1 and start with Email 2 (they know the process).

## Output

- In-app recovery banner displayed immediately on next login
- 4-email dunning sequence with escalating urgency
- Human outreach tasks for high-value accounts
- Automatic sequence cancellation on recovery
- Edge case handling for support interactions, multiple failures, and repeat offenders

## Triggers

- Starts: when `payment-failure-detection` drill routes a new failure
- Stops: when the invoice is paid OR the subscription is canceled
- Cadence: Day 0, Day 3, Day 7, Day 12
