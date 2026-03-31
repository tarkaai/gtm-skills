---
name: billing-issue-prevention-baseline
description: >
  Payment Failure Recovery — Baseline Run. Automated payment failure detection, multi-channel
  dunning sequences, and proactive card expiry alerts running always-on. First sustained
  measurement of recovery rate at ≥70%.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥70% recovery rate sustained over 2 weeks with automated dunning"
kpis: ["Recovery rate", "Involuntary churn rate", "Median time to recovery", "Dunning email open rate"]
slug: "billing-issue-prevention"
install: "npx gtm-skills add product/retain/billing-issue-prevention"
drills:
  - payment-failure-detection
  - dunning-sequence-automation
  - proactive-card-expiry-detection
  - payment-recovery-health-monitor
---

# Payment Failure Recovery — Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The first always-on automation. Payment failures are detected in real time via Stripe webhooks. A multi-channel dunning sequence fires automatically: in-app banner on next login, 4-email escalation ladder over 12 days, human routing for high-value accounts. Proactive card expiry detection prevents failures before they happen. A health dashboard tracks recovery rates, failure types, and dunning effectiveness. The pass threshold is 70%+ recovery rate sustained over 2 weeks.

## Leading Indicators

- Stripe webhook is receiving and processing 100% of `invoice.payment_failed` events within 5 seconds
- In-app recovery banners display correctly for 95%+ of dunning customers on their next login
- Dunning email sequence fires within 1 minute of failure detection (no delays or dropped events)
- Proactive card expiry scan identifies all cards expiring within 30 days (compare against Stripe's own expiry data)
- At least 30% of customers with expiring cards update proactively before any payment failure

## Instructions

### 1. Deploy real-time payment failure detection

Run the `payment-failure-detection` drill in production. This sets up:

- Stripe webhook listener in n8n for `invoice.payment_failed` events
- Failure classification (expired card, insufficient funds, auth required, etc.)
- Recovery likelihood scoring per failure
- Account enrichment from Attio (MRR, account owner, tenure)
- PostHog event logging: `payment_failure_detected` with all metadata
- PostHog cohorts: "Active Recovery," "High Priority," "Expired Card"
- Attio record updates: payment status, failure code, recovery priority

Verify the pipeline end-to-end: create a test subscription in Stripe test mode, trigger a payment failure, and confirm the event flows through n8n -> PostHog -> Attio within 60 seconds.

### 2. Deploy the automated dunning sequence

Run the `dunning-sequence-automation` drill. This builds:

- Immediate in-app recovery banner via Intercom (shows on next login with one-click update link)
- 4-email dunning sequence via Loops (Day 0, Day 3, Day 7, Day 12) with escalating urgency
- Human outreach tasks in Attio for accounts with MRR > $500
- Automatic sequence cancellation when the invoice is paid
- Edge case handling: support conversation pauses dunning, multiple failures consolidated, annual plan acceleration

Generate Stripe Billing Portal links at send time (not in advance) using the `payment-method-update-link` fundamental. Verify links work: click one in test mode and confirm it loads the payment update form.

**Human action required:** Review all email templates before launching. Ensure the copy is helpful (not threatening), the failure explanation is in plain language (not "code: card_declined"), and the update link is prominent. Test the full sequence on yourself with a test account.

### 3. Deploy proactive card expiry detection

Run the `proactive-card-expiry-detection` drill. This builds:

- Daily scan of all active subscriptions for cards expiring within 30 days
- 3-tier proactive email sequence: gentle at 30 days, direct at 14 days, urgent at 7 days
- In-app prompts with escalating prominence for customers with expiring cards
- Suppression logic: skip cards already updated, skip customers already in dunning

This is the prevention layer. Every card that updates proactively is a payment failure that never happens.

### 4. Build the health dashboard

Run the `payment-recovery-health-monitor` drill to create:

- PostHog recovery funnel: failure -> email sent -> email opened -> link clicked -> recovered
- Payment health dashboard with 6 panels: failure rate trend, recovery rate by type, time to recovery, dunning step effectiveness, involuntary churn rate, revenue at risk vs. recovered
- Threshold alerts: failure rate spikes, recovery rate drops, high-value account failures
- Weekly health report posted to Slack

### 5. Run for 2 weeks and evaluate

Let the system run for 2 full weeks. During this time:
- Monitor the health dashboard daily for the first 3 days (ensure no pipeline errors)
- Review the first weekly health report
- Check that in-app banners, emails, and human routing are all functioning
- Address any delivery issues (emails going to spam, webhook failures, broken links)

At the end of 2 weeks, evaluate against the threshold: ≥70% recovery rate.

If PASS, proceed to Scalable. If FAIL, diagnose using the recovery funnel — find the biggest drop-off point and fix it:
- Low email open rates -> test subject lines at Scalable level
- Low link click rates -> test email copy and link placement
- Low update completion -> check Stripe Portal UX, consider embedding update form in-app
- Low recovery for specific failure types -> adjust classification and routing

## Time Estimate

- 4 hours: deploy payment failure detection pipeline (webhook, n8n workflows, PostHog events, Attio sync)
- 4 hours: build and test dunning sequence (email templates, in-app banners, Loops sequences, n8n orchestration)
- 2 hours: deploy proactive card expiry detection
- 3 hours: build health dashboard and alerts
- 3 hours: monitoring and debugging over 2 weeks (15 min/day)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stripe | Payment failure webhooks, subscription status, billing portal links | Included with Stripe account — [stripe.com/pricing](https://stripe.com/pricing) |
| Loops | Dunning email sequences and proactive expiry emails | Free up to 1,000 contacts; $49/mo for 5K — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app recovery banners and prompts | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| PostHog | Event tracking, funnels, dashboards, cohorts | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Webhook processing, sequence orchestration, scheduling | Free self-hosted; cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost: $0-100/mo** (depends on existing tool subscriptions; Stripe access is free, PostHog and n8n free tiers may suffice)

## Drills Referenced

- `payment-failure-detection` — real-time detection, classification, and scoring of payment failures from Stripe webhooks
- `dunning-sequence-automation` — multi-channel recovery sequence: in-app banners, 4-email ladder, human routing
- `proactive-card-expiry-detection` — daily scan for expiring cards with pre-failure update prompts
- `payment-recovery-health-monitor` — dashboard, funnel tracking, alerts, and weekly health reports
