---
name: affiliate-performance-reporting
description: Monitor per-affiliate performance, revenue attribution, and generate weekly partnership performance briefs
category: Partnerships
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
  - Rewardful
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# Affiliate Performance Reporting

This drill builds the monitoring and reporting layer specific to the reseller & affiliate program play. It tracks per-partner referral volume, conversion rates, revenue attribution, and commission ROI, then generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active affiliates/resellers with Rewardful/FirstPromoter tracking in place
- PostHog tracking for affiliate referral events (UTM parameters, custom events)
- Attio partner records with program enrollment and tier data
- At least 4 weeks of referral data (minimum for meaningful trends)

## Steps

### 1. Build the affiliate program dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "Reseller & Affiliate Program — Performance" with these panels:

- **Referrals by partner** (bar chart): `affiliate_referral` events grouped by `utm_content` (affiliate slug), last 30 days
- **Revenue by partner** (bar chart): `affiliate_conversion` events with `revenue` property, grouped by `utm_content`, last 30 days
- **Click-to-signup conversion rate by partner** (table): signups / clicks per affiliate, sorted descending
- **Signup-to-paid conversion rate by partner** (table): paid conversions / signups per affiliate, sorted descending
- **Referral volume over time** (trend line): weekly `affiliate_referral` events, last 90 days
- **Commission ROI** (table): revenue generated / commissions paid per affiliate — identifies partners where commission spend is most efficient
- **Full affiliate funnel** (funnel): `affiliate_link_click` → `affiliate_signup` → `affiliate_trial_start` → `affiliate_conversion` → `affiliate_renewal`, filtered to affiliate traffic
- **Partner tier performance** (bar chart): revenue per tier (Standard / Silver / Gold) to validate the tier structure

### 2. Create affiliate performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **Star partners**: Affiliates generating >5 paid conversions/month with >20% signup-to-paid rate
- **Volume drivers**: Affiliates generating >50 clicks/month but low conversion (potential for optimization)
- **Declining partners**: Affiliates whose referral volume dropped >40% month-over-month
- **New partners**: Affiliates with first referral in the last 30 days (need more data before judging)
- **Dormant partners**: Affiliates with zero referral activity in 45+ days despite being active

These cohorts feed the `autonomous-optimization` drill's anomaly detection.

### 3. Build the weekly affiliate program brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of affiliate data from PostHog (clicks, signups, conversions, revenue per partner)
2. Pull commission data from Rewardful/FirstPromoter API (commissions earned, commissions paid, pending payouts)
3. Pull partner pipeline data from Attio (new partners recruited, partners activated, partners churned)
4. Compare this week's metrics to the 4-week rolling average
5. Use the `hypothesis-generation` fundamental to generate insights:
   - Which partners over/underperformed this week and why?
   - Which partner types (SaaS reseller vs. content creator vs. customer) drive the most value?
   - What should change next week?
6. Compile into a structured brief and post to Slack

Brief format:
```
## Affiliate Program Weekly Brief — {date}

**This week**: {total_clicks} clicks, {total_signups} signups, {total_conversions} paid conversions
**Revenue attributed**: ${revenue} ({commission_cost} in commissions, {roi}x ROI)
**vs 4-week avg**: {change_pct}% {up/down}

### Top partners this week
1. {partner_1}: {conversions} conversions, ${revenue} revenue
2. {partner_2}: {conversions} conversions, ${revenue} revenue

### Partner program health
- Active partners: {count} ({new_this_week} new, {churned_this_week} churned)
- Activation rate (30-day): {pct}%
- Average revenue per active partner: ${amount}

### Underperformers
- {partner}: {clicks} clicks, {conversions} conversions ({cvr}% CVR) — {hypothesis}

### Partner type analysis
- SaaS resellers: ${revenue} revenue, {count} partners
- Content creators: ${revenue} revenue, {count} partners
- Customer affiliates: ${revenue} revenue, {count} partners

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build the per-partner ROI tracker

In Attio, maintain these fields on each partner record (updated weekly by n8n):

- **Total clicks**: Cumulative affiliate link clicks
- **Total signups**: Signups attributed to this partner
- **Total paid conversions**: Customers who converted to paid
- **Total revenue generated**: Lifetime revenue from this partner's referrals
- **Total commissions paid**: Lifetime commissions paid to this partner
- **Commission ROI**: Revenue generated / commissions paid
- **Average deal size**: Mean revenue per referred customer
- **Best performing content**: Which of their promotions (blog post, newsletter, social) drove the most conversions
- **Last referral date**: When the most recent referral was generated
- **Partner health score**: Composite of recency, conversion rate, volume, and trend (calculated by n8n)

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:

- Any partner's weekly referrals drop >60% vs. prior week → flag in Slack, investigate
- A new partner generates their first paid conversion within 14 days of onboarding → celebrate in Slack, fast-track enablement
- Total program revenue drops below Scalable baseline for 2 consecutive weeks → trigger `autonomous-optimization` investigation
- A partner achieves >30% signup-to-paid conversion rate → flag as "star partner," investigate what they are doing differently and replicate
- Commission ROI for any partner drops below 2x for 3 consecutive months → review commission structure for that partner

## Output

- PostHog dashboard with per-partner and per-type performance
- Weekly automated affiliate program brief with insights and recommendations
- Per-partner ROI tracking in Attio
- Alert system for performance anomalies
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Scalable level. The weekly brief runs every Friday. Partner ROI fields update weekly via n8n.
