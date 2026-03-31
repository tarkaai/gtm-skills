---
name: usage-threshold-alerts-smoke
description: >
  Plan Limit Notifications — Smoke Test. Manually identify users near plan limits using PostHog
  queries, send a handful of contextual alerts, and validate that limit-proximity messaging
  drives upgrades at a higher rate than generic prompts.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥30% upgrade rate from alerted users"
kpis: ["Upgrade rate from alerted users", "Alert click-through rate", "Median hours from alert to upgrade"]
slug: "usage-threshold-alerts"
install: "npx gtm-skills add product/upsell/usage-threshold-alerts"
drills:
  - usage-threshold-detection
  - threshold-engine
---

# Plan Limit Notifications — Smoke Test

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Prove the concept: does alerting users who are approaching their plan limits drive upgrades at a meaningful rate? No automation, no always-on. Run the detection query once, manually send alerts to 20-50 users, and measure whether limit-proximity messaging converts better than your current upgrade path.

## Leading Indicators

- Detection query returns at least 20 accounts at 70%+ of a plan limit (sufficient signal exists)
- At least 3 distinct resources appear in the flagged accounts (not just one limit type)
- Alerted users click through at 40%+ (the message resonates)
- At least 2 users upgrade within 48 hours of receiving the alert (urgency works)

## Instructions

### 1. Verify usage data exists in PostHog

Confirm your PostHog project tracks per-account resource consumption. Run this verification query via PostHog API or MCP:

```sql
SELECT
  event,
  count(),
  uniq(properties.account_id)
FROM events
WHERE timestamp > now() - interval 30 day
  AND event IN ('resource_consumed', 'api_call', 'project_created', 'seat_added', 'storage_used')
GROUP BY event
ORDER BY count() DESC
```

You need at least one event type that tracks a metered resource against a plan limit. If no usage tracking exists, instrument it first using the `posthog-custom-events` fundamental. At minimum, capture: account_id, resource_type, current_count, and plan_limit.

### 2. Run the threshold detection manually

Run the `usage-threshold-detection` drill in manual mode — execute the detection query once rather than setting up the scheduled workflow. Query PostHog for all accounts at 70%+ of any plan limit:

```sql
SELECT
  properties.account_id,
  properties.resource_type,
  properties.current_count,
  properties.plan_limit,
  round(properties.current_count / properties.plan_limit * 100, 1) AS pct_used
FROM events
WHERE event = 'resource_consumed'
  AND timestamp > now() - interval 1 day
  AND properties.plan_limit > 0
  AND properties.current_count / properties.plan_limit >= 0.7
ORDER BY pct_used DESC
```

Export the results. Classify each account by urgency tier: approaching (70-84%), imminent (85-94%), critical (95%+).

**Human action required:** Review the flagged accounts. Remove any that are obviously incorrect (test accounts, internal accounts, accounts with known data issues). Select 20-50 accounts across urgency tiers for the smoke test.

### 3. Send contextual alerts manually

For each selected account, send a usage alert via Intercom or email. The message must include their actual numbers:

**For imminent accounts (85-94%):**
Subject: "You've used {{pct_used}}% of your {{resource_name}}"
Body: "Your {{plan_tier}} plan includes {{plan_limit}} {{resource_name}}. You've used {{current_count}}. Upgrade to {{next_tier}} for {{next_tier_limit}} — here's what you'll get: [value bullets]. [Upgrade link]"

**For critical accounts (95%+):**
Subject: "{{resource_name}} limit: you're at {{pct_used}}%"
Body: "You're about to hit your {{resource_name}} limit. When you do, [explain what happens — blocked, degraded, etc.]. Upgrade now to avoid interruption. [One-click upgrade link]"

Send via Intercom in-app message if the user is active in-product, or via email if not. Log every send: who received it, which resource, which tier, which channel.

### 4. Track responses for 7 days

Monitor for 7 days after sending alerts. Track manually in a spreadsheet or PostHog:

- Did the user open/click the alert?
- Did the user visit the pricing page?
- Did the user start an upgrade?
- Did the user complete an upgrade?
- How many hours elapsed from alert to upgrade?
- Did any user respond negatively (complaint, unsubscribe, support ticket)?

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure: of the 20-50 users who received a usage threshold alert, did at least 30% upgrade within 7 days?

Also compare against your baseline: what is the typical upgrade rate for users at similar usage levels who did NOT receive a threshold alert? The alert should outperform the organic upgrade rate by at least 2x.

Record:
- Total users alerted
- Upgrade rate (overall and by urgency tier)
- Click-through rate by channel (in-app vs. email)
- Median time from alert to upgrade
- Any negative reactions
- Which resource types drove the highest upgrade rate

If PASS (30%+ upgrade rate), proceed to Baseline. If FAIL, examine: were the messages too generic? Were users at the wrong urgency tier? Was the upgrade path too many clicks? Fix and re-run.

## Time Estimate

- 1 hour: verify PostHog data and run detection query
- 1 hour: review flagged accounts and select smoke test cohort
- 1.5 hours: craft contextual messages and send alerts
- 0.5 hours: set up tracking
- 1 hour: evaluate results after 7 days and document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data queries, cohort identification | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app alert delivery | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |

**Estimated cost for Smoke: Free** (using existing PostHog and Intercom instances, manual sends)

## Drills Referenced

- `usage-threshold-detection` — identifies accounts approaching plan limits by querying PostHog usage data (run manually for Smoke)
- `threshold-engine` — evaluates whether the upgrade rate meets the 30% pass threshold
