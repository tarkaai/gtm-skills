---
name: in-product-upgrade-flow-baseline
description: >
  Self-Serve Upgrade UX — Baseline Run. Always-on upgrade surface with full
  funnel tracking, usage-threshold-triggered prompts, pricing page conversion
  monitoring, and A/B comparison against a control group to prove sustained
  self-serve upgrade conversion.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥8% self-serve upgrade rate with ≥5pp lift over control group"
kpis: ["Self-serve upgrade rate", "Lift vs. control", "Checkout abandonment rate", "Time to upgrade", "Revenue per upgrade"]
slug: "in-product-upgrade-flow"
install: "npx gtm-skills add product/upsell/in-product-upgrade-flow"
drills:
  - usage-threshold-detection
  - upgrade-prompt
---

# Self-Serve Upgrade UX — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

8% or more of users who encounter upgrade surfaces complete a self-serve plan upgrade, with at least 5 percentage points lift over the control group (users who do not see the upgrade surface). The upgrade flow runs always-on for 2 weeks with automated trigger detection, real-time usage monitoring, and full funnel tracking. This proves that the in-product upgrade path drives sustained, incremental conversions — not just captures users who would have upgraded anyway.

## Leading Indicators

- Control group upgrade rate stays below 3% (validates the surface is causing lift, not correlating with organic upgrades)
- Usage threshold detection triggering 10+ alerts per day (the trigger system is catching real upgrade-ready moments)
- Checkout abandonment rate below 40% (the checkout path is not leaking users)
- Time-to-upgrade decreasing week over week (the flow is getting more efficient)
- Pricing page conversion monitor showing stable or improving conversion rates (the pricing page and in-product surfaces are not cannibalizing each other)
- Revenue per upgrade stable or increasing (users are selecting appropriate plans, not consistently choosing the cheapest option)

## Instructions

### 1. Deploy usage threshold detection

Run the `usage-threshold-detection` drill to build the automated system that identifies upgrade-ready accounts:

Configure detection for every metered resource that differs between plan tiers:
- **Seats**: Alert at 80% of plan limit (e.g., 4 of 5 seats on Free)
- **API calls / actions**: Alert at 80% of monthly quota
- **Storage**: Alert at 80% of storage cap
- **Projects / workspaces**: Alert at 80% of object limit

For each resource, the drill builds:
1. A daily n8n workflow querying PostHog for accounts at 70%+ of any limit
2. Consumption velocity calculation projecting when the account will hit the limit
3. Urgency tier classification: approaching (70-84%), imminent (85-94%), critical (95-100%), exceeded (>100%)
4. PostHog cohorts for each urgency tier, updated daily
5. Attio records enriched with threshold proximity and projected hit dates

Wire the threshold detection to the upgrade surface: when an account enters the "imminent" or "critical" tier, the next time the user performs an action related to that resource, show the upgrade surface with resource-specific context. Example: "You have used 24 of 25 seats. Upgrade to Pro for unlimited seats — $49/mo."

### 2. Set up pricing page conversion monitoring

Run the `pricing-page-conversion-monitor` drill to establish the observation layer for the self-serve pricing and checkout flow:

Build a PostHog dashboard with:
- **Pricing page to checkout conversion rate** (daily, 7-day rolling average)
- **Plan selection distribution** (which plan users choose most)
- **Checkout abandonment rate** (started checkout but did not complete)
- **In-product upgrade vs. pricing page upgrade** attribution (tracks whether the user upgraded via the in-product surface or by navigating to the pricing page)
- **ARPU for new upgrades** (average MRR increase per upgrade)

Configure daily anomaly detection:
- Alert if pricing page conversion drops >20% vs. 14-day average
- Alert if checkout abandonment exceeds 50% for 3 consecutive days
- Alert if ARPU drops >15% (users are selecting cheaper plans than expected)

This monitoring establishes the baseline metrics that the Scalable and Durable levels will optimize against.

### 3. Expand upgrade surfaces to multiple trigger points

Using the Smoke test's validated trigger, extend the `upgrade-prompt` drill to cover 3 trigger types simultaneously:

| Trigger | Surface | Timing |
|---------|---------|--------|
| **Limit proximity** (imminent/critical tier from threshold detection) | Inline modal with resource-specific context and one-click upgrade | When user performs an action related to the constrained resource |
| **Feature gate** | Contextual panel showing what the feature does + upgrade CTA | When user encounters a locked premium feature |
| **Growth signal** (added 3+ team members or doubled usage in 30 days) | Slide-in panel with team-oriented upgrade pitch | After the growth signal event, on next login |

For each trigger, configure:
1. PostHog events: `upgrade_surface_shown`, `upgrade_surface_clicked`, `upgrade_checkout_started`, `upgrade_checkout_completed` with `trigger_type` property
2. Suppression rules: do not show the same trigger type to the same user more than once per 48 hours; maximum 1 upgrade surface per session
3. Email follow-up via Loops: if a user sees the surface and clicks but does not complete checkout, send a follow-up email 24 hours later with a direct checkout link and the context from their trigger

### 4. Run with control group

Using PostHog feature flags, split upgrade-eligible users 80/20:
- **Treatment (80%)**: See upgrade surfaces at trigger points
- **Control (20%)**: Do not see upgrade surfaces, but can still upgrade via the pricing page or billing settings

Track both groups' upgrade rates in PostHog. The control group measures organic upgrade behavior — users who upgrade without any in-product prompting. The treatment group's lift over control is the true impact of the upgrade surfaces.

Log the assignment in PostHog person properties: `upgrade_flow_group: "treatment" | "control"` so all downstream analysis can segment by group.

### 5. Monitor and diagnose for 2 weeks

Build an n8n workflow running daily at 08:00 UTC:

1. Query PostHog for treatment vs. control upgrade rates (last 7 days, rolling)
2. Query per-trigger-type conversion rates: which trigger drives the most upgrades
3. Pull checkout abandonment data: at which step do users drop off
4. Check session recordings for the 5 most recent checkout abandonments
5. If any trigger type has <2% conversion after 7 days, flag it for review

Weekly digest (Monday, automated):
- Treatment upgrade rate vs. control rate with lift calculation
- Per-trigger breakdown: impressions, clicks, checkouts started, checkouts completed, conversion rate
- Top checkout drop-off step and recommended fix
- Revenue from in-product upgrades this week

### 6. Evaluate against threshold

At the end of 2 weeks:

- **Self-serve upgrade rate** (treatment group): `upgrade_checkout_completed` / `upgrade_surface_shown`. Target: >=8%.
- **Lift vs. control**: Treatment upgrade rate minus control upgrade rate. Target: >=5pp.

**Pass:** The in-product upgrade flow drives incremental self-serve conversions with always-on automation. Proceed to Scalable to test upgrade surface variants, personalize by segment, and scale to all users.

**Fail:** Diagnose by trigger type:
- All triggers low (<5%): The upgrade surfaces are not compelling. Watch session recordings to identify whether the issue is value communication, pricing clarity, or checkout friction.
- Limit proximity high but others low: Users upgrade when they must, not when nudged. Focus Scalable on expanding limit-based triggers and building a more seamless auto-upgrade path.
- High CTR but low checkout completion: Checkout friction. Investigate: is the target plan pre-selected? Is the price increase clear? Does the user have to re-enter payment info? Can you add inline checkout that does not navigate away from the current page?
- Low lift vs. control: The surfaces are catching users who would upgrade anyway, not creating new conversions. Test more aggressive triggers (show surface earlier in the usage arc) or new trigger types.

## Time Estimate

- 4 hours: Usage threshold detection setup (n8n workflow, PostHog cohorts, Attio enrichment)
- 4 hours: Pricing page conversion monitoring (PostHog dashboard, anomaly detection, n8n alerts)
- 4 hours: Multi-trigger upgrade surface deployment, email follow-up, suppression rules
- 4 hours: Control group setup, 2-week monitoring, weekly analysis, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, funnels, cohorts, session recordings, anomaly detection | Free up to 1M events/mo — https://posthog.com/pricing |
| Stripe | Payment processing for upgrade checkout | 2.9% + $0.30 per transaction — https://stripe.com/pricing |
| n8n | Threshold detection workflows, monitoring, alerting | Free self-hosted; Cloud from ~$24/mo — https://n8n.io/pricing |
| Loops | Checkout abandonment follow-up emails | Free up to 1,000 contacts — https://loops.so/pricing |
| Attio | Usage threshold records, upgrade deal tracking | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$0-50/mo (n8n Cloud if not self-hosting; Loops if exceeding free tier)

## Drills Referenced

- `usage-threshold-detection` — detect per-account usage approaching plan limits, classify urgency tiers, and wire threshold events to upgrade surface triggers
- `upgrade-prompt` — configure contextual upgrade surfaces across 3 trigger types with suppression rules and email follow-up
