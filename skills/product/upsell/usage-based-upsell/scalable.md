---
name: usage-based-upsell-scalable
description: >
  Automatic Usage Upsell — Scalable Automation. Extend auto-upgrade to all metered
  resources, segment messaging by account value, A/B test grace period parameters,
  and scale to 500+ accounts while maintaining ≥55% acceptance.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥55% auto-upgrade acceptance rate across all resources at 500+ exceeded accounts"
kpis: ["Auto-upgrade acceptance rate", "ARPU lift (total MRR from auto-upgrades)", "30-day retention by resource", "Acceptance rate by segment"]
slug: "usage-based-upsell"
install: "npx gtm-skills add product/upsell/usage-based-upsell"
drills:
  - usage-threshold-detection
  - auto-upgrade-execution
  - upgrade-prompt
  - ab-test-orchestrator
  - upgrade-prompt-health-monitor
---

# Automatic Usage Upsell — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Auto-upgrade covers ALL metered resources (not just one). Grace period messaging is segmented by account value and resource type. A/B tests have identified the optimal grace period duration, messaging copy, and notification cadence. The system processes 500+ exceeded accounts over 2 months with acceptance rate ≥55% across all resources. Total MRR from auto-upgrades is tracked and growing month-over-month.

## Leading Indicators

- Auto-upgrade rules configured for every metered resource within the first week
- At least 3 A/B tests launched within the first 4 weeks (grace period duration, subject lines, opt-out placement)
- Per-resource acceptance rates visible in the health dashboard — no resource drops below 40% acceptance
- High-value account routing creates at least 5 expansion deals per week in Attio
- Month 2 MRR from auto-upgrades exceeds Month 1 by at least 10%

## Instructions

### 1. Expand to all metered resources

Run the `usage-threshold-detection` drill for every metered resource in your product. At Smoke and Baseline you tested with one resource. Now extend:

- Add detection queries for seats, storage, projects, API calls, and any other plan-differentiated resource
- Update the auto-upgrade tier map in the `auto-upgrade-execution` configuration to cover every current_plan + resource combination
- Validate each new resource's threshold accuracy by spot-checking 10 accounts against your product database

Deploy each new resource incrementally (one per week). Monitor the health dashboard after each addition. If a new resource shows a false positive rate above 30%, recalibrate its detection thresholds before proceeding to the next resource.

### 2. Segment messaging by account value and resource

Not every auto-upgrade deserves the same communication. Run the `upgrade-prompt` drill, Steps 3-5, adapted for auto-upgrade messaging:

**Self-serve accounts (MRR < $200):**
- Standard grace period flow: in-app banner + email sequence
- Auto-upgrade executes automatically after grace period
- Messaging tone: helpful and matter-of-fact. "Your usage grew — we're upgrading your plan so nothing breaks."

**Mid-market accounts (MRR $200-$2,000):**
- Extended grace period: 5 days instead of 3
- Add a "Schedule a call to discuss options" CTA alongside opt-out
- If the account has an assigned owner in Attio, notify the owner when grace starts
- Messaging tone: consultative. "Your team's growth triggered an upgrade. Here's what changes and how to get the most value."

**Enterprise accounts (MRR > $2,000):**
- No auto-upgrade. Route to account owner via `attio-deals` with full usage context
- Create an expansion deal with: current usage per resource, projected growth, recommended plan, estimated ARR increase
- The account owner has a conversation and executes the upgrade manually or negotiates a custom plan

### 3. A/B test grace period parameters

Run the `ab-test-orchestrator` drill to systematically test each variable:

**Test 1 — Grace period duration (week 2-4):**
- Control: 72-hour grace period
- Variant A: 48-hour grace period
- Variant B: 120-hour (5-day) grace period
- Primary metric: acceptance rate. Secondary: rollback rate within 48 hours.
- Use PostHog feature flags to assign accounts to variants. Run until 50+ accounts per variant.

**Test 2 — Messaging frame (week 4-6):**
- Control: "We'll upgrade you to avoid service interruption" (loss-aversion frame)
- Variant: "Your usage grew — unlock more capacity with [plan]" (growth frame)
- Test via the Intercom in-app banner copy. Measure acceptance rate and opt-out rate.

**Test 3 — Opt-out friction (week 6-8):**
- Control: One-click opt-out button in the banner
- Variant: Opt-out requires selecting a reason from a dropdown (adds 5 seconds of friction)
- Measure: Does the dropdown reduce opt-outs? Does it increase support tickets? The reason data is valuable for product decisions, but only if it doesn't damage acceptance rate.

Log all experiment results in Attio. After each test, adopt the winner and roll it out to 100%.

### 4. Build per-resource and per-segment performance tracking

Run the `upgrade-prompt-health-monitor` drill adapted for auto-upgrades. Build a PostHog dashboard with:

| Panel | Breakdown | Purpose |
|-------|-----------|---------|
| Acceptance rate trend (weekly) | By resource type | Which resources users accept auto-upgrades for |
| Acceptance rate by segment | By MRR band | Are mid-market accounts behaving differently than self-serve |
| MRR from auto-upgrades (monthly) | By resource | Revenue attribution per resource |
| Opt-out reasons (if Test 3 adopted) | By resource | Why users prefer hard limits over upgrading |
| 30-day retention by resource | By resource | Are some resource-driven upgrades stickier than others |
| Grace period conversion timing | Histogram | Do most users accept immediately, or wait until the last day |
| Rollback rate trend | By resource | Are rollbacks increasing as you scale |

Set alerts:
- Any resource's acceptance rate drops below 40% for 7 consecutive days
- Total rollback rate exceeds 15%
- Payment failure rate exceeds 8%
- Zero auto-upgrades processed in 48 hours (system may be broken)

### 5. Evaluate against threshold

After 2 months, measure:

- Total exceeded accounts processed across all resources: must be ≥500
- Overall acceptance rate: must be ≥55%
- Per-resource acceptance rate: no resource below 40%
- Total MRR from auto-upgrades: tracked and growing month-over-month
- 30-day retention: ≥75% across all resources
- A/B test winners adopted: at least 2 of 3 tests produced a winner

**Pass:** ≥55% acceptance at 500+ accounts. Proceed to Durable.
**Fail:** If acceptance is below 55%, check per-resource breakdown. If one resource is dragging down the average (e.g., storage upgrades have 30% acceptance), investigate that resource specifically. Users may prefer to clean up storage rather than pay more. Consider offering "optimize your usage" guidance alongside the auto-upgrade for that resource.

## Time Estimate

- 8 hours: Expand threshold detection and auto-upgrade rules to all resources (2 hours per resource, ~4 resources)
- 8 hours: Build segmented messaging (self-serve, mid-market, enterprise routing)
- 12 hours: Design, deploy, and monitor 3 A/B tests (4 hours each)
- 8 hours: Build per-resource and per-segment dashboards
- 24 hours: Ongoing monitoring, debugging, and iteration over 2 months (3 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags for A/B tests, funnels, dashboards | Free: 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Subscription management across all plan tiers | 2.9% + $0.30/txn; Billing included ([stripe.com/pricing](https://stripe.com/pricing)) |
| n8n | Scheduled detection, upgrade execution, A/B test routing | Self-hosted free; Cloud from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | Segmented in-app messages, A/B test copy variants | Essential $29/seat/mo; Advanced $85/seat/mo for targeting ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Segmented email sequences by account tier | Free up to 1,000 contacts; Growth from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Expansion deals, segment tracking, experiment logging | Free tier available ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `usage-threshold-detection` — extended to cover all metered resources with per-resource accuracy validation
- `auto-upgrade-execution` — updated tier map and grace period parameters based on A/B test results
- `upgrade-prompt` — adapted for segmented messaging by account value (self-serve, mid-market, enterprise)
- `ab-test-orchestrator` — runs 3 experiments on grace period duration, messaging frame, and opt-out friction
- `upgrade-prompt-health-monitor` — per-resource and per-segment performance dashboard with degradation alerts
