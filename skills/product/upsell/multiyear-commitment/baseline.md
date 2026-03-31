---
name: multiyear-commitment-baseline
description: >
  Multi-Year Deal Incentives — Baseline Run. Automate commitment readiness scoring,
  deploy always-on offer delivery via in-app and email channels, and track the full
  conversion funnel. First always-on automation of the commitment program.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥10% of Ready-tier accounts convert to annual within 30 days"
kpis: ["Offer conversion rate", "Committed ARR", "Retention lift vs. monthly", "Funnel drop-off by step"]
slug: "multiyear-commitment"
install: "npx gtm-skills add product/upsell/multiyear-commitment"
drills:
  - multiyear-offer-engine
  - posthog-gtm-events
  - churn-risk-scoring
---

# Multi-Year Deal Incentives — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Automate the commitment offer pipeline end-to-end: readiness scoring runs daily, offers deploy automatically to qualifying accounts, and conversions flow through Stripe into Attio. The system runs without manual intervention. Prove that the automated pipeline converts at least 10% of Ready-tier accounts within 30 days.

## Leading Indicators

- Daily readiness scoring producing a stable Ready-tier population (target: 5-15% of active accounts)
- In-app offer impression rate (target: >80% of Ready-tier accounts see the offer within 7 days)
- Email sequence open rate (target: >45%)
- Stripe Checkout session start rate (target: >8% of accounts shown the offer)
- Churn risk scores for offered accounts remain stable (not worsening from offer fatigue)

## Instructions

### 1. Deploy full event tracking

Run the `posthog-gtm-events` drill to instrument the complete commitment funnel in PostHog:

Events to configure:
- `multiyear_offer_qualified` — fired when an account enters the Ready tier
- `multiyear_offer_shown` — fired when the in-app banner renders or the email sends
- `multiyear_offer_clicked` — fired when the user clicks the CTA
- `multiyear_offer_started` — fired when Stripe Checkout session is created
- `multiyear_offer_converted` — fired when subscription updates to annual
- `multiyear_offer_dismissed` — fired when user dismisses the in-app offer

Each event must carry: `account_id`, `channel` (in-app | email | sales), `offer_tier`, `discount_pct`, `readiness_score`.

Build a PostHog funnel: `qualified` → `shown` → `clicked` → `started` → `converted`. Set up a dashboard panel showing this funnel's conversion rate by channel, refreshing daily.

### 2. Activate the automated offer engine

Run the `multiyear-offer-engine` drill — all steps. This sets up:

1. **Daily readiness scoring** (n8n cron): queries PostHog for account signals, computes `commitment_readiness_score`, classifies into Ready/Warming/Not Ready tiers, updates Attio records
2. **In-app offer delivery** (Intercom): when a Ready-tier admin visits billing or settings, show a contextual banner with their personalized savings amount and a Stripe Checkout link
3. **Email offer sequence** (Loops): 3-email sequence triggered when an account enters Ready tier. Includes usage summary, savings calculation, and one-click upgrade link
4. **Sales routing** (Attio): accounts with ARR > $5,000 routed to the account owner instead of self-serve
5. **Conversion pipeline** (n8n + Stripe webhook): captures subscription updates, moves Attio deals to Won, fires PostHog conversion event

Start with the Standard offer tier only (17% discount). Do not test Enhanced or Premium yet — establish a baseline conversion rate first.

### 3. Integrate churn risk as a gate

Run the `churn-risk-scoring` drill to ensure at-risk accounts are excluded from commitment offers. The offer engine already checks `churn_risk_score < 25` as a readiness signal, but this drill provides the scoring infrastructure:

- Daily churn risk scoring runs alongside commitment readiness scoring
- Accounts with `churn_risk_tier` = medium, high, or critical are excluded from the Ready tier
- If an account receives a commitment offer and then churn risk spikes, suppress future offer emails (do not send Email 2 or 3)

This prevents the worst outcome: offering a discount to an account that was about to churn anyway, then having them commit, collect the discount, and cancel before the term ends.

### 4. Monitor and evaluate

After 3 weeks of always-on operation:

1. Pull the PostHog funnel: `qualified` → `shown` → `clicked` → `started` → `converted`
2. Calculate conversion rate: committed accounts / Ready-tier accounts shown an offer
3. Verify no negative signals: churn risk not increasing for offered accounts, support ticket volume not spiking about the offers

Pass threshold: **10% or more of Ready-tier accounts that were shown an offer convert to annual within 30 days.**

If PASS: Proceed to Scalable to add offer tier testing, multi-year terms, and segment-specific offers.

If FAIL: Diagnose the funnel drop-off:
- Qualified but not shown → delivery timing or targeting issue
- Shown but not clicked → offer copy, discount level, or placement issue
- Clicked but not started → Checkout page friction
- Started but not converted → payment method issue or price anxiety (add a "cancel anytime in first 30 days" guarantee)

Fix the biggest drop-off and re-run for another 2 weeks.

## Time Estimate

- 4 hours: configure PostHog events, funnels, and dashboard
- 6 hours: deploy the full offer engine (n8n workflows, Intercom messages, Loops sequences, Stripe prices)
- 3 hours: integrate churn risk scoring as a gate
- 2 hours: test end-to-end (trigger a test account through the full pipeline)
- 5 hours: monitor for 3 weeks (1-2 hours/week checking dashboards, fixing issues)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts | Free up to 1M events/mo; $0.00045/event after |
| Stripe | Annual prices, Checkout sessions, webhooks | 2.9% + $0.30/txn |
| Intercom | In-app offer banners | Starter $74/mo; https://www.intercom.com/pricing |
| Loops | Email offer sequences | Free up to 1,000 contacts; $49/mo for 5K; https://loops.so/pricing |
| n8n | Orchestration workflows (scoring, routing, webhooks) | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Attio | CRM deal tracking | Free up to 3 users; $29/seat/mo; https://attio.com/pricing |

## Drills Referenced

- `multiyear-offer-engine` — the core automation: readiness scoring, offer delivery, conversion pipeline
- `posthog-gtm-events` — event tracking configuration for the commitment funnel
- `churn-risk-scoring` — behavioral churn model that gates commitment offers to healthy accounts only
