---
name: usage-based-pricing-scalable
description: >
  Consumption-Based Pricing — Scalable Automation. Roll out usage-based pricing to 100% of
  customers. Auto-upgrade execution handles tier transitions without human intervention. A/B test
  pricing page, alert copy, and tier boundaries to find the 10x multiplier.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥8% ARPU lift sustained at 500+ customers with auto-upgrade acceptance rate ≥50%"
kpis: ["ARPU lift vs. pre-pricing-change baseline", "Auto-upgrade acceptance rate", "Net revenue retention", "Churn rate by tier", "Upgrade prompt conversion rate"]
slug: "usage-based-pricing"
install: "npx gtm-skills add product/upsell/usage-based-pricing"
drills:
  - auto-upgrade-execution
  - upgrade-prompt
  - ab-test-orchestrator
  - pricing-page-conversion-monitor
---

# Consumption-Based Pricing — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Usage-based pricing is live for 100% of customers. The auto-upgrade system seamlessly transitions accounts when they exceed plan limits, with a 72-hour opt-out grace period and acceptance rate of 50%+. Upgrade prompts fire at the right moment based on usage patterns and convert at 5%+ for limit-proximity triggers. The pricing page is optimized through systematic A/B testing. ARPU lift of at least 8% is sustained across the full customer base of 500+ accounts.

## Leading Indicators

- Full rollout completed: 100% of eligible customers on usage-based pricing within 2 weeks of Scalable launch
- Auto-upgrade grace period workflow running without payment failures exceeding 5%
- Auto-upgrade opt-out rate below 50% (acceptance rate at or above 50%)
- Auto-upgrade 30-day retention rate above 80% (upgraded customers stay on the higher tier)
- Upgrade prompts firing for the correct PostHog cohorts (limit-proximity, feature-gate, growth-signal)
- Pricing page conversion rate stable or improving vs. pre-change baseline
- At least 2 A/B tests reaching statistical significance per month

## Instructions

### 1. Deploy auto-upgrade execution

Run the `auto-upgrade-execution` drill. This builds the system that automatically moves customers to higher tiers when usage exceeds limits:

1. **Define the auto-upgrade tier map:** Create a JSON configuration mapping current_plan + exceeded_resource to target_plan and Stripe price IDs. Store in n8n as a static data node.

2. **Build the opt-out grace period flow:** When `usage-threshold-detection` flags an account as exceeded, start a 72-hour grace period. Show a persistent Intercom banner: "You've exceeded your {{resource_name}} limit. We'll automatically upgrade you to {{target_plan}} in 72 hours. [View details] [Opt out]." Send a Loops email with the same information.

3. **Handle opt-outs:** Create an n8n webhook endpoint for the opt-out action. Opted-out accounts get the hard limit enforced instead of the upgrade. Set a 30-day cooldown before re-triggering.

4. **Execute auto-upgrades:** An n8n cron job checks hourly for pending upgrades whose grace period has expired. It swaps the Stripe subscription to the target plan with proration, verifies the payment succeeds, sends confirmation via Intercom and Loops, and logs `auto_upgrade_completed` in PostHog.

5. **Build the rollback mechanism:** Support can revert any auto-upgrade within 48 hours. The workflow restores the previous plan, issues a credit, and applies the hard limit.

6. **Track the auto-upgrade funnel:** `usage_threshold_detected` -> `auto_upgrade_grace_started` -> `auto_upgrade_opted_out` or `auto_upgrade_completed` -> `auto_upgrade_retained_30d` or `auto_upgrade_rolled_back`. Target: 50%+ acceptance, 80%+ 30-day retention, below 10% rollback.

### 2. Configure upgrade prompts for expansion

Run the `upgrade-prompt` drill to detect and act on upgrade opportunities beyond the auto-upgrade threshold:

1. **Define upgrade triggers in PostHog:** Limit proximity (80%+ of a plan limit), feature discovery (user tried premium feature or hit a feature gate), growth signals (3+ team members added in a month, usage volume doubled), power user behavior (API access, integrations).

2. **Build trigger detection cohorts:** Create PostHog cohorts for each trigger type. Score urgency: limit proximity is time-sensitive, growth signals are opportunity-based.

3. **Design contextual prompts:** Each Intercom in-app message is tied to the specific trigger — not a generic "upgrade now" banner. Include what they get, the price difference, and a one-click upgrade path.

4. **Set up Loops email nudges:** Send upgrade emails 24-48 hours after a trigger event for non-urgent triggers. Include personalized usage summaries: "You've created 47 projects this month and invited 5 teammates."

5. **Route high-value accounts to sales:** For accounts above the MRR threshold, create expansion deals in Attio instead of self-serve upgrade prompts.

### 3. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test variations that improve the pricing experience:

1. **Pricing page experiments:** Test plan card order, feature comparison layout, annual vs. monthly toggle default, CTA copy, social proof placement. Use PostHog feature flags with 50/50 splits.

2. **Alert copy experiments:** Test different usage alert messages — urgency vs. value-based framing, specific numbers vs. percentage-based messaging, one-CTA vs. two-CTA layouts.

3. **Tier boundary experiments:** If the Smoke analysis identified multiple viable breakpoints, test them. Split new signups between pricing structures and compare 60-day ARPU and churn.

4. **Process:** For each test, form a hypothesis with predicted outcome, calculate required sample size, run until significance (minimum 2 weeks), and document results regardless of outcome. Maximum 2 concurrent experiments touching different surfaces.

### 4. Monitor pricing page health

Run the `pricing-page-conversion-monitor` drill to establish always-on monitoring of the pricing page:

1. **Build the pricing page dashboard in PostHog:** Visitor volume, conversion rate by traffic source, plan selection distribution, checkout abandonment rate, annual vs. monthly selection rate.

2. **Set anomaly detection rules:** Alert if conversion rate drops 20% vs. 14-day average, checkout abandonment exceeds 70% for 3 days, or ARPU drops 15% MoM.

3. **Build daily and weekly monitoring n8n workflows:** Daily anomaly checks with Slack alerts on High severity. Weekly pricing page digest with trends and action items.

4. **Maintain pricing sensitivity cohorts:** Comparison shoppers (3+ pricing page views without converting), plan hesitators (started checkout but abandoned), downgrade researchers (paying customers viewing pricing page repeatedly).

### 5. Evaluate against threshold

After 2 months of full rollout:

- ARPU lift: treatment ARPU is at least 8% higher than the pre-change baseline, sustained across 500+ customers
- Auto-upgrade acceptance rate is at or above 50%
- Net revenue retention is at or above 100%
- No tier is showing net negative migration flow for 3+ consecutive weeks

If PASS, proceed to Durable. If FAIL, identify the bottleneck: is auto-upgrade acceptance low (communication problem), is churn spiking in specific tiers (pricing problem), or is the pricing page underconverting (design problem)? Focus A/B testing on the specific bottleneck and re-evaluate in 4 weeks.

## Time Estimate

- 12 hours: Auto-upgrade execution workflow (tier map, grace period, n8n workflows, Stripe integration, rollback)
- 8 hours: Upgrade prompt configuration (triggers, cohorts, Intercom templates, Loops sequences)
- 12 hours: A/B test design, setup, and analysis (4-6 experiments over 2 months)
- 8 hours: Pricing page conversion monitor setup (dashboard, anomaly rules, n8n workflows)
- 20 hours: Ongoing monitoring, weekly analysis, experiment iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, pricing page analytics, session recordings | Free up to 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Metered billing, auto-upgrade subscription swaps, proration | 0.5% of recurring revenue for Billing ([stripe.com/pricing](https://stripe.com/pricing)) |
| Intercom | In-app upgrade prompts, auto-upgrade grace notices, feature gate messages | Essential $29/seat/mo; Proactive add-on $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered upgrade emails, usage alert sequences, grace period notifications | Free up to 1,000 contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at this level:** $150-350/mo (Intercom proactive messaging + Loops paid tier as contact volume grows)

## Drills Referenced

- `auto-upgrade-execution` — Automatically upgrades Stripe subscriptions when usage exceeds plan limits, with opt-out grace period and rollback safety
- `upgrade-prompt` — Detects usage patterns that signal upgrade readiness and triggers contextual upsell prompts via Intercom and Loops
- `ab-test-orchestrator` — Designs, runs, and analyzes A/B tests for pricing page, alert copy, and tier boundaries using PostHog experiments
- `pricing-page-conversion-monitor` — Always-on monitoring of pricing page conversion funnel with anomaly detection and weekly digests
