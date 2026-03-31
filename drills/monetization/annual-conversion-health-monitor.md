---
name: annual-conversion-health-monitor
description: Track monthly-to-annual conversion funnel, measure LTV uplift from annual cohorts, and detect offer fatigue or conversion decay
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
  - Stripe
fundamentals:
  - posthog-funnels
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-reporting
  - stripe-subscription-status
  - billing-event-streaming
---

# Annual Conversion Health Monitor

This drill builds the measurement and alerting layer for monthly-to-annual conversion campaigns. It tracks the full offer-to-conversion funnel, measures retention lift from annual cohorts vs monthly cohorts, detects offer fatigue, and surfaces which discount tiers and delivery channels drive the highest net revenue gain.

## Input

- Annual upgrade offers deployed via in-app prompts (Intercom) and/or lifecycle emails (Loops)
- PostHog tracking `annual_offer_shown`, `annual_offer_clicked`, `annual_offer_started`, `annual_upgrade_completed` events
- Stripe subscription data with `billing_interval` metadata (monthly vs annual)
- n8n instance for scheduled monitoring
- Attio CRM with subscription records

## Steps

### 1. Build the annual conversion funnel

Using the `posthog-funnels` fundamental, create a funnel:

```
annual_offer_shown
  -> annual_offer_clicked
    -> annual_offer_started (reached checkout/confirmation)
      -> annual_upgrade_completed (Stripe subscription updated to annual)
```

Break down by:
- `offer_channel` (in_app_modal, in_app_banner, email, pricing_page)
- `discount_tier` (e.g., "2_months_free", "20_pct_off", "no_discount")
- `months_on_monthly` (how long the user has been on monthly billing — bucket into 1-3mo, 3-6mo, 6-12mo, 12mo+)
- `plan_current` (starter, pro, team)

Set conversion window to 14 days (annual upgrade decisions take longer than impulse upsells because users evaluate the commitment).

### 2. Build the annual conversion dashboard

Using `posthog-dashboards`, create a dashboard called "Annual Upgrade Incentive — Health":

| Panel | Type | What it shows |
|-------|------|---------------|
| Offers shown this week | Trend | Daily count of `annual_offer_shown`, broken down by channel |
| Offer CTR by channel | Bar chart | Click rate per delivery channel, current week vs 4-week average |
| Conversion funnel | Funnel | Full funnel from offer shown to upgrade completed |
| Annual upgrade revenue | Trend | Sum of `annual_upgrade_completed.annual_revenue_delta` per week — the additional committed revenue |
| Retention comparison | Line chart | 30/60/90-day retention for annual_cohort vs monthly_cohort (using PostHog retention analysis) |
| Offer fatigue signal | Trend | Ratio of `annual_offer_dismissed` to `annual_offer_shown` over time |
| Discount tier performance | Table | Conversion rate and net revenue per discount tier |
| Tenure segment performance | Bar chart | Conversion rate by `months_on_monthly` bucket |

Set dashboard subscription to deliver Monday 09:00 to the growth team.

### 3. Create performance cohorts

Using `posthog-cohorts`, create dynamic cohorts:

- **annual-converted**: Users who switched from monthly to annual in the last 90 days. Track their retention and usage patterns vs monthly users.
- **annual-offer-fatigued**: Users who dismissed 3+ annual offers in 30 days without clicking. Suppress further offers.
- **annual-high-intent**: Users who clicked an annual offer but did not complete checkout. Route to a follow-up email with a limited-time sweetener.
- **annual-eligible-unseen**: Monthly users who have never been shown an annual offer. Untapped audience.
- **annual-regret-risk**: Users who converted to annual but whose usage dropped >50% in the 30 days after conversion. May need re-engagement to prevent cancellation at renewal.

### 4. Build degradation detection

Using `posthog-anomaly-detection` and `n8n-scheduling`, create a daily workflow (08:00 UTC) that:

1. Queries PostHog for offer CTR and conversion rate over the last 7 days, by channel and discount tier
2. Compares against the 4-week rolling average
3. Flags any channel where CTR dropped >20% from rolling average
4. Flags if the annual-offer-fatigued cohort grew >15% week-over-week
5. Queries Stripe via `stripe-subscription-status` for any annual subscriptions that were downgraded back to monthly within 30 days (regret signal)

When a flag fires, the n8n workflow:
- Creates a note on the Attio campaign record using `attio-reporting`
- Sends a Slack notification: "Annual conversion CTR for [channel] dropped [X]% vs 4-week avg. Fatigued cohort: [size]. Regret downgrades this week: [count]."
- If fatigued cohort exceeds 15% of monthly users, recommend pausing in-app offers and switching to email-only delivery

### 5. Measure net revenue impact

Using `posthog-custom-events` and `billing-event-streaming`, calculate the true net revenue impact of annual conversions:

```
net_annual_revenue_gain = (
  annual_price_paid
  - (monthly_price * months_remaining_in_annual_term)  // what they would have paid monthly
  + monthly_price * retained_months_bonus              // estimated additional months retained due to annual commitment
  - discount_amount                                     // cost of the incentive
)
```

Track monthly: total annual conversions, average discount given, estimated LTV uplift from commitment lock-in, and actual vs projected retention for the annual cohort. If the annual cohort's retention at month 6 is not meaningfully higher than the monthly cohort's, the play's core thesis (annual commitment improves retention) needs investigation.

### 6. Track Stripe billing lifecycle

Using `stripe-subscription-status` and `billing-event-streaming`, monitor:

- **Successful annual renewals:** Annual subscribers who auto-renewed at the end of their term (the ultimate success signal)
- **Annual-to-monthly downgrades:** Users who switched back to monthly at renewal. Log reason if captured.
- **Annual cancellations:** Users who cancelled before their annual term ended. Compare rate to monthly cancellation rate.
- **Payment failures on annual:** Failed charges on annual subscriptions (higher stakes since the amount is larger). Ensure dunning sequences from `stripe-retry-schedule` are configured.

## Output

- Annual conversion funnel per channel and discount tier in PostHog
- Health dashboard with 8 panels and weekly delivery
- 5 dynamic cohorts for segmentation, suppression, and follow-up
- Daily degradation detection with Slack + Attio alerting
- Net revenue impact calculation with LTV uplift tracking
- Stripe billing lifecycle monitoring for annual subscribers

## Triggers

Dashboard reviewed weekly. Degradation detection runs daily via n8n cron at 08:00 UTC. Stripe billing lifecycle checks run daily. Re-run full setup when adding new offer channels, discount tiers, or plan types.
