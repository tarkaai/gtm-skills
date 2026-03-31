---
name: usage-based-upsell-baseline
description: >
  Automatic Usage Upsell — Baseline Run. Automate threshold detection and auto-upgrade
  execution on a cron schedule, add email sequences, stream billing events to PostHog,
  and run always-on for 2 weeks to validate acceptance holds at ≥60%.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥60% auto-upgrade acceptance rate with ≥40 exceeded accounts over 2 weeks"
kpis: ["Auto-upgrade acceptance rate", "30-day upgrade retention", "ARPU lift", "Payment failure rate"]
slug: "usage-based-upsell"
install: "npx gtm-skills add product/upsell/usage-based-upsell"
drills:
  - posthog-gtm-events
  - auto-upgrade-execution
  - usage-alert-delivery
---

# Automatic Usage Upsell — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The auto-upgrade system runs fully automated — threshold detection fires daily, grace period notifications send automatically, and Stripe subscription changes execute without manual intervention. Email sequences complement in-app messages. Billing events stream to PostHog for revenue attribution. The system processes at least 40 exceeded accounts over 2 weeks with ≥60% accepting the auto-upgrade. Upgraded accounts retain on the new plan at ≥80% after 30 days.

## Leading Indicators

- Daily threshold detection workflow completes without errors for 5 consecutive days
- Grace period notifications deliver via both Intercom and email (check delivery logs)
- Billing event stream flowing to PostHog — `billing_subscription_updated` events appear within 5 minutes of a Stripe change
- Payment failure rate below 5% on auto-upgrade attempts
- No support tickets about unexpected charges within the first 3 days (confirms messaging is clear)

## Instructions

### 1. Automate the full detection and upgrade pipeline

Run the `posthog-gtm-events` drill to formalize event tracking. Ensure these events are instrumented with consistent property schemas:

| Event | Properties |
|-------|------------|
| `resource_consumed` | account_id, resource_type, current_count, plan_limit, plan_tier, pct_used |
| `auto_upgrade_grace_started` | account_id, current_plan, target_plan, resource, pct_consumed, grace_end |
| `auto_upgrade_opted_out` | account_id, resource, reason |
| `auto_upgrade_completed` | account_id, previous_plan, new_plan, resource, mrr_increase, proration_amount |
| `auto_upgrade_rolled_back` | account_id, resource, days_since_upgrade, reason |

Convert the manual Smoke-level workflows to always-on automation:
- Set `usage-threshold-detection` to run daily at 06:00 UTC via n8n cron
- Set the grace period checker to run hourly via n8n cron
- Verify both workflows execute successfully for 3 consecutive days before considering the pipeline stable

### 2. Add email sequences to the grace period

Run the `usage-alert-delivery` drill, Steps 3-4. Add email notifications that complement the in-app messages from Smoke:

**Grace start email (Day 0):** Subject: "Your [resource] limit is upgrading in 72 hours." Body: usage bar showing current vs. limit, what the next plan includes, price difference, opt-out link, FAQ link.

**Grace reminder email (Day 2, 24 hours before upgrade):** Subject: "Upgrading to [plan] tomorrow — here's what you'll get." Body: value-focused (not fear-focused), list the additional capacity and features, confirm the charge amount, final opt-out link.

**Upgrade confirmation email (after execution):** Subject: "You're now on [plan] — here's what changed." Body: new limits, next billing date, prorated charge amount, link to billing settings, link to support.

Route high-value accounts (MRR > $500) to the account owner in Attio instead of auto-upgrading. Create an expansion deal with the usage context so the account owner can have a personal conversation.

### 3. Stream billing events to PostHog

Run the `auto-upgrade-execution` drill, Step 5. Configure `billing-event-streaming` so that every Stripe subscription change appears in PostHog. This enables:

- Revenue attribution: how much MRR came from auto-upgrades vs. self-serve upgrades vs. sales-driven upgrades
- Retention analysis: do auto-upgraded accounts retain at the same rate as accounts that upgraded voluntarily?
- Proration accuracy: are prorated charges matching expectations?

Build a PostHog funnel connecting usage events to billing events:
```
resource_consumed (pct_used >= 100)
  -> auto_upgrade_grace_started
    -> auto_upgrade_completed
      -> billing_subscription_updated (change_type = "upgrade")
```

### 4. Build the health monitoring layer

Run the `usage-alert-health-monitor` drill. Set up the weekly health report that tracks:

- Detection accuracy: true positive rate, false positive rate, miss rate
- Alert-to-upgrade funnel conversion by resource and urgency tier
- Revenue impact: MRR from auto-upgrades this week
- System health: did detection and execution run without errors?

At Baseline, review this report manually each week. At Durable, it feeds into the autonomous optimization loop.

### 5. Evaluate against threshold

After 2 weeks of always-on operation, measure:

- Total exceeded accounts processed: must be ≥40
- Acceptance rate (completed / (completed + opted_out)): must be ≥60%
- 30-day retention on new plan (for accounts upgraded in week 1): target ≥80%
- Payment failure rate: must be below 5%
- Rollback rate (rolled_back / completed): must be below 10%

**Pass:** ≥60% acceptance rate from ≥40 accounts. Proceed to Scalable.
**Fail:** If acceptance rate dropped from Smoke, diagnose: Did the email sequences change user behavior? Did the automated timing differ from manual timing? Check if the reminder email is causing more opt-outs (users who would have passively accepted are now actively deciding). If so, test removing the Day 2 reminder.

## Time Estimate

- 3 hours: Automate detection and upgrade pipelines with n8n cron schedules
- 3 hours: Build email sequences (grace start, reminder, confirmation) in Loops
- 2 hours: Configure billing event streaming (Stripe webhooks to PostHog via n8n)
- 2 hours: Set up health monitoring dashboard and weekly report
- 2 hours: Build high-value account routing to Attio expansion deals
- 4 hours: Monitor, debug, and iterate over 2 weeks (30 min/day)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, dashboards, cohorts | Free: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Subscription changes, proration, billing webhooks | 2.9% + $0.30/txn; Billing included ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Scheduled detection, grace period checks, billing stream | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app grace notifications and confirmations | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences (grace, reminder, confirmation) | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Account status tracking, expansion deal routing | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `posthog-gtm-events` — formalizes the event schema and ensures all auto-upgrade lifecycle events are tracked consistently
- `auto-upgrade-execution` — the core workflow: grace period, opt-out handling, Stripe subscription change, and rollback
- `usage-alert-delivery` — adds email sequences and high-value account routing to complement in-app messages
