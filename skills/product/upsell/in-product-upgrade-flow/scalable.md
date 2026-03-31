---
name: in-product-upgrade-flow-scalable
description: >
  Self-Serve Upgrade UX — Scalable Automation. Systematic A/B testing of upgrade
  surface variants, segment-personalized upgrade flows, automated usage-based
  auto-upgrade execution, and cross-trigger optimization to sustain self-serve
  conversion across 500+ exposed users.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥10% self-serve upgrade rate sustained across 500+ surface-exposed users with auto-upgrade acceptance rate ≥50%"
kpis: ["Self-serve upgrade rate at scale", "Auto-upgrade acceptance rate", "Experiment win rate", "Upgrade-driven MRR", "Per-trigger conversion rate", "Checkout abandonment rate"]
slug: "in-product-upgrade-flow"
install: "npx gtm-skills add product/upsell/in-product-upgrade-flow"
drills:
  - ab-test-orchestrator
  - auto-upgrade-execution
---

# Self-Serve Upgrade UX — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

10% or more self-serve upgrade rate sustained across 500+ upgrade-surface-exposed users over 2 months. Auto-upgrade execution (for users who exceed plan limits) achieves >=50% acceptance rate. The 10x multiplier comes from two dimensions: systematic experimentation that finds the highest-converting surface variants, and automated upgrade execution that removes the manual decision entirely for users who have outgrown their plan.

## Leading Indicators

- Experiment velocity: at least 2 A/B tests completed per month with documented outcomes
- Winning experiments producing measurable lift (>2% improvement on the tested metric)
- Auto-upgrade grace period opt-out rate below 50% (most users who exceed limits accept the upgrade)
- Auto-upgrade retention: 80%+ of auto-upgraded users still on the higher plan 30 days later
- Per-trigger conversion rates all above 5% (no single trigger type dragging the average)
- Upgrade-driven MRR growing month over month
- Checkout abandonment declining as each experiment removes a friction point

## Instructions

### 1. Run systematic experiments on upgrade surfaces

Run the `ab-test-orchestrator` drill to test upgrade flow variants. Run each test for statistical significance (minimum 200 per variant).

**Month 1 experiments:**

- **Surface format**: Modal vs. slide-in panel vs. inline banner for the limit-proximity trigger. Hypothesis: inline banners that do not interrupt the user's workflow produce higher checkout completion because they reduce dismissal impulse. Measure: `upgrade_checkout_completed` rate per `upgrade_surface_shown`.

- **Checkout flow**: In-page inline checkout (plan selection + payment without navigating away) vs. redirect to billing settings page. Hypothesis: inline checkout increases completion by 15pp because it eliminates page transition friction and preserves context. Measure: `upgrade_checkout_completed` / `upgrade_checkout_started` (checkout completion rate specifically, not full funnel).

**Month 2 experiments:**

- **Price anchoring**: Show monthly price only vs. show monthly + annual with savings highlight ("Save 20% with annual billing"). Hypothesis: showing the annual option increases average revenue per upgrade by 30% because users who self-serve are higher intent and respond to savings framing. Measure: `mrr_delta` per upgrade and annual vs. monthly plan selection rate.

- **Social proof**: Standard upgrade surface vs. surface with usage context ("4,832 teams upgraded to Pro this month" or "Teams your size typically use Pro"). Hypothesis: social proof increases surface CTR by 10% for growth-signal triggers. Measure: `upgrade_surface_clicked` / `upgrade_surface_shown`.

For each experiment:
1. Form the hypothesis with predicted impact and reasoning
2. Calculate required sample size using PostHog's experiment calculator
3. Create a PostHog feature flag splitting users between control and variant
4. Run for the calculated duration without peeking at results
5. Evaluate: adopt the winner if statistically significant with >95% confidence; document the learning either way

### 2. Deploy auto-upgrade for limit-exceeded users

Run the `auto-upgrade-execution` drill to build the automated upgrade pipeline for users who have exceeded their plan limits:

**Auto-upgrade flow:**

1. `usage-threshold-detection` (from Baseline) flags an account as "exceeded" (>100% of a plan limit)
2. Look up the auto-upgrade rule: current plan + exceeded resource maps to target plan
3. If the account has a payment method on file, start a 72-hour grace period:
   - Show a persistent in-app banner: "You have exceeded your [resource] limit on [current plan]. We will upgrade you to [target plan] in 72 hours to keep your service running. [View details] [Opt out]"
   - Send an email via Loops: subject "Your plan is upgrading in 72 hours" with what changed, what it costs, how to opt out, and what happens if they opt out
4. If the user opts out: apply the hard limit, log `auto_upgrade_opted_out`, set 30-day cooldown
5. If the grace period expires without opt-out: execute the Stripe subscription change, send confirmation, log `auto_upgrade_completed`
6. Rollback mechanism: if the user contacts support within 48 hours, revert the subscription and issue a credit

**Auto-upgrade guardrails:**
- Never auto-upgrade from Free to any paid plan if no payment method is on file. Instead, show the standard upgrade surface with a payment collection step.
- Never auto-upgrade to Enterprise tier. Route those to sales via Attio deal creation.
- Maximum 1 auto-upgrade per account per billing cycle.
- If payment fails, set status to `payment_failed` and trigger a payment method update prompt.

**Measurement funnel:**
```
usage_threshold_detected (exceeded)
  -> auto_upgrade_grace_started
    -> auto_upgrade_opted_out OR auto_upgrade_completed
      -> (if completed) auto_upgrade_rolled_back OR auto_upgrade_retained_30d
```

Target metrics: acceptance rate >=50%, retention rate >=80%, rollback rate <10%.

### 3. Personalize upgrade surfaces by segment

Using PostHog cohorts and person properties, configure segment-specific upgrade experiences:

| Segment | Upgrade Strategy | Rationale |
|---------|-----------------|-----------|
| **Free, active 30+ days, approaching limit** | Aggressive: modal with resource context + inline checkout | High intent — they have invested in the product and are about to hit the wall |
| **Free, active <14 days, feature gate hit** | Gentle: contextual tooltip with "Available on Pro" and pricing link | Too early for aggressive upsell — build awareness, let them explore |
| **Trial users, day 5+** | Urgency: "Your trial ends in [N] days. Keep access to [features]" with one-click upgrade | They have experienced value, time pressure drives conversion |
| **Downgraded users** | Winback: "You used to have [feature] — you [accomplished X] with it. Re-upgrade to restore access" | Emotional connection to past usage is stronger than feature descriptions |
| **Power users on lower tier** (top 20% by usage) | Usage-based: "You are one of our most active users. Pro unlocks [specific capability they would use]" with personalized feature highlight | They are already heavy users; the upgrade pitch targets their actual behavior patterns |

Configure n8n to evaluate segment membership on each upgrade trigger event and route to the appropriate surface variant.

### 4. Build upgrade flow analytics

Extend the Baseline monitoring with cross-trigger and cross-segment analysis:

**PostHog dashboard — "Upgrade Flow Performance":**
- Upgrade rate by trigger type (limit proximity, feature gate, growth signal, auto-upgrade) trended weekly
- Upgrade rate by segment (new free, mature free, trial, downgraded, power user) trended weekly
- Revenue by trigger type: MRR from each upgrade path
- Experiment impact log: cumulative lift from adopted experiment winners
- Auto-upgrade funnel: grace started, opted out, completed, retained at 30 days
- Checkout completion rate by surface variant (which experiment winners are live)

**Automated alerts (n8n daily):**
- Any trigger type conversion drops below 5% for 3 consecutive days
- Auto-upgrade opt-out rate exceeds 60% for a week
- Overall upgrade-driven MRR declines 15% week over week
- Checkout abandonment exceeds 50%

### 5. Evaluate against threshold

At the end of 2 months:

- **Self-serve upgrade rate**: `upgrade_checkout_completed` / `upgrade_surface_shown` across all triggers. Target: >=10%.
- **Total surface-exposed users**: Target: 500+.
- **Auto-upgrade acceptance rate**: `auto_upgrade_completed` / (`auto_upgrade_completed` + `auto_upgrade_opted_out`). Target: >=50%.
- **Upgrade-driven MRR**: Growing month over month.

**Pass:** The self-serve upgrade system scales across trigger types and segments. Experiments produce consistent wins. Auto-upgrade handles the highest-intent users automatically. Proceed to Durable for autonomous optimization.

**Fail:** Diagnose:
- Low upgrade rate at scale (<10%): Check if the user pool is exhausted — are the same users seeing upgrade surfaces repeatedly? If so, expand trigger types or adjust suppression to reach new users.
- Low auto-upgrade acceptance (<50%): The grace period communication is not convincing. Test shorter grace periods, different value framing, or a more prominent display of what happens after opt-out (degraded service).
- Experiments not producing wins: The variants are too similar. Test bolder changes: entirely different checkout flows, different pricing presentation, or new trigger points.
- Revenue declining despite stable conversion: Users are selecting lower-priced plans. Add annual billing incentives or test the price anchoring experiment.

## Time Estimate

- 15 hours: A/B test design, implementation, and analysis (4 experiments over 2 months)
- 15 hours: Auto-upgrade execution setup (n8n workflows, Stripe integration, grace period flow, opt-out handling, rollback mechanism)
- 10 hours: Segment-personalized upgrade surfaces (cohort definition, n8n routing, per-segment surface variants)
- 10 hours: Analytics dashboard, monitoring automation, weekly performance reviews
- 10 hours: Ongoing optimization based on experiment results, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, funnels, dashboards | Growth from $0.00045/event beyond free tier — https://posthog.com/pricing |
| Stripe | Subscription management, auto-upgrade execution, proration | 2.9% + $0.30 per transaction — https://stripe.com/pricing |
| Intercom | In-app upgrade surfaces, auto-upgrade grace notifications | Essential $29/seat/mo — https://www.intercom.com/pricing |
| Loops | Checkout abandonment emails, auto-upgrade grace emails, trial expiry | Starter $49/mo for 5,000 contacts — https://loops.so/pricing |
| n8n | Auto-upgrade workflows, segment routing, monitoring, alerting | Free self-hosted; Cloud from ~$24/mo — https://n8n.io/pricing |
| Attio | Upgrade deal tracking, enterprise routing, revenue attribution | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$100-350/mo (Intercom for in-app messaging + Loops at scale + n8n Cloud)

## Drills Referenced

- `ab-test-orchestrator` — run systematic experiments on surface format, checkout flow, price anchoring, and social proof to find highest-converting variants
- `auto-upgrade-execution` — automatically upgrade users who exceed plan limits with a grace period, opt-out mechanism, and rollback safety
