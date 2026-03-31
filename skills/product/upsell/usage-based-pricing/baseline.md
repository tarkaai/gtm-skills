---
name: usage-based-pricing-baseline
description: >
  Consumption-Based Pricing — Baseline Run. Ship the usage-based pricing model to a controlled
  cohort via Stripe metered billing and PostHog feature flags. First always-on automation: usage
  threshold detection and alert delivery running continuously.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥10% ARPU lift in treatment group vs. control over 2 billing cycles"
kpis: ["ARPU (treatment vs. control)", "Net revenue retention", "30-day churn rate by group", "Usage threshold alert conversion rate"]
slug: "usage-based-pricing"
install: "npx gtm-skills add product/upsell/usage-based-pricing"
drills:
  - pricing-experiment-runner
  - usage-threshold-detection
  - usage-alert-delivery
---

# Consumption-Based Pricing — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The usage-based pricing model from Smoke is live for a controlled treatment group (50% of eligible customers). Stripe metered billing is configured with the recommended pricing structure. Usage threshold detection runs daily, automatically identifying accounts approaching plan limits. Alert delivery triggers contextual in-app messages and emails when accounts cross usage thresholds. After 2 full billing cycles, ARPU in the treatment group is at least 10% higher than the control group.

## Leading Indicators

- Stripe meter events flowing correctly: usage records match PostHog usage events within 5% variance
- Treatment group subscription migration completed without payment failures exceeding 5%
- Usage threshold detection identifying accounts in approaching/imminent/critical tiers daily
- Alert delivery conversion rate (alert shown to upgrade completed) exceeding 3% for critical-tier alerts
- No guardrail breaches: treatment group churn does not exceed control by more than 50%

## Instructions

### 1. Run the pricing experiment

Run the `pricing-experiment-runner` drill. This executes the controlled rollout:

1. **Create variant prices in Stripe:** Build the new Price objects that implement the pricing model recommended by the Smoke analysis. For hybrid pricing (base + overage), create both the base price and the metered overage price. Tag all experiment prices with `metadata[experiment]=usage_pricing_v1` and `metadata[variant]=treatment`.

2. **Set up the PostHog feature flag:** Create `pricing-experiment-usage-v1` with 50/50 control/treatment split. Target only active paying customers on the plan being tested. Exclude: enterprise contracts, customers with custom pricing, accounts younger than 30 days.

3. **Build the subscription migration workflow in n8n:** When a user is assigned to treatment, swap their Stripe subscription items from control prices to treatment prices. Set `proration_behavior=none` so new pricing takes effect at the next billing cycle. Log `pricing_experiment_enrolled` in PostHog.

4. **Notify enrolled users via Intercom:** Send an in-app message explaining the pricing change: what is changing, why, and what it means for their bill. Link to a help article with full details.

**Human action required:** Review the Intercom notification copy before launching the experiment. Pricing changes require clear, honest communication. Approve the experiment launch.

5. **Define success and guardrail metrics:** Primary: ARPU lift and 30-day churn rate. Guardrails: treatment churn exceeds control by 50%, gross revenue drops 15%, or 10+ support tickets about the pricing change in 7 days. If any guardrail is breached, the drill auto-reverts all treatment users to control pricing.

6. **Monitor weekly:** The drill runs a weekly n8n workflow that queries PostHog for treatment vs. control metrics and checks guardrails. Minimum experiment duration: 2 full billing cycles (60 days).

### 2. Deploy usage threshold detection

Run the `usage-threshold-detection` drill. This builds the always-on monitoring system:

1. **Define metered resources and plan caps:** Enumerate every resource that differs between tiers. Store the tier-to-limit mapping as a JSON config accessible to n8n.

2. **Build the daily detection workflow:** An n8n cron job runs daily at 06:00 UTC. It queries PostHog for all accounts at 70%+ of any plan limit, computes consumption velocity to project hit dates, classifies accounts into urgency tiers (approaching, imminent, critical, exceeded), and updates Attio records with threshold proximity data.

3. **Create PostHog cohorts:** Four dynamic cohorts (approaching, imminent, critical, exceeded) that update automatically as detection runs.

### 3. Deploy usage alert delivery

Run the `usage-alert-delivery` drill. This connects threshold detection to customer communication:

1. **Build routing rules in n8n:** When threshold detection fires a webhook for an account, route based on urgency tier and account MRR. Self-serve accounts get automated Intercom in-app messages and Loops emails. High-value accounts get Attio expansion deals created for the account owner.

2. **Create Intercom message templates:** Three templates — imminent (banner with usage numbers + upgrade CTA), critical (modal with projected hit date + one-click upgrade), exceeded (blocking modal with upgrade/contact-sales CTAs). Each template includes actual usage numbers, not generic copy.

3. **Create Loops email sequences:** Triggered emails for imminent and critical tiers with visual usage bars, next-tier value propositions, and one-click upgrade links. A 2-email follow-up sequence for accounts that do not upgrade within 3 days.

4. **Track the full alert lifecycle:** Log `usage_alert_shown`, `usage_alert_clicked`, `usage_alert_converted` events in PostHog to measure alert effectiveness.

### 4. Evaluate against threshold

After 2 full billing cycles (minimum 60 days):

- Compare ARPU between treatment and control groups. Pass threshold: treatment ARPU is at least 10% higher.
- Check that treatment churn rate is not materially higher than control (within 20% relative).
- Check that usage threshold alerts are converting at 3%+ for critical-tier alerts.

If PASS, proceed to Scalable. If FAIL, diagnose: is the pricing model wrong (ARPU not lifting) or is the communication wrong (churn spiking)? Iterate on the specific failure point and re-run.

## Time Estimate

- 4 hours: Stripe meter and price setup, n8n migration workflow
- 3 hours: PostHog feature flag, experiment configuration, guardrail setup
- 3 hours: Usage threshold detection n8n workflow and Attio integration
- 3 hours: Intercom templates, Loops emails, alert delivery routing
- 3 hours: Monitoring, weekly analysis, final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiment tracking, usage analytics, cohorts | Free up to 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Stripe | Metered billing, price objects, subscription management | 0.5% of recurring revenue for Billing ([stripe.com/pricing](https://stripe.com/pricing)) |
| Intercom | In-app usage alerts, upgrade prompts | Essential $29/seat/mo; Proactive messaging add-on $99/mo for 500 messages ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered usage alert emails, follow-up sequences | Free up to 1,000 contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at this level:** $50-150/mo (Intercom proactive messaging add-on + Loops if over free tier)

## Drills Referenced

- `pricing-experiment-runner` — Manages the full pricing experiment lifecycle: Stripe variant prices, PostHog feature flags, subscription migration, guardrail monitoring, and adopt/revert decisions
- `usage-threshold-detection` — Daily per-account usage threshold detection with urgency tier classification and consumption velocity projection
- `usage-alert-delivery` — Routes threshold alerts to contextual in-app messages, emails, and sales expansion deals based on account value and urgency
