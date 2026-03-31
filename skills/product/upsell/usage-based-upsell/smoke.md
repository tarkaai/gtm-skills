---
name: usage-based-upsell-smoke
description: >
  Automatic Usage Upsell — Smoke Test. Identify the right value metric, instrument
  usage tracking, build a minimal auto-upgrade flow for one resource, and test whether
  users accept automatic plan changes when they exceed their limit.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥50% auto-upgrade acceptance rate from ≥20 exceeded accounts"
kpis: ["Auto-upgrade acceptance rate", "Opt-out rate", "ARPU lift per upgraded account"]
slug: "usage-based-upsell"
install: "npx gtm-skills add product/upsell/usage-based-upsell"
drills:
  - usage-pricing-model-analysis
  - usage-threshold-detection
  - auto-upgrade-execution
  - threshold-engine
---

# Automatic Usage Upsell — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

One metered resource has usage tracking instrumented in PostHog and threshold detection running. When accounts exceed 100% of their plan limit for that resource, an automatic upgrade fires with a 72-hour opt-out window. At least 20 accounts hit the exceeded threshold during the test period. At least 50% accept the auto-upgrade (do not opt out). This proves that users will tolerate — and even prefer — automatic plan changes over hitting a hard wall.

## Leading Indicators

- Usage tracking events flowing correctly in PostHog Live Events within the first hour of instrumentation
- At least 5 accounts classified as "imminent" (85-94%) within the first 3 days (confirms threshold detection is calibrated correctly and enough users are near limits)
- First auto-upgrade grace period triggered within 48 hours of going live
- Opt-out rate below 30% in the first 3 grace periods (early signal that the messaging feels fair)

## Instructions

### 1. Identify the value metric and plan boundaries

Run the `usage-pricing-model-analysis` drill, Steps 1-2 only. Pick ONE metered resource for this test — the one where the most users are clustered near plan limits. Query your product database or PostHog for current usage distribution across all metered resources (API calls, seats, storage, projects, etc.). Select the resource where at least 20 accounts are currently at 70%+ of their plan limit — this ensures enough volume for the test.

Document: the resource name, the plan limit per tier, and which plan each tier should upgrade to.

### 2. Instrument usage threshold detection

Run the `usage-threshold-detection` drill for your chosen resource only. Set up:

- PostHog custom events tracking current consumption vs. plan limit per account
- The daily detection query that classifies accounts into urgency tiers (approaching, imminent, critical, exceeded)
- Attio custom attributes storing threshold proximity data per account

At this level, run the detection query manually once per day (no n8n automation yet). Verify the results make sense: spot-check 5 flagged accounts against your product database to confirm the usage numbers are accurate.

**Human action required:** Validate that the plan limit configuration matches your actual pricing tiers. An incorrect limit will trigger false auto-upgrades.

### 3. Build the auto-upgrade flow

Run the `auto-upgrade-execution` drill, Steps 1-4. Build the minimal version:

- Define the auto-upgrade tier map for your chosen resource (one resource, all relevant plan tiers)
- Build the 72-hour grace period notification using Intercom in-app messages: "You've exceeded your [resource] limit. We'll upgrade you to [next plan] in 72 hours. [View details] [Opt out]"
- Build the opt-out handler
- Build the upgrade execution that changes the Stripe subscription when the grace period expires

At Smoke level, run the hourly grace-period check manually (trigger the n8n workflow by hand) rather than on a cron schedule. This lets you monitor each upgrade as it happens.

Track every event in PostHog: `auto_upgrade_grace_started`, `auto_upgrade_opted_out`, `auto_upgrade_completed`.

**Human action required:** Test the full flow on a test account before going live. Create a test account, push its usage past the limit, verify the grace notification appears, wait for the opt-out window to pass, and confirm the Stripe subscription changes correctly. Check the prorated charge is calculated correctly.

### 4. Go live and evaluate

Deploy the auto-upgrade flow to all accounts. Let it run for 7 days.

Run the `threshold-engine` drill to evaluate results. Query PostHog:

- Count of `auto_upgrade_grace_started` events (must be ≥20)
- Count of `auto_upgrade_completed` events
- Count of `auto_upgrade_opted_out` events
- Acceptance rate = completed / (completed + opted_out)

**Pass:** Acceptance rate ≥50% from ≥20 exceeded accounts. Proceed to Baseline.
**Fail:** If acceptance rate <50%, diagnose: Are users opting out because the price increase is too high? Because the grace period messaging is unclear? Because they prefer a hard limit? Review PostHog events and Intercom message interaction data. Adjust messaging or grace period duration and re-run.

## Time Estimate

- 1 hour: Analyze usage distribution and select resource + plan boundaries
- 1.5 hours: Instrument threshold detection and validate accuracy
- 1.5 hours: Build auto-upgrade flow (grace period, opt-out, execution)
- 0.5 hours: Test on a test account end-to-end
- 0.5 hours: Evaluate after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage event tracking, threshold detection queries, funnel measurement | Free: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Subscription management, plan changes, proration | 2.9% + $0.30 per transaction; Billing included ([stripe.com/pricing](https://stripe.com/pricing)) |
| Intercom | Grace period in-app notification | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Attio | Account-level threshold data storage | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `usage-pricing-model-analysis` — identifies the value metric and usage distribution to select the right resource for testing
- `usage-threshold-detection` — builds the system that classifies accounts by urgency tier based on consumption vs. plan limits
- `auto-upgrade-execution` — implements the grace period, opt-out, and Stripe subscription change when usage exceeds limits
- `threshold-engine` — evaluates the 50% acceptance rate against the pass threshold and recommends next action
