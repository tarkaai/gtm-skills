---
name: downgrade-prevention-baseline
description: >
  Downgrade Intervention — Baseline Run. Deploy automated daily downgrade intent scoring,
  tiered intervention routing, and PostHog tracking. First always-on system targeting all
  paid users. Validate >=50% prevention rate over 2 weeks.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥50% prevention rate across all paid users over 2 weeks"
kpis: ["Downgrade prevention rate", "Intercept engagement rate", "Offer acceptance rate", "MRR saved"]
slug: "downgrade-prevention"
install: "npx gtm-skills add product/retain/downgrade-prevention"
drills:
  - downgrade-intent-detection
  - downgrade-intercept-flow
  - posthog-gtm-events
---

# Downgrade Intervention — Baseline Run

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

First always-on automation. The downgrade intent detection runs daily, scoring every paid user. Tiered interventions fire automatically based on intent severity. The system runs continuously for 2 weeks. Validate that the prevention rate holds at >=50% across the full paid user base (not just a hand-picked cohort).

## Leading Indicators

- Daily detection workflow runs without errors for 14 consecutive days
- At least 80% of moderate+ intent users receive an intervention within 24 hours of scoring
- Intervention engagement rate (opened email, saw in-app message, clicked CTA) is >=30%
- At least 3 different offer/intervention types have been presented
- PostHog funnels show data flowing through every stage: scored -> intervention sent -> engaged -> prevented/lost

## Instructions

### 1. Deploy automated detection

Run the `downgrade-intent-detection` drill in full automation mode. Build the n8n daily cron workflow that:

1. Runs at 07:00 UTC daily
2. Queries PostHog for all paid users with their downgrade signal metrics
3. Scores each user and classifies into intent tiers (none, watch, moderate, high, imminent)
4. Emits `downgrade_intent_scored` events to PostHog with score, tier, and top signals
5. Updates Attio records with current intent scores
6. Creates PostHog cohorts: "Downgrade Intent: Moderate", "Downgrade Intent: High", "Downgrade Intent: Imminent"

Also deploy the real-time trigger: when a `downgrade_page_viewed` event fires in PostHog, immediately score that user and escalate if needed.

Verify the workflow by checking the first 3 days of runs: are the cohorts populating? Are scores distributing across tiers? Spot-check 5 scored users manually to confirm the signals match reality.

### 2. Configure full event tracking

Run the `posthog-gtm-events` drill to set up the complete downgrade prevention event schema:

| Event | Trigger |
|-------|---------|
| `downgrade_intent_scored` | Daily detection scores a user |
| `downgrade_intervention_sent` | In-app message shown or email sent |
| `downgrade_intervention_engaged` | User clicked CTA, opened email, or took action |
| `downgrade_intercept_shown` | User saw the downgrade page intercept |
| `downgrade_intercept_action` | User chose keep/discount/continue on intercept page |
| `retention_offer_shown` | Retention offer presented |
| `retention_offer_accepted` | User accepted an offer |
| `retention_offer_fulfilled` | Offer applied to their account |
| `downgrade_prevented` | User remained on plan 30 days post-intervention |
| `downgrade_completed` | User downgraded despite intervention |

Build PostHog funnels:
1. **Detection to prevention:** `downgrade_intent_scored` (tier >= moderate) -> `downgrade_intervention_sent` -> `downgrade_intervention_engaged` -> `downgrade_prevented`
2. **Intercept page funnel:** `downgrade_intercept_shown` -> `downgrade_intercept_action` (breakdown by action type)
3. **Offer funnel:** `retention_offer_shown` -> `retention_offer_accepted` -> `retention_offer_fulfilled`

### 3. Deploy tiered interventions

Run the `downgrade-intercept-flow` drill to deploy all 3 intervention tiers as always-on automations:

**Moderate intent interventions:**
- Intercom in-app banner targeting the "Downgrade Intent: Moderate" cohort. Shows when user logs in. Highlights premium features they are underutilizing.
- Loops 3-email feature education sequence. Auto-enrolls users entering the moderate cohort.
- Frequency cap: 1 in-app message per week, maximum 3 total.

**High intent interventions:**
- Intercom modal targeting the "Downgrade Intent: High" cohort. Personalized with usage data: what they would lose, how much they have used premium features.
- Loops transactional email within 2 hours of entering high tier. Includes a retention offer (20% discount for 3 months).
- CTA: "Keep my plan" (primary) and "Talk to someone" (secondary).

**Imminent intent interventions:**
- Attio task for account owner with user context, MRR at risk, and pre-drafted outreach.
- Loops transactional email offering plan pause (30 days) as an alternative to downgrade.
- Deploy within 1 hour of scoring.

**Downgrade page intercept:**
- PostHog feature flag gating the downgrade flow for ALL paid users (not just flagged users).
- Shows personalized usage summary and retention options before the user can proceed with downgrade.

### 4. Build the retention offer fulfillment pipeline

Using the n8n workflow from `downgrade-intercept-flow`:
- When a user accepts a discount: apply coupon via billing API, confirm via Loops, log in Attio as "Retention Save" deal
- When a user accepts plan pause: set pause via billing API, schedule a reactivation reminder for 23 days later
- When a user requests coaching: create a Cal.com booking link, email via Loops, create Attio task

### 5. Run for 2 weeks and evaluate

Let the system run for 14 days without manual intervention (unless guardrails fire). At the end of 2 weeks, evaluate against the pass threshold: **>=50% prevention rate**.

Prevention rate = (users who remained on their plan 14+ days after being scored moderate+) / (total users scored moderate+ during the evaluation period).

Also measure:
- Prevention rate by tier (moderate, high, imminent separately)
- Prevention rate by channel (in-app, email, personal outreach)
- Offer acceptance rate by offer type
- MRR saved (sum of plan deltas for prevented downgrades)
- False positive rate (users scored moderate+ who showed no actual downgrade behavior)
- Intercept page keep rate vs. bypass rate

If PASS, proceed to Scalable. If FAIL, diagnose by tier: which tier has the lowest prevention rate? Focus optimization there. Common failure modes:
- Detection too late (users downgrade before scoring runs) -> add more real-time triggers
- Intervention too generic (same message for everyone) -> personalize by signal type
- Offer not compelling (low acceptance) -> test different offers
- Wrong channel (users not seeing messages) -> shift to higher-attention channels

## Time Estimate

- 4 hours: deploy detection workflow, verify scoring, set up real-time triggers
- 3 hours: configure full PostHog event tracking and funnels
- 4 hours: deploy all intervention tiers (in-app, email, intercept page, offer fulfillment)
- 3 hours: monitor during 2-week run (check daily, 15 min each)
- 2 hours: evaluate results, document findings, diagnose any failures

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Detection queries, event tracking, funnels, feature flags, cohorts | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Daily detection workflow, offer fulfillment workflows, real-time triggers | Self-hosted free; Cloud from EUR20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app intervention messages (banners + modals) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Feature education sequences + retention offer emails | $49/mo for 5,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost: $50-100/mo** (Loops sequence + incremental Intercom messages)

## Drills Referenced

- `downgrade-intent-detection` -- automated daily scoring of all paid users for downgrade intent, plus real-time triggers
- `downgrade-intercept-flow` -- tiered interventions (feature education, retention offers, personal outreach) and downgrade page intercept
- `posthog-gtm-events` -- complete event schema and funnel setup for measuring the full prevention pipeline
